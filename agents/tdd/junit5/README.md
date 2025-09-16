# JUnit5 TDD Example

## Introduction to JUnit5
JUnit5 is the next generation of the JUnit testing framework for Java applications. It provides a modern foundation for developer-side testing on the JVM with powerful features like parameterized tests, dynamic tests, nested test classes, and improved assertions. JUnit5 is compatible with most IDEs, build tools, and CI servers. For more details, visit the [JUnit5 Documentation](https://junit.org/junit5/docs/current/user-guide/).

## Running the Example
To run the JUnit5 TDD example, execute the `example.sh` script located in `agents/tdd/junit5/`. This script performs the following actions:
- Clones the target repository: `git clone git@github.com:davidparry/tdd-agent-junit.git`
- Invokes the `tddjunit5` agent with the specification: `qodo tddjunit5 --set spec="Implement the OddEvenCamp interface requirements from the javadoc for this interface" -y -s`

This sets up and runs the TDD process for implementing the `OddEvenCamp` interface using JUnit5.

## Agent Configuration (agent.toml)
The `agent.toml` file in `agents/tdd/junit5/` configures the `tddjunit5` agent for executing JUnit5 tests in a Java environment following TDD and BDD principles. Key instructions include:
- Identifying the project's build system (Gradle or Maven) by checking for specific files like `build.gradle` or `pom.xml`.
- Creating skeleton classes with stub methods to allow tests to compile.
- Writing comprehensive JUnit5 test classes that use annotations like `@Test`, `@ParameterizedTest`, `@DisplayName`, and `@Nested`, utilizing features like assertions, parameterized tests with `@ValueSource` or `@CsvSource`, mocks with Mockito, and exception testing with `assertThrows`.
- Ensuring tests cover basic functionality, exceptions, interactions, and adhere to SOLID principles.
- Running tests to verify failures (Red phase), with the expectation that implementation will follow to make them pass (Green phase).
- Providing templates and examples for test structure, test methods, and build configurations.

This configuration guides the agent to produce failing tests first, enforcing TDD practices.

## TDD Example Explanation
This example demonstrates Test-Driven Development (TDD) using JUnit5. In TDD, development cycles through Red-Green-Refactor phases:
- **Red**: Write failing tests.
- **Green**: Implement minimal code to pass the tests.
- **Refactor**: Improve code while keeping tests green.

Here, the agent creates a skeleton implementation and comprehensive tests for the `OddEvenCamp` interface, which checks if a number is even (return 1) or odd (return 0), throwing `NegativeNumberException` for zero or negative numbers. The tests are designed to fail initially since only stubs are present. This represents the Red phase, where 44 out of 75 tests fail as expected, covering even/odd checks, exceptions, edge cases, and design principles.

## MCP Confluence Setup

This project can be configured to work with a local MCP (Machine-readable Capability Profile) server for Atlassian Confluence. This allows the agent to interact with Confluence for tasks like creating and updating pages.

To use this functionality, you need to set up a Confluence MCP server. You can use any compatible server; for example, one option is available at [https://github.com/aashari/mcp-server-atlassian-confluence](https://github.com/aashari/mcp-server-atlassian-confluence). Follow the setup instructions provided by the MCP server you choose.

Once your server is set up and running, configure the `mcp.json` file in this project to point to it:

**Configure `mcp.json`:**
Update the `mcp.json` file with the path to your server's entry point and your Atlassian credentials.

    ```json
    {
      "mcpServers": {
        "confluence": {
          "command": "node",
          "args": ["/path/to/your/mcp-server-atlassian-confluence/dist/index.js"],
          "env": {
            "ATLASSIAN_SITE_NAME": "your-confluence-site",
            "ATLASSIAN_USER_EMAIL": "your-email@example.com",
            "ATLASSIAN_API_TOKEN": "your-api-token"
          }
        }
      }
    }
    ```

    Replace the placeholder values with your specific information.
