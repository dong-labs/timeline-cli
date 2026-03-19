"""delete 命令"""

import typer
from ..db import get_cursor, is_initialized
from dong import json_output, DongError


@json_output
def delete(
    event_id: int = typer.Argument(..., help="事件 ID"),
    force: bool = typer.Option(False, "--force", "-f", help="强制删除，不确认"),
):
    """删除事件"""
    if not is_initialized():
        raise DongError("NOT_INITIALIZED", "请先运行 dong-timeline init")
    
    if not force:
        if not typer.confirm(f"确定要删除 ID={event_id} 的事件吗？"):
            return {"cancelled": True}
    
    with get_cursor() as cur:
        # 先检查是否存在
        cur.execute("SELECT title FROM events WHERE id = ?", (event_id,))
        row = cur.fetchone()
        
        if not row:
            raise DongError("NOT_FOUND", f"未找到 ID={event_id} 的事件")
        
        title = row[0]
        
        # 删除事件
        cur.execute("DELETE FROM events WHERE id = ?", (event_id,))
    
    return {"id": event_id, "title": title, "deleted": True}
