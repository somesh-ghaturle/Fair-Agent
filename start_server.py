#!/usr/bin/env python3
"""
FAIR-Agent Startup Script with HTTPS Prevention
"""

import os
import sys
import subprocess
import time
import socket
import requests
from urllib.parse import urljoin

def check_port_available(port):
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return True
        except OSError:
            return False

def kill_process_on_port(port):
    """Kill any process running on the specified port"""
    try:
        result = subprocess.run(['lsof', '-ti', f':{port}'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            pid = result.stdout.strip()
            subprocess.run(['kill', '-9', pid], check=True)
            print(f"✅ Killed process {pid} on port {port}")
            time.sleep(2)  # Give time for the port to be released
            return True
    except subprocess.CalledProcessError:
        pass
    return False

def start_server(port=8000):
    """Start the FAIR-Agent web server with proper HTTP configuration"""
    
    print("🚀 Starting FAIR-Agent Web Server")
    print("=" * 50)
    
    # Check if port is available
    if not check_port_available(port):
        print(f"⚠️  Port {port} is in use. Attempting to free it...")
        if kill_process_on_port(port):
            if not check_port_available(port):
                print(f"❌ Could not free port {port}. Please manually kill the process.")
                return False
        else:
            print(f"❌ Port {port} is in use and could not be freed.")
            return False
    
    # Set environment variables to prevent HTTPS issues
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'webapp.settings'
    os.environ['PYTHONPATH'] = os.getcwd()
    
    # Start the server
    print(f"🔧 Configuring server on port {port}...")
    print("📡 Setting offline mode for transformers...")
    print("🔒 Configuring HTTP-only mode...")
    
    try:
        # Change to the correct directory
        os.chdir('/Users/somesh/Documents/Fair-Agent')
        
        # Start the server process
        cmd = ['python3', 'main.py', '--mode', 'web', '--port', str(port)]
        print(f"🏃 Running: {' '.join(cmd)}")
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                 stderr=subprocess.STDOUT, 
                                 universal_newlines=True, 
                                 bufsize=1)
        
        # Wait for server to start and monitor output
        server_started = False
        start_time = time.time()
        timeout = 60  # 60 seconds timeout
        
        print("⏳ Waiting for server to start...")
        
        while time.time() - start_time < timeout:
            line = process.stdout.readline()
            if line:
                print(f"📝 {line.strip()}")
                
                if "Starting development server" in line:
                    server_started = True
                    break
                elif "Error" in line or "Exception" in line:
                    print(f"❌ Server error: {line}")
                    break
            
            # Check if process is still running
            if process.poll() is not None:
                print("❌ Server process exited unexpectedly")
                return False
            
            time.sleep(0.1)
        
        if server_started:
            print("\n" + "=" * 50)
            print("✅ FAIR-Agent Server Started Successfully!")
            print("=" * 50)
            print(f"🌐 Server URL: http://127.0.0.1:{port}/")
            print(f"📊 Datasets:   http://127.0.0.1:{port}/datasets/")
            print(f"💬 Query:      http://127.0.0.1:{port}/query/")
            print("=" * 50)
            print("⚠️  IMPORTANT: Use HTTP, NOT HTTPS!")
            print("❌ Wrong:  https://127.0.0.1:8000/")
            print("✅ Correct: http://127.0.0.1:8000/")
            print("=" * 50)
            print("🔧 To stop: Press Ctrl+C")
            print()
            
            # Wait for the process to complete or be interrupted
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Shutting down server...")
                process.terminate()
                process.wait()
                print("✅ Server stopped.")
        else:
            print("❌ Server failed to start within timeout period")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Start FAIR-Agent Web Server')
    parser.add_argument('--port', type=int, default=8000, 
                       help='Port to run the server on (default: 8000)')
    
    args = parser.parse_args()
    
    success = start_server(args.port)
    sys.exit(0 if success else 1)