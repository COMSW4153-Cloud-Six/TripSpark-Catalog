from __future__ import annotations

import os
import socket
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, Path, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import mysql.connector
import jwt

from models.catalog import CatalogCreate, CatalogRead, CatalogUpdate
from models.health import Health

# ---------------------------------------------------------------------------
# MySQL Connectivity
# ---------------------------------------------------------------------------
DB_CONFIG = {
    "host": "10.142.0.4",
    "user": "felicia",
    "password": "1234",
    "database": "TripSparkCatalog",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ---------------------------------------------------------------------------
# App Config
# ---------------------------------------------------------------------------
port = int(os.environ.get("FASTAPIPORT", 8000))

app = FastAPI(
    title="TripSpark - Catalog API (main3)",
    description="FastAPI app using Pydantic v2 models for TripSpark - Catalog deployed in GCP VM (with JWT demo).",
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# JWT Auth (for Requirement 2)
# ---------------------------------------------------------------------------
AUTH_JWT_SECRET = os.environ.get("AUTH_JWT_SECRET", "dev-secret-change-me")
token_auth = HTTPBearer()


def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(token_auth)):
    """
    Read Authorization: Bearer <token> and verify our TripSpark JWT.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, AUTH_JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or malformed token",
        )


@app.get("/secure-catalog-ping")
def secure_catalog_ping(user=Depends(verify_jwt)):
    """
    Simple secure endpoint to demonstrate JWT validation.
    Returns 200 only if a valid TripSpark JWT is provided.
    """
    return {
        "message": "Secure Catalog endpoint OK",
        "user": user,
    }


# ---------------------------------------------------------------------------
# Health Endpoint
# ---------------------------------------------------------------------------
def make_health(echo: Optional[str], path_echo: Optional[str] = None) -> Health:
    try:
        ip_catalog = socket.gethostbyname(socket.gethostname())
    except Exception:
        ip_catalog = "127.0.0.1"

    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=ip_catalog,
        echo=echo,
        path_echo=path_echo,
    )


@app.get("/health", response_model=Health)
def get_health_no_path(echo: Optional[str] = Query(None)):
    return make_health(echo=echo)


@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(path_echo: str = Path(...), echo: Optional[str] = Query(None)):
    return make_health(echo=echo, path_echo=path_echo)


# ---------------------------------------------------------------------------
# Utility: normalize DB rows for CatalogRead
# ---------------------------------------------------------------------------
def normalize_catalog_row(row: dict) -> dict:
    """Convert sets/lists in DB row to comma-separated strings for Pydantic."""
    for field in ["vibes", "activities", "food"]:
        if field in row and isinstance(row[field], (set, list)):
            row[field] = ", ".join(sorted(row[field]))
    return row


# ---------------------------------------------------------------------------
# Create Catalog
# ---------------------------------------------------------------------------
@app.post("/catalogs", response_model=CatalogRead, status_code=201)
def create_catalog(catalog: CatalogCreate):
    cnx = cursor = None
    try:
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)

        insert_query = """
        INSERT INTO catalog 
        (
            poi, city, country, currency, latitude, longitude, rating,
            description, spending, budget, vibes, activities, food,
            best_season, trip_days, nearest_airport, transport,
            accessibility, direction
        )
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

        cursor.execute(
            "SELECT * FROM catalog WHERE poi = %s",
            (catalog.poi.lower().strip(),),
        )
        row = cursor.fetchone()
        row = normalize_catalog_row(row)
        return CatalogRead(**row)

    except mysql.connector.Error as err:
        if err.errno == 1062:
            raise HTTPException(
                status_code=400,
                detail=f"The location {catalog.poi} already exists",
            )
        raise HTTPException(status_code=500, detail=f"MySQL error: {err}")

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()


# ---------------------------------------------------------------------------
# List / Filter Catalogs
# ---------------------------------------------------------------------------
@app.get("/catalogs", response_model=List[CatalogRead])
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
        if best_season:
            query += " AND best_season = %(best_season)s"
            params["best_season"] = best_season.lower().strip()
        if transport:
            query += " AND transport = %(transport)s"
            params["transport"] = transport.lower().strip()
        if rating_avg is not None:
            query += " AND rating >= %(rating_avg)s"
            params["rating_avg"] = rating_avg
        if activities:
            query += " AND activities LIKE %(activities)s"
            params["activities"] = f"%{activities.lower().strip()}%"
        if accessibility:
            query += " AND accessibility LIKE %(accessibility)s"
            params["accessibility"] = f"%{accessibility.lower().strip()}%"
        if vibes:
            vibes_list = [v.strip().lower() for v in vibes.split(",") if v.strip()]
            if vibes_list:
                vibes_conditions = " OR ".join(
                    [f"vibes LIKE %({i})s" for i in range(len(vibes_list))]
                )
                query += f" AND ({vibes_conditions})"
                for i, v in enumerate(vibes_list):
                    params[str(i)] = f"%{v}%"
        if food:
            food_list = [f.strip().lower() for f in food.split(",") if f.strip()]
            if food_list:
                food_conditions = " OR ".join(
                    [f"food LIKE %({100+i})s" for i in range(len(food_list))]
                )
                query += f" AND ({food_conditions})"
                for i, f_val in enumerate(food_list):
                    params[str(100 + i)] = f"%{f_val}%"
        if budget is not None:
            query += " AND budget <= %(budget)s"
            params["budget"] = budget
        if poi:
            query += " AND poi LIKE %(poi)s"
            params["poi"] = f"%{poi.lower().strip()}%"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail="No matching catalogs found")

        return [CatalogRead(**normalize_catalog_row(row)) for row in rows]

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()


# ---------------------------------------------------------------------------
# Get Single Catalog
# ---------------------------------------------------------------------------
@app.get("/catalogs/{poi}", response_model=CatalogRead)
def get_catalog(poi: str):
    cnx = cursor = None
    try:
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM catalog WHERE poi = %s",
            (poi.lower().strip(),),
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=404,
                detail=f"Catalog with location {poi} not found",
            )

        return CatalogRead(**normalize_catalog_row(row))

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()


# ---------------------------------------------------------------------------
# Update Catalog
# ---------------------------------------------------------------------------
@app.patch("/catalogs/{poi}", response_model=CatalogRead)
def update_catalog(poi: str, update: CatalogUpdate):
    cnx = cursor = None
    try:
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)

        updates = update.model_dump(exclude_unset=True)
        if not updates:
            raise HTTPException(
                status_code=400, detail="No fields provided for update"
            )

        for key, value in updates.items():
            if isinstance(value, str):
                updates[key] = value.lower().strip()

        set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
        values = list(updates.values()) + [poi.lower().strip()]

        query = f"UPDATE catalog SET {set_clause} WHERE poi = %s"
        cursor.execute(query, values)
        cnx.commit()
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, detail=f"Catalog with location {poi} not found"
            )

        cursor.execute(
            "SELECT * FROM catalog WHERE poi = %s",
            (poi.lower().strip(),),
        )
        row = cursor.fetchone()
        return CatalogRead(**normalize_catalog_row(row))

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()


# ---------------------------------------------------------------------------
# Delete Catalog
# ---------------------------------------------------------------------------
@app.delete("/catalogs/{poi}", status_code=204)
def delete_catalog(poi: str):
    cnx = cursor = None
    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        cursor.execute(
            "DELETE FROM catalog WHERE poi = %s",
            (poi.lower().strip(),),
        )
        cnx.commit()
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, detail=f"Catalog with location {poi} not found"
            )
    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "Welcome to the TripSpark - Catalog API (main3). See /docs for OpenAPI UI."
    }


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main3:app", host="0.0.0.0", port=port, reload=True)
