def generate_ast_graph(node, graph=None):

    if graph is None:
        graph = graphviz.Digraph(format='png')

    node_id = str(id(node))

    if node.value is not None:
        if isinstance(node.value, ASTNode):
            value_id = str(id(node.value))
            graph.node(value_id, label=f"{node.value.node_type}")
            graph.edge(node_id, value_id)
            generate_ast_graph(node.value, graph)
        else:
            graph.node(node_id, label=f"{node.node_type}\n{node.value}")
    else:
        graph.node(node_id, label=f"{node.node_type}")

    for child in node.children:
        if child is not None:
            child_id = str(id(child))

            if isinstance(child, ASTNode):
                graph.edge(node_id, child_id)
                generate_ast_graph(child, graph)
            else:
                graph.node(child_id, label=f"{child}")
        else:
            pass

    return graph


generate_ast_graph(result).view()