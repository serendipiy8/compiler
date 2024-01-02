import tkinter as tk
from tkinter import scrolledtext, filedialog
from graphviz import Digraph
import ply.lex as lex
import ply.yacc as yacc
from define import lexer
from define import tokens

class ASTNode:
    def __init__(self, node_type, children=None, value=None):
        self.node_type = node_type
        self.children = children if children is not None else []
        self.value = value

    def __str__(self, indent=0):
        result = "  " * indent + f"{self.node_type}"
        if self.value is not None:
            result += f"\n{'  ' * (indent + 1)}Value: {self.value}"
        for child in self.children:
            result += "\n" + child.__str__(indent + 1)
        return result

def p_program(p):
    '''
    program : program declaration
            | empty
    '''
    if len(p) == 3:
        p[0] = ASTNode("Program", [p[1], p[2]])
    else:
        p[0] = ASTNode("Program", [p[1]])

def p_statement(p):
    '''
    statement : declaration
              | expression_statement
    '''
    p[0] = p[1]

def p_declaration(p):
    '''
    declaration : type declaration_list SEMICOLON
                | declaration_without_type SEMICOLON
    '''
    if len(p) == 4:
        p[0] = ASTNode("Declaration", [p[1], p[2]])
    else:
        p[0] = p[1]

def p_declaration_list(p):
    '''
    declaration_list : declaration_item
                    | declaration_list COMMA declaration_item
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode("DeclarationList", [p[1], p[3]])

def p_declaration_item(p):
    '''
    declaration_item : IDENTIFIER
                    | IDENTIFIER OPEN_BRACKET CONSTANT CLOSE_BRACKET
                    | IDENTIFIER ASSIGN expression
                    | IDENTIFIER OPEN_BRACKET CONSTANT CLOSE_BRACKET ASSIGN expression
                    | IDENTIFIER ASSIGN float_constant
                    | IDENTIFIER OPEN_BRACKET CONSTANT CLOSE_BRACKET ASSIGN float_constant
    '''
    if len(p) == 2:
        p[0] = ASTNode("Identifier", value=p[1])
    elif len(p) == 5:
        p[0] = ASTNode("ArrayDeclaration", [ASTNode("Identifier", value=p[1]), ASTNode("Constant", value=p[3])])
    elif len(p) == 4:
        p[0] = ASTNode("DeclarationWithAssignment", [ASTNode("Identifier", value=p[1]), p[3]])
    elif len(p) == 7:
        p[0] = ASTNode("ArrayDeclarationWithAssignment", [ASTNode("Identifier", value=p[1]), ASTNode("Constant", value=p[5]), p[7]])
    elif len(p) == 5 and p[2] == '=':
        p[0] = ASTNode("DeclarationWithFloatAssignment", [ASTNode("Identifier", value=p[1]), p[4]])
    elif len(p) == 7 and p[4] == '=':
        p[0] = ASTNode("ArrayDeclarationWithFloatAssignment", [ASTNode("Identifier", value=p[1]), ASTNode("Constant", value=p[5]), p[7]])

def p_declaration_without_type(p):
    '''
    declaration_without_type : IDENTIFIER
                            | IDENTIFIER ASSIGN expression
                            | IDENTIFIER OPEN_BRACKET CONSTANT CLOSE_BRACKET
                            | IDENTIFIER OPEN_BRACKET CONSTANT CLOSE_BRACKET ASSIGN expression
                            | IDENTIFIER ASSIGN float_constant
                            | IDENTIFIER OPEN_BRACKET CONSTANT CLOSE_BRACKET ASSIGN float_constant
    '''
    if len(p) == 2:
        p[0] = ASTNode("Identifier", value=p[1])
    elif len(p) == 4:
        p[0] = ASTNode("ArrayDeclarationWithoutType", [ASTNode("Identifier", value=p[1]), ASTNode("Constant", value=p[3])])
    elif len(p) == 3:
        p[0] = ASTNode("DeclarationWithoutType", [ASTNode("Identifier", value=p[1]), p[2]])
    elif len(p) == 6:
        p[0] = ASTNode("ArrayDeclarationWithoutTypeWithAssignment", [ASTNode("Identifier", value=p[1]), ASTNode("Constant", value=p[4]), p[6]])
    elif len(p) == 4 and p[2] == '=':
        p[0] = ASTNode("DeclarationWithoutTypeWithFloatAssignment", [ASTNode("Identifier", value=p[1]), p[3]])
    elif len(p) == 7 and p[5] == '=':
        p[0] = ASTNode("ArrayDeclarationWithoutTypeWithFloatAssignment", [ASTNode("Identifier", value=p[1]), ASTNode("Constant", value=p[4]), p[6]])



def p_type(p):
    '''
    type : INTEGER
         | CHAR
         | FLOAT
         | DOUBLE
    '''
    p[0] = ASTNode("Type", value=p[1])

def p_expression(p):
    '''
    expression : additive_expression
               | conditional_expression
               | expression LOGICAL_OR expression
               | expression LOGICAL_AND expression
               | expression BITWISE_OR expression
               | expression BITWISE_XOR expression
               | expression BITWISE_AND expression
               | expression EQUALS expression
               | expression NOT_EQUALS expression
               | expression LESS_THAN expression
               | expression GREATER_THAN expression
               | expression LESS_EQUALS expression
               | expression GREATER_EQUALS expression
               | expression SHIFT_LEFT expression
               | expression SHIFT_RIGHT expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode("BinaryExpression", [p[1], ASTNode("Operator", value=p[2]), p[3]])

def p_expression_statement(p):
    '''
    expression_statement : expression SEMICOLON
    '''
    p[0] = p[1]

def p_assignment_expression(p):
    '''
    assignment_expression : conditional_expression
                        | unary_expression assignment_operator assignment_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode("AssignmentExpression", [p[1], ASTNode("AssignmentOperator", value=p[2]), p[3]])

def p_conditional_expression(p):
    '''
    conditional_expression : logical_or_expression
                          | logical_or_expression CONDITIONAL_OPERATOR expression COLON conditional_expression
                          | logical_or_expression CONDITIONAL_OPERATOR expression COMMA conditional_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 5:
        p[0] = ASTNode("ConditionalExpression", [p[1], ASTNode("ConditionalOperator", value=p[2]), p[3], p[5]])
    else:
        # Assuming there is a comma after the expression in the true branch
        p[0] = ASTNode("ConditionalExpression", [p[1], ASTNode("ConditionalOperator", value=p[2]), p[3], p[5]])


def p_logical_or_expression(p):
    '''
    logical_or_expression : logical_and_expression
                        | logical_or_expression LOGICAL_OR logical_and_expression
                        | conditional_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode("LogicalOrExpression", [p[1], ASTNode("LogicalOrOperator", value=p[2]), p[3]])

def p_logical_and_expression(p):
    '''
    logical_and_expression : bitwise_or_expression
                        | logical_and_expression LOGICAL_AND bitwise_or_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode("LogicalAndExpression", [p[1], ASTNode("LogicalAndOperator", value=p[2]), p[3]])

def p_bitwise_or_expression(p):
    '''
    bitwise_or_expression : bitwise_xor_expression
                        | bitwise_or_expression BITWISE_OR bitwise_xor_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode("BitwiseOrExpression", [p[1], ASTNode("BitwiseOrOperator", value=p[2]), p[3]])

def p_bitwise_xor_expression(p):
    '''
    bitwise_xor_expression : bitwise_and_expression
                        | bitwise_xor_expression BITWISE_XOR bitwise_and_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode("BitwiseXorExpression", [p[1], ASTNode("BitwiseXorOperator", value=p[2]), p[3]])

def p_bitwise_and_expression(p):
    '''
    bitwise_and_expression : equality_expression
                        | bitwise_and_expression BITWISE_AND equality_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode("BitwiseAndExpression", [p[1], ASTNode("BitwiseAndOperator", value=p[2]), p[3]])

def p_equality_expression(p):
    '''
    equality_expression : relational_expression
                     | equality_expression EQUALS relational_expression
                     | equality_expression NOT_EQUALS relational_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode("EqualityExpression", [p[1], ASTNode("EqualityOperator", value=p[2]), p[3]])

def p_relational_expression(p):
    '''
    relational_expression : shift_expression
                      | relational_expression LESS_THAN shift_expression
                      | relational_expression GREATER_THAN shift_expression
                      | relational_expression LESS_EQUALS shift_expression
                      | relational_expression GREATER_EQUALS shift_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode("RelationalExpression", [p[1], ASTNode("RelationalOperator", value=p[2]), p[3]])

def p_shift_expression(p):
    '''
    shift_expression : additive_expression
                     | shift_expression SHIFT_LEFT additive_expression
                     | shift_expression SHIFT_RIGHT additive_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode("ShiftExpression", [p[1], ASTNode("ShiftOperator", value=p[2]), p[3]])

def p_additive_expression(p):
    '''
    additive_expression : multiplicative_expression
                     | additive_expression PLUS multiplicative_expression
                     | additive_expression MINUS multiplicative_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode("AdditiveExpression", [p[1], ASTNode("AdditiveOperator", value=p[2]), p[3]])

def p_multiplicative_expression(p):
    '''
    multiplicative_expression : unary_expression
                         | multiplicative_expression MUL unary_expression
                         | multiplicative_expression DIV unary_expression
                         | multiplicative_expression MOD unary_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode("MultiplicativeExpression", [p[1], ASTNode("MultiplicativeOperator", value=p[2]), p[3]])

def p_unary_expression(p):
    '''
    unary_expression : postfix_expression
                    | BITWISE_AND unary_expression
                    | TIMES unary_expression
                    | PLUS unary_expression
                    | MINUS unary_expression
                    | LOGICAL_NOT unary_expression
                    | INCREMENT unary_expression
                    | DECREMENT unary_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = ASTNode("UnaryExpression", [ASTNode("Operator", value=p[1]), p[2]])
    else:
        p[0] = ASTNode("UnaryExpression", [ASTNode("Operator", value=p[1]), p[3]])



def p_postfix_expression(p):
    '''
    postfix_expression : primary_expression
                    | postfix_expression OPEN_PAREN CLOSE_PAREN
                    | postfix_expression OPEN_BRACKET expression CLOSE_BRACKET
                    | postfix_expression DOT IDENTIFIER
                    | postfix_expression ARROW IDENTIFIER
                    | postfix_expression INCREMENT
                    | postfix_expression DECREMENT
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ASTNode("FunctionCall", [p[1]]) if p[2] == '(' else ASTNode("ArrayAccess", [p[1], p[3]])
    elif len(p) == 5:
        p[0] = ASTNode("MemberAccess", [p[1], ASTNode("Identifier", value=p[3])])
    else:
        p[0] = ASTNode("UnaryExpression", [ASTNode("Operator", value=p[2]), p[1]])

def p_primary_expression(p):
    '''
    primary_expression : IDENTIFIER
                    | CONSTANT
                    | STRING_CONSTANT
                    | FLOAT
                    | OPEN_PAREN expression CLOSE_PAREN
    '''
    if len(p) == 2:
        p[0] = ASTNode("PrimaryExpression", value=p[1])
    else:
        p[0] = p[2]

def p_basic_expression(p):
    '''
    basic_expression : unary_expression
                    | basic_expression PLUS basic_expression
                    | basic_expression MINUS basic_expression
                    | basic_expression MUL basic_expression
                    | basic_expression DIV basic_expression
                    | basic_expression MOD basic_expression
                    | basic_expression INCREMENT
                    | basic_expression DECREMENT
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = ASTNode("UnaryExpression", [ASTNode("Operator", value=p[2]), p[1]])
    else:
        p[0] = ASTNode("BinaryExpression", [p[1], ASTNode("Operator", value=p[2]), p[3]])


def p_constant(p):
    '''
    constant : INTEGER
             | CHAR
             | float_constant
    '''
    p[0] = ASTNode("Constant", value=p[1])


def p_integer_constant(p):
    '''
    integer_constant : INTEGER
                    | FLOAT
                    | MINUS INTEGER
                    | MINUS FLOAT
    '''
    if len(p) == 2:
        p[0] = ASTNode("IntegerConstant", value=p[1])
    else:
        p[0] = ASTNode("NegativeIntegerConstant" if p[2] == '-' else "NegativeFloatConstant", [ASTNode("IntegerConstant" if p[2] == '-' else "FloatConstant", value=p[3])])

def p_float_constant(p):
    '''
    float_constant : FLOAT
                  | MINUS FLOAT
    '''
    if len(p) == 2:
        p[0] = ASTNode("FloatConstant", value=p[1])
    else:
        p[0] = ASTNode("NegativeFloatConstant", [ASTNode("FloatConstant", value=p[2])])

def p_assignment_operator(p):
    '''
    assignment_operator : '='
    '''
    p[0] = ASTNode("AssignmentOperator", value=p[1])

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print(f"Syntax error at line {p.lineno}, token {p.type}")

parser = yacc.yacc()

# input_string = """
#     int a=10, b=20, c; c=a<40? A+b,a-b;
# """
#
#
# result = parser.parse(input_string)
#
# if result:
#     print("语法分析成功！")
# else:
#     print("语法分析失败！")
#
# def print_ast(node, indent=0):
#     if node:
#         print("  " * indent + f"{node.node_type}")
#         if node.value is not None:
#             print("  " * (indent + 1) + f"Value: {node.value}")
#         for child in node.children:
#             print_ast(child, indent + 1)
#
# # 在解析完成后打印AST
# print_ast(result)