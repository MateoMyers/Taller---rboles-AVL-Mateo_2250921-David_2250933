import sys

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

def getHeight(node):
    if not node:
        return 0
    return node.height

def getBalance(node):
    if not node:
        return 0
    return getHeight(node.left) - getHeight(node.right)

def updateHeight(node):
    if node:
        node.height = 1 + max(getHeight(node.left), getHeight(node.right))

def rotate_right(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    updateHeight(y)
    updateHeight(x)
    return x

def rotate_left(x):
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    updateHeight(x)
    updateHeight(y)
    return y

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if not node:
            return Node(value)

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            return node

        updateHeight(node)
        balance = getBalance(node)

        if balance > 1 and getBalance(node.left) >= 0:
            return rotate_right(node)
        elif balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            return rotate_right(node)
        elif balance < -1 and getBalance(node.right) <= 0:
            return rotate_left(node)
        elif balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            return rotate_left(node)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        if node is None:
            return node

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.value)

        updateHeight(node)
        balance = getBalance(node)

        if balance > 1 and getBalance(node.left) >= 0:
            return rotate_right(node)
        if balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            return rotate_right(node)
        if balance < -1 and getBalance(node.right) <= 0:
            return rotate_left(node)
        if balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            return rotate_left(node)

        return node

    def get_inorder(self):
        return self._inorder_helper(self.root, [])

    def _inorder_helper(self, node, result):
        if node:
            self._inorder_helper(node.left, result)
            result.append(node.value)
            self._inorder_helper(node.right, result)
        return result

    def print_tree(self):
        print("\\nÁrbol AVL:")
        if self.root:
            self._print_helper(self.root, 0)
        else:
            print("Árbol vacío")

    def _print_helper(self, node, level):
        if node is not None:
            self._print_helper(node.right, level + 1)
            print("   " * level + str(node.value) + "(h:" + str(node.height) + ",b:" + str(getBalance(node)) + ")")
            self._print_helper(node.left, level + 1)




avl = AVLTree()  # New tree for interactive

while True:
    print("\\nOpciones:")
    print("1. Insertar valor")
    print("2. Eliminar valor")
    print("3. Mostrar recorrido in-order")
    print("4. Mostrar estructura del árbol (altura, balance)")
    print("5. Salir")
    choice = input("Elija opción (1-5): ").strip()

    if choice == '1':
        try:
            val = int(input("Valor a insertar: "))
            avl.insert(val)
            print(f"Valor {val} insertado.")
        except ValueError:
            print("Valor inválido. Debe ser número entero.")
    elif choice == '2':
        try:
            val = int(input("Valor a eliminar: "))
            avl.delete(val)
            print(f"Valor {val} eliminado (si existía).")
        except ValueError:
            print("Valor inválido.")
    elif choice == '3':
        inorder = avl.get_inorder()
        print("Recorrido in-order:", inorder)
    elif choice == '4':
        avl.print_tree()
    elif choice == '5':
        print("¡Gracias!")
        break
    else:
        print("Opción inválida. Intente de nuevo.")
