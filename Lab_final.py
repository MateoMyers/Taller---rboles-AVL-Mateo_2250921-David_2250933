#David Cediel - 2250933
#Mateo Amaya - 2250921
import sys

class Node:
    # Nodo del arbol con valor, hijos y altura
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

# Auxiliares
def getHeight(node):
    # Obtiene altura del nodo
    if not node:
        return 0
    return node.height

def getBalance(node):
    # Calcula factor de balance
    if not node:
        return 0
    return getHeight(node.left) - getHeight(node.right)

def updateHeight(node):
    # Actualiza altura del nodo
    if node:
        node.height = 1 + max(getHeight(node.left), getHeight(node.right))

def rotate_right(y):
    # Rotación simple derecha
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    updateHeight(y)
    updateHeight(x)
    return x

def rotate_left(x):
    # Rotación simple izquierda
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    updateHeight(x)
    updateHeight(y)
    return y

class AVLTree:
    # Árbol AVL principal
    def __init__(self):
        self.root = None

    def insert(self, value):
        # Inserta valor manteniendo balance
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        # Inserción recursiva con rebalanceo
        if not node:
            return Node(value)
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            return node  # No duplicados

        updateHeight(node)
        balance = getBalance(node)

        # Rebalanceo (4 casos)
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

    def delete(self, value):
        # Elimina valor manteniendo balance
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        # Eliminación recursiva con rebalanceo
        if not node:
            return node

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.value)

        updateHeight(node)
        balance = getBalance(node)

        # Rebalanceo (4 casos)
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

    def _min_value_node(self, node):
        # Nodo mínimo en subárbol
        current = node
        while current.left:
            current = current.left
        return current

    def get_inorder(self):
        # Retorna lista in-order (orden ascendente)
        return self._inorder_helper(self.root, [])

    def _inorder_helper(self, node, result):
        if node:
            self._inorder_helper(node.left, result)
            result.append(node.value)
            self._inorder_helper(node.right, result)
        return result

    def print_tree(self):
        # Visualiza árbol con valores, alturas y balances
        print("\nArbol:")
        if self.root:
            self._print_helper(self.root, 0)
        else:
            print("Vacío")

    def _print_helper(self, node, level):
        if node:
            self._print_helper(node.right, level + 1)
            print("   " * level + str(node.value) + f"(h:{node.height},b:{getBalance(node)})")
            self._print_helper(node.left, level + 1)


avl = AVLTree()  # Nuevo árbol

while True:
    # Menu para prueba y error de las funciones pedidas
    print("\n1. Insertar valor\n2. Eliminar nodo\n3. Forma In-order del Arbol\n4. Mostrar la estructura del Árbol\n5. Salir")
    ch = input("Opcion: ").strip()

    if ch == '1':
        v = input("Valor: ")
        try:
            avl.insert(int(v))
            print("Insertado.")
        except:
            print("Error.")
    elif ch == '2':
        v = input("Valor: ")
        try:
            avl.delete(int(v))
            print("Eliminado.")
        except:
            print("Error.")
    elif ch == '3':
        print("In-order:", avl.get_inorder())
    elif ch == '4':
        avl.print_tree()
    elif ch == '5':
        break
    else:
        print("ILa opcion ingresada no es valida")
