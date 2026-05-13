"""
Использование специфичных динамических возможностей Python

**Почему все JIT'ы плохи здесь:**
- eval() и exec() - чистая интерпретация
- Reflection (getattr, setattr) - динамический доступ
- Dynamic code generation - невозможно предсказать
- Introspection - runtime метаданные

**Эти задачи показывают:**
- Где JIT не помогает
- Ограничения компиляции
- Важность интерпретатора
"""


def eval_expressions(n: int) -> float:
    """
    Вычисление выражений через eval().
    """ 
    expressions = [
        "1 + 2 * 3",
        "sum(range(10))",
        "len([i for i in range(20)])",
        "max(5, 10, 15)",
        "[x**2 for x in range(5)][-1]",
    ]
    
    result = 0.0
    for _ in range(n):
        for expr in expressions:
            result += float(eval(expr))
    
    return result


def dynamic_attributes(n: int) -> int:
    """
    Динамическая работа с атрибутами.
    """
    class DynamicObject:
        pass
    
    obj = DynamicObject()
    
    # Установка атрибутов
    for i in range(n):
        attr_name = f"attr_{i % 100}"
        setattr(obj, attr_name, i)
    
    # Чтение атрибутов
    total = 0
    for i in range(n):
        attr_name = f"attr_{i % 100}"
        if hasattr(obj, attr_name):
            total += getattr(obj, attr_name)
    
    return total % 1_000_000_007


def string_formatting_complex(n: int) -> str:
    """
    Сложное форматирование строк.
    """
    data = {"name": "Alice", "age": 30, "score": 95.5}
    
    result = ""
    for i in range(n):
        # f-strings
        result = f"User {data['name']} is {data['age']} years old"
        
        # format()
        result = "Score: {score:.2f}, Age: {age}".format(**data)
        
        # %
        result = "Name: %s, Score: %.1f" % (data['name'], data['score'])
    
    return result


def generator_expressions(n: int) -> int:
    """
    Генераторные выражения и comprehensions.
    """
    # Generator expression
    gen = [x for x in range(n) if x % 2 == 0]

    return sum(gen) % 1_000_000_007


def decorator_heavy(n: int) -> int:
    """
    Много вызовов через декораторы.
    """
    def timing_decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result
        return wrapper
    
    def validation_decorator(func):
        def wrapper(*args, **kwargs):
            if args and args[0] < 0:
                return 0
            return func(*args, **kwargs)
        return wrapper
    
    @timing_decorator
    @validation_decorator
    def compute(x):
        return x * 2 + 1
    
    total = 0
    for i in range(n):
        total += compute(i)
    
    return total % 1_000_000_007


def context_managers(n: int) -> int:
    """
    Использование context managers.
    """
    class CounterContext:
        def __init__(self):
            self.count = 0
        
        def __enter__(self):
            self.count += 1
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.count += 1
            return False
    
    total = 0
    for _ in range(n):
        with CounterContext() as ctx:
            total += ctx.count
    
    return total


def exception_handling_heavy(n: int) -> int:
    """
    Тяжелая обработка исключений.
    """
    caught = 0
    
    for i in range(n):
        try:
            if i % 10 == 0:
                raise ValueError("test exception")
            result = 100 / (i % 5 or 1)
        except ValueError:
            caught += 1
        except ZeroDivisionError:
            caught += 1
        finally:
            pass
    
    return caught


def metaclass_usage(n: int) -> int:
    """
    Использование метаклассов.
    """
    class CountingMeta(type):
        instance_count = 0
        
        def __call__(cls, *args, **kwargs):
            CountingMeta.instance_count += 1
            return super().__call__(*args, **kwargs)
    
    class MyClass(metaclass=CountingMeta):
        def __init__(self, value):
            self.value = value
    
    instances = []
    for i in range(n):
        instances.append(MyClass(i))
    
    return CountingMeta.instance_count


# Параметры для бенчмарка
BENCHMARK_PARAMS = {
    "eval_expressions": {"n": 1_000},
    "dynamic_attributes": {"n": 10_000},
    "string_formatting_complex": {"n": 100_000},
    "generator_expressions": {"n": 10_000},
    "decorator_heavy": {"n": 100_000},
    "context_managers": {"n": 50_000},
    "exception_handling_heavy": {"n": 10_000},
    "metaclass_usage": {"n": 1_000},
}
