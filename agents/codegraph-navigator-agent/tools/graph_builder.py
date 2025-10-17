# tools/graph_builder.py

import json
import sys
from typing import Optional # <--- IMPORT THIS

GRAPH_PATH = 'data/knowledge_graph.json'

def update_graph(scan_results_json: str):
    """Updates the knowledge graph with new scan results."""
    scan_results = json.loads(scan_results_json)
    
    with open(GRAPH_PATH, 'r+') as f:
        graph = json.load(f)
        nodes = graph.get('nodes', [])
        edges = graph.get('edges', [])
        
        # --- Node Management ---
        repo_name = scan_results['name']
        node_exists = any(node['id'] == repo_name for node in nodes)
        
        if not node_exists:
            nodes.append({
                "id": repo_name,
                "type": "service",
                "language": scan_results['language']
            })
        
        # --- Edge Management ---
        existing_edges = {(edge['source'], edge['target']) for edge in edges}
        
        for imp in scan_results.get('imports', []):
            target_node_exists = any(node['id'] == imp for node in nodes)
            if not target_node_exists:
                 nodes.append({"id": imp, "type": "library"})

            if (repo_name, imp) not in existing_edges:
                edges.append({
                    "source": repo_name,
                    "target": imp,
                    "type": "imports"
                })
        
        # Update the graph object
        graph['nodes'] = nodes
        graph['edges'] = edges
        
        # Write the updated graph back to the file
        f.seek(0)
        f.truncate()
        json.dump(graph, f, indent=2)

    print(f"Graph updated successfully with data from {repo_name}.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        with open(filepath, 'r') as f:
            scan_results_json = f.read()
    else:
        scan_results_json = sys.stdin.read()
    
    update_graph(scan_results_json)