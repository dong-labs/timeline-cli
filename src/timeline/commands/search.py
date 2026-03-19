"""search 命令"""

import typer
from rich.console import Console
from rich.table import Table
from ..db import get_cursor, is_initialized, get_db_path
from dong import json_output, DongError

console = Console()


@json_output
def search(
    query: str = typer.Argument(..., help="搜索关键词"),
    limit: int = typer.Option(20, "--limit", "-l", help="限制数量"),
):
    """搜索事件"""
    if not is_initialized():
        raise DongError("NOT_INITIALIZED", "请先运行 dong-timeline init")
    
    db_path = get_db_path()
    if not db_path.exists():
        raise DongError("NOT_INITIALIZED", "数据库不存在，请运行 dong-timeline init")
    
    search_pattern = f"%{query}%"
    
    with get_cursor() as cur:
        cur.execute("""
            SELECT * FROM events
            WHERE title LIKE ? OR description LIKE ? OR project LIKE ? OR tags LIKE ?
            ORDER BY event_date DESC
            LIMIT ?
        """, (search_pattern, search_pattern, search_pattern, search_pattern, limit))
        
        rows = cur.fetchall()
    
    if not rows:
        console.print(f"未找到包含 '[yellow]{query}[/yellow]' 的事件")
        return {"query": query, "items": [], "total": 0}
    
    # 渲染表格
    table = Table(title=f"搜索结果：{query}")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("日期", style="yellow")
    table.add_column("事件", style="green")
    table.add_column("项目", style="blue")
    table.add_column("重要程度", style="magenta")
    
    items = []
    for row in rows:
        event_id, title, event_date, description, project, tags, importance, created_at, updated_at = row
        
        importance_emoji = {"high": "🔴", "normal": "🟡", "low": "🟢"}.get(importance, "🟡")
        
        table.add_row(
            str(event_id),
            event_date,
            title,
            project or "-",
            f"{importance_emoji} {importance}",
        )
        
        items.append({
            "id": event_id,
            "title": title,
            "date": event_date,
            "project": project,
            "importance": importance,
        })
    
    console.print(table)
    
    return {"query": query, "items": items, "total": len(items)}
