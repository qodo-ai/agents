# Repository Tour

## 🎯 What This Repository Does

JUnit5 TDD Example is a demonstration project that showcases Test-Driven Development (TDD) practices using JUnit5 testing framework for Java applications. It serves as both a learning resource and a target for automated TDD agent testing.

**Key responsibilities:**
- Demonstrates the Red-Green-Refactor TDD cycle with JUnit5
- Provides a complete example of interface-driven development with comprehensive test coverage
- Showcases modern JUnit5 features including parameterized tests, nested test classes, and descriptive assertions
- Serves as a target repository for the tddjunit5 agent to practice automated test generation and implementation

---

## 🏗️ Architecture Overview

### System Context
```
[TDD Agent] → [JUnit5 TDD Example] → [Gradle Build System]
                        ↓
                   [JUnit5 Test Framework]
                        ↓
                   [Test Reports & Coverage]
```

### Key Components
- **OddEvenCamp Interface** - Core business contract defining number classification behavior (even=1, odd=0)
- **OddEvenCampImpl** - Implementation class that fulfills the interface contract with proper validation
- **NegativeNumberException** - Custom runtime exception for handling invalid input (zero or negative numbers)
- **Validation Framework** - Reusable validation components for input checking and business rule enforcement
- **Comprehensive Test Suite** - JUnit5 tests covering functionality, exceptions, edge cases, and design principles

### Data Flow
1. **Input Validation** - Numbers are validated through the NegativeChecker validation framework
2. **Business Logic Processing** - Valid positive numbers are classified as even (return 1) or odd (return 0)
3. **Exception Handling** - Zero or negative numbers trigger NegativeNumberException with descriptive messages
4. **Test Verification** - JUnit5 test suite validates all scenarios including boundary conditions and performance

---

## 📁 Project Structure [Partial Directory Tree]

```
junit5/
├── tdd-agent-junit/           # Main Java project demonstrating TDD with JUnit5
│   ├── src/
│   │   ├── main/java/com/davidparry/junit/
│   │   │   ├── OddEvenCamp.java              # Core interface defining number classification contract
│   │   │   ├── OddEvenCampImpl.java          # Implementation class (skeleton for TDD)
│   │   │   ├── NegativeNumberException.java  # Custom exception for invalid inputs
│   │   │   └── validation/
│   │   │       ├── Validator.java            # Generic validation interface
│   │   │       └── NegativeChecker.java      # Specific validator for negative numbers
│   │   └── test/java/com/davidparry/junit/
│   │       ├── OddEvenCampTest.java          # Comprehensive test suite (75+ test scenarios)
│   │       └── NegativeNumberExceptionTest.java # Exception-specific tests
│   ├── build.gradle                          # Gradle build configuration with JUnit5 dependencies
│   ├── gradle.properties                     # Project metadata and version information
│   └── README.md                             # Project-specific documentation
├── agent.toml                                # TDD agent configuration for automated testing
├── README.md                                 # Main documentation explaining TDD concepts
└── run-example.sh                           # Script to execute the TDD demonstration
```

### Key Files to Know

| File | Purpose | When You'd Touch It |
|------|---------|---------------------|
| `tdd-agent-junit/src/main/java/com/davidparry/junit/OddEvenCamp.java` | Core interface definition | Modifying business requirements |
| `tdd-agent-junit/src/main/java/com/davidparry/junit/OddEvenCampImpl.java` | Implementation class | Writing actual business logic |
| `tdd-agent-junit/src/test/java/com/davidparry/junit/OddEvenCampTest.java` | Comprehensive test suite | Adding new test scenarios |
| `tdd-agent-junit/build.gradle` | Build configuration | Adding dependencies or build tasks |
| `agent.toml` | TDD agent configuration | Modifying agent behavior or instructions |

---

## 🔧 Technology Stack

### Core Technologies
- **Language:** Java 21 - Modern LTS version with latest language features for robust development
- **Testing Framework:** JUnit5 (Jupiter 5.11.4) - Next-generation testing framework with advanced features
- **Build Tool:** Gradle 8.12.1 - Modern build automation with dependency management
- **Code Coverage:** JaCoCo - Comprehensive test coverage reporting and analysis

### Key Libraries
- **Mockito 5.15.2** - Mocking framework for unit testing with dependency isolation
- **AssertJ 3.27.3** - Fluent assertion library providing readable and maintainable test assertions
- **JUnit Jupiter** - Core JUnit5 engine enabling parameterized tests, nested classes, and dynamic tests

### Development Tools
- **Gradle Wrapper** - Ensures consistent build environment across different machines
- **JaCoCo Plugin** - Generates detailed code coverage reports in XML and HTML formats
- **IntelliJ IDEA Support** - IDE integration for seamless development and testing workflow

---

## 🔄 Common Workflows

### TDD Red-Green-Refactor Cycle
1. **Red Phase** - Write failing tests that specify desired behavior before implementation exists
2. **Green Phase** - Write minimal code to make tests pass without over-engineering
3. **Refactor Phase** - Improve code structure while maintaining all tests in passing state

**Code path:** `OddEvenCampTest.java` → `OddEvenCampImpl.java` → `Gradle test execution`

### Automated Agent Testing Workflow
1. **Agent Initialization** - TDD agent analyzes the specification and project structure
2. **Test Generation** - Comprehensive JUnit5 tests are created covering all scenarios
3. **Implementation Creation** - Skeleton classes with stub methods allow tests to compile
4. **Verification** - Tests are executed to confirm they fail (Red phase validation)

**Code path:** `agent.toml` → `tddjunit5 agent` → `Test generation` → `Gradle test execution`

### Manual Development Workflow
1. **Build Project** - `./gradlew build` compiles source code and runs all tests
2. **Run Tests** - `./gradlew test` executes JUnit5 test suite with detailed reporting
3. **Coverage Analysis** - `./gradlew jacocoTestReport` generates coverage metrics
4. **Continuous Testing** - `./gradlew test --continuous` re-runs tests on file changes

**Code path:** `Gradle wrapper` → `JUnit5 platform` → `Test execution` → `Coverage reporting`

---

## 📈 Performance & Scale

### Performance Considerations
- **Test Execution Speed** - Performance tests ensure 10,000 operations complete in under 1 second
- **Memory Efficiency** - Lightweight implementation with minimal object allocation
- **Consistent Results** - Tests verify consistent behavior across multiple invocations

### Monitoring
- **Test Coverage** - JaCoCo reports track line, branch, and method coverage metrics
- **Build Performance** - Gradle build cache optimizes compilation and test execution times
- **Test Results** - Detailed HTML reports provide insights into test execution and failures

---

## 🚨 Things to Be Careful About

### 🔒 Security Considerations
- **Input Validation** - All numeric inputs are validated to prevent invalid state transitions
- **Exception Handling** - Custom exceptions provide controlled error responses without exposing internals
- **Test Isolation** - Each test method runs independently to prevent state leakage between tests

### ⚠️ Development Guidelines
- **TDD Discipline** - Always write tests before implementation to ensure proper behavior specification
- **Test Independence** - Tests must not depend on execution order or shared state
- **Exception Messages** - Provide meaningful error messages that help developers understand failures
- **Boundary Testing** - Thoroughly test edge cases including Integer.MAX_VALUE and Integer.MIN_VALUE

*Update to last commit: d3771d006da5335d3ada37eecf64de88581958a9*
*Updated at: 2025-01-27 21:47:00 UTC*