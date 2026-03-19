# 时间咚（dong-timeline）

记录人生/项目的关键节点，让时间有迹可循

## 安装

```bash
pipx install dong-timeline
```

## 快速开始

```bash
# 初始化
dong-timeline init

# 添加事件
dong-timeline add "499社群启动" --date 2026-03-19 --project "社群" --tags "里程碑"

# 列出事件
dong-timeline list

# 按年份筛选
dong-timeline list --year 2026

# 按项目筛选
dong-timeline list --project "咚咚家族"

# 查看详情
dong-timeline get 1

# 搜索
dong-timeline search "社群"

# 统计
dong-timeline stats
```

## 命令

| 命令 | 说明 |
|------|------|
| `init` | 初始化数据库 |
| `add` | 添加事件 |
| `list` | 列出事件 |
| `get` | 获取详情 |
| `update` | 更新事件 |
| `delete` | 删除事件 |
| `search` | 搜索事件 |
| `stats` | 统计信息 |

## 数据结构

| 字段 | 说明 |
|------|------|
| title | 事件标题 |
| event_date | 发生日期 |
| description | 详细描述 |
| project | 关联项目 |
| tags | 标签 |
| importance | 重要程度 (high/normal/low) |

## 数据库

数据存储在 `~/.dong/timeline.db`

## License

MIT
