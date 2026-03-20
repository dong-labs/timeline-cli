from typing import Any
from dong.io import BaseImporter, ImporterRegistry
from .db.connection import TimelineDatabase

class TimelineImporter(BaseImporter):
    name = "timeline"
    
    def validate(self, data: list[dict[str, Any]]) -> tuple[bool, str]:
        if not isinstance(data, list): return False, "数据必须是列表格式"
        for i, item in enumerate(data):
            if not isinstance(item, dict) or "title" not in item or "event_date" not in item:
                return False, f"第 {i+1} 条数据缺少 title 或 event_date 字段"
        return True, ""
    
    def import_data(self, data: list[dict[str, Any]], merge: bool = False) -> dict[str, Any]:
        with TimelineDatabase.get_cursor() as cur:
            if not merge: cur.execute("DELETE FROM events")
            imported, skipped = 0, 0
            for item in data:
                if merge:
                    cur.execute("SELECT id FROM events WHERE title = ? AND event_date = ?", (item["title"], item["event_date"]))
                    if cur.fetchone(): skipped += 1; continue
                cur.execute("INSERT INTO events (title, event_date, description, project, tags, importance) VALUES (?, ?, ?, ?, ?, ?)",
                    (item["title"], item["event_date"], item.get("description"), item.get("project"), ",".join(item.get("tags", [])), item.get("importance", "normal")))
                imported += 1
            return {"imported": imported, "skipped": skipped, "total": len(data)}

ImporterRegistry.register(TimelineImporter())
