---
trigger: always_on
---

# Python 代码生成规范

## 运行环境
- 目标运行时: Python 3.12+
- 框架: FastAPI + SQLModel

## 类型提示标准 (严格执行)
你必须使用现代的 Python 3.10+ 语法进行类型提示。

1. 使用管道操作符 (|) 表示 Unions:
   - 禁止: from typing import Union -> Union[str, int]
   - 必须: str | int

2. 使用管道操作符 (|) 表示 Optionals:
   - 禁止: from typing import Optional -> Optional[str]
   - 必须: str | None

3. 使用内置泛型 (PEP 585):
   - 不要从 typing 导入集合类型。请使用标准的内置类型。
   - 禁止: from typing import List, Dict, Tuple, Set
   - 必须: list[str], dict[str, Any], tuple[int, int], set[str]

4. 导入规范 (Import Hygiene):
   - 不要从 typing 导入 Union, Optional, List, Dict, Tuple。
   - 只有在绝对必要时才从 typing 导入复杂类型 (如 Any, Callable, TypeVar)。

## 示例

### 错误示范 (Bad)
```python
from typing import Union, List, Optional, Dict

def process_items(items: List[str]) -> Optional