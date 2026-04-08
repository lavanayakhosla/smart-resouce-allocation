"""Matching engine for volunteer-to-need assignment."""

from __future__ import annotations

from collections import Counter
from typing import Any

import database
from data import AVAILABILITY_SCORE, CATEGORY_TO_SKILL, normalize_skills, proximity_score


def calculate_score(
    volunteer: dict[str, Any], need: dict[str, Any], current_load: int
) -> dict[str, int]:
    """Score components for one volunteer-need pair."""
    required_skill = CATEGORY_TO_SKILL.get(need["category"], "")
    volunteer_skills = normalize_skills(volunteer["skills"])

    skill_component = 40 if required_skill in volunteer_skills else 0
    proximity_component = proximity_score(volunteer["area"], need["area"])
    availability_component = AVAILABILITY_SCORE.get(volunteer["availability"], 0)

    # Small penalty to avoid assigning everything to one volunteer.
    load_penalty = min(current_load * 5, 20)

    total = max(
        skill_component + proximity_component + availability_component - load_penalty,
        0,
    )

    return {
        "skill": skill_component,
        "proximity": proximity_component,
        "availability": availability_component,
        "penalty": load_penalty,
        "total": total,
    }


def run_matching() -> int:
    """
    Assign the best volunteer to each unassigned need.
    Returns number of assignments created in this run.
    """
    volunteers = database.get_volunteers()
    needs = database.get_unassigned_needs()
    if not volunteers or not needs:
        return 0

    existing_assignments = database.get_assignments()
    volunteer_load = Counter(a["volunteer_id"] for a in existing_assignments)

    created = 0
    for need in needs:
        best_volunteer = None
        best_score = -1

        for volunteer in volunteers:
            score_breakdown = calculate_score(
                volunteer, need, volunteer_load[volunteer["id"]]
            )
            score = score_breakdown["total"]
            if score > best_score:
                best_score = score
                best_volunteer = volunteer

        if best_volunteer and best_score > 0:
            database.create_assignment(need["id"], best_volunteer["id"], best_score)
            volunteer_load[best_volunteer["id"]] += 1
            created += 1

    return created

