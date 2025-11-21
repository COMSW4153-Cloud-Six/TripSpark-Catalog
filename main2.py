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
    'host': '10.142.0.4',  #'10.142.0.4',# to connect between VMs in same project use internal IP of catalog-mysql to test from local pycharm use external IP 'host': '34.139.223.61',
    'user': 'felicia',
    'password': '1234',
    'database': 'TripSparkCatalog'
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


app = FastAPI(
    title="TripSpark - Catalog API",
    description="FastAPI app using Pydantic v2 models for TripSpark - Catalog deployed in GCP VM",
    version="0.1.0",
)

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
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



# -----------------------------------------------------------------------------
# Catalog endpoints
# -----------------------------------------------------------------------------


@app.post("/catalogs", response_model=CatalogRead, status_code=201)
def create_catalog(catalog: CatalogCreate):

    cnx = None
    cursor = None
    try:
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)

        # Prepare insert query
        insert_query = """
            INSERT INTO catalog (poi, city, country, currency, latitude, longitude, rating, description, spending, budget, vibes, activities, food, best_season,trip_days, nearest_airport, transport, accessibility, direction) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        values = (
            catalog.poi.lower().strip(), catalog.city.lower().strip(), catalog.country.lower().strip(), catalog.currency.lower().strip(), catalog.latitude, catalog.longitude, catalog.rating,
            catalog.description.lower().strip(), catalog.spending.lower().strip(), catalog.budget, catalog.vibes.lower().strip(), catalog.activities.lower().strip(), catalog.food.lower().strip(),
            catalog.best_season.lower().strip(), catalog.trip_days, catalog.nearest_airport.lower().strip(), catalog.transport.lower().strip(),
            catalog.accessibility.lower().strip(), catalog.direction
        )

        cursor.execute(insert_query, values)
        cnx.commit()

        cursor.execute("SELECT * FROM catalog WHERE poi = %s", (catalog.poi.lower().strip(),))
        row = cursor.fetchone()

        return CatalogRead(**row)

    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")
        if err.errno == 1062:  # Duplicate primary key
            raise HTTPException(status_code=400, detail=f"The location {catalog.poi} already exists")
        raise HTTPException(status_code=500, detail=f"MySQL error: {err}")

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()


@app.get("/catalogs", response_model=List[CatalogRead])
def list_catalogs(
    city: Optional[str] = Query(None, description="Filter by city"),
    country: Optional[str] = Query(None, description="Filter by country"),
    rating_avg: Optional[float] = Query(None, description="Filter by minimum rating (0.0)"),
    vibes: Optional[str] = Query(None, description="Filter by vibe ('relaxed', 'adventure', 'cultural', 'nightlife','nature', 'urban', 'historic', 'modern')"),
    budget: Optional[str] = Query(None, description="Filter by maximum budget"),
    poi: Optional[str] = Query(None, description="Filter by place of interest"),
    activities: Optional[str] = Query(None, description="Filter by interested activities ('museums', 'shopping', 'parks', 'architecture', 'live music', 'sports', 'photography', 'walking tours')"),
    food: Optional[str] = Query(None, description="Filter by food preferences (coffee', 'fine dining', 'street food', 'vegetarian', 'seafood', 'local cuisine', 'bakeries', 'brunch')"),
    best_season: Optional[str] = Query(None, description="Filter by season"),
    transport: Optional[str] = Query(None, description="Filter by mode of commute ('walkable', 'public_transit', 'rideshare', 'car_rental')"),
    accessibility: Optional[str] = Query(None, description="Filter by accessibility"),
):

    cnx = None
    cursor = None
    try:
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)

        # Start building query
        query = "SELECT * FROM catalog WHERE 1=1"
        params = {}

        # Add filters dynamically
        if city:
            query += " AND city = %(city)s"
            params["city"] = city
        if country:
            query += " AND country = %(country)s"
            params["country"] = country
        if best_season:
            query += " AND best_season = %(best_season)s"
            params["best_season"] = best_season
        if transport:
            query += " AND transport = %(transport)s"
            params["transport"] = transport
        if rating_avg:
            query += " AND rating >= %(rating_avg)s"
            params["rating"] = rating_avg
        if activities:
            query += " AND activities LIKE %(activities)s"
            params["activities"] = f"%{activities}%"
        if accessibility:
            query += " AND accessibility LIKE %(accessibility)s"
            params["accessibility"] = f"%{accessibility}%"
        if food:
            query += " AND food LIKE %(food)s"
            params["food"] = f"%{food}%"
        if vibes:
            query += " AND vibes LIKE %(vibes)s"
            params["vibes"] = f"%{vibes}%"
        if budget:
            query += " AND budget <= %(budget)s"
            params["budget"] = budget
        if poi:
            query += " AND poi LIKE %(poi)s"
            params["poi"] = f"%{poi}%"

        cursor.execute(query, params)
        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail="No matching catalogs found")

        # Convert MySQL rows → Pydantic models
        return [CatalogRead(**row) for row in rows]

    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")
        raise HTTPException(status_code=500, detail=f"MySQL error: {err}")

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()


@app.get("/catalogs/{poi}", response_model=CatalogRead)
def get_catalog(poi: str):
    """
    Fetch a single catalog record from MySQL by ID.
    """
    print(poi)
    cnx = None
    cursor = None
    try:
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM catalog WHERE poi = %s"
        cursor.execute(query, (poi.lower(),))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail=f"Catalog with location {poi} not found")

        return CatalogRead(**row)

    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")
        raise HTTPException(status_code=500, detail=f"MySQL error: {err}")

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()



'''@app.patch("/catalogs/{catalog_id}", response_model=CatalogRead)
def update_catalog(catalog_id: int, update: CatalogUpdate):
    """
    Update a catalog record in MySQL by ID.
    """
    cnx = None
    cursor = None
    try:
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)

        updates = update.model_dump(exclude_unset=True)
        if not updates:
            raise HTTPException(status_code=400, detail="No fields provided for update")

        set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
        values = list(updates.values()) + [catalog_id]

        query = f"UPDATE catalog SET {set_clause} WHERE id = %s"
        cursor.execute(query, values)
        cnx.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Catalog with ID {catalog_id} not found")

        cursor.execute("SELECT * FROM catalog WHERE id = %s", (catalog_id,))
        row = cursor.fetchone()

        return CatalogRead(**row)

    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")
        raise HTTPException(status_code=500, detail=f"MySQL error: {err}")

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()
'''

@app.patch("/catalogs/{poi}", response_model=CatalogRead)
def update_catalog(poi: str, update: CatalogUpdate):
    cnx = None
    cursor = None
    try:
        cnx = get_connection()
        cursor = cnx.cursor(dictionary=True)

        updates = update.model_dump(exclude_unset=True)
        if not updates:
            raise HTTPException(status_code=400, detail="No fields provided for update")

        set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
        values = list(updates.values()) + [poi]

        query = f"UPDATE catalog SET {set_clause} WHERE poi = %s"
        cursor.execute(query, values)
        cnx.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Catalog with location {poi} not found")

        # Fetch updated row
        cursor.execute("SELECT * FROM catalog WHERE poi = %s", (poi,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"Catalog with location {poi} not found")

        return CatalogRead(**row)

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"MySQL error: {err}")

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()



@app.delete("/catalogs/{poi}", status_code=204)
def delete_catalog(poi: str):

    cnx = None
    cursor = None
    try:
        cnx = get_connection()
        cursor = cnx.cursor()

        query = "DELETE FROM catalog WHERE poi = %s"
        cursor.execute(query, (poi.lower(),))
        cnx.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Catalog with location {poi} not found")

        return

    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")
        raise HTTPException(status_code=500, detail=f"MySQL error: {err}")

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()


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

    uvicorn.run("main2:app", host="0.0.0.0", port=port, reload=True)
