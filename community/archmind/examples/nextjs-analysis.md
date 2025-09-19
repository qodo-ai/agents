# Next.js Framework Analysis Example

## Running the Analysis

### Standard Demo
```bash
./run-demo.sh
```

### Interactive Analysis
```bash
./run-interactive.sh
```

### Custom Analysis
```bash
docker-compose run --rm archmind-interactive qodo archmind \
  --analysis-depth=expert \
  --focus-area=patterns \
  --include-diagrams=true
```

## Expected Output

The analysis will generate comprehensive documentation including:

- **architecture-overview.md** - Executive summary with key findings
- **component-analysis.md** - Detailed breakdown of Next.js packages
- **dependency-analysis.json** - Machine-readable dependency data
- **patterns-detected.md** - Design patterns and architectural styles identified
- **recommendations.md** - Actionable improvement suggestions
- **diagrams/** - SVG architectural diagrams and visualizations

## Key Insights from Next.js Analysis

### Framework Architecture
- Modular package-based design with clear separation of concerns
- Build system integration with webpack and custom optimizations
- Server-side rendering and client hydration patterns
- Plugin architecture for extensibility

### React Integration Patterns
- Custom React Server Components implementation
- Hydration strategies and streaming architecture
- Client-side navigation with prefetching
- Image and font optimization systems

### Build System Architecture
- Complex webpack configuration with multiple entry points
- Code splitting and lazy loading strategies
- Static generation and incremental static regeneration
- Edge runtime and middleware integration

### Performance Optimizations
- Bundle size optimization techniques
- Runtime performance monitoring
- Caching strategies at multiple levels
- Resource prioritization and loading

### Architectural Evolution
- Migration patterns from pages to app router
- Backwards compatibility strategies
- Feature flag implementation
- Gradual adoption pathways

## Analysis Depth Examples

### Quick Analysis (2-3 minutes)
- Package structure overview
- Technology stack identification
- Basic dependency relationships
- High-level architectural patterns

### Standard Analysis (5-10 minutes)
- Detailed package analysis
- Design pattern detection
- Build system understanding
- Component relationship mapping

### Deep Analysis (15-30 minutes)
- Complete dependency graph
- Historical evolution tracking
- Performance bottleneck identification
- Security vulnerability assessment

### Expert Analysis (30+ minutes)
- Comprehensive architectural documentation
- Refactoring recommendations
- Team collaboration insights
- Long-term maintenance guidance
