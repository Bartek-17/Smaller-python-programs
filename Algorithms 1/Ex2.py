class Stack:
    def __init__(self, max_size):
        self.stack = [0] * max_size
        self.max_size = max_size
        self.top_index = -1

    def push(self, item):
        if self.top_index >= self.max_size:
            raise OverflowError("Stack overflow")
        self.top_index += 1
        self.stack[self.top_index] = item

    def pop(self):
        if self.isempty():
            raise IndexError("Stack underflow")
        item = self.stack[self.top_index]
        self.stack[self.top_index] = 0  # Clear the top stack element
        self.top_index -= 1
        return item

    def isempty(self):
        return self.top_index == -1

    def top(self):
        if self.isempty():
            raise IndexError("Stack is empty")
        return self.stack[self.top_index]


class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.current = None

    def insert(self, data):
        new_node = Node(data)
        if not self.head:  # list currently empty
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def is_empty(self):
        return self.head is None

    def start_iteration(self):
        self.current = self.head  # Initialize the current attribute

    def get_next(self):
        if self.current is None:
            return None
        data = self.current.data  # retrieve data in current node
        self.current = self.current.next
        return data


def is_palindrome(linkedlist):
    stack = Stack(100)
    linkedlist.start_iteration()
    current_data = linkedlist.get_next()

    # Push whole linked list on the stack
    while current_data is not None:
        stack.push(current_data)
        current_data = linkedlist.get_next()

    linkedlist.start_iteration()
    current_data = linkedlist.get_next()

    # Compare the stack with the linked list
    while current_data is not None:
        if current_data != stack.pop():
            return False
        current_data = linkedlist.get_next()
    return True


if __name__ == '__main__':
    expressions = [
        "12203022",
        "3120213"
    ]

    for expr in expressions:
        linked_list = SinglyLinkedList()
        for char in expr:
            linked_list.insert(char)

        print(f"Expression: {expr}")
        if is_palindrome(linked_list):
            print("Result: Palindrome")
        else:
            print("Result: Not a palindrome")
        print('---')
