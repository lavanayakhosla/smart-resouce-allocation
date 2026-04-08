"""Dummy data + small helpers for the Delhi flood prototype."""

from __future__ import annotations

import math

# Approximate coordinates for selected Delhi areas (dummy-friendly precision).
AREA_COORDS = {
    "Connaught Place": (28.6315, 77.2167),
    "Rohini": (28.7495, 77.0565),
    "Dwarka": (28.5921, 77.0460),
    "Lajpat Nagar": (28.5677, 77.2434),
    "Saket": (28.5245, 77.2066),
    "Karol Bagh": (28.6519, 77.1909),
    "Mayur Vihar": (28.6115, 77.3010),
    "Shahdara": (28.6735, 77.2890),
    "Narela": (28.8527, 77.0929),
    "Okhla": (28.5355, 77.2732),
    "Janakpuri": (28.6219, 77.0878),
    "Bawana": (28.7982, 77.0415),
}

CATEGORY_TO_SKILL = {
    "Food": "Food",
    "Medical": "Medical",
    "Shelter": "Shelter",
    "Rescue": "Rescue",
}

AVAILABILITY_SCORE = {
    "Available now": 20,
    "Within 2 hours": 15,
    "Today": 10,
    "Tomorrow": 5,
    "Not available": 0,
}

DUMMY_VOLUNTEERS = [
    {
        "name": "Aman Verma",
        "phone": "9810010001",
        "skills": "Medical,Rescue",
        "area": "Lajpat Nagar",
        "availability": "Available now",
    },
    {
        "name": "Priya Singh",
        "phone": "9810010002",
        "skills": "Food,Shelter",
        "area": "Dwarka",
        "availability": "Within 2 hours",
    },
    {
        "name": "Ravi Kumar",
        "phone": "9810010003",
        "skills": "Driving,Rescue",
        "area": "Rohini",
        "availability": "Available now",
    },
    {
        "name": "Neha Arora",
        "phone": "9810010004",
        "skills": "Medical,Food",
        "area": "Mayur Vihar",
        "availability": "Today",
    },
    {
        "name": "Sahil Khan",
        "phone": "9810010005",
        "skills": "Shelter,Driving",
        "area": "Janakpuri",
        "availability": "Within 2 hours",
    },
    {
        "name": "Ishita Jain",
        "phone": "9810010006",
        "skills": "Food,Rescue",
        "area": "Karol Bagh",
        "availability": "Available now",
    },
    {
        "name": "Mohit Yadav",
        "phone": "9810010007",
        "skills": "Medical,Shelter",
        "area": "Okhla",
        "availability": "Today",
    },
    {
        "name": "Farhan Ali",
        "phone": "9810010008",
        "skills": "Rescue,Driving",
        "area": "Shahdara",
        "availability": "Available now",
    },
]

DUMMY_NEEDS = [
    {
        "category": "Rescue",
        "area": "Shahdara",
        "urgency": "Critical",
        "description": "Families stranded on first floors due to rising water.",
        "people_affected": 28,
    },
    {
        "category": "Medical",
        "area": "Okhla",
        "urgency": "Critical",
        "description": "Immediate medical assistance required for injured residents.",
        "people_affected": 19,
    },
    {
        "category": "Food",
        "area": "Mayur Vihar",
        "urgency": "High",
        "description": "Cooked meals needed at temporary shelter camp.",
        "people_affected": 65,
    },
    {
        "category": "Shelter",
        "area": "Dwarka",
        "urgency": "High",
        "description": "School building needs bedding and shelter setup.",
        "people_affected": 43,
    },
    {
        "category": "Rescue",
        "area": "Narela",
        "urgency": "Critical",
        "description": "Boat support needed near waterlogged colonies.",
        "people_affected": 34,
    },
    {
        "category": "Food",
        "area": "Karol Bagh",
        "urgency": "Medium",
        "description": "Dry ration packets required for displaced households.",
        "people_affected": 22,
    },
    {
        "category": "Medical",
        "area": "Saket",
        "urgency": "High",
        "description": "Need first aid and medicines for fever and dehydration.",
        "people_affected": 17,
    },
    {
        "category": "Shelter",
        "area": "Lajpat Nagar",
        "urgency": "Medium",
        "description": "Temporary tents required for evacuated residents.",
        "people_affected": 31,
    },
    {
        "category": "Food",
        "area": "Connaught Place",
        "urgency": "Low",
        "description": "Community kitchen support for transit workers.",
        "people_affected": 14,
    },
    {
        "category": "Rescue",
        "area": "Bawana",
        "urgency": "High",
        "description": "Need transport volunteers for evacuation.",
        "people_affected": 26,
    },
    {
        "category": "Medical",
        "area": "Rohini",
        "urgency": "Medium",
        "description": "Senior citizens need check-ups and medicine delivery.",
        "people_affected": 20,
    },
    {
        "category": "Shelter",
        "area": "Janakpuri",
        "urgency": "High",
        "description": "Need volunteers to manage shelter occupancy.",
        "people_affected": 37,
    },
    {
        "category": "Food",
        "area": "Shahdara",
        "urgency": "Critical",
        "description": "Children at relief camp need immediate food kits.",
        "people_affected": 49,
    },
    {
        "category": "Medical",
        "area": "Connaught Place",
        "urgency": "Low",
        "description": "Basic health desk setup at aid center.",
        "people_affected": 11,
    },
    {
        "category": "Shelter",
        "area": "Mayur Vihar",
        "urgency": "Medium",
        "description": "Need blankets and volunteers for nighttime shelter.",
        "people_affected": 25,
    },
]


def get_area_coord(area: str) -> tuple[float, float] | None:
    return AREA_COORDS.get(area)


def normalize_skills(skills_value: str) -> set[str]:
    return {s.strip() for s in skills_value.split(",") if s.strip()}


def haversine_km(a: tuple[float, float], b: tuple[float, float]) -> float:
    """Distance in kilometers between two lat/lon points."""
    lat1, lon1 = a
    lat2, lon2 = b
    r = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    x = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return 2 * r * math.atan2(math.sqrt(x), math.sqrt(1 - x))


def proximity_score(volunteer_area: str, need_area: str) -> int:
    """Simple score for proximity: max 30."""
    if volunteer_area == need_area:
        return 30

    vol_coord = get_area_coord(volunteer_area)
    need_coord = get_area_coord(need_area)
    if not vol_coord or not need_coord:
        return 10

    distance = haversine_km(vol_coord, need_coord)
    if distance <= 3:
        return 30
    if distance <= 7:
        return 20
    if distance <= 12:
        return 10
    return 0

