from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.catalog import CatalogCreate, CatalogRead, CatalogUpdate
from models.health import Health


# -----------------------------------------------------------------------------
# MySQL connectivity to display the data in catalog table
# -----------------------------------------------------------------------------

import mysql.connector

DB_CONFIG = {
    'host': 'your_ec2_instance_public_ip',  # or private IP if in same VPC
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database_name'
}

def get_connection():
    """Establish and return a new database connection."""
    return mysql.connector.connect(**DB_CONFIG)

def fetch_places():
    cnx = None
    cursor = None
    try:
        cnx = get_connection()
        cursor = cnx.cursor()

        select_query = "SELECT * FROM catalog"
        cursor.execute(select_query)
        results = cursor.fetchall()

        print("\nLocations in the catalog:")
        for row in results:
            print(row)

    except Exception as err:
        print("Not connected to server!")
        print(f"Error: {err}")

    finally:
        if cursor:
            try:
                cursor.close()
            except Exception:
                pass

        if cnx and cnx.is_connected():
            try:
                cnx.close()
                print("MySQL connection closed.")
            except Exception:
                pass




port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
catalogs: Dict[int, CatalogRead] = {}

app = FastAPI(
    title="TripSpark - Catalog API",
    description="FastAPI app using Pydantic v2 models for TripSpark - Catalog",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Catalog endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_catalog=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

@app.post("/catalogs", response_model=CatalogRead, status_code=201)
def create_catalog(catalog: CatalogCreate):
    if catalog.id in catalogs:
        raise HTTPException(status_code=400, detail="Catalog with this ID already exists")
    catalogs[catalog.id] = CatalogRead(**catalog.model_dump())
    return catalogs[catalog.id]

@app.get("/catalogs", response_model=List[CatalogRead])
def list_catalogs(
    name: Optional[str] = Query(None, description="Filter by city"),
    country: Optional[str] = Query(None, description="Filter by country"),
    currency: Optional[str] = Query(None, description="Filter by currency"),
    lat: Optional[float] = Query(None, description="Filter by latitude"),
    lon: Optional[float] = Query(None, description="Filter by longitude"),
    rating_avg: Optional[int] = Query(None, description="Filter by rating"),
    description: Optional[str] = Query(None, description="Filter by description"),
    vibe: Optional[str] = Query(None, description="Filter by vibe"),
    budget: Optional[str] = Query(None, description="Filter by budget"),
    poi: Optional[str] = Query(None, description="Filter by place of interest"),
):
    results = list(catalogs.values())

    if name is not None:
        results = [a for a in results if a.name == name]
    if currency is not None:
        results = [a for a in results if a.currency == currency]
    if lat is not None:
        results = [a for a in results if a.lat == lat]
    if lon is not None:
        results = [a for a in results if a.lon == lon]
    if country is not None:
        results = [a for a in results if a.country == country]
    if rating_avg is not None:
        results = [a for a in results if a.rating_avg == rating_avg]
    if description is not None:
        results = [a for a in results if a.description == description]
    if vibe is not None:
        results = [a for a in results if a.vibe == vibe]
    if budget is not None:
        results = [a for a in results if a.budget == budget]
    if poi is not None:
        results = [a for a in results if a.poi == poi]

    ## select query in mysql to display all data from database
    fetch_places()

    return results

@app.get("/catalogs/{catalog_id}", response_model=CatalogRead)
def get_catalog(catalog_id: int):
    if catalog_id not in catalogs:
        raise HTTPException(status_code=404, detail="Catalog not found")
    return catalogs[catalog_id]

@app.patch("/catalogs/{catalog_id}", response_model=CatalogRead)
def update_catalog(catalog_id: int, update: CatalogUpdate):
    if catalog_id not in catalogs:
        raise HTTPException(status_code=404, detail="Catalog not found")
    stored = catalogs[catalog_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    catalogs[catalog_id] = CatalogRead(**stored)
    return catalogs[catalog_id]

@app.delete("/catalogs/{catalog_id}", status_code=204)
def delete_catalog(catalog_id: int):
    if catalog_id not in catalogs:
        raise HTTPException(status_code=404, detail="Catalog not found")
    del catalogs[catalog_id]
    return


# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the TripSpark - Catalog API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)