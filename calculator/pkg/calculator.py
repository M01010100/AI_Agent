def calculate(expression):
    tokens = []
    current_number = ""
    
    for char in expression:
        if char.isdigit() or char == '.':
            current_number += char
        elif char in '+-*/()':
            if current_number:
                tokens.append(float(current_number))
                current_number = ""
            tokens.append(char)
        elif char.strip():  
            raise ValueError(f"Invalid character in expression: {char}")
    
    if current_number:  
        tokens.append(float(current_number))
    
    precedence = {
        '+': 1,  
        '-': 1,
        '*': 2,
        '/': 2
    }
    
    output_queue = []
    operator_stack = []
    
    for token in tokens:
        if isinstance(token, (int, float)):
            output_queue.append(token)
        elif token in precedence:
            while (operator_stack and operator_stack[-1] in precedence and
                   precedence[operator_stack[-1]] >= precedence[token]):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if operator_stack and operator_stack[-1] == '(':
                operator_stack.pop()  
            else:
                raise ValueError("Mismatched parentheses")
    
    while operator_stack:
        if operator_stack[-1] == '(' or operator_stack[-1] == ')':
            raise ValueError("Mismatched parentheses")
        output_queue.append(operator_stack.pop())
    
    stack = []
    for token in output_queue:
        if isinstance(token, (int, float)):
            stack.append(token)
        else:
            if len(stack) < 2:
                raise ValueError("Invalid expression")
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ValueError("Division by zero")
                stack.append(a / b)
    
    if len(stack) != 1:
        raise ValueError("Invalid expression")
        
    return stack[0]
