"""add 命令"""

import typer
from datetime import datetime
from ..db import get_cursor, is_initialized
from dong import json_output, DongError


@json_output
def add(
    title: str = typer.Argument(..., help="事件标题"),
    date: str = typer.Option(None, "--date", "-d", help="发生日期 (YYYY-MM-DD)，默认今天"),
    project: str = typer.Option(None, "--project", "-p", help="关联项目"),
    tags: str = typer.Option(None, "--tags", "-t", help="标签，多个用逗号分隔"),
    description: str = typer.Option(None, "--description", "--desc", help="详细描述"),
    importance: str = typer.Option("normal", "--importance", "-i", help="重要程度 (high/normal/low)"),
):
    """添加时间轴事件"""
    if not is_initialized():
        raise DongError("NOT_INITIALIZED", "请先运行 dong-timeline init")
    
    # 处理日期
    if not date:
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date, "%Y-%m-%d")
            date_str = date
        except ValueError:
            raise DongError("INVALID_DATE", "日期格式错误，请使用 YYYY-MM-DD")
    
    # 处理标签
    tags_str = ""
    if tags:
        tags_list = [t.strip() for t in tags.split(",") if t.strip()]
        tags_str = ",".join(tags_list)
    
    # 验证重要程度
    if importance not in ["high", "normal", "low"]:
        raise DongError("INVALID_IMPORTANCE", "重要程度必须是 high/normal/low")
    
    with get_cursor() as cur:
        cur.execute("""
            INSERT INTO events (title, event_date, description, project, tags, importance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, date_str, description, project, tags_str, importance))
        
        event_id = cur.lastrowid
    
    return {
        "id": event_id,
        "title": title,
        "date": date_str,
        "project": project,
        "tags": tags_str,
        "importance": importance,
    }
