"""SQLite helpers for the disaster relief volunteer-need matching prototype."""

from __future__ import annotations

import sqlite3
from typing import Any

DB_PATH = "relief.db"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they do not exist."""
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS volunteers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL UNIQUE,
                skills TEXT NOT NULL,
                area TEXT NOT NULL,
                availability TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS needs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                area TEXT NOT NULL,
                urgency TEXT NOT NULL,
                description TEXT NOT NULL,
                people_affected INTEGER NOT NULL DEFAULT 1,
                status TEXT NOT NULL DEFAULT 'Open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                need_id INTEGER NOT NULL UNIQUE,
                volunteer_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (need_id) REFERENCES needs(id),
                FOREIGN KEY (volunteer_id) REFERENCES volunteers(id)
            )
            """
        )


def add_volunteer(
    name: str, phone: str, skills: str, area: str, availability: str
) -> tuple[bool, str]:
    """Insert a volunteer. Returns (success, message)."""
    try:
        with _connect() as conn:
            conn.execute(
                """
                INSERT INTO volunteers (name, phone, skills, area, availability)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, phone, skills, area, availability),
            )
        return True, "Volunteer registered."
    except sqlite3.IntegrityError:
        return False, "Phone number already exists."


def add_need(
    category: str, area: str, urgency: str, description: str, people_affected: int
) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO needs (category, area, urgency, description, people_affected)
            VALUES (?, ?, ?, ?, ?)
            """,
            (category, area, urgency, description, people_affected),
        )


def create_assignment(need_id: int, volunteer_id: int, score: int) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO assignments (need_id, volunteer_id, score)
            VALUES (?, ?, ?)
            """,
            (need_id, volunteer_id, score),
        )
        conn.execute("UPDATE needs SET status = 'Assigned' WHERE id = ?", (need_id,))


def mark_need_completed(need_id: int) -> None:
    with _connect() as conn:
        conn.execute("UPDATE needs SET status = 'Completed' WHERE id = ?", (need_id,))


def get_volunteers() -> list[dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT id, name, phone, skills, area, availability, created_at
            FROM volunteers
            ORDER BY id DESC
            """
        ).fetchall()
    return [dict(r) for r in rows]


def get_needs(order_by_urgency: bool = False) -> list[dict[str, Any]]:
    query = """
        SELECT id, category, area, urgency, description, people_affected, status, created_at
        FROM needs
    """
    if order_by_urgency:
        query += """
            ORDER BY
                CASE urgency
                    WHEN 'Critical' THEN 4
                    WHEN 'High' THEN 3
                    WHEN 'Medium' THEN 2
                    ELSE 1
                END DESC,
                id DESC
        """
    else:
        query += " ORDER BY id DESC"

    with _connect() as conn:
        rows = conn.execute(query).fetchall()
    return [dict(r) for r in rows]


def get_unassigned_needs() -> list[dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT n.id, n.category, n.area, n.urgency, n.description, n.people_affected, n.status
            FROM needs n
            LEFT JOIN assignments a ON a.need_id = n.id
            WHERE a.id IS NULL AND n.status != 'Completed'
            ORDER BY
                CASE n.urgency
                    WHEN 'Critical' THEN 4
                    WHEN 'High' THEN 3
                    WHEN 'Medium' THEN 2
                    ELSE 1
                END DESC,
                n.id DESC
            """
        ).fetchall()
    return [dict(r) for r in rows]


def get_assignments() -> list[dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT
                a.id,
                a.need_id,
                a.volunteer_id,
                a.score,
                a.assigned_at,
                n.category AS need_category,
                n.urgency AS need_urgency,
                n.area AS need_area,
                n.description AS need_description,
                n.people_affected,
                n.status AS need_status,
                v.name AS volunteer_name,
                v.phone AS volunteer_phone,
                v.skills AS volunteer_skills,
                v.area AS volunteer_area,
                v.availability AS volunteer_availability
            FROM assignments a
            JOIN needs n ON n.id = a.need_id
            JOIN volunteers v ON v.id = a.volunteer_id
            ORDER BY a.id DESC
            """
        ).fetchall()
    return [dict(r) for r in rows]


def get_need_counts_by_urgency() -> dict[str, int]:
    result = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT urgency, COUNT(*) AS total
            FROM needs
            GROUP BY urgency
            """
        ).fetchall()
    for row in rows:
        result[row["urgency"]] = row["total"]
    return result


def clear_needs_and_assignments() -> None:
    """Used for simulation reset."""
    with _connect() as conn:
        conn.execute("DELETE FROM assignments")
        conn.execute("DELETE FROM needs")


def seed_dummy_volunteers(volunteers: list[dict[str, Any]]) -> None:
    with _connect() as conn:
        for v in volunteers:
            conn.execute(
                """
                INSERT OR IGNORE INTO volunteers (name, phone, skills, area, availability)
                VALUES (?, ?, ?, ?, ?)
                """,
                (v["name"], v["phone"], v["skills"], v["area"], v["availability"]),
            )


def seed_dummy_needs(needs: list[dict[str, Any]]) -> None:
    with _connect() as conn:
        for n in needs:
            conn.execute(
                """
                INSERT INTO needs (category, area, urgency, description, people_affected)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    n["category"],
                    n["area"],
                    n["urgency"],
                    n["description"],
                    n["people_affected"],
                ),
            )
