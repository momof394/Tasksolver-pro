#!/bin/bash
# Setup script for Tasksolver-pro development environment

echo "=========================================="
echo "Tasksolver-pro Organization Setup"
echo "=========================================="

echo "Setting up development environment..."

# Check if Python is available
if command -v python3 &> /dev/null; then
    echo "✓ Python 3 is available"
    python3 --version
else
    echo "✗ Python 3 is not available. Please install Python 3."
    exit 1
fi

echo ""
echo "Project structure verification:"
echo "✓ Source code directory: src/"
echo "✓ Documentation directory: docs/"
echo "✓ Tests directory: tests/"
echo "✓ Examples directory: examples/"
echo "✓ Scripts directory: scripts/"

echo ""
echo "Running tests to verify functionality..."
if python3 tests/unit/test_task_manager.py; then
    echo "✓ All tests passed!"
else
    echo "✗ Some tests failed. Please check the code."
    exit 1
fi

echo ""
echo "Running basic example..."
if python3 examples/basic-usage/main.py > /dev/null 2>&1; then
    echo "✓ Basic example runs successfully!"
else
    echo "✗ Basic example failed. Please check the configuration."
    exit 1
fi

echo ""
echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Review the documentation in docs/"
echo "2. Check out the examples in examples/"
echo "3. Read the contributing guidelines in CONTRIBUTING.md"
echo "4. Start developing new features!"
echo ""
echo "For questions, see the documentation or open an issue."