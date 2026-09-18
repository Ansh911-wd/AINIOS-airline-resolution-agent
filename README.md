# ✈️ AINIOS Airline Resolution Agent

A customer-facing AI resolution agent for handling airline disruption scenarios such as flight cancellations, delays, refunds, accommodation requests, and higher-fare rebooking.

## Problem

Customers affected by airline disruptions often need immediate answers about refunds, compensation, accommodation, and rebooking.

The agent understands the customer's request, retrieves the relevant booking/customer context, applies supplied airline policies, provides a resolution, and escalates cases that exceed agent authority.

## Key Features

- Customer and booking identification using PNR
- Natural-language customer intent extraction using Gemini
- Deterministic policy evaluation
- Refund and rebooking decisions
- Delay compensation evaluation
- Hotel accommodation evaluation
- Loyalty-tier based priority rebooking
- Fare-difference authority checks
- Supervisor escalation for out-of-authority requests
- Customer-friendly response generation
- Policy source visibility
- Audit trail of the resolution process
- Fallback intent extraction when the LLM is temporarily unavailable

## Architecture

```text
Customer
   |
   v
React Frontend
   |
   v
FastAPI Backend
   |
   +--------------------+
   |                    |
   v                    v
Gemini AI          Customer/Booking Data
   |                    |
   |                    |
   +---------+----------+
             |
             v
      Intent Extraction
             |
             v
    Deterministic Policy Engine
             |
             v
       Resolution Decision
             |
       +-----+------+
       |            |
       v            v
 Customer       Audit Trail
 Response

##Project Structure

 AINIOS-airline-resolution-agent/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── agent.py
│   │   ├── policy_engine.py
│   │   └── data_loader.py
│   ├── requirements.txt
│   ├── test_gemini.py
│   └── .env
│
├── data/
│   ├── customers.json
│   ├── bookings.json
│   └── policies.json
│
├── docs/
│   └── architecture.md
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md


##AI Approach

The system follows a hybrid AI architecture.

LLM responsibilities

Gemini is used for:

-Understanding customer language
-Extracting intent
-Detecting sentiment
-Generating customer-facing responses
-Deterministic responsibilities

The policy engine is responsible for:

  Checking delay thresholds
  Checking refund eligibility
  Checking hotel eligibility
  Checking fare-difference limits
  Checking loyalty benefits
  Triggering escalation

This prevents the LLM from inventing or changing airline policy.

##Technology Stack
  Frontend

   React
   Vite
   JavaScript
   CSS

Backend
   Python
   FastAPI
   Uvicorn
   Pydantic
AI

   Google Gemini API
   Gemini 3.6 Flash

Data
  JSON-based customer data
  JSON-based booking data
  JSON-based airline policy data

 ## Running Locally

### 1. Backend Setup

Open a terminal and navigate to the backend folder:

```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.6-flash

Backend:http://127.0.0.1:8000

Swagger:http://127.0.0.1:8000/docs

Frontend:
cd frontend
npm install
npm run dev
http://localhost:5173

Design Principle

The system uses:

"LLM for language understanding, deterministic rules for policy enforcement".

This provides flexibility in customer conversation while keeping resolution decisions grounded in the supplied airline policy.

Security

API keys are stored in environment variables and should never be committed to GitHub
:-backend/.env

---

# 2. `docs/architecture.md`

Replace the file with:

```markdown
# Architecture & Process Flow

## 1. System Overview

The AINIOS Airline Resolution Agent uses a hybrid architecture combining an LLM with deterministic business-policy enforcement.

The architecture separates:

1. Language understanding
2. Customer/booking context
3. Policy evaluation
4. Resolution generation
5. Auditability

## 2. Process Flow

```text
Customer Message
      |
      v
React Customer UI
      |
      v
POST /api/resolve
      |
      v
FastAPI
      |
      +----------------------+
      |                      |
      v                      v
Customer/Booking Data      Gemini
      |                      |
      |                Intent Extraction
      |                      |
      +----------+-----------+
                 |
                 v
        Deterministic Policy Engine
                 |
          +------+------+
          |             |
          v             v
       Resolve       Escalate
          |
          v
   Gemini Response Generation
          |
          v
      React UI
          |
    +-----+------+
    |            |
    v            v
Decision     Audit Trail