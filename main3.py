from __future__ import annotations

import os
import socket
import json
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, Path, Header
import mysql.connector
import jwt

# NEW for Requirement 4
from google.cloud import pubsub_v1


# ---------------------------------------------------------------------
# MySQL Connectivity
# ---------------------------------------------------------------------
DB_CONFIG = {
    "host": "10.142.0.4",
    "user": "felicia",
    "password": "1234",
    "database": "TripSparkCatalog",
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ---------------------------------------------------------------------
# App Config
# ---------------------------------------------------------------------
port = int(os.environ.get("FASTAPIPORT", 8000))

AUTH_JWT_SECRET = os.environ.get("AUTH_JWT_SECRET")

app = FastAPI(
    title="TripSpark - Catalog API",
    description="FastAPI app using Pydantic v2 models for TripSpark - Catalog deployed in GCP VM",
    version="0.1.0",
)


# ---------------------------------------------------------------------
# Pub/Sub configuration (Requirement 4)
# ---------------------------------------------------------------------
PUBSUB_TOPIC = "projects/long-way-475401-b6/topics/tripspark-events"
publisher = pubsub_v1.PublisherClient()


# ---------------------------------------------------------------------
# HEALTH ENDPOINTS
# ---------------------------------------------------------------------
def make_health(echo: Optional[str], path_echo: Optional[str] = None):
    try:
        ip_catalog = socket.gethostbyname(socket.gethostname())
    except Exception:
        ip_catalog = "127.0.0.1"

    return {
        "status": 200,
        "status_message": "OK",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "ip_address": ip_catalog,
        "echo": echo,
        "path_echo": path_echo,
    }


@app.get("/health")
def get_health_no_path(echo: Optional[str] = Query(None)):
    return make_health(echo=echo)


@app.get("/health/{path_echo}")
def get_health_with_path(path_echo: str = Path(...), echo: Optional[str] = Query(None)):
    return make_health(echo=echo, path_echo=path_echo)


# ---------------------------------------------------------------------
# Utility: normalize DB rows
# ---------------------------------------------------------------------
def normalize_catalog_row(row: dict) -> dict:
    for field in ["vibes", "activities", "food"]:
        if field in row and isinstance(row[field], (set, list)):
            row[field] = ", ".join(sorted(row[field]))
    return row


# ---------------------------------------------------------------------
# CREATE CATALOG
# ---------------------------------------------------------------------
@app.post("/catalogs", status_code=201)
def create_catalog(catalog):
    cnx = cursor = None
    try:
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)

        insert_query = """
        INSERT INTO catalog 
        (poi, city, country, currency, latitude, longitude, rating,
         description, spending, budget, vibes, activities, food,
         best_season, trip_days, nearest_airport, transport,
         accessibility, direction)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            catalog.poi.lower().strip(),
            catalog.city.lower().strip(),
            catalog.country.lower().strip(),
            catalog.currency.lower().strip(),
            catalog.latitude,
            catalog.longitude,
            catalog.rating,
            catalog.description.lower().strip(),
            catalog.spending.lower().strip(),
            catalog.budget,
            catalog.vibes.lower().strip(),
            catalog.activities.lower().strip(),
            catalog.food.lower().strip(),
            catalog.best_season.lower().strip(),
            catalog.trip_days,
            catalog.nearest_airport.lower().strip(),
            catalog.transport.lower().strip(),
            catalog.accessibility.lower().strip(),
            catalog.direction,
        )

        cursor.execute(insert_query, values)
        cnx.commit()

        cursor.execute("SELECT * FROM catalog WHERE poi = %s", (catalog.poi.lower().strip(),))
        row = cursor.fetchone()
        return normalize_catalog_row(row)

    except mysql.connector.Error as err:
        if err.errno == 1062:
            raise HTTPException(status_code=400, detail=f"The location {catalog.poi} already exists")
        raise HTTPException(status_code=500, detail=f"MySQL error: {err}")

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()


# ---------------------------------------------------------------------
# LIST / FILTER CATALOGS
# ---------------------------------------------------------------------
@app.get("/catalogs")
def list_catalogs(
    city: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    rating_avg: Optional[float] = Query(None),
    vibes: Optional[str] = Query(None),
    budget: Optional[float] = Query(None),
    poi: Optional[str] = Query(None),
    activities: Optional[str] = Query(None),
    food: Optional[str] = Query(None),
    best_season: Optional[str] = Query(None),
    transport: Optional[str] = Query(None),
    accessibility: Optional[str] = Query(None),
):
    cnx = cursor = None
    try:
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM catalog WHERE 1=1"
        params = {}

        if city:
            query += " AND city = %(city)s"
            params["city"] = city.lower().strip()
        if country:
            query += " AND country = %(country)s"
            params["country"] = country.lower().strip()
        if rating_avg is not None:
            query += " AND rating >= %(rating_avg)s"
            params["rating_avg"] = rating_avg
        if vibes:
            vibes_list = [v.strip().lower() for v in vibes.split(",") if v.strip()]
            if vibes_list:
                conditions = " OR ".join([f"vibes LIKE %({i})s" for i in range(len(vibes_list))])
                query += f" AND ({conditions})"
                for i, v in enumerate(vibes_list):
                    params[str(i)] = f"%{v}%"
        if poi:
            query += " AND poi LIKE %(poi)s"
            params["poi"] = f"%{poi.lower().strip()}%"

        cursor.execute(query, params)
        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail="No results")

        return [normalize_catalog_row(row) for row in rows]

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()


# ---------------------------------------------------------------------
# GET SINGLE CATALOG
# ---------------------------------------------------------------------
@app.get("/catalogs/{poi}")
def get_catalog(poi: str):
    cnx = cursor = None
    try:
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("SELECT * FROM catalog WHERE poi = %s", (poi.lower().strip(),))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Catalog not found")

        return normalize_catalog_row(row)

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()


# ---------------------------------------------------------------------
# UPDATE CATALOG
# ---------------------------------------------------------------------
@app.patch("/catalogs/{poi}")
def update_catalog(poi: str, update):
    cnx = cursor = None
    try:
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)

        updates = update.model_dump(exclude_unset=True)

        if not updates:
            raise HTTPException(status_code=400, detail="No fields provided")

        for key, val in updates.items():
            if isinstance(val, str):
                updates[key] = val.lower().strip()

        set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
        values = list(updates.values()) + [poi.lower().strip()]

        query = f"UPDATE catalog SET {set_clause} WHERE poi = %s"
        cursor.execute(query, values)
        cnx.commit()

        cursor.execute("SELECT * FROM catalog WHERE poi = %s", (poi.lower().strip(),))
        row = cursor.fetchone()

        return normalize_catalog_row(row)

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()


# ---------------------------------------------------------------------
# DELETE CATALOG
# ---------------------------------------------------------------------
@app.delete("/catalogs/{poi}", status_code=204)
def delete_catalog(poi: str):
    cnx = cursor = None
    try:
        cnx = get_connection()
        cursor = cnx.cursor()

        cursor.execute("DELETE FROM catalog WHERE poi = %s", (poi.lower().strip(),))
        cnx.commit()

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()


# ---------------------------------------------------------------------
# NEW: JWT-PROTECTED + PUB/SUB TRIGGER ENDPOINT
# ---------------------------------------------------------------------
@app.get("/secure-catalog-ping")
def secure_catalog_ping(authorization: str = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=403, detail="Not authenticated")

    token = authorization.split(" ", 1)[1]

    try:
        decoded = jwt.decode(
            token,
            AUTH_JWT_SECRET,
            algorithms=["HS256"],
            options={"require": ["sub", "email", "exp"]},
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    # ------------------------ NEW: PUBLISH EVENT ------------------------
    event = {
        "event_type": "CATALOG_SECURE_PING",
        "source": "catalog-service",
        "user_email": decoded.get("email"),
        "user_sub": decoded.get("sub"),
        "iss": decoded.get("iss"),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    publisher.publish(PUBSUB_TOPIC, data=json.dumps(event).encode("utf-8"))
    # -------------------------------------------------------------------

    return {"message": "Secure Catalog endpoint OK", "user": decoded}


# ---------------------------------------------------------------------
# ROOT
# ---------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to TripSpark Catalog API"}


# ---------------------------------------------------------------------
# RUN SERVER
# ---------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main3:app", host="0.0.0.0", port=port, reload=True)
