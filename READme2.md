# TripSpark – Sprint 3 Submission

### *Cloud Computing – COMS W4153*

**Team: Cloud Six**

**Watch Sprint 3 Demo here: https://www.youtube.com/watch?v=8tgauc3XBxY**

This repository contains our **Sprint 3 implementation** of the TripSpark cloud platform.

We implemented **all four required features**:

1. **OAuth2 Login with Google (Auth Microservice on Cloud Run)**
2. **JWT-protected endpoint in Catalog Microservice (Compute Engine VM)**
3. **Cloud Function-style event handler using Functions Framework (Cloud Run)**
4. **Event Triggering — Catalog microservice emits a Pub/Sub event processed by the handler**

This README explains **architecture, commands, testing, and demo steps** for each requirement.

---

# Requirement 1 — OAuth2 Login Using Google

### **Microservice:** `tripspark-auth` (Cloud Run)

We implemented a Google OAuth2 login flow:

* User clicks **Login with Google**
* We verify Google ID token
* Extract user info (`email`, `sub`, etc.)
* Generate our own **TripSpark JWT** using:

```
AUTH_JWT_SECRET="dev-secret-change-me"
```

* Return:

  * Google user metadata
  * TripSpark JWT
  * JSON display for debugging

### **Auth Microservice URL**

```
https://tripspark-auth-817898523355.us-central1.run.app/
```

---

## **How to Demo Requirement 1**

1. Open the URL above in a browser.
2. Click **Login with Google**.
3. Show the returned page:

   * Google Email
   * Google Sub ID
   * The generated TripSpark JWT
4. Copy the TripSpark JWT (used in Req 2).

---

# Requirement 2 — JWT Validation in Catalog Microservice

### **Microservice:** Catalog (FastAPI on Compute Engine VM)

### **Secure Endpoint:** `/secure-catalog-ping`

We implemented JWT validation:

* Requires header:

  ```
  Authorization: Bearer <jwt>
  ```
* Validates JWT with same secret used in auth microservice.
* Returns decoded user info if valid.
* Returns `403 Not authenticated` if missing / invalid.

---

### Swagger UI

```
http://<EXTERNAL-IP>:8000/docs
```

### How to Run Catalog Microservice

```bash
cd ~/TripSpark-Catalog
source venv/bin/activate
export AUTH_JWT_SECRET="dev-secret-change-me"
python3 -m uvicorn main3:app --host 0.0.0.0 --port 8000
```

---

## **How to Demo Requirement 2**

1. Open Swagger UI:

   ```
   http://<EXTERNAL-IP>:8000/docs
   ```

2. Click **Authorize** (top right).

3. Paste token:

```
Bearer <your_tripspark_jwt>
```

4. Call:

```
GET /secure-catalog-ping
```

Expected success response:

```json
{
  "message": "Secure Catalog endpoint OK",
  "user": {
    "email": "hk3351@columbia.edu",
    "sub": "104014995704084647314",
    "iss": "tripspark-auth"
  }
}
```

5. Remove the JWT → call again → shows:

```
403 Not authenticated
```

---

# Requirement 3 — Cloud Function-Style Handler (Functions Framework)

### **Service:** `tripspark-event-handler` (Cloud Run)

### **Trigger:** Pub/Sub topic: `tripspark-events`

We deployed a Python Cloud Functions Framework service that:

* Receives Pub/Sub messages via push subscription
* Decodes event payload
* Logs structured event data

### Cloud Run URL

```
https://tripspark-event-handler-817898523355.us-central1.run.app
```

### Pub/Sub Topic

```
tripspark-events
```

---

## **How to Demo Requirement 3**

1. Open Cloud Run → `tripspark-event-handler`
2. Click **Logs**
3. Show function logs whenever a Pub/Sub message is delivered

Example log output:

```
=== TripSpark Event Received ===
Function triggered by Pub/Sub!
Payload: {"event_type":"TEST","source":"catalog"}
```

---

Requirement 4
Trigger the Cloud Function from a Microservice
run this: 

cd ~/TripSpark-Catalog/TripSpark-Catalog

source venv/bin/activate


export AUTH_JWT_SECRET="dev-secret-change-me"

export GCP_PROJECT_ID="long-way-475401-b6"

export TRIPSPARK_EVENTS_TOPIC="tripspark-events"

The Catalog microservice publishes events to Pub/Sub using:

POST /event-test


The Cloud Run function (tripspark-event-handler) processes these events.

Step 1: Trigger Event from Swagger UI

In Swagger:

Select POST /event-test and execute with:

Hello from Catalog VM!


The response should be:

{
  "status": "event published",
  "payload": {
    "source": "catalog-microservice",
    "event_type": "CATALOG_TEST",
    "message": "Hello from Catalog VM!"
  }
}

Step 2: Verify Cloud Function Trigger via Logs

In Cloud Shell:

gcloud logging read \
  'resource.type="cloud_run_revision" AND resource.labels.service_name="tripspark-event-handler"' \
  --limit=20 \
  --format="table(timestamp, textPayload)"


Expected log output:

=== TripSpark Event Received (HTTP-style) ===
Cloud Function TRIGGERED by Pub/Sub!
Payload: {'event_type': 'CATALOG_TEST', 'source': 'catalog-microservice', 'message': 'Hello from Catalog VM!'}


This completes Requirement 4.

---



# Full Demo Checklist

| Req   | Description           | Demo Steps                                             |
| ----- | --------------------- | ------------------------------------------------------ |
| **1** | Google OAuth Sign-in  | Visit auth URL → Login → Show TripSpark JWT            |
| **2** | JWT Validation        | Open `/docs` → Authorize → Call `/secure-catalog-ping` |
| **3** | Cloud Function        | Show Cloud Run logs for event handler                  |
| **4** | Pub/Sub Event Trigger | Publish event → show logs processed                    |

---

# Final Notes

* All secrets and configs match across microservices.
* All endpoints run independently and demonstrate microservice communication.
* Architecture is production-style with Cloud Run + VM + Pub/Sub.

