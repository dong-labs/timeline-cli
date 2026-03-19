"""update 命令"""

import typer
from datetime import datetime
from ..db import get_cursor, is_initialized
from dong import json_output, DongError


@json_output
def update(
    event_id: int = typer.Argument(..., help="事件 ID"),
    title: str = typer.Option(None, "--title", help="事件标题"),
    date: str = typer.Option(None, "--date", "-d", help="发生日期"),
    project: str = typer.Option(None, "--project", "-p", help="关联项目"),
    tags: str = typer.Option(None, "--tags", "-t", help="标签"),
    description: str = typer.Option(None, "--description", "--desc", help="详细描述"),
    importance: str = typer.Option(None, "--importance", "-i", help="重要程度"),
):
    """更新事件"""
    if not is_initialized():
        raise DongError("NOT_INITIALIZED", "请先运行 dong-timeline init")
    
    # 构建更新语句
    updates = []
    params = []
    
    if title:
        updates.append("title = ?")
        params.append(title)
    
    if date:
        try:
            datetime.strptime(date, "%Y-%m-%d")
            updates.append("event_date = ?")
            params.append(date)
        except ValueError:
            raise DongError("INVALID_DATE", "日期格式错误，请使用 YYYY-MM-DD")
    
    if project:
        updates.append("project = ?")
        params.append(project)
    
    if tags:
        tags_list = [t.strip() for t in tags.split(",") if t.strip()]
        tags_str = ",".join(tags_list)
        updates.append("tags = ?")
        params.append(tags_str)
    
    if description:
        updates.append("description = ?")
        params.append(description)
    
    if importance:
        if importance not in ["high", "normal", "low"]:
            raise DongError("INVALID_IMPORTANCE", "重要程度必须是 high/normal/low")
        updates.append("importance = ?")
        params.append(importance)
    
    if not updates:
        raise DongError("NO_UPDATES", "没有指定要更新的字段")
    
    updates.append("updated_at = CURRENT_TIMESTAMP")
    params.append(event_id)
    
    with get_cursor() as cur:
        cur.execute(
            f"UPDATE events SET {', '.join(updates)} WHERE id = ?",
            params
        )
        
        if cur.rowcount == 0:
            raise DongError("NOT_FOUND", f"未找到 ID={event_id} 的事件")
    
    return {"id": event_id, "updated": True}
