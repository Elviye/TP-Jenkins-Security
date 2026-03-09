import pytest
from app import add, subtract, multiply, divide

def test_add():
    """Test de la fonction add"""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    """Test de la fonction subtract"""
    assert subtract(5, 3) == 2
    assert subtract(1, 5) == -4
    assert subtract(0, 0) == 0

def test_multiply():
    """Test de la fonction multiply"""
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(0, 5) == 0

def test_divide():
    """Test de la fonction divide"""
    assert divide(6, 3) == 2
    assert divide(5, 2) == 2.5
    
    # Test de la division par zéro
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

# Test paramétré pour tester plusieurs cas en une seule fonction
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (-1, -1, -2),
    (0, 5, 5),
    (100, 200, 300)
])
def test_add_parametrized(a, b, expected):
    """Test paramétré de la fonction add"""
    assert add(a, b) == expected