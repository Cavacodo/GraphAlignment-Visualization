from py2neo import Graph,Node,Relationship

graph = Graph("bolt://localhost:7687", auth=("neo4j", "neo4jpassword"))

def add_node(label, properties):
    """
    Adds a node to the Neo4j graph database.

    :param label: The label of the node.
    :param properties: A dictionary of properties for the node.
    """
    node = Node(label, **properties)
    graph.create(node)
    return node


def find_node_by_label(label):
    """
    Finds all nodes with a specific label.

    :param label: The label of the nodes to find.
    :return: A list of nodes with the specified label.
    """
    if not label:
        raise ValueError("Label cannot be empty")
    query = f"MATCH (n:{label}) RETURN n"
    result = graph.run(query)
    return [record['n'] for record in result]

def add_relationship(node1, node2, rel_type, properties=None):
    """
    Adds a relationship between two nodes.

    :param node1: The first node.
    :param node2: The second node.
    :param rel_type: The type of the relationship.
    :param properties: A dictionary of properties for the relationship.
    """
    if properties is None:
        properties = {}
    relationship = Relationship(node1, rel_type, node2, **properties)
    graph.create(relationship)
    return relationship



if __name__ == '__main__':
