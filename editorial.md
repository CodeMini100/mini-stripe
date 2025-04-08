# Building Stripe_lite From Scratch

Welcome to this hands-on tutorial for creating a minimal viable product (MVP) of **Stripe_lite**, a simplified, self-contained payment processing service inspired by the functionality of Stripe. In this guide, we will:

1. Build and configure the core FastAPI application (our Stripe_lite API).  
2. Implement payment (charges, refunds), customer management, subscription handling, and event webhooks.  
3. Create a minimal dashboard or set of endpoints for viewing transactions.  
4. Add an example integration using Flask (backend) and React (frontend) to demonstrate how a consumer application might talk to Stripe_lite.  

You’ll learn best practices for folder structure, environment configuration, and bridging backend to frontend, along with suggested approaches for data modeling and logic design.

---

## Prerequisites

- Python 3.8+  
- pip (or Poetry) for Python package management  
- Node.js (14.x+) for running the React demo app  
- A database (PostgreSQL, SQLite, etc.)—we’ll assume SQLite for simplicity  
- Basic familiarity with FastAPI, Flask, and React concepts  

---

## Step 1: Project Initialization

First, create a new folder for your Stripe_lite MVP codebase. From your terminal:

```bash
mkdir stripe_lite
cd stripe_lite
```

Initialize a Git repository if desired:

```bash
git init
```

Then, create a `requirements.txt` for the Python dependencies:

```bash
echo "fastapi==0.95.2
uvicorn==0.22.0
pydantic==1.10.2
sqlalchemy==2.0.15
python-dotenv==1.0.0
requests==2.28.2
flask==2.2.5" > requirements.txt
```

(Adjust versions as needed or desired.)

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

> **Tip**: If you prefer Poetry, run `poetry init` and then add these dependencies to your `pyproject.toml`.

---

## Step 2: Directory Structure

Below is an overview of the directory structure we will create:

```
stripe_lite/
├── main.py
├── config.py
├── requirements.txt
├── payments/
│   ├── payments_router.py
│   ├── payments_service.py
│   └── payments_models.py
├── customers/
│   ├── customers_router.py
│   ├── customers_service.py
│   └── customers_models.py
├── subscriptions/
│   ├── subscriptions_router.py
│   ├── subscriptions_service.py
│   └── subscriptions_models.py
├── webhooks/
│   ├── webhooks_router.py
│   ├── webhooks_service.py
│   └── webhooks_models.py
├── dashboard/
│   └── dashboard_router.py
├── utils/
│   ├── logger.py
│   └── auth.py
└── examples/
    └── basic_demo/
        ├── demo_api.py
        ├── demo_app.py
        ├── demo_config.py
        ├── frontend/
        │   ├── package.json
        │   ├── public/
        │   │   └── index.html
        │   └── src/
        │       ├── App.js
        │       └── index.js
        └── README.md
```

We’ll now walk through each of these key files/folders.

---

## Step 3: Configuration and Entry Point

### 3.1 config.py

A place for environment-based or file-based configuration. You might use `python-dotenv` to load variables from a `.env` file.

```python
# config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from a .env file if present

def load_config():
    """Reads environment variables or a .env file."""
    return {
        "DATABASE_URL": os.getenv("DATABASE_URL", "sqlite:///stripe_lite.db"),
        "SECRET_KEY": os.getenv("SECRET_KEY", "supersecretkey"),
    }

def get_database_url() -> str:
    """Returns a valid SQLAlchemy DB URL."""
    config = load_config()
    return config["DATABASE_URL"]
```

> **Best Practice**: Avoid committing real secrets or production credentials (like `SECRET_KEY`) to version control. Use environment variables or Vault solutions in production.

### 3.2 main.py

Your main FastAPI application entry point. You can import and mount routers from each module, starting the application with `uvicorn main:app --reload`.

```python
# main.py

from fastapi import FastAPI
import uvicorn

from config import load_config
from payments.payments_router import router as payments_router
from customers.customers_router import router as customers_router
from subscriptions.subscriptions_router import router as subscriptions_router
from webhooks.webhooks_router import router as webhooks_router
from dashboard.dashboard_router import router as dashboard_router

def create_app() -> FastAPI:
    """Initializes FastAPI, includes router modules, and returns the application."""
    app = FastAPI(title="Stripe_lite")

    # Load config (not strictly necessary to store inside FastAPI instance, but can be done)
    config = load_config()
    app.state.config = config

    # Include routers
    app.include_router(payments_router, prefix="/payments", tags=["payments"])
    app.include_router(customers_router, prefix="/customers", tags=["customers"])
    app.include_router(subscriptions_router, prefix="/subscriptions", tags=["subscriptions"])
    app.include_router(webhooks_router, prefix="/webhooks", tags=["webhooks"])
    app.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])

    return app

app = create_app()

def run_app():
    """Optional: Launches the server on a specific port if not using uvicorn CLI."""
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_app()
```

> **Potential Pitfall**: Make sure to configure CORS if you’ll be calling the API from JS apps served on different domains. You can use `fastapi.middleware.cors` for that.

---

## Step 4: Payments Module

### 4.1 payments_router.py

Endpoints for creating charges and processing refunds. We’ll accept request data as JSON and use Pydantic models for validation.

```python
# payments/payments_router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .payments_service import create_charge, refund_charge

router = APIRouter()

class ChargeRequest(BaseModel):
    customer_id: str
    amount: float
    payment_method: str  # e.g. "card_xxxx"

class RefundRequest(BaseModel):
    charge_id: str

@router.post("/create_charge")
def create_charge_endpoint(request_data: ChargeRequest):
    charge = create_charge(
        request_data.customer_id,
        request_data.amount,
        request_data.payment_method
    )
    if not charge:
        raise HTTPException(status_code=400, detail="Charge creation failed.")
    return {"status": "success", "charge": charge}

@router.post("/refund_charge")
def refund_charge_endpoint(request_data: RefundRequest):
    result = refund_charge(request_data.charge_id)
    if not result:
        raise HTTPException(status_code=400, detail="Refund failed.")
    return {"status": "success", "refund_details": result}
```

### 4.2 payments_service.py

Business logic that either simulates or calls a real payment provider. For now, we’ll just store data in memory or in a database (e.g., via SQLAlchemy).

```python
# payments/payments_service.py

from typing import Optional
# from .payments_models import Charge  # If using SQLAlchemy or pydantic models
# from sqlalchemy.orm import Session

FAKE_DB = {
    "charges": []
}

def create_charge(customer_id: str, amount: float, payment_method: str) -> dict:
    """Writes a charge record, calls or simulates payment."""
    new_charge = {
        "id": f"ch_{len(FAKE_DB['charges']) + 1}",
        "customer_id": customer_id,
        "amount": amount,
        "payment_method": payment_method,
        "status": "succeeded",  # let's assume success
    }
    FAKE_DB["charges"].append(new_charge)
    return new_charge

def refund_charge(charge_id: str) -> Optional[dict]:
    """Updates the charge record to reflect a refund."""
    for c in FAKE_DB["charges"]:
        if c["id"] == charge_id:
            c["status"] = "refunded"
            return c
    return None
```

### 4.3 payments_models.py

Pydantic or SQLAlchemy models for the `payments` module. Below is a placeholder if you want to set up a real database model with SQLAlchemy.

```python
# payments/payments_models.py

# Example of a SQLAlchemy model
# from sqlalchemy import Column, Integer, String, Float
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Charge(Base):
#     __tablename__ = "charges"
#     id = Column(String, primary_key=True)
#     customer_id = Column(String)
#     amount = Column(Float)
#     payment_method = Column(String)
#     status = Column(String)
```

---

## Step 5: Customers Module

Similar approach for creating/fetching customers.

### 5.1 customers_router.py

```python
# customers/customers_router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .customers_service import create_customer, fetch_customer

router = APIRouter()

class CustomerRequest(BaseModel):
    name: str
    email: str
    payment_info: str

@router.post("/")
def create_customer_endpoint(request_data: CustomerRequest):
    customer = create_customer(
        request_data.name,
        request_data.email,
        request_data.payment_info
    )
    if not customer:
        raise HTTPException(status_code=400, detail="Customer creation failed.")
    return {"status": "success", "customer": customer}

@router.get("/{customer_id}")
def get_customer_endpoint(customer_id: str):
    customer = fetch_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return customer
```

### 5.2 customers_service.py

```python
# customers/customers_service.py

from typing import Optional

FAKE_DB = {
    "customers": []
}

def create_customer(name: str, email: str, payment_info: str) -> dict:
    customer_id = f"cust_{len(FAKE_DB['customers']) + 1}"
    new_customer = {
        "id": customer_id,
        "name": name,
        "email": email,
        "payment_info": payment_info
    }
    FAKE_DB["customers"].append(new_customer)
    return new_customer

def fetch_customer(customer_id: str) -> Optional[dict]:
    for c in FAKE_DB["customers"]:
        if c["id"] == customer_id:
            return c
    return None
```

### 5.3 customers_models.py

Optionally define Pydantic or SQLAlchemy models here.

---

## Step 6: Subscriptions Module

Handles recurring plans, billing, and invoice generation.

### 6.1 subscriptions_router.py

```python
# subscriptions/subscriptions_router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .subscriptions_service import create_subscription, cancel_subscription

router = APIRouter()

class SubscriptionRequest(BaseModel):
    customer_id: str
    plan_id: str

class CancelRequest(BaseModel):
    subscription_id: str

@router.post("/create")
def create_subscription_endpoint(request_data: SubscriptionRequest):
    sub = create_subscription(request_data.customer_id, request_data.plan_id)
    if not sub:
        raise HTTPException(status_code=400, detail="Subscription creation failed.")
    return {"status": "success", "subscription": sub}

@router.post("/cancel")
def cancel_subscription_endpoint(request_data: CancelRequest):
    result = cancel_subscription(request_data.subscription_id)
    if not result:
        raise HTTPException(status_code=400, detail="Subscription cancellation failed.")
    return {"status": "success", "subscription": result}
```

### 6.2 subscriptions_service.py

```python
# subscriptions/subscriptions_service.py

from typing import Optional

FAKE_DB = {
    "subscriptions": []
}

def create_subscription(customer_id: str, plan_id: str) -> dict:
    new_subscription = {
        "id": f"sub_{len(FAKE_DB['subscriptions']) + 1}",
        "customer_id": customer_id,
        "plan_id": plan_id,
        "status": "active"
    }
    FAKE_DB["subscriptions"].append(new_subscription)
    return new_subscription

def cancel_subscription(subscription_id: str) -> Optional[dict]:
    for s in FAKE_DB["subscriptions"]:
        if s["id"] == subscription_id:
            s["status"] = "canceled"
            return s
    return None

def generate_invoice(subscription_id: str) -> dict:
    """Can be triggered periodically or by a webhook event for renewal."""
    # Minimal mock example
    invoice = {
        "id": f"inv_{subscription_id}",
        "subscription_id": subscription_id,
        "status": "issued"
    }
    # In real scenarios, store in DB and handle billing logic
    return invoice
```

### 6.3 subscriptions_models.py

Where you’d define subscription-related Pydantic or SQLAlchemy models.

---

## Step 7: Webhooks Module

Simulates receiving asynchronous event data from a payment processor or other system.

### 7.1 webhooks_router.py

```python
# webhooks/webhooks_router.py

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from .webhooks_service import handle_charge_succeeded, handle_subscription_renewed

router = APIRouter()

class WebhookEvent(BaseModel):
    event_type: str
    data: dict

@router.post("/")
def webhook_receiver_endpoint(event: WebhookEvent, x_signature: str = Header(None)):
    # In real scenario, validate x_signature to ensure authenticity
    if not x_signature:
        raise HTTPException(status_code=400, detail="Missing signature header.")

    if event.event_type == "charge.succeeded":
        handle_charge_succeeded(event.data)
    elif event.event_type == "subscription.renewed":
        handle_subscription_renewed(event.data)
    else:
        raise HTTPException(status_code=400, detail="Unsupported event type.")

    return {"status": "processed"}
```

### 7.2 webhooks_service.py

```python
# webhooks/webhooks_service.py

def handle_charge_succeeded(event_data: dict):
    # Mark a stored charge as succeeded, or create one if needed
    print("Handling charge succeeded:", event_data)

def handle_subscription_renewed(event_data: dict):
    # Possibly call generate_invoice or update subscription status
    print("Handling subscription renewal:", event_data)
```

### 7.3 webhooks_models.py

Placeholder for request validation models if needed.

---

## Step 8: Dashboard Module

A minimal external or internal admin interface, or purely an API-based approach.

```python
# dashboard/dashboard_router.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/summary")
def get_dashboard_data_endpoint():
    # Summarize recent charges, new customers, subscription metrics
    return {
        "recent_charges": [],
        "new_customers": [],
        "subscription_metrics": {}
    }

@router.get("/transaction/{charge_id}")
def get_transaction_details_endpoint(charge_id: str):
    # Return details about a single charge
    return {
        "charge_id": charge_id,
        "status": "mocked"
    }
```

---

## Step 9: Utilities

### 9.1 logger.py

Centralized logging. You might integrate with Python’s built-in `logging`.

```python
# utils/logger.py

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("stripe_lite")

def log_debug(message: str):
    logger.debug(message)

def log_info(message: str):
    logger.info(message)

def log_error(message: str):
    logger.error(message)
```

### 9.2 auth.py

Token-based or session-based security. For demonstration:

```python
# utils/auth.py

import jwt
from datetime import datetime, timedelta

SECRET_KEY = "CHANGEME"

def create_jwt(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_jwt(token: str) -> dict:
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
```

---

## Step 10: Example Usage (Flask + React)

To showcase how an external application might call Stripe_lite, we’ll build a small demo in `examples/basic_demo/`.

### 10.1 demo_config.py

```python
# examples/basic_demo/demo_config.py

import os

def load_demo_config():
    return {
        "STRIPE_LITE_BASE_URL": os.getenv("STRIPE_LITE_BASE_URL", "http://localhost:8000")
    }

def get_stripe_lite_api_url() -> str:
    return load_demo_config()["STRIPE_LITE_BASE_URL"]
```

### 10.2 demo_api.py

A thin client to call our Stripe_lite endpoints from Python. We’ll assume the FastAPI server is running at `localhost:8000`.

```python
# examples/basic_demo/demo_api.py

import requests
from .demo_config import get_stripe_lite_api_url

def create_charge(customer_id, amount, payment_method):
    url = f"{get_stripe_lite_api_url()}/payments/create_charge"
    payload = {
        "customer_id": customer_id,
        "amount": amount,
        "payment_method": payment_method
    }
    response = requests.post(url, json=payload)
    return response.json()

def refund_charge(charge_id):
    url = f"{get_stripe_lite_api_url()}/payments/refund_charge"
    payload = {"charge_id": charge_id}
    response = requests.post(url, json=payload)
    return response.json()

def list_customers():
    url = f"{get_stripe_lite_api_url()}/customers"
    response = requests.get(url)
    return response.json()
```

### 10.3 demo_app.py

A simple Flask server to serve endpoints and a minimal HTML or React app.

```python
# examples/basic_demo/demo_app.py

from flask import Flask, request, jsonify
from . import demo_api

def create_flask_app():
    app = Flask(__name__)

    @app.route("/create_charge", methods=["POST"])
    def create_charge_route():
        data = request.json
        result = demo_api.create_charge(
            data["customer_id"],
            data["amount"],
            data["payment_method"]
        )
        return jsonify(result)

    @app.route("/refund_charge", methods=["POST"])
    def refund_charge_route():
        data = request.json
        result = demo_api.refund_charge(data["charge_id"])
        return jsonify(result)

    @app.route("/customers", methods=["GET"])
    def list_customers_route():
        result = demo_api.list_customers()
        return jsonify(result)

    return app

def run_demo_app():
    app = create_flask_app()
    app.run(port=5000, debug=True)

if __name__ == "__main__":
    run_demo_app()
```

### 10.4 frontend (React)

A minimal React example that sends requests to the Flask routes (which, in turn, talk to Stripe_lite).

• package.json  
• public/index.html  
• src/App.js  
• src/index.js  

(We’ll only show the highlights.)

#### 10.4.1 package.json

```json
{
  "name": "stripe-lite-demo-frontend",
  "version": "1.0.0",
  "scripts": {
    "start": "react-scripts start"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
```

#### 10.4.2 public/index.html

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Stripe_lite Demo</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
```

#### 10.4.3 src/App.js

```jsx
import React, { useState } from 'react';

function App() {
  const [chargeId, setChargeId] = useState(null);

  const createCharge = async () => {
    const response = await fetch('/create_charge', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        customer_id: 'cust_1',
        amount: 100.00,
        payment_method: 'card_4242'
      })
    });
    const data = await response.json();
    if (data.charge) {
      setChargeId(data.charge.id);
    }
  };

  const refundCharge = async () => {
    if (!chargeId) return;
    const response = await fetch('/refund_charge', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ charge_id: chargeId })
    });
    const data = await response.json();
    console.log('Refund response', data);
  };

  return (
    <div>
      <h1>Stripe_lite Demo</h1>
      <button onClick={createCharge}>Create Charge</button>
      {chargeId && (
        <div>
          <p>Charge created with ID: {chargeId}</p>
          <button onClick={refundCharge}>Refund Charge</button>
        </div>
      )}
    </div>
  );
}

export default App;
```

#### 10.4.4 src/index.js

```jsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);
```

### 10.5 README.md

Document how to run the Flask server and React dev server. Example:

```
# Basic Demo

1. Ensure Stripe_lite (FastAPI) is running on http://localhost:8000
2. Install dependencies for Flask:
   pip install -r ../../requirements.txt
3. Run the Flask server:
   python demo_app.py
4. In a separate terminal, navigate to frontend/ and run:
   npm install
   npm start
```

> **Pitfall**: Make sure the frontend is configured to send requests to the correct Flask route. If your React app is on http://localhost:3000 and your Flask server on http://localhost:5000, you may need to proxy or adjust your fetch calls.

---

## Step 11: Running and Testing Stripe_lite

1. Start Stripe_lite (FastAPI) in one terminal:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
2. Open a separate terminal to run the Demo (Flask) server:
   ```bash
   cd examples/basic_demo
   python demo_app.py
   ```
3. In another terminal, start the React dev server:
   ```bash
   cd frontend
   npm install
   npm start
   ```
4. Navigate to http://localhost:3000 in your browser to see the simple UI.  

Now you can click “Create Charge” and see the request flow:
• React → Flask → Stripe_lite.  

---

## Conclusion

Congratulations! You have built a minimal version of **Stripe_lite**:

- FastAPI-based Payment endpoints (charges/refunds).  
- Customer management.  
- Subscriptions with mocked recurring billing logic.  
- Webhook endpoints for event handling.  
- A minimal dashboard.  
- A working example bridging a Flask server and React client to call your Stripe_lite API.

While this tutorial demonstrates core concepts, production-grade solutions (like Stripe) require robust payment gateways, security, data migrations, and compliance. Nonetheless, the structure here provides a solid foundation to expand upon. 

Feel free to adapt and extend the code to integrate real payment processors, advanced authentication, or robust database integrations. Happy coding!