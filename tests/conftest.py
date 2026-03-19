"""测试配置"""

import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_db():
    """创建临时数据库"""
    temp_dir = Path(tempfile.mkdtemp())
    db_path = temp_dir / "timeline.db"
    yield db_path
    shutil.rmtree(temp_dir)
