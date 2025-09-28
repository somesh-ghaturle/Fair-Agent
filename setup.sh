#!/bin/bash

# FAIR-Agent System Startup Script
# CS668 Analytics Capstone - Fall 2025

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Python version
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        exit 1
    fi
    
    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_status "Python version: $python_version"
    
    if [[ "$(printf '%s\n' "3.9" "$python_version" | sort -V | head -n1)" != "3.9" ]]; then
        print_warning "Python 3.9+ recommended for best compatibility"
    fi
}

# Setup virtual environment
setup_venv() {
    if [ ! -d ".venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv .venv
    fi
    
    print_status "Activating virtual environment..."
    source .venv/bin/activate
    
    print_status "Upgrading pip..."
    pip install --upgrade pip --quiet
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    pip install -r requirements.txt --quiet
    print_status "Dependencies installed successfully"
}

# Check system resources
check_resources() {
    # Check available memory (macOS)
    if command -v vm_stat &> /dev/null; then
        free_pages=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
        page_size=$(vm_stat | grep "page size" | awk '{print $8}')
        free_mb=$((free_pages * page_size / 1024 / 1024))
        
        if [ $free_mb -lt 4000 ]; then
            print_warning "Low memory detected (${free_mb}MB free). System may run slowly."
        else
            print_status "Memory check passed (${free_mb}MB free)"
        fi
    fi
}

# Initialize database
init_database() {
    print_status "Initializing database..."
    cd webapp
    python manage.py migrate --quiet
    cd ..
    print_status "Database initialized"
}

# Main function
main() {
    echo "=========================================="
    echo "FAIR-Agent System Setup"
    echo "CS668 Analytics Capstone - Fall 2025"
    echo "=========================================="
    
    check_python
    setup_venv
    install_dependencies
    check_resources
    init_database
    
    echo "=========================================="
    print_status "Setup completed successfully!"
    echo ""
    echo "To start the system:"
    echo "  Web interface:  python main.py --mode web"
    echo "  CLI interface:  python main.py --mode cli"
    echo "  Help:           python main.py --help"
    echo ""
    echo "Web interface will be available at:"
    echo "  http://127.0.0.1:8000"
    echo "=========================================="
}

# Run main function
main "$@"