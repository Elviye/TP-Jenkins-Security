def add(a, b):
    """Fonction simple pour tester l'addition"""
    return a + b

def subtract(a, b):
    """Fonction simple pour tester la soustraction"""
    return a - b

def multiply(a, b):
    """Fonction simple pour tester la multiplication"""
    return a * b

def divide(a, b):
    """Fonction simple pour tester la division"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

if __name__ == "__main__":
    print(f"2 + 3 = {add(2, 3)}")
    print(f"5 - 3 = {subtract(5, 3)}")
    print(f"4 * 3 = {multiply(4, 3)}")
    print(f"10 / 2 = {divide(10, 2)}")