"""
Код с использованием классов и объектов.

Почему PyPy выигрывает:
- Inline caching для method calls
- Hidden classes optimization
- Специализация методов под типы
- Оптимизация attribute access

Почему Numba плох:
- Numba nopython mode не поддерживает классы
- object mode в Numba медленный
"""


class Point2D:
    """Простой 2D точка."""
    
    __slots__ = ['x', 'y']
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def distance_to(self, other: 'Point2D') -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx * dx + dy * dy) ** 0.5
    
    def move(self, dx: float, dy: float) -> None:
        self.x += dx
        self.y += dy
    
    def scale(self, factor: float) -> None:
        self.x *= factor
        self.y *= factor


class Vector3D:
    """3D вектор с операциями."""
    
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
    
    def dot(self, other: 'Vector3D') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def length(self) -> float:
        return (self.x * self.x + self.y * self.y + self.z * self.z) ** 0.5
    
    def normalize(self) -> 'Vector3D':
        l = self.length()
        if l > 0:
            return Vector3D(self.x / l, self.y / l, self.z / l)
        return Vector3D(0, 0, 0)


class Shape:
    """Базовый класс для фигур."""
    
    def area(self) -> float:
        raise NotImplementedError
    
    def perimeter(self) -> float:
        raise NotImplementedError


class Rectangle(Shape):
    """Прямоугольник."""
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Circle(Shape):
    """Круг."""
    
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        return 3.14159 * self.radius * self.radius
    
    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius


def point_operations(n: int) -> float:
    """
    Операции с точками.
    
    Args:
        n: количество операций
        
    Returns:
        суммарное расстояние
    """
    points = [Point2D(float(i), float(i * 2)) for i in range(100)]
    
    total_distance = 0.0
    for _ in range(n):
        for i in range(len(points) - 1):
            total_distance += points[i].distance_to(points[i + 1])
            points[i].move(0.1, 0.1)
            points[i].scale(0.99)
    
    return total_distance


def vector_math(n: int) -> float:
    """
    Векторная математика.
    
    Args:
        n: количество операций
        
    Returns:
        результат вычислений
    """
    v1 = Vector3D(1.0, 2.0, 3.0)
    v2 = Vector3D(4.0, 5.0, 6.0)
    
    result = 0.0
    for i in range(n):
        dot = v1.dot(v2)
        cross = v1.cross(v2)
        length = cross.length()
        normalized = cross.normalize()
        
        result += dot + length + normalized.x
        
        # Обновляем векторы
        v1 = Vector3D(v1.x + 0.01, v1.y + 0.01, v1.z + 0.01)
        v2 = Vector3D(v2.x - 0.01, v2.y - 0.01, v2.z - 0.01)
    
    return result


def polymorphic_shapes(n: int) -> float:
    """
    Полиморфные вызовы методов.
    
    Args:
        n: количество итераций
        
    Returns:
        сумма площадей
    """
    shapes = []
    for i in range(100):
        if i % 2 == 0:
            shapes.append(Rectangle(float(i + 1), float(i + 2)))
        else:
            shapes.append(Circle(float(i + 1)))
    
    total_area = 0.0
    for _ in range(n):
        for shape in shapes:
            total_area += shape.area()  # Polymorphic call
            total_area += shape.perimeter()
    
    return total_area


class LinkedListNode:
    """Узел связного списка."""
    
    def __init__(self, value: int):
        self.value = value
        self.next = None


def linked_list_traversal(n: int) -> int:
    """
    Обход связного списка.
    
    Args:
        n: размер списка
        
    Returns:
        сумма значений
    """
    # Создание списка
    head = LinkedListNode(0)
    current = head
    for i in range(1, n):
        current.next = LinkedListNode(i)
        current = current.next
    
    # Обход списка несколько раз
    total = 0
    for _ in range(100):
        current = head
        while current is not None:
            total += current.value
            current = current.next
    
    return total % 1_000_000_007


class Counter:
    """Простой счетчик с методами."""
    
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
    
    def add(self, value: int):
        self.count += value
    
    def get(self) -> int:
        return self.count


def method_calls_heavy(n: int) -> int:
    """
    Много вызовов методов.
    
    Args:
        n: количество вызовов
        
    Returns:
        финальное значение счетчика
    """
    counter = Counter()
    
    for i in range(n):
        if i % 2 == 0:
            counter.increment()
        else:
            counter.add(i % 100)
    
    return counter.get()


# Параметры для бенчмарка
BENCHMARK_PARAMS = {
    "point_operations": {"n": 10_000},
    "vector_math": {"n": 100_000},
    "polymorphic_shapes": {"n": 10_000},
    "linked_list_traversal": {"n": 1_000},
    "method_calls_heavy": {"n": 1_000_000},
}


# Совместимость
COMPATIBILITY = {
    "cpython": True,
    "cpython_jit": True,
    "pypy": True,
    "numba": "object_mode",
}
