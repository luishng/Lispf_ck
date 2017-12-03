import ox
import click
from getch import getche

"""
Create tokens list and its lexer and parser
"""
lexer = ox.make_lexer([
    ('NUMBER', r'\d+'),
    ('NAME', r'[-a-zA-Z]+'),
    ('LPARAN', r'[(]'),
    ('RPARAN', r'[)]'),
    ('COMMENT', r';.*'),
    ('NEWLINE', r'\s+'),
])

tokens_list = ['NAME', 'NUMBER', 'LPARAN', 'RPARAN']

parser = ox.make_parser([
    ('stmt : LPARAN RPARAN', lambda x,y: '()'),
    ('stmt : LPARAN expr RPARAN', lambda x,y,z: y),
    ('expr : term expr', lambda x,y: [x] + y),
    ('expr : term', lambda x: [x]),
    ('term : stmt', lambda x: x),
    ('term : NUMBER', lambda x: int(x)),
    ('term : NAME', lambda x: x),
], tokens_list)

collection = [0]
p = 0

@click.command()
@click.argument('lispf_data', type=click.File('r'))
def ast(lispf_data):
    """
    Generate ast of lispf_code
    """
    collection = lispf_data.read()
    tokens = [token for token in (lexer(collection)) if token.type != 'COMMENT' and token.type != 'NEWLINE' ]
    ast = parser(tokens)
    eval(ast, p)

def eval(ast, p):
    """
    Evaluates a result from an AST of lispf_ck code
    """
    for item in ast:
        if isinstance(item, list):
            if item[0] == 'do-after':
                x = 0
                while x < len(item[2]):
                    tape = ['do', item[1], item[2][x]]
                    eval(tape, p)
                    x += 1

            elif item[0] == 'do':
                x = 1
                while i < len(item):
                    eval(item[x], p)
                    x += 1
            elif item[0] == 'loop':
                while collection[p] != 0:
                    eval(item[1:len(item)], p)
            elif item[0] == 'do-before':
                z = 0
                while z < len(item[2]):
                    tape = ['do', item[2][z], item[1]]
                    eval(tape, p)
                    z += 1
            elif item[0] == 'add':
                collection[p] = (collection[p] + int(item[1])) % 256;
            elif item[0] == 'sub':
                collection[p] = (collection[p] - int(item[1])) % 256;
        elif item == 'right':
            p += 1
            if p == len(collection):
                collection.append(0)
        elif item == 'left':
            p -= 1
        elif item == 'inc':
            collection[p] = (collection[p] + 1) % 256;
        elif item == 'dec':
            collection[p] = (collection[p] - 1) % 256;

ast()