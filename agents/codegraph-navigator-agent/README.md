# Qodo Agent: CodeGraph Navigator

🧭 **Microservice Dependency Intelligence Agent - Best agent for Complex Codebase**

Navigate complex microservice architectures with intelligent dependency analysis, criticality assessment, and impact prediction. This agent builds comprehensive knowledge graphs to help developers understand service relationships and make informed changes safely.

---

## Features

- **🔍 Multi-Language Repository Scanning**: Supports Go, JavaScript/TypeScript, Python, Java, and C#
- **🕸️ Knowledge Graph Construction**: Builds comprehensive dependency maps across multiple repositories
- **⚡ Criticality Assessment**: Calculates risk levels based on dependent services
- **🎯 Impact Analysis**: Predicts the impact of changes before implementation
- **🧠 Natural Language Querying**: Answer complex architectural questions in plain English
- **📊 Visual Risk Matrix**: Clear criticality levels with actionable recommendations
- **📈 Comprehensive Reporting**: Detailed analysis reports with deployment strategies
- **🔄 Incremental Learning**: Continuously updates knowledge as repositories evolve

---

## Quick Start

```bash
# Analyze a single microservice
qodo run analyze_codebase --repository_path="./microservices-demo/src/paymentservice"

# Perform impact analysis before making changes
qodo run impact_analysis --service_name="cartservice" --include_deployment_plan=true

# Generate complete criticality matrix
qodo run criticality_matrix --group_by_language=true --show_statistics=true
```

---

## Core Commands

The agent is defined by the `agent.toml` file and exposes several powerful commands.

### 1. analyze_codebase

This is the primary command for performing a comprehensive analysis.

**Analyze a single service and assess its impact:**
```bash
qodo run analyze_codebase --service_name="paymentservice"
```

**Analyze multiple repositories at once:**
```bash
qodo run analyze_codebase --repository_paths='["./microservices-demo/src/paymentservice", "./microservices-demo/src/checkoutservice"]'
```

**Ask a direct question about dependencies:**
```bash
qodo run analyze_codebase --query="Which services depend on productcatalogservice?"
```

### 2. impact_analysis

Perform a deep-dive impact analysis for a specific service.

```bash
qodo run impact_analysis --service_name="cartservice" --include_deployment_plan=true
```

### 3. criticality_matrix

Generate a report showing the criticality score for every service in the knowledge graph.

```bash
qodo run criticality_matrix --group_by_language=true
```

---

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `repository_path` | string | ❌ | `.` | Path to the repository or service to analyze |
| `service_name` | string | ❌ | - | Specific service name for targeted analysis |
| `analysis_type` | string | ❌ | `analyze_codebase` | Type of analysis: `analyze_codebase`, `impact_analysis`, `criticality_matrix` |
| `include_deployment_plan` | boolean | ❌ | `false` | Include deployment strategy in impact analysis |
| `include_testing_strategy` | boolean | ❌ | `false` | Include testing recommendations |
| `group_by_language` | boolean | ❌ | `false` | Group services by programming language |
| `group_by_risk` | boolean | ❌ | `false` | Group services by risk level |
| `show_statistics` | boolean | ❌ | `true` | Show overall statistics in reports |
| `sort_by` | string | ❌ | `dependents` | Sort order: `dependents`, `alphabetical`, `language` |
| `include_visualization` | boolean | ❌ | `false` | Generate ASCII art dependency trees |

---

## Criticality Scale

The agent uses a comprehensive 4-level criticality scale to assess change risk:

### 🟢 LOW RISK (0-1 dependents) - ✅ SAFE TO CHANGE
- **Risk**: Minimal impact
- **Recommendation**: Changes are isolated and safe
- **Action**: Proceed with standard testing

### 🟡 MEDIUM RISK (2-3 dependents) - ⚠️ CAUTION ADVISED  
- **Risk**: Moderate impact on downstream services
- **Recommendation**: Test affected services thoroughly
- **Action**: Coordinate with dependent service teams

### 🟠 HIGH RISK (4-6 dependents) - ⛔ NOT RECOMMENDED
- **Risk**: High impact across multiple services
- **Recommendation**: Extensive coordination required
- **Action**: Architecture review and phased rollout

### 🔴 CRITICAL (7+ dependents) - 🚫 DO NOT CHANGE
- **Risk**: Severe impact on entire system
- **Recommendation**: Requires migration plan
- **Action**: Full architecture review and gradual migration

---

## Usage Examples

### 1. Learn About a Service

```bash
# Analyze payment service and build knowledge graph
qodo run analyze_codebase --repository_path="./microservices-demo/src/paymentservice"
```

**Expected Output:**
```
✓ Successfully analyzed paymentservice
📊 Language: Go | Dependencies: 12 | Criticality: 🟡 MEDIUM
📄 Report: data/reports/analysis_report_20251017_143052.txt

🔍 DISCOVERED DEPENDENCIES:
├── checkoutservice → paymentservice (gRPC)
├── frontend → paymentservice (HTTP)
└── cartservice → paymentservice (gRPC)

⚠️ IMPACT ASSESSMENT: 3 services depend on this service
```

### 2. Impact Analysis Before Changes

```bash
# Check if it's safe to modify the cart service
qodo run impact_analysis --service_name="cartservice" --include_deployment_plan=true
```

**Expected Output:**
```
📊 IMPACT ANALYSIS FOR: cartservice

🟡 CRITICALITY LEVEL: MEDIUM
⚠️ RECOMMENDATION: CAUTION ADVISED

Direct Dependents (2):
├── checkoutservice
└── frontend

Risk Assessment:
- Changes will affect checkout flow
- Frontend cart functionality may be impacted

🚀 DEPLOYMENT STRATEGY:
1. Pre-deployment: Verify checkout and frontend test suites
2. Deployment Order: cartservice → checkoutservice → frontend
3. Post-deployment: Monitor cart operations and checkout success rate
4. Rollback: Automated rollback on >5% error rate increase
```

### 3. Complete Architecture Analysis

```bash
# Generate comprehensive criticality matrix
qodo run criticality_matrix --group_by_language=true --show_statistics=true
```

**Expected Output:**
```
📊 CRITICALITY MATRIX FOR ALL SERVICES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 OVERALL STATISTICS:
- Total Services: 10
- Total Dependencies: 45
- Average Criticality: MEDIUM
- Most Critical Service: frontend (6 dependents)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 CRITICAL SERVICES (7+ dependents) - DO NOT CHANGE:
None - No critically over-depended services

🟠 HIGH RISK SERVICES (4-6 dependents) - NOT RECOMMENDED:
- frontend (TypeScript): affects 6 services

🟡 MEDIUM RISK SERVICES (2-3 dependents) - CAUTION ADVISED:
- cartservice (Go): affects checkoutservice, frontend
- paymentservice (Go): affects checkoutservice, frontend

🟢 LOW RISK SERVICES (0-1 dependents) - SAFE TO CHANGE:
- adservice (Java): affects frontend
- currencyservice (Node.js): affects frontend
- recommendationservice (Python): affects frontend
```

---

## Analysis Types

### 1. Codebase Analysis (`analyze_codebase`)
- Scans repository structure and dependencies
- Updates knowledge graph with new findings
- Calculates criticality for the analyzed service
- Generates comprehensive analysis report

### 2. Impact Analysis (`impact_analysis`)
- Focuses on a specific service's impact
- Lists all dependent services
- Provides change recommendations
- Optional deployment and testing strategies

### 3. Criticality Matrix (`criticality_matrix`)
- Shows risk levels for all known services
- Groups services by criticality level
- Optional grouping by language or risk
- Provides architectural insights

---

## Supported Languages & Frameworks

| Language | Framework/Type | Dependency Detection |
|----------|----------------|---------------------|
| **Go** | gRPC Services | Extracts client dependencies from `.go` files |
| **JavaScript/TypeScript** | Node.js, React, Express | Reads `package.json` dependencies |
| **Python** | Django, Flask, FastAPI | Analyzes `requirements.txt`, `setup.py`, `pyproject.toml` |
| **Java** | Spring Boot, Maven, Gradle | Parses `pom.xml`, `build.gradle` |
| **C#** | .NET Core, ASP.NET | Reads `.csproj`, `packages.config` |

---

## Output Schema

### Analysis Report Structure
```json
{
  "success": true,
  "analysis_type": "analyze_codebase",
  "timestamp": "2025-10-17T14:30:52Z",
  "service_analyzed": {
    "name": "paymentservice",
    "path": "./microservices-demo/src/paymentservice",
    "language": "Go",
    "dependency_count": 12
  },
  "criticality": {
    "level": "MEDIUM",
    "dependent_count": 3,
    "dependents": ["checkoutservice", "frontend", "cartservice"]
  },
  "knowledge_graph_stats": {
    "total_nodes": 25,
    "total_edges": 45,
    "services": 10,
    "libraries": 15
  },
  "report_path": "data/reports/analysis_report_20251017_143052.txt",
  "recommendations": [
    "Service has moderate impact - coordinate with dependent teams",
    "Consider implementing feature flags for breaking changes",
    "Monitor checkout and cart functionality during deployments"
  ]
}
```

### Impact Analysis Output
```json
{
  "success": true,
  "analysis_type": "impact_analysis",
  "service": "cartservice",
  "criticality": {
    "level": "MEDIUM",
    "risk_score": 65,
    "dependent_count": 2
  },
  "impact_assessment": {
    "direct_dependents": ["checkoutservice", "frontend"],
    "transitive_impact": 4,
    "affected_workflows": ["checkout", "cart_management"]
  },
  "recommendations": {
    "change_safety": "CAUTION_ADVISED",
    "testing_requirements": ["integration_tests", "e2e_tests"],
    "deployment_strategy": "phased_rollout"
  }
}
```

---

## Prerequisites

### System Requirements
- Python 3.8+ (for analysis tools)
- Node.js 18+ (for Qodo CLI)
- Git (for repository access)

### Installation

The agent includes built-in analysis tools that are automatically configured:

```bash
# Install Qodo CLI
npm install -g @qodo/command

# The agent automatically sets up:
# - Python analysis tools (scanner.py, graph_builder.py, query_engine.py)
# - Knowledge graph storage (data/knowledge_graph.json)
# - Report generation (data/reports/)
```

---

## Advanced Usage

### Multi-Repository Analysis

```bash
# Analyze multiple services in sequence
for service in paymentservice cartservice checkoutservice; do
  qodo run analyze_codebase --repository_path="./microservices-demo/src/$service"
done

# Generate final criticality matrix
qodo run criticality_matrix --group_by_language=true
```

### Natural Language Queries

The agent supports natural language queries through the query engine:

```bash
# Ask architectural questions
qodo run analyze_codebase --query="Which services depend on the payment service?"

qodo run analyze_codebase --query="What happens if I change the cart service?"

qodo run analyze_codebase --query="Show me all Go services with high criticality"
```


---

## File Structure

The agent creates and maintains the following file structure:

```
data/
├── reports
     |--knowledge_graph.json          # Central dependency graph
├── reports/                      # Analysis reports
│   ├── analysis_report_*.txt     # Service analysis reports
│   ├── impact_*.txt              # Impact analysis reports
│   └── criticality_matrix_*.txt  # Criticality matrices
└── tools/                        # Analysis utilities
    ├── scanner.py                # Repository scanner
    ├── graph_builder.py          # Knowledge graph builder
    └── query_engine.py           # Natural language query processor
```

---


## Examples

### Real-World Microservices Demo

```bash
# Clone Google's microservices demo
git clone https://github.com/GoogleCloudPlatform/microservices-demo.git
cd microservices-demo

# Analyze all services
for service in src/*/; do
  echo "Analyzing: $service"
  qodo run analyze_codebase --repository_path="$repo-path-to-analyzed"
done

# Generate comprehensive report
qodo run criticality_matrix --group_by_language=true --include_visualization=true
```


---

## Architecture Insights

The CodeGraph Navigator provides valuable architectural insights:

### Dependency Patterns
- **Hub Services**: Services with many dependents (high criticality)
- **Leaf Services**: Services with few/no dependents (low risk)
- **Circular Dependencies**: Potential architectural issues
- **Language Boundaries**: Cross-language communication patterns

### Risk Assessment
- **Change Impact**: Predict affected services before changes
- **Deployment Ordering**: Optimize deployment sequences
- **Testing Strategy**: Focus testing on high-impact areas
- **Rollback Planning**: Prepare contingency plans

### Team Coordination
- **Ownership Mapping**: Identify service owners for coordination
- **Communication Paths**: Understand team dependencies
- **Change Management**: Plan cross-team changes effectively

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-language-support`)
3. Make your changes
4. Test with the provided examples
5. Submit a pull request

### Adding New Language Support

To add support for a new programming language:

1. Update `tools/scanner.py` with language detection logic
2. Add dependency extraction patterns
3. Test with sample repositories
4. Update documentation and examples

---

## Tools

- `filesystem`: For reading repository structures and managing knowledge graphs
- `shell`: For executing analysis tools and git operations

---

## License

See top-level LICENSE.

---

## Support

- 📚 [Qodo Documentation](https://docs.qodo.ai/)
- 💬 [Discord Community](https://discord.gg/qodo)
- 🐛 [Report Issues](https://github.com/qodo-ai/agents/issues)


---
