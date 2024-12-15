import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt


def plot_graph(expr):
    """
    Make a graph plot of the internal representation of SymPy expression.
    """

    node_list = []
    link_list = []

    class Id:
        """A helper class for autoincrementing node numbers."""
        counter = 0

        @classmethod
        def get(cls):
            cls.counter += 1
            return cls.counter

    class Node:
        """Represents a single operation or atomic argument."""

        def __init__(self, label, expr_id):
            self.id = expr_id
            self.name = label

        def __repr__(self):
            return self.name
        
        
    def _walk(parent, expr):
        """Walk over the expression tree recursively creating nodes and links."""
        if expr.is_Atom:
            node = Node(str(expr), Id.get())
            node_list.append({"id": node.id, "name": node.name})
            link_list.append({"source": parent.id, "target": node.id})
        else:
            node = Node(str(type(expr).__name__), Id.get())
            node_list.append({"id": node.id, "name": node.name})
            link_list.append({"source": parent.id, "target": node.id})
            for arg in expr.args:
                _walk(node, arg)

    _walk(Node("Root", 0), expr)

    # Create the graph from the lists of nodes and links:    
    graph_json = {"nodes": node_list, "links": link_list}
    print("the type of graph_json in tree format is",type(graph_json))
    print(graph_json)

    node_labels = {node['id']: node['name'] for node in graph_json['nodes']}
    print(type(node_labels))
    print(node_labels)
    for n in graph_json['nodes']:
        del n['name']
    graph = json_graph.node_link_graph(graph_json, directed=True, multigraph=False)
    
    # Layout and plot the graph
    pos = graphviz_layout(graph, prog="dot")
    nx.draw(graph.to_directed(), pos, labels=node_labels, node_shape="s",  node_color="none", bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.2'))

    plt.show()

    return {"nodes": node_list, "links": link_list,"graph_json": graph_json, "node_labels":node_labels}