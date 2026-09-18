from .data_loader import get_policies


def evaluate_request(customer, bookings, intent_data):
    policies = get_policies()

    decisions = []
    escalation_required = False

    # ---------------------------------------------------------
    # EXTRACT INTENT DATA
    # ---------------------------------------------------------

    status = intent_data.get("status")
    delay_hours = intent_data.get("delay_hours")

    requested_hotel = intent_data.get(
        "requested_hotel",
        False
    )

    requested_full_night_hotel = intent_data.get(
        "requested_full_night_hotel",
        False
    )

    requested_refund = intent_data.get(
        "requested_refund",
        False
    )

    requested_higher_fare = intent_data.get(
        "requested_higher_fare",
        False
    )

    fare_difference = intent_data.get(
        "fare_difference",
        0
    ) or 0

    # ---------------------------------------------------------
    # CANCELLATION
    # ---------------------------------------------------------

    if status == "cancelled":

        if requested_refund:

            decisions.append({
                "action": "FULL_REFUND",
                "status": "APPROVED",
                "reason": (
                    "Airline-caused cancellation qualifies "
                    "for a full refund."
                ),
                "source": "Cancellation Rebooking Rule"
            })

        else:

            decisions.append({
                "action": "FREE_REBOOKING",
                "status": "AVAILABLE",
                "reason": (
                    "Airline-caused cancellation allows free "
                    "rebooking on the next available flight "
                    "within 24 hours."
                ),
                "source": "Cancellation Rebooking Rule"
            })

    # ---------------------------------------------------------
    # DELAY COMPENSATION
    # ---------------------------------------------------------

    if delay_hours is not None:

        # -----------------------------------------------------
        # DELAY MORE THAN 5 HOURS
        # -----------------------------------------------------

        if delay_hours > 5:

            decisions.append({
                "action": "MEAL_VOUCHER",
                "status": "APPROVED",
                "reason": (
                    "Delay is more than 5 hours and qualifies "
                    "for the ₹500 meal voucher."
                ),
                "source": "Delay Compensation Rule"
            })

            decisions.append({
                "action": "LOUNGE_ACCESS",
                "status": "APPROVED",
                "reason": (
                    "Delay is more than 3 hours and qualifies "
                    "for lounge access."
                ),
                "source": "Delay Compensation Rule"
            })

            decisions.append({
                "action": "HOTEL_ACCOMMODATION",
                "status": "APPROVED",
                "reason": (
                    "Delay is more than 5 hours. Hotel "
                    "accommodation covers the delayed hours only."
                ),
                "source": "Delay Compensation Rule"
            })

            # Customer explicitly asks for a full night
            if requested_full_night_hotel:

                decisions.append({
                    "action": "FULL_NIGHT_HOTEL",
                    "status": "NOT_APPROVED",
                    "reason": (
                        "The supplied policy covers hotel "
                        "accommodation for delayed hours only, "
                        "not a full night's stay."
                    ),
                    "source": "Delay Compensation Rule"
                })

        # -----------------------------------------------------
        # DELAY MORE THAN 3 HOURS AND UP TO 5 HOURS
        # -----------------------------------------------------

        elif delay_hours > 3:

            decisions.append({
                "action": "MEAL_VOUCHER",
                "status": "APPROVED",
                "reason": (
                    "Delay is more than 3 hours and qualifies "
                    "for the ₹500 meal voucher."
                ),
                "source": "Delay Compensation Rule"
            })

            decisions.append({
                "action": "LOUNGE_ACCESS",
                "status": "APPROVED",
                "reason": (
                    "Delay is more than 3 hours and qualifies "
                    "for lounge access."
                ),
                "source": "Delay Compensation Rule"
            })

            if requested_hotel:

                decisions.append({
                    "action": "HOTEL_ACCOMMODATION",
                    "status": "NOT_APPROVED",
                    "reason": (
                        "Hotel accommodation applies only when "
                        "the delay is more than 5 hours."
                    ),
                    "source": "Delay Compensation Rule"
                })

        # -----------------------------------------------------
        # DELAY 3 HOURS OR LESS
        # -----------------------------------------------------

        else:

            if requested_hotel:

                decisions.append({
                    "action": "HOTEL_ACCOMMODATION",
                    "status": "NOT_APPROVED",
                    "reason": (
                        "The supplied policy does not provide "
                        "hotel accommodation for delays of "
                        "3 hours or less."
                    ),
                    "source": "Delay Compensation Rule"
                })

    # ---------------------------------------------------------
    # HIGHER FARE / UPGRADE REQUEST
    # ---------------------------------------------------------

    if requested_higher_fare:

        # -----------------------------------------------------
        # EXPLICIT FARE DIFFERENCE PROVIDED
        # -----------------------------------------------------

        if fare_difference > 0:

            if fare_difference > 1500:

                escalation_required = True

                decisions.append({
                    "action": "HIGHER_FARE_REBOOKING",
                    "status": "ESCALATE",
                    "reason": (
                        f"Fare difference is ₹{fare_difference}, "
                        "which is above the agent approval limit "
                        "of ₹1,500."
                    ),
                    "source": "Fare Difference Rule"
                })

            else:

                decisions.append({
                    "action": "HIGHER_FARE_REBOOKING",
                    "status": "CUSTOMER_PAYS",
                    "reason": (
                        f"Customer must pay the fare difference "
                        f"of ₹{fare_difference}."
                    ),
                    "source": "Fare Difference Rule"
                })

        # -----------------------------------------------------
        # NO FARE DIFFERENCE PROVIDED
        # -----------------------------------------------------

        else:

            decisions.append({
                "action": "BUSINESS_CLASS_UPGRADE",
                "status": "NOT_APPROVED",
                "reason": (
                    "The supplied policy does not provide a "
                    "free business-class or higher-fare upgrade."
                ),
                "source": "Supplied Airline Policy"
            })

    # ---------------------------------------------------------
    # LOYALTY TIER
    # ---------------------------------------------------------

    tier = customer.get("loyalty_tier")

    if tier in ["Gold", "Platinum"]:

        decisions.append({
            "action": "PRIORITY_REBOOKING",
            "status": "AVAILABLE",
            "reason": (
                f"{tier} tier customers receive "
                "priority rebooking."
            ),
            "source": "Loyalty Tier Rule"
        })

    # ---------------------------------------------------------
    # FINAL DECISION
    # ---------------------------------------------------------

    if escalation_required:

        final_status = "ESCALATION_REQUIRED"

    elif any(
        decision["status"] == "APPROVED"
        for decision in decisions
    ):

        final_status = "RESOLVED"

    else:

        final_status = "POLICY_RESPONSE"

    # ---------------------------------------------------------
    # RETURN DECISION
    # ---------------------------------------------------------

    return {
        "final_status": final_status,
        "escalation_required": escalation_required,
        "decisions": decisions
    }