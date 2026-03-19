"""数据库 Schema 定义和版本管理

继承 dong.db.SchemaManager，管理 timeline 的数据库 schema。
"""

from dong.db import SchemaManager

from .connection import TimelineDatabase


# 当前 Schema 版本
SCHEMA_VERSION = "1.0.0"


class TimelineSchemaManager(SchemaManager):
    """
    时间咚 Schema 管理器

    继承自 dong.db.SchemaManager，管理 timeline 的数据库 schema。
    """

    def __init__(self):
        super().__init__(
            db_class=TimelineDatabase,
            current_version=SCHEMA_VERSION
        )

    def init_schema(self) -> None:
        """初始化数据库，创建所有必要表"""
        self._create_events_table()
        self._create_indexes()

    def _create_events_table(self) -> None:
        """创建 events 表"""
        with TimelineDatabase.get_cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    event_date TEXT NOT NULL,
                    description TEXT,
                    project TEXT,
                    tags TEXT DEFAULT '',
                    importance TEXT DEFAULT 'normal',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def _create_indexes(self) -> None:
        """创建索引"""
        with TimelineDatabase.get_cursor() as cur:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_events_date ON events(event_date)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_events_project ON events(project)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_events_importance ON events(importance)")


def init_database():
    """初始化数据库"""
    manager = TimelineSchemaManager()
    manager.init_schema()
    return {"message": "数据库初始化成功", "version": SCHEMA_VERSION}


def is_initialized() -> bool:
    """检查数据库是否已初始化"""
    db_path = TimelineDatabase.get_db_path()
    if not db_path.exists():
        return False

    try:
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
        result = cur.fetchone() is not None
        conn.close()
        return result
    except Exception:
        return False
