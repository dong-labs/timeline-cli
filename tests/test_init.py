"""测试 init 命令"""

from click.testing import CliRunner
from timeline.cli import app


def test_init():
    """测试初始化"""
    runner = CliRunner()
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "数据库初始化成功" in result.output or "success" in result.output.lower()
