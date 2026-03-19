"""ls 命令"""

import typer
from rich.console import Console
from rich.table import Table
from datetime import datetime
from ..db import get_cursor, is_initialized, get_db_path
from dong import json_output, DongError

console = Console()


@json_output
def list_events(
    year: int = typer.Option(None, "--year", "-y", help="按年份筛选"),
    project: str = typer.Option(None, "--project", "-p", help="按项目筛选"),
    importance: str = typer.Option(None, "--importance", "-i", help="按重要程度筛选"),
    range_str: str = typer.Option(None, "--range", "-r", help="时间范围 (YYYY-MM,YYYY-MM)"),
    limit: int = typer.Option(50, "--limit", "-l", help="限制数量"),
):
    """列出时间轴事件"""
    if not is_initialized():
        raise DongError("NOT_INITIALIZED", "请先运行 dong-timeline init")
    
    db_path = get_db_path()
    if not db_path.exists():
        raise DongError("NOT_INITIALIZED", "数据库不存在，请运行 dong-timeline init")
    
    with get_cursor() as cur:
        # 构建查询
        query = "SELECT * FROM events"
        params = []
        conditions = []
        
        if year:
            conditions.append("strftime('%Y', event_date) = ?")
            params.append(str(year))
        
        if project:
            conditions.append("project = ?")
            params.append(project)
        
        if importance:
            conditions.append("importance = ?")
            params.append(importance)
        
        if range_str:
            try:
                start, end = range_str.split(",")
                conditions.append("event_date >= ? AND event_date <= ?")
                params.extend([start, end])
            except ValueError:
                raise DongError("INVALID_RANGE", "时间范围格式错误，请使用 YYYY-MM,YYYY-MM")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY event_date DESC LIMIT ?"
        params.append(limit)
        
        cur.execute(query, params)
        rows = cur.fetchall()
    
    if not rows:
        console.print("暂无事件记录")
        return {"items": [], "total": 0}
    
    # 渲染表格
    table = Table(title="时间轴事件")
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
    
    return {"items": items, "total": len(items)}
