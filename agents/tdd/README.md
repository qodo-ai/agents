# TDD Agents

## Goal

The goal of this directory is to provide specific agents that facilitate Test-Driven Development (TDD) style development. These agents create tests before the actual code, ensuring a robust and reliable development process.

## What is Test-Driven Development (TDD)?

Test-Driven Development (TDD) is a software development process where tests are written before the actual code. It follows a repetitive cycle known as **Red-Green-Refactor**:

- **Red Phase**: Write a test that defines a desired feature or behavior (the test fails initially).
- **Green Phase**: Write the minimum code necessary to pass the test.
- **Refactor**: Optimize the code while ensuring the test still passes.

TDD allows you to catch bugs early, ensure your code meets requirements, and build reliable, maintainable software. It was popularized by Kent Beck in his 2003 book *Test Driven Development: By Example*.

## Unit Testing Frameworks

TDD is supported by various unit testing frameworks across different programming languages. Some popular ones include:

- **Java**: JUnit, TestNG
- **Python**: unittest (PyUnit), pytest
- **.NET**: NUnit, xUnit.net
- **Ruby**: RSpec
- **JavaScript**: Jest, Mocha
- **Groovy**: Spock Framework
- **Go (Golang)**: testing (built-in), Testify, Ginkgo
- **Scala**: ScalaTest, Specs2

These frameworks provide tools to write, run, and manage automated tests effectively.

## Child Directories

Each child directory in this folder represents an example of a TDD agent tailored for a specific testing framework:

- **spockframework/**: An agent for TDD using the Spock Framework, which is a testing and specification framework for JVM applications. To run this example, navigate to the `spockframework` directory and execute `./run-example.sh`.
