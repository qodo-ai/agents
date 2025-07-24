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


# 2. Clone the target repo
if [ ! -d "groovy-spock" ]; then
    git clone https://github.com/davidparry/groovy-spock.git
else
    cd groovy-spock && git pull origin main && cd ..
fi
# 3. Invoke the tddspock agent
qodo tddspock --set spec="Implement the OddEvenCamp interface requirements from the javadoc for this interface" -y -s
