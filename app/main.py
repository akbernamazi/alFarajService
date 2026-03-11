from __future__ import annotations

from dataclasses import asdict
from datetime import date
from typing import Literal, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.data import (
    EVENTS,
    INVITATIONS,
    PRAYER_PLACES,
    EventInvitation,
    EventRecord,
    by_visibility,
    event_by_id,
    get_private_events_for_user,
    get_prayer_times_for_date,
)

app = FastAPI(title="Aza Python", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "https://akbernamazi.github.io",
    ],
    allow_origin_regex=r"^https://[a-zA-Z0-9-]+\.github\.io$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateEventPayload(BaseModel):
    title: str
    description: str
    start_time: str
    end_time: str
    latitude: float = 0
    longitude: float = 0
    visibility: Literal["public", "private"] = "public"
    created_by: str = "system"


class InvitePayload(BaseModel):
    user_id: str
    invited_by: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "aza-python"}


@app.get("/api/v1/health")
def health_v1() -> dict:
    return health()


@app.get("/api/v1/events/public")
def get_public_events() -> list[dict]:
    return by_visibility("public")


@app.get("/api/v1/events/private")
def get_private_events(userId: str = Query(..., min_length=1)) -> list[dict]:
    return get_private_events_for_user(userId.strip())


@app.get("/api/v1/events/{event_id}")
def get_event(event_id: str) -> dict:
    event = event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    return asdict(event)


@app.post("/api/v1/events", status_code=201)
def create_event(payload: CreateEventPayload) -> dict:
    created = EventRecord(
        event_id=f"e{len(EVENTS) + 1}",
        title=payload.title,
        description=payload.description,
        latitude=payload.latitude,
        longitude=payload.longitude,
        start_time=payload.start_time,
        end_time=payload.end_time,
        visibility=payload.visibility,
        created_by=payload.created_by,
    )
    EVENTS.append(created)
    return asdict(created)


@app.post("/api/v1/events/{event_id}/invite", status_code=201)
def invite_user(event_id: str, payload: InvitePayload) -> dict:
    event = event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")

    invite = EventInvitation(
        invitation_id=f"i{len(INVITATIONS) + 1}",
        event_id=event.event_id,
        user_id=payload.user_id,
        invited_by=payload.invited_by,
        status="pending",
    )
    INVITATIONS.append(invite)
    return asdict(invite)


@app.get("/api/v1/prayer-places")
def get_prayer_places() -> list[dict]:
    return [asdict(place) for place in PRAYER_PLACES]


@app.get("/api/v1/prayer-times")
def get_prayer_times(
    date_value: str = Query(default_factory=lambda: date.today().isoformat(), alias="date"),
    lat: Optional[float] = Query(default=None),
    lng: Optional[float] = Query(default=None),
) -> dict:
    day = date.fromisoformat(date_value)
    return {
        "date": day.isoformat(),
        "location": {"lat": lat, "lng": lng},
        "times": get_prayer_times_for_date(day, lat, lng),
    }
