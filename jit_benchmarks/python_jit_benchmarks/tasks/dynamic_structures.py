"""
Работа с динамическими структурами данных (списки, словари).

**Почему PyPy выигрывает:**
- Специализация dict/list операций
- Inline caching для методов
- Оптимизация аллокаций

**Почему Numba не может:**
- Numba nopython mode не поддерживает Python collections
- Можно использовать object mode, но будет медленно
"""


def dict_operations(n: int) -> int:
    """
    Операции со словарями.
    
    Args:
        n: количество операций
        
    Returns:
        размер словаря
    """
    data = {}
    
    # Добавление элементов
    for i in range(n):
        key = f"key_{i % 1000}"
        data[key] = data.get(key, 0) + 1
    
    # Обновление
    for key in list(data.keys()):
        data[key] *= 2
    
    # Фильтрация
    filtered = {k: v for k, v in data.items() if v > 5}
    
    return len(filtered)


def list_operations(n: int) -> int:
    """
    Операции со списками.
    
    Args:
        n: количество операций
        
    Returns:
        сумма элементов
    """
    data = []
    
    # Добавление
    for i in range(n):
        data.append(i)
    
    # Фильтрация
    filtered = [x for x in data if x % 2 == 0]
    
    # Map
    squared = [x ** 2 for x in filtered]
    
    # Reduce
    return sum(squared) % 1_000_000_007


def nested_structures(depth: int, width: int) -> int:
    """
    Работа с вложенными структурами.
    
    Args:
        depth: глубина вложенности
        width: количество элементов на уровне
        
    Returns:
        общее количество элементов
    """
    def create_tree(d):
        if d == 0:
            return {"value": 1, "children": []}
        return {
            "value": d,
            "children": [create_tree(d - 1) for _ in range(width)]
        }
    
    def count_nodes(node):
        if not node["children"]:
            return 1
        return 1 + sum(count_nodes(child) for child in node["children"])
    
    tree = create_tree(depth)
    return count_nodes(tree)


def json_like_processing(n: int) -> int:
    """
    Обработка JSON-подобных структур.
    
    Args:
        n: количество записей
        
    Returns:
        количество обработанных записей
    """
    records = []
    
    # Создание данных
    for i in range(n):
        record = {
            "id": i,
            "name": f"user_{i}",
            "active": i % 2 == 0,
            "score": float(i) * 1.5,
            "tags": [f"tag_{i % 10}", f"group_{i % 5}"],
            "metadata": {
                "created_at": i * 1000,
                "updated_at": i * 1000 + 500,
            }
        }
        records.append(record)
    
    # Фильтрация
    active_users = [r for r in records if r["active"]]
    
    # Агрегация
    total_score = sum(r["score"] for r in active_users)
    
    # Группировка
    by_tag = {}
    for r in active_users:
        for tag in r["tags"]:
            if tag not in by_tag:
                by_tag[tag] = []
            by_tag[tag].append(r["id"])
    
    return len(by_tag)


def set_operations(n: int) -> int:
    """
    Операции с множествами.
    
    Args:
        n: размер множеств
        
    Returns:
        размер результата
    """
    set_a = {i for i in range(n)}
    set_b = {i for i in range(n // 2, n + n // 2)}
    
    # Объединение
    union = set_a | set_b
    
    # Пересечение
    intersection = set_a & set_b
    
    # Разность
    difference = set_a - set_b
    
    # Симметрическая разность
    sym_diff = set_a ^ set_b
    
    return len(union) + len(intersection) + len(difference) + len(sym_diff)


# Параметры для бенчмарка
BENCHMARK_PARAMS = {
    "dict_operations": {"n": 100_000},
    "list_operations": {"n": 100_000},
    "nested_structures": {"depth": 8, "width": 3},
    "json_like_processing": {"n": 10_000},
    "set_operations": {"n": 50_000},
}
