from __future__ import annotations

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal, List

'''class CatalogBase(BaseModel):
    id: int = Field(
        ...,
        description="Catalog ID.",
        json_schema_extra={"example": 1},
    )
    name: str = Field(
        ...,
        description="City.",
        json_schema_extra={"example": "New York City"},
    )
    country: str = Field(
        ...,
        description="Country.",
        json_schema_extra={"example": "USA"},
    )
    currency: Optional[str] = Field(
        None,
        description="Currency.",
        json_schema_extra={"example": "USD"},
    )
    lat: Optional[float] = Field(
        None,
        description="Latitude of the location.",
        json_schema_extra={"example": 40.712776},
    )
    lon: Optional[float] = Field(
        None,
        description="Longitude of the location.",
        json_schema_extra={"example": -74.005974},
    )
    rating_avg: Optional[float] = Field(
        None,
        description="Rating of the location.",
        json_schema_extra={"example": 4.5},
    )
    description: str = Field(
        ...,
        description="Description of the location.",
        json_schema_extra={"example": "Lively location"},
    )
    vibe: str = Field(
        ...,
        description="Vibe of the location.",
        json_schema_extra={"example": "Good"},
    )
    budget: str = Field(
        ...,
        description="Budget of the trip.",
        json_schema_extra={"example": "$200"},
    )
    poi: str = Field(
        ...,
        description="Place of Interest in the city.",
        json_schema_extra={"example": "Times Square"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "New York City",
                    "country":"USA",
                    "currency": "USD",
                    "lat": 40.712776,
                    "lon": -74.005974,
                    "rating_avg": 4.5,
                    "description": "Lively location",
                    "vibe": "Good",
                    "budget": "$200",
                    "poi": "Times Square",
                }
            ]
        }
    }


class CatalogCreate(CatalogBase):
    """Creation payload; ID is generated server-side but present in the base model."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 2,
                    "name": "Seattle",
                    "country":"USA",
                    "currency": "USD",
                    "lat": 37.774929,
                    "lon": -122.419418,
                    "rating_avg": 3.6,
                    "description": "Scenic location",
                    "vibe": "Cool",
                    "budget": "$100",
                    "poi": "Space Needle",
                }
            ]
        }
    }


class CatalogUpdate(BaseModel):
    """Partial update; """
    name: Optional[str] = Field(
        None,
        description="City.",
        json_schema_extra={"example": "New York City"},
    )
    country: Optional[str] = Field(
        None,
        description="Country.",
        json_schema_extra={"example": "USA"},
    )
    currency: Optional[str] = Field(
        None,
        description="Currency.",
        json_schema_extra={"example": "USD"},
    )
    lat: Optional[float] = Field(
        None,
        description="Latitude of the location.",
        json_schema_extra={"example": 51.507351},
    )
    lon: Optional[float] = Field(
        None,
        description="Longitude of the location.",
        json_schema_extra={"example": -0.127758},
    )
    rating_avg: Optional[float] = Field(
        None,
        description="Rating of the location.",
        json_schema_extra={"example": 4.1},
    )
    description: Optional[str] = Field(
        None,
        description="Description of the location.",
        json_schema_extra={"example": "Scenic location"},
    )
    vibe: Optional[str] = Field(
        None,
        description="Vibe of the location.",
        json_schema_extra={"example": "Good"},
    )
    budget: Optional[str] = Field(
        None,
        description="Budget of the trip.",
        json_schema_extra={"example": "$80"},
    )
    poi: Optional[str] = Field(
        None,
        description="Place of Interest in the city.",
        json_schema_extra={"example": "Central Park"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "New York City",
                    "country":"USA",
                    "currency": "USD",
                    "lat": 51.507351,
                    "lon": -0.127758,
                    "rating_avg": 4.1,
                    "description": "Scenic location",
                    "vibe": "Good",
                    "budget": "$80",
                    "poi": "Central Park",
                },
                {"poi": "Empire State Building"},
            ]
        }
    }


class CatalogRead(CatalogBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-10-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-10-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "New York City",
                    "country":"USA",
                    "currency": "USD",
                    "lat": 40.712776,
                    "lon": -74.005974,
                    "rating_avg": 4.5,
                    "description": "Lively location",
                    "vibe": "Good",
                    "budget": "$200",
                    "poi": "Times Square",
                    "created_at": "2025-10-15T10:20:30Z",
                    "updated_at": "2025-10-16T12:00:00Z",
                }
            ]
        }
    }'''

SpendingEnum = Literal["low", "medium", "high"]
SeasonEnum = Literal["spring", "summer", "fall", "winter"]
TransportEnum = Literal["walkable", "public_transit", "rideshare", "car_rental"]


class CatalogBase(BaseModel):

    poi: str = Field(
        ..., 
        description="Place of Interest",
        json_schema_extra={"example": "Times Square"},
    )

    city: str = Field(
        ...,
        description="City name",
        json_schema_extra={"example": "New York City"},
    )

    country: str = Field(
        ...,
        description="Country",
        json_schema_extra={"example": "USA"},
    )

    currency: str = Field(
        ...,
        description="Currency",
        json_schema_extra={"example": "USD"},
    )

    latitude: float = Field(
        ...,
        description="Latitude of the location",
        json_schema_extra={"example": 40.7580},
    )

    longitude: float = Field(
        ...,
        description="Longitude of the location",
        json_schema_extra={"example": -73.9855},
    )

    rating: float = Field(
        ...,
        description="Average rating",
        json_schema_extra={"example": 4.6},
    )

    description: str = Field(
        ...,
        description="Description of the place",
        json_schema_extra={"example": "Famous commercial intersection in Manhattan"},
    )

    spending: SpendingEnum = Field(
        ...,
        description="Expense level",
        json_schema_extra={"example": "high"},
    )

    budget: int = Field(
        ...,
        description="Estimated budget",
        json_schema_extra={"example": 200},
    )

    vibes: str = Field(
        ...,
        description="Comma-separated set of vibes",
        json_schema_extra={"example": "Urban,Modern,Nightlife"},
    )

    activities: str = Field(
        ...,
        description="Comma-separated set of activities",
        json_schema_extra={"example": "Photography,Shopping,Walking Tours"},
    )

    food: str = Field(
        ...,
        description="Comma-separated set of food types",
        json_schema_extra={"example": "Street Food,Coffee,Local Cuisine"},
    )

    best_season: SeasonEnum = Field(
        ...,
        description="Best season to visit",
        json_schema_extra={"example": "summer"},
    )

    trip_days: int = Field(
        ...,
        description="Suggested number of days",
        json_schema_extra={"example": 2},
    )

    nearest_airport: str = Field(
        ...,
        description="Nearest airport",
        json_schema_extra={"example": "JFK"},
    )

    transport: TransportEnum = Field(
        ...,
        description="Main mode of transport",
        json_schema_extra={"example": "walkable"},
    )

    accessibility: str = Field(
        ...,
        description="Accessibility information",
        json_schema_extra={"example": "Crowded area with lots of walking"},
    )

    direction: str = Field(
        ...,
        description="Google Maps or direct link",
        json_schema_extra={"example": "https://maps.google.com/timessquare"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "poi": "Times Square",
                    "city": "New York City",
                    "country": "USA",
                    "currency": "USD",
                    "latitude": 40.7580,
                    "longitude": -73.9855,
                    "rating": 4.6,
                    "description": "Famous commercial district",
                    "spending": "high",
                    "budget": 200,
                    "vibes": "Urban,Modern,Nightlife",
                    "activities": "Photography,Shopping,Walking Tours",
                    "food": "Street Food,Coffee",
                    "best_season": "summer",
                    "trip_days": 2,
                    "nearest_airport": "JFK",
                    "transport": "walkable",
                    "accessibility": "Crowded but manageable",
                    "direction": "https://maps.google.com/timessquare"
                }
            ]
        }
    }

'''class CatalogBase(BaseModel):
    id: int = Field(
        ...,
        description="Catalog ID.",
        json_schema_extra={"example": 1},
    )
    name: str = Field(
        ...,
        description="City.",
        json_schema_extra={"example": "New York City"},
    )
    country: str = Field(
        ...,
        description="Country.",
        json_schema_extra={"example": "USA"},
    )
    currency: Optional[str] = Field(
        None,
        description="Currency.",
        json_schema_extra={"example": "USD"},
    )
    lat: Optional[float] = Field(
        None,
        description="Latitude of the location.",
        json_schema_extra={"example": 40.712776},
    )
    lon: Optional[float] = Field(
        None,
        description="Longitude of the location.",
        json_schema_extra={"example": -74.005974},
    )
    rating_avg: Optional[float] = Field(
        None,
        description="Rating of the location.",
        json_schema_extra={"example": 4.5},
    )
    description: str = Field(
        ...,
        description="Description of the location.",
        json_schema_extra={"example": "Lively location"},
    )
    vibe: str = Field(
        ...,
        description="Vibe of the location.",
        json_schema_extra={"example": "Good"},
    )
    budget: str = Field(
        ...,
        description="Budget of the trip.",
        json_schema_extra={"example": "$200"},
    )
    poi: str = Field(
        ...,
        description="Place of Interest in the city.",
        json_schema_extra={"example": "Times Square"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "New York City",
                    "country":"USA",
                    "currency": "USD",
                    "lat": 40.712776,
                    "lon": -74.005974,
                    "rating_avg": 4.5,
                    "description": "Lively location",
                    "vibe": "Good",
                    "budget": "$200",
                    "poi": "Times Square",
                }
            ]
        }
    }
'''

class CatalogCreate(CatalogBase):
    """Creation payload; ID is generated server-side but present in the base model."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "poi": "Central Park",
                    "city": "New York City",
                    "country": "USA",
                    "currency": "USD",
                    "latitude": 40.7851,
                    "longitude": -73.9683,
                    "rating": 4.8,
                    "description": "Large urban park offering scenic landscapes and recreational spaces",
                    "spending": "medium",
                    "budget": 100,
                    "vibes": "Nature,Relaxing,Scenic",
                    "activities": "Jogging,Picnicking,Boating,Photography",
                    "food": "Snacks,Ice Cream,Food Carts",
                    "best_season": "spring",
                    "trip_days": 1,
                    "nearest_airport": "JFK",
                    "transport": "walkable",
                    "accessibility": "Wheelchair friendly paths available",
                    "direction": "https://maps.google.com/centralpark"
                }

            ]
        }
    }


'''class CatalogUpdate(BaseModel):
    """Partial update; """
    name: Optional[str] = Field(
        None,
        description="City.",
        json_schema_extra={"example": "New York City"},
    )
    country: Optional[str] = Field(
        None,
        description="Country.",
        json_schema_extra={"example": "USA"},
    )
    currency: Optional[str] = Field(
        None,
        description="Currency.",
        json_schema_extra={"example": "USD"},
    )
    lat: Optional[float] = Field(
        None,
        description="Latitude of the location.",
        json_schema_extra={"example": 51.507351},
    )
    lon: Optional[float] = Field(
        None,
        description="Longitude of the location.",
        json_schema_extra={"example": -0.127758},
    )
    rating_avg: Optional[float] = Field(
        None,
        description="Rating of the location.",
        json_schema_extra={"example": 4.1},
    )
    description: Optional[str] = Field(
        None,
        description="Description of the location.",
        json_schema_extra={"example": "Scenic location"},
    )
    vibe: Optional[str] = Field(
        None,
        description="Vibe of the location.",
        json_schema_extra={"example": "Good"},
    )
    budget: Optional[str] = Field(
        None,
        description="Budget of the trip.",
        json_schema_extra={"example": "$80"},
    )
    poi: Optional[str] = Field(
        None,
        description="Place of Interest in the city.",
        json_schema_extra={"example": "Central Park"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "New York City",
                    "country":"USA",
                    "currency": "USD",
                    "lat": 51.507351,
                    "lon": -0.127758,
                    "rating_avg": 4.1,
                    "description": "Scenic location",
                    "vibe": "Good",
                    "budget": "$80",
                    "poi": "Central Park",
                },
                {"poi": "Empire State Building"},
            ]
        }
    }'''

class CatalogUpdate(BaseModel):
    """Partial update model for catalog table"""


    city: Optional[str] = Field(
        None,
        description="City name.",
        json_schema_extra={"example": "New York City"},
    )

    country: Optional[str] = Field(
        None,
        description="Country.",
        json_schema_extra={"example": "USA"},
    )

    currency: Optional[str] = Field(
        None,
        description="Currency used.",
        json_schema_extra={"example": "USD"},
    )

    latitude: Optional[float] = Field(
        None,
        description="Latitude of the location.",
        json_schema_extra={"example": 40.785091},
    )

    longitude: Optional[float] = Field(
        None,
        description="Longitude of the location.",
        json_schema_extra={"example": -73.968285},
    )

    rating: Optional[float] = Field(
        None,
        description="User rating.",
        json_schema_extra={"example": 4.8},
    )

    description: Optional[str] = Field(
        None,
        description="Description of the location.",
        json_schema_extra={"example": "Large urban park offering scenic landscapes"},
    )

    spending: Optional[str] = Field(
        None,
        description="Spending level.",
        json_schema_extra={"example": "medium"},
    )

    budget: Optional[int] = Field(
        None,
        description="Estimated daily budget.",
        json_schema_extra={"example": 120},
    )

    vibes: Optional[str] = Field(
        None,
        description="Comma-separated vibes.",
        json_schema_extra={"example": "Relaxed,Nature,Urban"},
    )

    activities: Optional[str] = Field(
        None,
        description="Comma-separated activities.",
        json_schema_extra={"example": "Walking Tours,Photography,Parks"},
    )

    food: Optional[str] = Field(
        None,
        description="Comma-separated food types.",
        json_schema_extra={"example": "Street Food,Coffee"},
    )

    best_season: Optional[str] = Field(
        None,
        description="Best season to visit.",
        json_schema_extra={"example": "spring"},
    )

    trip_days: Optional[int] = Field(
        None,
        description="Recommended number of days.",
        json_schema_extra={"example": 1},
    )

    nearest_airport: Optional[str] = Field(
        None,
        description="Nearest major airport.",
        json_schema_extra={"example": "JFK"},
    )

    transport: Optional[str] = Field(
        None,
        description="Best transport option.",
        json_schema_extra={"example": "walkable"},
    )

    accessibility: Optional[str] = Field(
        None,
        description="Accessibility notes.",
        json_schema_extra={"example": "Wheelchair accessible paths available"},
    )

    direction: Optional[str] = Field(
        None,
        description="Google Maps or direction link.",
        json_schema_extra={"example": "https://maps.google.com/?q=Central+Park"},
    )


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "description": "Large urban park offering scenic landscapes and recreational spaces",
                    "vibe": "Nature,Relaxing,Scenic",
                    "budget": "110"
                },
                {
                    "budget": "120"
                },
            ]
        }
    }


class CatalogRead(CatalogBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-10-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-10-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "poi": "Times Square",
                    "city": "New York City",
                    "country": "USA",
                    "currency": "USD",
                    "latitude": 40.7580,
                    "longitude": -73.9855,
                    "rating": 4.6,
                    "description": "Famous commercial district",
                    "spending": "high",
                    "budget": 200,
                    "vibes": "Urban,Modern,Nightlife",
                    "activities": "Photography,Shopping,Walking Tours",
                    "food": "Street Food,Coffee",
                    "best_season": "summer",
                    "trip_days": 2,
                    "nearest_airport": "JFK",
                    "transport": "walkable",
                    "accessibility": "Crowded but manageable",
                    "direction": "https://maps.google.com/timessquare",
                    "created_at": "2025-10-15T10:20:30Z",
                    "updated_at": "2025-10-16T12:00:00Z",
                }
            ]
        }
    }
