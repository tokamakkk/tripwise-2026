# Tests 模块

应用测试模块，包含单元测试和集成测试。

## 文件说明

### `__init__.py`
测试模块初始化文件。

### `test_services.py`
服务层测试文件（示例）。

#### 测试类（Test Classes）

1. **TestFirebaseService**
   - Firebase 服务测试
   - 测试内容：
     - Firebase 初始化
     - Token 验证
     - 用户 CRUD 操作
     - 旅行计划存储

2. **TestAIService**
   - AI 服务测试
   - 测试内容：
     - 旅行计划生成
     - 输出解析

## 运行测试

### 安装测试依赖

```bash
pip install pytest pytest-flask
```

### 运行所有测试

```bash
# 在项目根目录运行
pytest tests/

# 显示详细输出
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_services.py

# 运行特定测试类
pytest tests/test_services.py::TestFirebaseService

# 运行特定测试方法
pytest tests/test_services.py::TestFirebaseService::test_init_firebase
```

### 测试覆盖率

```bash
# 安装覆盖率工具
pip install pytest-cov

# 运行并生成覆盖率报告
pytest tests/ --cov=app --cov-report=html

# 查看报告
open htmlcov/index.html
```

## 测试结构

```
tests/
├── __init__.py
├── test_services.py          # 服务层测试
├── test_routes.py            # 路由测试（待添加）
├── test_models.py            # 模型验证测试（待添加）
├── test_agents.py            # Agent 测试（待添加）
└── conftest.py               # pytest 配置（待添加）
```

## 编写测试指南

### 基本测试结构

```python
import pytest
from app import create_app

class TestMyFeature:
    """功能测试类"""
    
    @pytest.fixture
    def app(self):
        """创建测试应用"""
        app = create_app('testing')
        return app
    
    @pytest.fixture
    def client(self, app):
        """创建测试客户端"""
        return app.test_client()
    
    def test_something(self, client):
        """测试某个功能"""
        response = client.get('/api/endpoint')
        assert response.status_code == 200
```

### Mock 外部服务

使用 `pytest-mock` 或 `unittest.mock` mock 外部服务：

```python
from unittest.mock import Mock, patch

def test_with_mock():
    """使用 mock 测试"""
    with patch('app.services.firebase_service.FirebaseService.verify_token') as mock_verify:
        mock_verify.return_value = {'uid': 'test_uid'}
        # 测试代码
        result = some_function()
        assert result is not None
```

### 测试 API 端点

```python
def test_create_travel_plan(client):
    """测试创建旅行计划"""
    # Mock 认证
    with patch('app.utils.decorators.FirebaseService.verify_token'):
        response = client.post('/api/travel/plan',
            json={
                'from_location': '北京',
                'destination': '成都',
                'num_people': 2,
                'duration': 5
            },
            headers={'Authorization': 'Bearer mock_token'}
        )
        assert response.status_code == 202
        data = response.get_json()
        assert 'plan_id' in data
```

### 测试数据验证

```python
from app.models import TravelPlanRequest
from pydantic import ValidationError

def test_travel_plan_validation():
    """测试旅行请求验证"""
    # 有效数据
    request = TravelPlanRequest(
        from_location="北京",
        destination="成都",
        num_people=2,
        duration=5
    )
    assert request.from_location == "北京"
    
    # 无效数据
    with pytest.raises(ValidationError):
        TravelPlanRequest(
            from_location="",
            destination="成都",
            num_people=0,  # 无效
            duration=5
        )
```

## 测试配置

### conftest.py 示例

```python
import pytest
from app import create_app
from app.config import TestingConfig

@pytest.fixture(scope='session')
def app():
    """创建测试应用实例"""
    app = create_app('testing')
    return app

@pytest.fixture(scope='function')
def client(app):
    """创建测试客户端"""
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """创建 CLI 测试运行器"""
    return app.test_cli_runner()

@pytest.fixture(scope='function')
def auth_headers():
    """创建认证请求头"""
    return {'Authorization': 'Bearer test_token'}
```

## 持续集成

### GitHub Actions 示例

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: pytest tests/ --cov=app
      env:
        FLASK_ENV: testing
        SECRET_KEY: test-secret-key
```

## 最佳实践

1. **隔离测试**：每个测试应该独立，不依赖其他测试
2. **使用 Fixtures**：共享测试数据和配置
3. **Mock 外部依赖**：避免测试依赖外部服务
4. **测试边界情况**：不仅测试正常情况，还要测试错误处理
5. **保持测试简单**：一个测试只测试一个功能点
6. **命名清晰**：测试名称应该清楚说明测试内容
7. **定期运行**：在 CI/CD 中自动运行测试

## 性能测试

使用 `pytest-benchmark` 进行性能测试：

```python
def test_performance(benchmark):
    """性能测试"""
    result = benchmark(some_function, arg1, arg2)
    assert result is not None
```

## 待添加的测试

- [ ] 路由测试（`test_routes.py`）
- [ ] 模型验证测试（`test_models.py`）
- [ ] Agent 测试（`test_agents.py`）
- [ ] 工具测试（`test_tools.py`）
- [ ] 集成测试（`test_integration.py`）
- [ ] API 端到端测试（`test_e2e.py`）

