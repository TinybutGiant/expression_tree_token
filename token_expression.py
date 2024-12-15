import lex as lex

# Define the list of token names
tokens = (
    'OPERATOR',
    'SYMBOL',
    'EQUAL',
    'NUMBER',
    'LPAREN',
    'RPAREN',
    'LEFT_L_BRACKET',
    'RIGHT_L_BRACKET',
    'LBRACKET',
    'RBRACKET',
    #'FRAC',
    #'CDOT',
    'EPSILON',
    #'POWER'
)

# Define the regular expressions for each token
t_OPERATOR = r'[-+*/]|\^'
t_SYMBOL = r'[a-zA-Z]+|\\[a-zA-Z]+'
t_EQUAL = r'='
t_NUMBER = r'\d+'
t_LPAREN = r'\('
t_LBRACKET = r'\['
t_LEFT_L_BRACKET = r'\{'
t_RPAREN = r'\)'
t_RBRACKET = r'\]'
t_RIGHT_L_BRACKET = r'\}'
#t_POWER = r'\^'

# Ignore whitespace characters
t_ignore = ' \t\n'

# Error handling for unknown characters
def t_error(t):
    print(f"Unknown character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test the lexer

expression_asci_math = "r=(t*[3*(1+m)^(2)+(1+m*n)*(m^(2)+(1)/(m*n))])/(6*(1+m)^(2) * epsilon)"
#expression_latex = "r=\frac {t \cdot [33 \cdot (1+m)^2 + (1+m \cdot n) \cdot (m^2 + \frac {1}{m \cdot n})]}{6 \cdot (1+m)^2 \cdot \epsilon}"
#expression = str('r= \frac {t \cdot A}{B}')
lexer.input(expression_asci_math)
#lexer.input(expression_latex)

# Iterate over the tokens and print each one
i = 0
symbols = set()
operators = set()
values = []
while True:
    i=i+1
    token = lexer.token()
    if not token:
        break    
    token_value = token.value   
    token_type_name = token.type
    entry = {"type": token_type_name, "value": token_value}
    values.append(entry)
    #print(f"the {i} token is: {token}")
    #print(f"the {i} token type name is: {token_type_name}") 
    #print(f"the {i} token value is: {token_value}")    
    if token_type_name == 'SYMBOL':
        symbols.add(token_value)
        #print(f'The expression has # {len(symbols)} symbols : {token_value}')
    if token_type_name == 'OPERATOR' :
        operators.add(token_value)
        #print(f'The expression has # {len(operators)} operators : {token_value}')
#print(values)   
new_operators = {'**' if item == '^' else item for item in operators}
new_expression = expression_asci_math.replace('^', '**').replace('[', '(').replace(']', ')')
print(f'The expression has {len(symbols)} symbols {symbols} and {len(operators)} operators {new_operators}.') 
print(expression_asci_math)
print(new_expression) 
def initialize_token():
    return {"symbols": symbols, "new_operators":new_operators,"new_expression":new_expression}
#output is The expression has 17 symbols and 7 operators.



