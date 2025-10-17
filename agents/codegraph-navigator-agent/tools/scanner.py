# tools/scanner.py

import os
import json
import sys
import re

def scan_repository(repo_path: str):
    """Scans a repository to find dependencies and other info."""
    
    clean_path = os.path.normpath(repo_path)
    repo_name = os.path.basename(clean_path)

    results = {
        "name": repo_name,
        "path": repo_path,
        "language": "unknown",
        "imports": []
    }

    # --- Language Detection ---
    if os.path.exists(os.path.join(repo_path, 'go.mod')):
        results["language"] = "Go"
    elif os.path.exists(os.path.join(repo_path, 'package.json')):
        results["language"] = "JavaScript/TypeScript"

    # --- Dependency Parsing ---
    # For Go, find gRPC client initializations (the real dependency)
    if results["language"] == "Go":
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith('.go'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', errors='ignore') as f:
                            content = f.read()
                            # This regex finds patterns like pb.NewPaymentServiceClient(conn)
                            matches = re.findall(r'pb\.New(\w+?)ServiceClient', content)
                            for match in matches:
                                # Convert "Payment" to "paymentservice"
                                # THIS IS THE CORRECTED LINE:
                                service_name = match.lower() + "service" 
                                results["imports"].append(service_name)
                    except Exception:
                        continue
    
    # For JS, read package.json
    elif results["language"] == "JavaScript/TypeScript":
        package_json_path = os.path.join(repo_path, 'package.json')
        if os.path.exists(package_json_path):
            with open(package_json_path, 'r') as f:
                data = json.load(f)
                dependencies = data.get('dependencies', {})
                results["imports"].extend(dependencies.keys())

    # Remove duplicates
    results["imports"] = sorted(list(set(results["imports"])))

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scanner.py <path_to_repository>", file=sys.stderr)
        sys.exit(1)
    repo_path = sys.argv[1]
    scan_repository(repo_path)