import ox

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