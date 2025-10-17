# API Tester Agent

Automated API testing agent that analyzes Swagger/OpenAPI specifications and generates comprehensive test plans and RestAssured.Net (C#) test code.

Scope: This agent targets .NET/C# exclusively. It does not generate Java code and does not use Java-based RestAssured.

## Features

- **Two Commands**: Plan and Create
  - `api_test_plan`: Analyzes API specs and creates detailed test plans
  - `api_test_create`: Generates production-ready RestAssured.Net C# test code
- **Swagger/OpenAPI Integration**: Uses Swagger MCP to fetch and parse API specifications
- **Comprehensive Test Coverage**: Generates both positive and negative test scenarios
- **RestAssured.Net**: Leverages the RestAssured.Net library for fluent API testing (C# only)
- **Multiple Test Frameworks**: Supports NUnit, xUnit, and MSTest
- **Production Ready**: Generates complete test projects with dependencies and configuration
- **Filesystem Access**: Automatically creates directories and writes all necessary files
- **Shell Integration**: Can optionally restore packages and run tests using dotnet CLI

## Prerequisites

- [Qodo Command](https://docs.qodo.ai/qodo-documentation/qodo-command) installed
- Swagger MCP server configured (for fetching API specifications)
- .NET SDK 6.0 or later (for running generated tests)
- Access to Swagger/OpenAPI specification URL

**Note**: The agent has built-in filesystem and shell access, so it can:

- Create directories and write files automatically
- Optionally run `dotnet restore`, `dotnet build`, and `dotnet test` commands

## Usage

### Command 1: Generate Test Plan

Analyzes your API and creates a comprehensive test plan document:

```bash
qodo api_test_plan --set swagger_url="https://petstore.swagger.io/v2/swagger.json"
```

With custom options:

```bash
qodo api_test_plan \
  --set swagger_url="https://api.example.com/swagger.json" \
  --set output_path="test-plan.md" \
  --set include_negative_tests=true
```

**Parameters:**

- `swagger_url` (required): URL to Swagger/OpenAPI specification
- `output_path` (optional): Path for test plan file (default: "api-test-plan.md")
- `include_negative_tests` (optional): Include negative test scenarios (default: true)
- `single_api` (optional): Specific API endpoint to test (e.g., '/pet/{petId}' or 'GET /pet/{petId}')

**Output:**
The command generates a markdown document containing:

- Complete endpoint inventory
- Positive test scenarios
- Negative test scenarios
- Test data requirements
- Test priorities
- Test dependencies

### Command 2: Generate Test Code

Creates RestAssured.Net C# test project with executable tests:

```bash
qodo api_test_create --set swagger_url="https://petstore.swagger.io/v2/swagger.json"
```

With full customization:

```bash
qodo api_test_create \
  --set swagger_url="https://api.example.com/swagger.json" \
  --set output_dir="MyApiTests" \
  --set test_framework="NUnit" \
  --set namespace="MyCompany.ApiTests" \
  --set include_negative_tests=true \
  --set base_url="https://api.staging.example.com"
```

**Example with specific endpoint:**

```bash
qodo api_test_create \
  --set swagger_url="https://effizienterest.azurewebsites.net/swagger/v1/swagger.json" \
  --set single_api="POST /servers" \
  --set output_dir="RestAssured/Tests" \
  --set include_negative_tests=true
```

**Parameters:**

All parameters must be passed using the `--set` flag format: `--set parameter_name="value"`

- `swagger_url` (required): URL to Swagger/OpenAPI specification
- `output_dir` (optional): Directory for test files (default: "ApiTests")
- `test_framework` (optional): NUnit, xUnit, or MSTest (default: "NUnit")
- `namespace` (optional): C# namespace (default: "ApiTests")
- `include_negative_tests` (optional): Generate negative tests (default: true)
- `base_url` (optional): Override API base URL from spec
- `single_api` (optional): Specific API endpoint to test (e.g., '/pet/{petId}' or 'GET /pet/{petId}')

**Output:**
The agent has **filesystem access** and will automatically:

- Create the output directory if it doesn't exist (e.g., `RestAssured/Tests`)
- Generate a complete .NET test project with .csproj file
- Write RestAssured.Net test classes organized by resource
- Create test configuration files (appsettings.json)
- Generate README with execution instructions
- Add helper utilities and fixtures as needed

All files are written directly to the specified `output_dir` location.

## Running Generated Tests

After generating tests with `api_test_create`:

```bash
cd ApiTests
dotnet restore
dotnet test
```

Run specific test class:

```bash
dotnet test --filter "FullyQualifiedName~PetApiTests"
```

Run with verbose output:

```bash
dotnet test --logger "console;verbosity=detailed"
```

## Example Workflows

### 1. Complete Testing Workflow

```bash
# Step 1: Create test plan
qodo api_test_plan --set swagger_url="https://api.example.com/swagger.json"

# Step 2: Review the generated test plan
cat api-test-plan.md

# Step 3: Generate test code
qodo api_test_create --set swagger_url="https://api.example.com/swagger.json"

# Step 4: Run the tests
cd ApiTests && dotnet test
```

### 2. CI/CD Integration

```bash
# Generate and run tests in CI pipeline
qodo api_test_create \
  --set swagger_url="${SWAGGER_URL}" \
  --set base_url="${API_BASE_URL}" \
  --set output_dir="GeneratedTests" \
  --ci

cd GeneratedTests && dotnet test --logger trx
```

### 3. Custom Test Framework

```bash
# Generate tests with xUnit
qodo api_test_create \
  --set swagger_url="https://api.example.com/swagger.json" \
  --set test_framework="xUnit" \
  --set namespace="MyApp.Integration.Tests"
```

### 4. Test Single API Endpoint

```bash
# Generate test plan for a specific endpoint only
qodo api_test_plan \
  --set swagger_url="https://petstore.swagger.io/v2/swagger.json" \
  --set single_api="/pet/{petId}"

# Generate tests for a specific endpoint and HTTP method
qodo api_test_create \
  --set swagger_url="https://petstore.swagger.io/v2/swagger.json" \
  --set single_api="GET /pet/{petId}"

# Test a specific POST endpoint with detailed coverage
qodo api_test_create \
  --set swagger_url="https://api.example.com/swagger.json" \
  --set single_api="POST /users" \
  --set include_negative_tests=true

# Real-world example: Test POST /servers endpoint
qodo api_test_create \
  --set swagger_url="https://effizienterest.azurewebsites.net/swagger/v1/swagger.json" \
  --set single_api="POST /servers" \
  --set output_dir="RestAssured/Tests" \
  --set include_negative_tests=true \
  --set test_framework="NUnit"
```

## Generated Test Structure

```
ApiTests/
├── ApiTests.csproj
├── README.md
├── appsettings.json
├── {Resource}ApiTests.cs
├── {Resource}ApiTests.cs
└── Helpers/
    └── TestConfiguration.cs
```

## Example Generated Test

```csharp
using RestAssured.Net;
using NUnit.Framework;

namespace ApiTests
{
    [TestFixture]
    public class PetApiTests
    {
        private string _baseUrl;

        [SetUp]
        public void Setup()
        {
            _baseUrl = "https://petstore.swagger.io/v2";
        }

        [Test]
        public void GetPet_ValidId_ReturnsOk()
        {
            var response = new RestAssuredClient()
                .Given()
                    .Accept("application/json")
                .When()
                    .Get($"{_baseUrl}/pet/1")
                .Then()
                    .StatusCode(200)
                    .Extract().Response();

            Assert.That(response, Is.Not.Null);
        }

        [Test]
        public void GetPet_InvalidId_ReturnsNotFound()
        {
            new RestAssuredClient()
                .Given()
                .When()
                    .Get($"{_baseUrl}/pet/999999999")
                .Then()
                    .StatusCode(404);
        }
    }
}
```

## Best Practices

1. **Review Test Plans First**: Always generate and review test plans before creating test code
2. **Use Environment Variables**: Store sensitive data (API keys, tokens) in environment variables
3. **Customize Base URL**: Override base URL for different environments (dev, staging, prod)
4. **Organize Tests**: Use test categories/traits to organize tests by feature or priority
5. **Version Control**: Commit generated tests to version control for team collaboration
6. **CI/CD Integration**: Integrate generated tests into your CI/CD pipeline

## Troubleshooting

### Error: "Unable to execute api_test_create"

**Problem**: Trying to run `api_test_create` as a standalone command.

**Solution**: This is a Qodo Command agent, not a standalone executable. Always use the `qodo` CLI:

```bash
# ❌ WRONG - This will not work
api_test_create --output_dir="RestAssured/Tests" --swaggerUrl="..."

# ✅ CORRECT - Use qodo with --set flags
qodo api_test_create \
  --set swagger_url="https://api.example.com/swagger.json" \
  --set output_dir="RestAssured/Tests"
```

**Note**: All parameters must use the `--set` flag format and use underscores (e.g., `swagger_url`, not `swaggerUrl`).

### Swagger URL Not Accessible

Ensure the Swagger URL is publicly accessible or configure authentication if required.

### MCP Server Not Found

Verify Swagger MCP server is properly configured in your Qodo Command MCP settings.

### Test Compilation Errors

Check that all required NuGet packages are restored: `dotnet restore`

### Test Failures

Verify the API base URL is correct and the API is accessible from your test environment.

## Advanced Configuration

### Custom Authentication

The agent automatically detects authentication requirements from the Swagger/OpenAPI specification and generates appropriate test code.

**Automatic Detection:**

The agent checks the Swagger spec for:

- `securitySchemes` section defining authentication types (Bearer, API Key, OAuth2, Basic Auth)
- Endpoint-level `security` requirements
- Authentication parameter locations (header, query, cookie)

**Generated Code Examples:**

Bearer Token (most common):

```csharp
using static RestAssured.Dsl;

private string _authToken;


[SetUp]
public void Setup()
{

}

[Test]
public void GetProtectedResource_WithAuth_ReturnsOk()
{
    Given()
        .Header("Authorization", $"Bearer {_authToken}")
    .When()
        .Get($"{_baseUrl}/protected")
    .Then()
        .StatusCode(200);
}

[Test]
public void GetProtectedResource_WithoutAuth_ReturnsUnauthorized()
{
    Given()
    .When()
        .Get($"{_baseUrl}/protected")
    .Then()
        .StatusCode(401);
}
```

API Key in Header:

```csharp
[Test]
public void GetResource_WithApiKey_ReturnsOk()
{
    Given()
        .Header("X-API-Key", Environment.GetEnvironmentVariable("API_KEY"))
    .When()
        .Get($"{_baseUrl}/resource")
    .Then()
        .StatusCode(200);
}
```

**Setting Authentication Tokens:**

Set environment variables before running tests:

```bash
export AUTH_TOKEN="your-bearer-token-here"
export API_KEY="your-api-key-here"
dotnet test
```

Or in appsettings.json (for non-sensitive test environments):

```json
{
  "TestSettings": {
    "BaseUrl": "https://api.example.com",
    "AuthToken": "test-token"
  }
}
```

### Test Data Management

Create test data fixtures for complex scenarios:

```csharp
public class TestData
{
    public static object CreateValidPet() => new
    {
        name = "Fluffy",
        status = "available"
    };
}
```

## Contributing

Contributions are welcome! Please ensure:

- Tests are well-documented
- Follow C# coding conventions
- Include both positive and negative test scenarios
- Test your changes with real Swagger specifications

## License

MIT License - See repository LICENSE file for details.
