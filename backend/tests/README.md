# RAG系统测试框架

这个测试框架为RAG（检索增强生成）系统提供了全面的测试覆盖，包括单元测试、API测试和集成测试。

## 测试结构

```
backend/tests/
├── __init__.py           # 测试包初始化
├── conftest.py           # 测试配置和共享夹具
├── test_api.py          # API端点测试
├── test_models.py       # 数据模型单元测试
├── test_app.py          # 测试专用FastAPI应用
└── README.md            # 本文档
```

## 测试类型

### 1. 单元测试 (`test_models.py`)
- 测试数据模型（Course, Lesson, CourseChunk）
- 验证序列化和反序列化功能
- 确保基本模型功能正确

### 2. API测试 (`test_api.py`)
- 测试所有API端点：
  - POST `/api/query` - 查询课程材料
  - GET `/api/courses` - 获取课程统计信息
- 验证请求/响应格式
- 测试错误处理和边界情况
- 测试CORS配置

### 3. 集成测试
- 测试完整查询流程
- 会话管理测试
- 错误恢复测试

## 测试标记

- `@pytest.mark.api` - API端点测试
- `@pytest.mark.unit` - 单元测试
- `@pytest.mark.integration` - 集成测试
- `@pytest.mark.slow` - 耗时测试

## 使用方法

### 运行所有测试
```bash
./run_tests.sh
```

### 运行特定测试
```bash
# 运行API测试
uv run pytest backend/tests/test_api.py -v

# 运行单元测试
uv run pytest backend/tests/test_models.py -v

# 运行带标记的测试
uv run pytest backend/tests/ -m "not slow" -v

# 运行特定测试类
uv run pytest backend/tests/test_api.py::TestAPIEndpoints -v
```

### 生成测试覆盖率报告
```bash
uv run pytest backend/tests/ --cov=backend --cov-report=html
# 查看报告：打开 htmlcov/index.html
```

## 测试夹具

`conftest.py` 提供了以下共享夹具：

- `test_client` - FastAPI测试客户端
- `mock_rag_system` - 模拟的RAG系统
- `mock_vector_store` - 模拟的向量存储
- `mock_ai_generator` - 模拟的AI生成器
- `sample_course` - 示例课程数据
- `sample_course_chunks` - 示例课程分块数据
- `sample_query_data` - 示例查询数据

## 测试配置

测试配置位于 `pyproject.toml` 中：

- 测试路径：`backend/tests/`
- 测试文件模式：`test_*.py`, `*_test.py`
- 覆盖率报告：HTML、XML和终端输出
- 测试标记：slow, integration, unit, api

## 环境要求

确保已安装测试依赖：

```bash
uv sync --extra dev
```

## 添加新测试

1. 创建新的测试文件，遵循命名约定 `test_*.py`
2. 使用提供的夹具进行测试
3. 添加适当的测试标记
4. 确保测试覆盖所有边缘情况

## 最佳实践

- 使用异步测试标记 `@pytest.mark.asyncio` 测试异步函数
- 使用适当的测试标记组织测试
- 充分利用提供的模拟对象和夹具
- 为每个测试类添加清晰的文档字符串
- 测试正向和负向场景
- 验证错误处理行为