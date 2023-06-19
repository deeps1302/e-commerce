import sys

class Product:
    def __init__(self, pid, name, price, stock=0):
        self.pid = pid
        self.name = name
        self.price = price
        self.stock = stock

    def __lt__(self, other):
        return self.pid < other.pid
    
#to store the Product objects with their unique product id as the key
class HashTable:
    def __init__(self):
        self.table = {}

    def add(self, pid, product):
        if pid in self.table:
            self.table[pid].append(product)
        else:
            self.table[pid] = [product]

    def get(self, pid):
        return self.table.get(pid)

#used for efficient storage and retrieval of sorted products with pid
class BinarySearchTree:
    class Node:
        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None

    def compare(self,product1, product2):
        return product1.pid < product2.pid

# used to add a new Product object to the binary search tree
    def add(self, value):
        if self.root is None:
            self.root = BinarySearchTree.Node(value)
        else:
            self.add1(self.root, value)

    def add1(self, node, value):
        if self.compare(value, node.value):
            if node.left is None:
                node.left = BinarySearchTree.Node(value)
            else:
                self.add1(node.left, value)
        else:
            if node.right is None:
                node.right = BinarySearchTree.Node(value)
            else:
                self.add1(node.right, value)

# used to retrieve a Product object from the tree based on its pid value
    def get(self, value):
        return self.get1(self.root, value)

    def get1(self, node, value):
        if node is None:
            return None
        elif node.value == value:
            return node.value
        elif value < node.value:
            return self.get1(node.left, value)
        else:
            return self.get1(node.right, value)

    def inorder(self):
        if self.root is not None:
            return self.inorder1(self.root)

    def inorder1(self, node):
        result = []
        if node.left is not None:
            result += self.inorder1(node.left)
        result.append(node.value)
        if node.right is not None:
            result += self.inorder1(node.right)
        return result

#Used to implement a shopping cart as a linked list of Product objects
class LinkedList:
    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None

    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, value):
        if self.head is None:
            self.head = LinkedList.Node(value)
            self.tail = self.head
        else:
            self.tail.next = LinkedList.Node(value)
            self.tail = self.tail.next

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.value
            current = current.next


class Transaction:
    def __init__(self, products):
        self.products = products

    def total(self):
        return sum(product.price for product in self.products)

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.transactions = []
        self.email_verified = False

class ECommercePlatform:
    def __init__(self):
        self.product_table = HashTable()
        self.product_tree = BinarySearchTree()
        self.users = [User("Dharsan", "dharsan11@gmail.com","123"),
                      User("Deepthika", "deepti123@gmail.com","000")]
        self.current_user = None
        self.current_transaction = None

    def add_sample_products(self):
        products = [
            Product("pid001", "Product 1", 10.0, stock=100),
            Product("pid002", "Product 2", 20.0, stock=50),
            Product("pid003", "Product 3", 30.0, stock=75),
            Product("pid004", "Product 4", 40.0, stock=25),
            Product("pid005", "Product 5", 50.0, stock=200),
            Product("pid006", "Product 6", 60.0, stock=150),
            Product("pid007", "Product 7", 70.0, stock=100),
            Product("pid008", "Product 8", 80.0, stock=50),
            Product("pid009", "Product 9", 90.0, stock=25),
            Product("pid010", "Product 10", 100.0, stock=200)
        ]
        for product in products:
            self.product_table.add(product.pid, product)
            self.product_tree.add(product)

        while True:
            self.main_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                self.add_product()
            elif choice == "2":
                self.view_products()
            elif choice == "3":
                self.search_product_by_pid()
            elif choice == "4":
                self.add_to_cart()
            elif choice == "5":
                self.view_cart()
            elif choice == "6":
                self.checkout()
            elif choice == "7":
                if self.current_user:
                    self.logout()
                else:
                    self.login()
            elif choice == "9":
                self.exit()
            elif choice == "8":
                self.register()
            
            else:
                print("Invalid choice. Please try again.")

    def main_menu(self):
        print("************************************************************************************************")
        print("Main Menu")
        print("1. Add a product")
        print("2. View all products")
        print("3. Search for a product by product id")
        print("4. Add a product to the cart")
        print("5. View the cart")
        print("6. Checkout")
        if self.current_user:
            print("7. Logout")
        else:
            print("7. Login")
            print("8. Register")
        print("9. Exit")
        print("************************************************************************************************")


    def add_product(self):
        pid = input("Enter the pid: ")
        name = input("Enter the name: ")
        price = float(input("Enter the price: "))
        stock = int(input("Enter the stock quantity: "))
        product = Product(pid, name, price, stock=stock)
        self.product_table.add(pid, product)
        self.product_tree.add(product)
        print("Product added.")

    def view_products(self):
        print("All products:")
        for product in self.product_tree.inorder():
            print(product.name, product.price, product.stock)

    def search_product_by_pid(self):
        pid = input("Enter the pid: ")
        products = self.product_table.get(pid)
        if products:
            for product in products:
                print(product.name, product.price, product.stock)
        else:
            print("Product not found.")

    def add_to_cart(self):
        if not self.current_user:
            print("Please login first.")
            return

        pid = input("Enter the pid: ")
        products = self.product_table.get(pid)
        if not products:
            print("Product not found.")
            return

        product = None
        if len(products) == 1:
          product = products[0]
        else:
          for p in products:
            if p.stock > 0:
                product = p
                break
          if not product:
            print("Product out of stock.")
            return

        if self.current_transaction is None:
           self.current_transaction = Transaction(LinkedList())  # Use empty LinkedList to store products
        self.current_transaction.products.add(product)  # Add product to the linked list
        product.stock -= 1
        print("Product added to cart.")
    
    def view_cart(self):
        if not self.current_user:
            print("Please login first.")
            return
        if self.current_transaction is None:
            print("Cart is empty.")
            return
        print("Cart:")
        for product in self.current_transaction.products:
            print(product.name, product.price)
        print("Total:", self.current_transaction.total())

    def checkout(self):
        if not self.current_user:
            print("Please login first.")
            return
        if self.current_transaction is None:
            print("Cart is empty.")
            return
        
        self.current_user.transactions.append(self.current_transaction)
        self.current_transaction = None
        print("Checkout complete.")
        return

    def login(self):
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        for user in self.users:
            if user.email == email and user.password == password:
                self.current_user = user
                print("Login successful.")
                return
        print("Email or password incorrect.")

    def logout(self):
        self.current_user = None
        self.current_transaction = None
        print("Logout successful.")

    def register(self):
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        user = User(name, email,password)
        self.users.append(user)
        print("Registration successful.")

    def exit(self):
        print("Exiting the program.")
        sys.exit()

platform = ECommercePlatform()
platform.add_sample_products()