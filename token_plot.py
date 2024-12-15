from sympy import symbols, Eq, sympify, parse_expr

import token_expression
tokens = token_expression.initialize_token()
new_operator= tokens["new_operators"]
symbol = tokens["symbols"]
expression = tokens["new_expression"]
print ("by import",symbol)
print ("by import",new_operator)
print ("by import",expression)


# Define some symbols
#r, t, m, n, epsilon = symbols('r t m n epsilon')
# Create a string that defines the symbols
symbols_str = ', '.join(symbol) + ' = symbols(\'' + ' '.join(symbol) + '\', commutative=False)'
# Execute the string as Python code
exec(symbols_str)
print("symbols_str is ",symbols_str)
# Define an expression
#expr =  Eq(r,   t * (3*(1+m)**2 + (1+m*n)*(m**2 + 1/(m*n)   ) )  / (6*(1+m)**2*epsilon)     )

# Check if the string contains an equals sign = and define
if "=" in expression:
    print("The expression string contains an equals sign =.")

    # Split the string into left and right hand side
    lhs_str, rhs_str = expression.split('=')
    print(lhs_str)  # r
    print(rhs_str)  # (t*(3*(1+m)**(2)+(1+m*n)*(m**(2)+(1)/(m*n))))/(6*(1+m)**(2) * epsilon)
    # Parse the right hand side into a sympy expression
    lhs = parse_expr(lhs_str)
    rhs = parse_expr(rhs_str)
    # Define the equation
    expr = Eq(lhs, rhs,evaluate=False,commutative=0)
    # Simplify the equation to remove some unwanted brackets, such as (2)
    expr = sympify(expr,evaluate=False)  # t*(3*(m + 1)**2 + (m**2 + 1/(m*n))*(m*n + 1))/(6*epsilon*(m + 1)**2)
    print(expr)
else:
    print("The expression string does not contain an equals sign =.")


from sympy import *
import re
s= srepr(expr)
print(type(s)) # <class 'str'>
print("srepr(expr) is:", s)  
'''
srepr(expr) is: Equality(Symbol('r'), Mul(Rational(1, 6), Pow(Symbol('epsilon'), 
Integer(-1)), Symbol('t'), Pow(Add(Symbol('m'), Integer(1)), Integer(-2)), 
Add(Mul(Integer(3), Pow(Add(Symbol('m'), Integer(1)), Integer(2))), 
Mul(Add(Pow(Symbol('m'), Integer(2)), Mul(Pow(Symbol('m'), Integer(-1)), 
Pow(Symbol('n'), Integer(-1)))), Add(Mul(Symbol('m'), Symbol('n')), Integer(1))))))
'''
parts = re.split(r"\), ", s)
for id, node  in enumerate(parts):
    print (id, "is ", node+')')
'''
0 is  Equality(Symbol('r')
1 is  Mul(Rational(1, 6)
2 is  Pow(Symbol('epsilon')
3 is  Integer(-1))
4 is  Symbol('t')
5 is  Pow(Add(Symbol('m')
6 is  Integer(1))
7 is  Integer(-2))
8 is  Add(Mul(Integer(3)
9 is  Pow(Add(Symbol('m')
10 is  Integer(1))
11 is  Integer(2)))
12 is  Mul(Add(Pow(Symbol('m')
13 is  Integer(2))
14 is  Mul(Pow(Symbol('m')
15 is  Integer(-1))
16 is  Pow(Symbol('n')
17 is  Integer(-1))))
18 is  Add(Mul(Symbol('m')
19 is  Symbol('n'))
20 is  Integer(1)))))))'''
print(type(expr.args))
print (expr.args)
for arg in expr.args:
    print(type(arg))
    print (arg)



from sympy_expression_tree import plot_graph
graph_data = plot_graph(expr)
'''
nodes = graph_data["nodes"]
links = graph_data["links"]
graph_json=graph_data["graph_json"]
node_labels = graph_data["node_labels"]
print (graph_json)
print (node_labels)

import pandas as pd
# define the CSV file we want to write to
csv_file = "graph_json.csv"
csv_file_nodes = "graph_nodes.csv"
csv_file_links = "graph_links.csv"
csv_file_node_labels = "graph_node_labels.csv"
# Convert to DataFrame
df_graph_json = pd.DataFrame(graph_json)
df_nodes = pd.DataFrame(nodes)
df_links = pd.DataFrame(links)
df_node_labels = pd.DataFrame(list(node_labels.items()), columns=['node_labels_id', 'name'])
# Save to CSV
df_graph_json.to_csv('graph_json.csv', index=False)
df_nodes.to_csv('graph_nodes.csv', index=False)
df_links.to_csv('graph_links.csv', index=False)
df_node_labels.to_csv('graph_node_labels.csv', index=False)


'''
'''
from neo4j import GraphDatabase
# Initialize the Neo4j driver
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

# Start a new Neo4j session
with driver.session() as session:
    # Traverse the SymPy expression tree
    for node in postorder_traversal(expr):
        # Create a node in the Neo4j graph for each node in the expression tree
        session.run("CREATE (:Expression {name: $name})", name=str(node))

        # If the node has arguments (i.e., it's an operation with operands), create relationships in the Neo4j graph
        for arg in node.args:
            session.run("""
                MATCH (parent:Expression {name: $parent_name})
                MATCH (child:Expression {name: $child_name})
                CREATE (parent)-[:HAS_OPERAND]->(child)
                """)



'''