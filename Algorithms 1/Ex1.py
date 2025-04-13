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


def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0


def infix_to_postfix(expression):
    stack = Stack(100)
    postfix = []
    tokens = expression.split()

    for token in tokens:
        # print(postfix)
        # to recognize float/negative numbers
        if token.replace('.', '', 1).replace('-', '', 1).isdigit():
            postfix.append(token)
        elif token == '(':
            stack.push(token)
        elif token == ')':
            while not stack.isempty() and stack.top() != '(':
                postfix.append(stack.pop())
            stack.pop()  # Remove '('
        else:
            while not stack.isempty() and (precedence(stack.top()) >= precedence(token)):
                postfix.append(stack.pop())
            stack.push(token)

    while not stack.isempty():
        postfix.append(stack.pop())

    return ' '.join(postfix)


def evaluate_postfix(expression):
    stack = Stack(100)
    tokens = expression.split()

    for token in tokens:
        if token.replace('.', '', 1).replace('-', '', 1).isdigit():  # token is a number
            stack.push(float(token) if '.' in token else int(token))
        else:  # token is an operator
            right = stack.pop()  # right number
            left = stack.pop()  # left number
            if token == '+':
                stack.push(left + right)
            elif token == '-':
                stack.push(left - right)
            elif token == '*':
                stack.push(left * right)
            elif token == '/':
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                stack.push(left / right)
    return stack.pop()


if __name__ == '__main__':
    expressions = [
        "( 3 * 6.5 + 2 ) + ( -14 / 3 + 4 )",
        "17 * ( 2 + 3 ) + 4 + ( 8 * 5 )"
    ]

    for expr in expressions:
        postfix_expr = infix_to_postfix(expr)
        print(f"Infix: {expr}")
        print(f"Postfix: {postfix_expr}")

        result = round(evaluate_postfix(postfix_expr), 2)
        print(f"Result: {result}")
        print('---')
