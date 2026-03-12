from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date, datetime, timedelta
from typing import Literal, Optional

Visibility = Literal["public", "private"]


@dataclass
class EventRecord:
    event_id: str
    title: str
    description: str
    latitude: float
    longitude: float
    start_time: str
    end_time: str
    visibility: Visibility
    created_by: str


@dataclass
class EventInvitation:
    invitation_id: str
    event_id: str
    user_id: str
    invited_by: str
    status: str


@dataclass
class PrayerPlace:
    place_id: str
    name: str
    address: str
    latitude: float
    longitude: float
    has_wudu: bool
    has_women_area: bool
    has_parking: bool
    jumuah_time: Optional[str]


TODAY = datetime.now().replace(minute=0, second=0, microsecond=0)

EVENTS: list[EventRecord] = [
    EventRecord(
        event_id="e1",
        title="Community Iftar Meetup",
        description="Neighborhood iftar with short reminders and open networking.",
        latitude=17.3616,
        longitude=78.4747,
        start_time=(TODAY + timedelta(days=1, hours=1)).isoformat(),
        end_time=(TODAY + timedelta(days=1, hours=3)).isoformat(),
        visibility="public",
        created_by="u1",
    ),
    EventRecord(
        event_id="e2",
        title="Quran Study Circle",
        description="Small private halaqah focused on Surah Al-Mulk reflection.",
        latitude=17.4039,
        longitude=78.4256,
        start_time=(TODAY + timedelta(days=2, hours=2)).isoformat(),
        end_time=(TODAY + timedelta(days=2, hours=4)).isoformat(),
        visibility="private",
        created_by="u2",
    ),
    EventRecord(
        event_id="e3",
        title="Youth Volunteer Drive",
        description="Public volunteer coordination for weekend food distribution.",
        latitude=17.4401,
        longitude=78.3489,
        start_time=(TODAY + timedelta(days=3, hours=2)).isoformat(),
        end_time=(TODAY + timedelta(days=3, hours=5)).isoformat(),
        visibility="public",
        created_by="u3",
    ),
]

INVITATIONS: list[EventInvitation] = [
    EventInvitation(
        invitation_id="i1",
        event_id="e2",
        user_id="u1",
        invited_by="u2",
        status="pending",
    )
]

PRAYER_PLACES: list[PrayerPlace] = [
    PrayerPlace(
        place_id="p1",
        name="Badshahi Ashurkhana",
        address="Pathergatti Rd, Ghansi Bazaar, Charminar, Hyderabad, Telangana",
        latitude=17.3674,
        longitude=78.4763,
        has_wudu=True,
        has_women_area=True,
        has_parking=False,
        jumuah_time="13:15",
    ),
    PrayerPlace(
        place_id="p2",
        name="Bibi Ka Alawa (Dabeerpura)",
        address="Dabeerpura South, Hyderabad, Telangana",
        latitude=17.3732,
        longitude=78.5015,
        has_wudu=True,
        has_women_area=True,
        has_parking=False,
        jumuah_time="13:20",
    ),
    PrayerPlace(
        place_id="p3",
        name="Masjid-e-Jafaria, Tolichowki",
        address="Tolichowki, Hyderabad, Telangana",
        latitude=17.4062,
        longitude=78.4048,
        has_wudu=True,
        has_women_area=True,
        has_parking=True,
        jumuah_time="13:10",
    ),
    PrayerPlace(
        place_id="p4",
        name="Imambargah Panjeshah",
        address="Hussaini Alam, Hyderabad, Telangana",
        latitude=17.3705,
        longitude=78.4688,
        has_wudu=True,
        has_women_area=True,
        has_parking=False,
        jumuah_time="13:25",
    ),
    PrayerPlace(
        place_id="p5",
        name="Idgah-e-Zehra, Pahadi Shareef",
        address="Pahadi Shareef, Hyderabad, Telangana",
        latitude=17.3289,
        longitude=78.5209,
        has_wudu=True,
        has_women_area=True,
        has_parking=True,
        jumuah_time="13:00",
    ),
    PrayerPlace(
        place_id="p6",
        name="Imambargah Azakhana-e-Zahra",
        address="Yakhutpura, Hyderabad, Telangana",
        latitude=17.3658,
        longitude=78.4955,
        has_wudu=True,
        has_women_area=True,
        has_parking=False,
        jumuah_time="13:20",
    ),
]


def by_visibility(visibility: Visibility) -> list[dict]:
    return [asdict(event) for event in EVENTS if event.visibility == visibility]


def event_by_id(event_id: str) -> Optional[EventRecord]:
    return next((event for event in EVENTS if event.event_id == event_id), None)


def get_private_events_for_user(user_id: str) -> list[dict]:
    invited_event_ids = {
        invitation.event_id for invitation in INVITATIONS if invitation.user_id == user_id
    }
    return [
        asdict(event)
        for event in EVENTS
        if event.visibility == "private" and event.event_id in invited_event_ids
    ]


def get_prayer_times_for_date(day: date, lat: Optional[float] = None, lng: Optional[float] = None) -> dict[str, str]:
    base_offset = 0
    if lat is not None and lng is not None:
        base_offset = int((abs(lat) + abs(lng)) % 12)

    return {
        "fajr": f"05:{10 + (base_offset % 10):02d}",
        "dhuhr": f"12:{18 + (base_offset % 10):02d}",
        "asr": f"15:{44 + (base_offset % 10):02d}",
        "maghrib": f"18:{30 + (base_offset % 10):02d}",
        "isha": f"20:{2 + (base_offset % 10):02d}",
        "date": day.isoformat(),
    }
