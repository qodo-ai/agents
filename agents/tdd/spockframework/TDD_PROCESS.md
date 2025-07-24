# TDD Process Documentation for OddEvenCamp Implementation

## Overview
This document describes the Test-Driven Development (TDD) process for implementing the `OddEvenCamp` interface requirements using the Spock Framework.

## Requirements Analysis
Based on the `OddEvenCamp` interface javadoc:

```java
/**
 * Create a method that checks if the integer value is an even or odd number, return 1 for even and 0 for odd.
 * If number is 0 or negative number throw a runtime exception
 *
 * @param number the number to be checked
 * @return 1 for even 0 for odd
 * @throws NegativeNumberException
 */
int check(int number);
```

### Functional Requirements:
1. **Even Numbers**: Return `1` for even positive integers
2. **Odd Numbers**: Return `0` for odd positive integers  
3. **Zero**: Throw `NegativeNumberException`
4. **Negative Numbers**: Throw `NegativeNumberException`

### Non-Functional Requirements:
- Method should be consistent (same input → same output)
- Should handle edge cases (Integer.MAX_VALUE, Integer.MIN_VALUE)
- Should follow SOLID principles
- Should be stateless

## TDD Red Phase ✅ COMPLETED

### 1. Skeleton Implementation Created
Created `OddEvenCampImpl.java` with minimal stub implementation:
```java
@Override
public int check(int number) {
    // Skeleton implementation - will be implemented after tests
    return 0;
}
```

### 2. Comprehensive Spock Tests Written
Created `OddEvenCampSpec.groovy` with 64 test scenarios covering:

#### Positive Test Cases:
- **Even Numbers**: Tests for various positive even numbers (2, 4, 6, 8, 10, 12, 100, 1000, 9998)
- **Odd Numbers**: Tests for various positive odd numbers (1, 3, 5, 7, 9, 11, 99, 999, 9999)
- **Boundary Cases**: Edge values and specific scenarios

#### Exception Handling Tests:
- **Zero Input**: Multiple tests ensuring `NegativeNumberException` is thrown for 0
- **Negative Numbers**: Comprehensive tests for various negative values (-1, -2, -5, -10, -100, -999, -1000)
- **Exception Message Validation**: Ensuring meaningful error messages

#### Behavioral Tests:
- **Consistency**: Same input always produces same output
- **State Independence**: Multiple calls don't affect each other
- **Method Contract**: Always returns 0 or 1 for valid inputs
- **Interface Compliance**: Implements `OddEvenCamp` interface correctly

#### Data-Driven Tests:
- **Comprehensive Coverage**: Using `@Unroll` for multiple test scenarios
- **Edge Cases**: Maximum/minimum integer values
- **Sequential Operations**: Testing multiple operations in sequence

#### Design Principle Tests:
- **Interface Implementation**: Verifies proper interface compliance
- **Exception Type Validation**: Ensures only `NegativeNumberException` is thrown
- **Performance Edge Cases**: Tests with extreme values

### 3. Test Execution Results
```
64 tests completed, 41 failed
```

**Expected Failures** (Red Phase):
- ✅ All even number tests fail (skeleton returns 0, expected 1)
- ✅ All exception tests fail (skeleton doesn't throw exceptions)
- ✅ Consistency tests fail (skeleton behavior doesn't match requirements)

**Passing Tests** (22 tests):
- ✅ Odd number tests pass (skeleton returns 0, which is correct for odd)
- ✅ Interface compliance tests pass
- ✅ Basic method signature tests pass

## Test Categories and Coverage

### 1. Happy Path Testing
```groovy
def "should return 1 for positive even numbers"() {
    expect: "even numbers return 1"
    oddEvenCamp.check(number) == 1
    where: "testing various positive even numbers"
    number << [2, 4, 6, 8, 10, 12, 100, 1000, 9998]
}
```

### 2. Exception Testing
```groovy
def "should throw NegativeNumberException when number is zero"() {
    given: "the number zero"
    def number = 0
    when: "checking zero"
    oddEvenCamp.check(number)
    then: "NegativeNumberException is thrown"
    def exception = thrown(NegativeNumberException)
    exception.message != null
}
```

### 3. Data-Driven Testing
```groovy
@Unroll
def "should return #expectedResult for #description number #number"() {
    expect: "correct classification for comprehensive test cases"
    oddEvenCamp.check(number) == expectedResult
    where: "comprehensive test data"
    number || expectedResult || description
    1      || 0              || "smallest odd"
    2      || 1              || "smallest even"
    // ... more test data
}
```

### 4. BDD-Style Specifications
```groovy
@Title("Odd Even Camp Number Classification")
@Narrative('''
As a developer using the OddEvenCamp service
I want to classify numbers as odd or even
So that I can determine the parity of integers with proper error handling
''')
```

## Build System Integration

### Gradle Configuration
The project uses Gradle with Spock Framework dependencies:
```groovy
dependencies {
    testImplementation "org.spockframework:spock-core:2.3-groovy-4.0"
    testImplementation "org.apache.groovy:groovy:4.0.27"
}
```

### Test Execution Commands
```bash
# Run all tests
./gradlew test

# Run specific test class
./gradlew test --tests "OddEvenCampSpec"

# Run with continuous mode
./gradlew test --continuous

# Clean and test
./gradlew clean test
```

## Next Steps (Green Phase)

The next phase will involve implementing the actual logic in `OddEvenCampImpl.java` to make all tests pass:

1. **Implement Even/Odd Logic**: Use modulo operator to determine parity
2. **Add Exception Handling**: Throw `NegativeNumberException` for zero and negative numbers
3. **Add Meaningful Error Messages**: Provide descriptive exception messages
4. **Verify All Tests Pass**: Run tests to ensure Green phase completion

## Test Quality Metrics

- **Total Tests**: 64 test scenarios
- **Coverage Areas**: 
  - Positive cases (even/odd numbers)
  - Exception handling (zero/negative)
  - Edge cases (boundary values)
  - Behavioral contracts
  - Design principles
- **Test Types**:
  - Unit tests
  - Data-driven tests
  - Exception tests
  - Behavioral tests
  - Integration tests

## Spock Framework Features Utilized

1. **Given-When-Then**: Clear test structure
2. **@Unroll**: Data-driven test execution
3. **Where Blocks**: Parameterized testing
4. **Exception Testing**: `thrown()` method
5. **@Title/@Narrative**: BDD documentation
6. **@Subject**: Test subject specification
7. **Setup/Cleanup**: Test lifecycle management

This comprehensive test suite ensures that the implementation will be robust, well-tested, and follow TDD best practices.