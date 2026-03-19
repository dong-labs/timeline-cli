"""stats 命令"""

import typer
from rich.console import Console
from rich.table import Table
from ..db import get_cursor, is_initialized, get_db_path
from dong import json_output, DongError

console = Console()


@json_output
def stats():
    """统计信息"""
    if not is_initialized():
        raise DongError("NOT_INITIALIZED", "请先运行 dong-timeline init")
    
    db_path = get_db_path()
    if not db_path.exists():
        raise DongError("NOT_INITIALIZED", "数据库不存在，请运行 dong-timeline init")
    
    with get_cursor() as cur:
        # 总数
        cur.execute("SELECT COUNT(*) FROM events")
        total = cur.fetchone()[0]
        
        # 按项目统计
        cur.execute("""
            SELECT project, COUNT(*) as count
            FROM events
            GROUP BY project
            ORDER BY count DESC
        """)
        project_stats = cur.fetchall()
        
        # 按重要程度统计
        cur.execute("""
            SELECT importance, COUNT(*) as count
            FROM events
            GROUP BY importance
        """)
        importance_stats = cur.fetchall()
        
        # 按年份统计
        cur.execute("""
            SELECT strftime('%Y', event_date) as year, COUNT(*) as count
            FROM events
            GROUP BY year
            ORDER BY year DESC
        """)
        year_stats = cur.fetchall()
    
    if total == 0:
        console.print("暂无事件记录")
        return {"total": 0, "projects": [], "importance": [], "years": []}
    
    # 渲染表格
    table = Table(title="时间轴统计")
    table.add_column("分类", style="blue")
    table.add_column("数量", justify="right", style="cyan")
    
    table.add_row("总事件数", str(total))
    console.print(table)
    
    # 按项目统计
    if project_stats:
        project_table = Table(title="按项目统计")
        project_table.add_column("项目", style="blue")
        project_table.add_column("数量", justify="right", style="cyan")
        
        for project, count in project_stats:
            project_table.add_row(project or "未分类", str(count))
        
        console.print(project_table)
    
    # 按重要程度统计
    if importance_stats:
        importance_table = Table(title="按重要程度统计")
        importance_table.add_column("重要程度", style="blue")
        importance_table.add_column("数量", justify="right", style="cyan")
        
        for importance, count in importance_stats:
            importance_emoji = {"high": "🔴", "normal": "🟡", "low": "🟢"}.get(importance, "🟡")
            importance_table.add_row(f"{importance_emoji} {importance}", str(count))
        
        console.print(importance_table)
    
    # 按年份统计
    if year_stats:
        year_table = Table(title="按年份统计")
        year_table.add_column("年份", style="blue")
        year_table.add_column("数量", justify="right", style="cyan")
        
        for year, count in year_stats:
            year_table.add_row(year, str(count))
        
        console.print(year_table)
    
    return {
        "total": total,
        "projects": [{"project": p, "count": c} for p, c in project_stats],
        "importance": [{"importance": i, "count": c} for i, c in importance_stats],
        "years": [{"year": y, "count": c} for y, c in year_stats],
    }
