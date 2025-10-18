from __future__ import annotations

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class CatalogBase(BaseModel):
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
    }