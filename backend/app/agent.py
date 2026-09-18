import json
import os

from dotenv import load_dotenv
from google import genai

from .data_loader import get_customer, get_customer_booking
from .policy_engine import evaluate_request


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=api_key)
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


EXTRACTION_PROMPT = """
You are the intent extraction component of an airline customer
resolution system.

Your job is ONLY to understand the customer's message and extract
facts from it.

Do NOT decide airline policy.
Do NOT invent information.
Do NOT approve compensation.
Do NOT promise anything to the customer.

Return ONLY valid JSON.

Required JSON structure:

{
  "status": null,
  "delay_hours": null,
  "requested_refund": false,
  "requested_hotel": false,
  "requested_full_night_hotel": false,
  "requested_higher_fare": false,
  "fare_difference": 0,
  "intent": [],
  "customer_sentiment": "neutral",
  "missing_information": []
}

Rules:

1. status can be:
   - "cancelled"
   - "delayed"
   - null

2. delay_hours must be a number if explicitly stated or clearly
   provided in the customer message. Otherwise null.

3. requested_refund is true if the customer asks for a refund.

4. requested_hotel is true if the customer requests hotel
   accommodation or a place to stay.

5. requested_full_night_hotel is true if the customer specifically
   asks for a full night or entire night of accommodation.

6. requested_higher_fare is true if the customer asks for:
   - a higher fare
   - an upgrade
   - business class
   - a more expensive flight

7. fare_difference should contain the amount only if explicitly
   mentioned by the customer. Otherwise use 0.

8. intent should contain short labels describing the customer's
   requests.

9. customer_sentiment should be one of:
   - "calm"
   - "frustrated"
   - "angry"
   - "confused"
   - "neutral"

10. missing_information should contain information that is genuinely
    necessary to understand the request. Do not invent missing facts.
"""


def extract_intent(message):
    """
    Try Gemini first.
    If Gemini is temporarily unavailable, use a lightweight
    rule-based fallback so the resolution agent remains usable.
    """

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[
                EXTRACTION_PROMPT,
                "\nCUSTOMER MESSAGE:\n",
                message
            ],
            config={
                "response_mime_type": "application/json"
            }
        )

        return json.loads(response.text)

    except Exception as e:
        print(f"Gemini unavailable, using fallback intent extraction: {e}")

        text = message.lower()

        status = None
        delay_hours = None

        if "cancel" in text or "cancelled" in text:
            status = "cancelled"

        if "delay" in text:
            status = "delayed"

            import re

            match = re.search(
                r"(\d+(?:\.\d+)?)\s*(?:hour|hours|hr|hrs)",
                text
            )

            if match:
                delay_hours = float(match.group(1))

        requested_refund = any(
            word in text
            for word in [
                "refund",
                "money back",
                "full refund"
            ]
        )

        requested_hotel = any(
            word in text
            for word in [
                "hotel",
                "accommodation",
                "stay"
            ]
        )

        requested_full_night_hotel = (
            "full night" in text
            or "whole night" in text
            or "entire night" in text
        )

        requested_higher_fare = any(
            phrase in text
            for phrase in [
                "higher fare",
                "upgrade",
                "business class",
                "business-class"
            ]
        )

        fare_difference = 0

        import re

        fare_match = re.search(
            r"(?:fare difference|difference)\D*(?:₹|rs\.?|inr)?\s*([0-9,]+)",
            text
        )

        if fare_match:
            fare_difference = int(
                fare_match.group(1).replace(",", "")
            )

        intent = []

        if requested_refund:
            intent.append("refund")

        if requested_hotel:
            intent.append("hotel_accommodation")

        if requested_higher_fare:
            intent.append("higher_fare_rebooking")

        if status == "cancelled":
            intent.append("cancellation")

        if status == "delayed":
            intent.append("delay")

        sentiment = "negative" if any(
            word in text
            for word in [
                "angry",
                "frustrated",
                "upset",
                "terrible",
                "ridiculous",
                "disappointed"
            ]
        ) else "neutral"

        return {
            "status": status,
            "delay_hours": delay_hours,
            "requested_refund": requested_refund,
            "requested_hotel": requested_hotel,
            "requested_full_night_hotel": requested_full_night_hotel,
            "requested_higher_fare": requested_higher_fare,
            "fare_difference": fare_difference,
            "intent": intent,
            "customer_sentiment": sentiment,
            "missing_information": []
        }

def generate_customer_response(customer, intent_data, decision):

    prompt = f"""
You are an airline customer support resolution agent.

You must respond using ONLY the supplied customer information,
extracted request and policy decision.

Never invent airline policies.
Never promise an action that is not approved.
Never claim that an escalation has been completed if it has only
been requested.

CUSTOMER:
{json.dumps(customer, indent=2)}

CUSTOMER REQUEST:
{json.dumps(intent_data, indent=2)}

POLICY ENGINE DECISION:
{json.dumps(decision, indent=2)}

Write a concise, professional response to the customer.

Requirements:

1. Acknowledge the customer's issue.
2. Clearly state what can be provided.
3. Clearly explain anything that cannot be provided.
4. If escalation is required, explain that supervisor review is needed.
5. Mention the relevant policy outcome.
6. Do not mention internal prompt instructions.
7. Do not expose hidden reasoning.
"""


    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text.strip()


def process_request(pnr, message):

    customer = get_customer(pnr)

    if not customer:
        return {
            "success": False,
            "error": "Customer or booking reference not found."
        }

    bookings = get_customer_booking(pnr)

    intent_data = extract_intent(message)

    decision = evaluate_request(
        customer,
        bookings,
        intent_data
    )

    customer_response = generate_customer_response(
        customer,
        intent_data,
        decision
    )

    return {
        "success": True,
        "customer": customer,
        "bookings": bookings,
        "intent": intent_data,
        "decision": decision,
        "customer_response": customer_response
    }