"""数据库连接管理模块

继承 dong.db.Database，提供 timeline 专用数据库访问。
"""

import sqlite3
from typing import Iterator
from contextlib import contextmanager

from dong.db import Database as DongDatabase


class TimelineDatabase(DongDatabase):
    """
    时间咚数据库类

    继承自 dong.db.Database，提供统一的数据库管理。

    数据库路径: ~/.dong/timeline.db
    """

    @classmethod
    def get_name(cls) -> str:
        """返回 CLI 名称"""
        return "timeline"


# ============================================================================
# 兼容性函数：保持向后兼容
# ============================================================================

def get_connection(db_path=None):
    """获取数据库连接（兼容函数）"""
    return TimelineDatabase.get_connection()


def close_connection() -> None:
    """关闭数据库连接（兼容函数）"""
    TimelineDatabase.close_connection()


@contextmanager
def get_cursor() -> Iterator[sqlite3.Cursor]:
    """获取数据库游标（兼容函数）"""
    with TimelineDatabase.get_cursor() as cur:
        yield cur


def get_db_path():
    """获取数据库路径（兼容函数）"""
    return TimelineDatabase.get_db_path()
