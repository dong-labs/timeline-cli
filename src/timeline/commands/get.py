"""get 命令"""

import typer
from rich.console import Console
from rich.table import Table
from ..db import get_cursor, is_initialized, get_db_path
from dong import json_output, DongError

console = Console()


@json_output
def get(
    event_id: int = typer.Argument(..., help="事件 ID"),
):
    """获取事件详情"""
    if not is_initialized():
        raise DongError("NOT_INITIALIZED", "请先运行 dong-timeline init")
    
    db_path = get_db_path()
    if not db_path.exists():
        raise DongError("NOT_INITIALIZED", "数据库不存在，请运行 dong-timeline init")
    
    with get_cursor() as cur:
        cur.execute("SELECT * FROM events WHERE id = ?", (event_id,))
        row = cur.fetchone()
        
        if not row:
            raise DongError("NOT_FOUND", f"未找到 ID={event_id} 的事件")
        
        event_id, title, event_date, description, project, tags, importance, created_at, updated_at = row
    
    # 渲染详情
    console.print(f"\n[bold green]{title}[/bold green]")
    console.print(f"  ID: {event_id}")
    console.print(f"  日期: [yellow]{event_date}[/yellow]")
    console.print(f"  项目: {project or '-'}")
    console.print(f"  重要程度: {importance}")
    console.print(f"  标签: {tags or '-'}")
    if description:
        console.print(f"  描述: {description}")
    console.print(f"  创建时间: {created_at}")
    console.print(f"  更新时间: {updated_at}")
    
    return {
        "id": event_id,
        "title": title,
        "date": event_date,
        "project": project,
        "tags": tags,
        "importance": importance,
        "description": description,
        "created_at": created_at,
        "updated_at": updated_at,
    }
