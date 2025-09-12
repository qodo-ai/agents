#!/bin/bash
# 1. Check for a JDK 21 is installed and  JAVA_HOME is set
# Step 1: Verify JDK is installed and version is at least 21
echo "Step 1: Verifying JDK installation..."
echo "------------------------------------"
if command -v java &> /dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | head -n 1 | awk -F'"' '{print $2}' | awk -F'.' '{if($1 == 1) print $2; else print $1}')
    echo "Java version detected: $(java -version 2>&1 | head -n 1)"

    # Check if version is numeric and at least 21
    if [[ "$JAVA_VERSION" =~ ^[0-9]+$ ]] && [ "$JAVA_VERSION" -ge 21 ]; then
        echo ""
        echo "✅ Step 1 PASSED: JDK $JAVA_VERSION is installed (meets minimum requirement of 21)"
        JDK_EXIT_CODE=0
    else
        echo ""
        echo "❌ Step 1 FAILED: JDK version $JAVA_VERSION is below the minimum requirement of 21"
        JDK_EXIT_CODE=1
    fi
else
    echo ""
    echo "❌ Step 1 FAILED: Java is not installed or not in PATH"
    JDK_EXIT_CODE=1
fi

echo ""

# Abort if JDK check failed
if [ "$JDK_EXIT_CODE" -ne 0 ]; then
  echo "Aborting: JDK 21+ is required."
  exit 1
fi

# 2. Clone the target repo
if [ ! -d "tdd-agent-junit" ]; then
  git clone git@github.com:davidparry/tdd-agent-junit.git || { echo "Failed to clone repository"; exit 1; }
else
  (cd tdd-agent-junit && git pull --ff-only origin main) || { echo "Failed to update repository"; exit 1; }
fi
echo ""
echo "Running Agents"
# 3. Invoke the tdd agent
qodo chain "tdd -y -q --set pageid=52985865 > dev -y -q"


