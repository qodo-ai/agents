import json
import sys

GRAPH_PATH = 'data/knowledge_graph.json'

def find_dependents(target_service, graph):
    """Finds all services that depend on the target_service."""
    dependents = []
    for edge in graph['edges']:
        if edge['target'] == target_service:
            dependents.append(edge['source'])
    return dependents

def find_dependencies(target_service, graph):
    """Finds all libraries/services that the target_service depends on."""
    dependencies = []
    for edge in graph['edges']:
        if edge['source'] == target_service:
            dependencies.append(edge['target'])
    return dependencies

def query_graph(query):
    """Processes a natural language query against the knowledge graph."""
    with open(GRAPH_PATH, 'r') as f:
        graph = json.load(f)
    
    query = query.lower()
    
    if "depend on" in query or "rely on" in query or "use" in query:
        # e.g., "Which services depend on auth-service?"
        parts = query.split()
        target = parts[-1].replace('?','')
        results = find_dependents(target, graph)
        if results:
            print(f"The following services depend on '{target}': {', '.join(results)}")
        else:
            print(f"No services were found that depend on '{target}'.")

    elif "dependencies of" in query:
        # e.g., "Show dependencies of order-service"
        parts = query.split()
        target = parts[-1].replace('?','')
        results = find_dependencies(target, graph)
        if results:
            print(f"'{target}' has the following dependencies: {', '.join(results)}")
        else:
            print(f"No dependencies found for '{target}'.")
    else:
        print("Sorry, I can only answer questions about dependencies. Try 'Which services depend on X?'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python query_engine.py \"<your_query>\"")
        sys.exit(1)
    query = sys.argv[1]
    query_graph(query)