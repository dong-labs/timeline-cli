from typing import Any
from dong.io import BaseExporter, ExporterRegistry
from .db.connection import TimelineDatabase

class TimelineExporter(BaseExporter):
    name = "timeline"
    
    def fetch_all(self) -> list[dict[str, Any]]:
        with TimelineDatabase.get_cursor() as cur:
            cur.execute("SELECT id, title, event_date, description, project, tags, importance, created_at, updated_at FROM events ORDER BY event_date DESC")
            return [
                {
                    "id": row[0], "title": row[1], "event_date": row[2],
                    "description": row[3], "project": row[4], "tags": row[5].split(",") if row[5] else [],
                    "importance": row[6], "created_at": row[7], "updated_at": row[8],
                }
                for row in cur.fetchall()
            ]

ExporterRegistry.register(TimelineExporter())
