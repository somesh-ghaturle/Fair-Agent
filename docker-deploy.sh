#!/bin/bash

# FAIR-Agent Docker Deployment Script
# This script helps build and deploy the FAIR-Agent system using Docker

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker and try again."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose and try again."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Function to build the Docker image
build_image() {
    print_status "Building FAIR-Agent Docker image..."
    docker build -t fair-agent:latest .
    print_success "Docker image built successfully"
}

# Function to start the services
start_services() {
    print_status "Starting FAIR-Agent services..."
    docker-compose up -d
    print_success "Services started successfully"
    
    print_status "Waiting for services to be healthy..."
    sleep 10
    
    # Check if the service is running
    if docker-compose ps | grep -q "Up"; then
        print_success "FAIR-Agent is running at http://localhost:8000"
    else
        print_error "Failed to start services. Check logs with: docker-compose logs"
        exit 1
    fi
}

# Function to stop the services
stop_services() {
    print_status "Stopping FAIR-Agent services..."
    docker-compose down
    print_success "Services stopped successfully"
}

# Function to view logs
view_logs() {
    print_status "Viewing FAIR-Agent logs..."
    docker-compose logs -f
}

# Function to run CLI mode
run_cli() {
    print_status "Starting FAIR-Agent in CLI mode..."
    docker-compose --profile cli run --rm fair-agent-cli
}

# Function to clean up
cleanup() {
    print_status "Cleaning up Docker resources..."
    docker-compose down -v
    docker rmi fair-agent:latest 2>/dev/null || true
    print_success "Cleanup completed"
}

# Function to show status
show_status() {
    print_status "FAIR-Agent Docker Status:"
    echo ""
    echo "Services:"
    docker-compose ps
    echo ""
    echo "Images:"
    docker images | grep fair-agent || echo "No FAIR-Agent images found"
}

# Function to update the system
update_system() {
    print_status "Updating FAIR-Agent system..."
    docker-compose down
    build_image
    start_services
    print_success "System updated successfully"
}

# Main menu
show_help() {
    echo "FAIR-Agent Docker Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build     Build the Docker image"
    echo "  start     Start the services"
    echo "  stop      Stop the services"
    echo "  restart   Restart the services"
    echo "  logs      View service logs"
    echo "  cli       Run in CLI mode"
    echo "  status    Show service status"
    echo "  update    Update and restart services"
    echo "  cleanup   Stop services and remove images"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build     # Build the Docker image"
    echo "  $0 start     # Start the web interface"
    echo "  $0 cli       # Run in interactive CLI mode"
    echo "  $0 logs      # View real-time logs"
}

# Main script logic
case "${1:-help}" in
    "build")
        check_docker
        build_image
        ;;
    "start")
        check_docker
        build_image
        start_services
        ;;
    "stop")
        check_docker
        stop_services
        ;;
    "restart")
        check_docker
        stop_services
        build_image
        start_services
        ;;
    "logs")
        check_docker
        view_logs
        ;;
    "cli")
        check_docker
        build_image
        run_cli
        ;;
    "status")
        check_docker
        show_status
        ;;
    "update")
        check_docker
        update_system
        ;;
    "cleanup")
        check_docker
        cleanup
        ;;
    "help"|*)
        show_help
        ;;
esac