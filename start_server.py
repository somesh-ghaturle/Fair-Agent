#!/usr/bin/env python3
"""
FAIR-Agent Startup Script with HTTPS Prevention
"""

import os
import sys
import subprocess
import time
import socket

def check_port_available(port):
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return True
        except OSError:
            return False

def kill_process_on_port(port, *, verbose: bool = False):
    """Kill any process running on the specified port"""
    try:
        # Find PID(s) using the port
        result = subprocess.run(['lsof', '-ti', f':{port}'], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            killed_any = False
            for pid in pids:
                if pid.strip():
                    try:
                        subprocess.run(['kill', '-9', pid.strip()], check=True)
                        if verbose:
                            print(f"Killed process {pid.strip()} on port {port}")
                        killed_any = True
                    except subprocess.CalledProcessError:
                        if verbose:
                            print(f"Failed to kill process {pid.strip()}")
            
            if killed_any:
                time.sleep(2)  # Give time for the port to be released
                return True
    except Exception as e:
        if verbose:
            print(f"Error trying to kill process on port {port}: {e}")
        pass
    return False

def start_server(port: int = 8000, *, verbose: bool = False, kill_port: bool = False):
    """Start the FAIR-Agent web server with proper HTTP configuration"""

    if verbose:
        print("Starting FAIR-Agent web server...")
    
    # Check if port is available
    if not check_port_available(port):
        if not kill_port:
            print(f"Port {port} is already in use. Stop the existing process or re-run with --kill-port.")
            return False
        if verbose:
            print(f"Port {port} is in use. Attempting to free it...")
        if kill_process_on_port(port, verbose=verbose):
            if not check_port_available(port):
                print(f"Could not free port {port}. Please manually stop the process.")
                return False
        else:
            print(f"Port {port} is in use and could not be freed.")
            return False
    
    # Set environment variables to prevent HTTPS issues
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'webapp.settings'
    os.environ['PYTHONPATH'] = os.getcwd()
    
    # Start the server
    if verbose:
        print(f"Configuring server on port {port}...")
    
    try:
        # Change to the correct directory
        os.chdir('/Users/somesh/Documents/Fair-Agent')
        
        # Start the server process
        cmd = [sys.executable, 'main.py', '--mode', 'web', '--port', str(port)]
        if verbose:
            print(f"Running: {' '.join(cmd)}")
        
        if verbose:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
            )
        else:
            process = subprocess.Popen(cmd)
        
        # Wait for server to start and monitor output
        server_started = False
        start_time = time.time()
        timeout = 300  # 300 seconds timeout (5 minutes)
        
        if verbose:
            print("Waiting for server to start...")
        
        while time.time() - start_time < timeout:
            if verbose and process.stdout is not None:
                line = process.stdout.readline()
                if line:
                    # Pass through server output as-is.
                    print(line.rstrip())

                    if (
                        "Starting development server" in line
                        or "Watching for file changes" in line
                        or "Starting ASGI/Daphne" in line
                    ):
                        server_started = True
                        break
                    elif "Error" in line or "Exception" in line:
                        break
            else:
                # In quiet mode we don't stream logs; assume it's started once the process is still alive.
                server_started = True
                break
            
            # Check if process is still running
            if process.poll() is not None:
                print("❌ Server process exited unexpectedly")
                return False
            
            time.sleep(0.1)
        
        if server_started:
            print(f"Server started: http://127.0.0.1:{port}/ (use HTTP)")
            
            # Wait for the process to complete or be interrupted
            try:
                process.wait()
            except KeyboardInterrupt:
                if verbose:
                    print("Shutting down server...")
                process.terminate()
                process.wait()
                if verbose:
                    print("Server stopped.")
        else:
            print("Server failed to start within timeout period")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"Failed to start server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Start FAIR-Agent Web Server')
    parser.add_argument('--port', type=int, default=8000, 
                       help='Port to run the server on (default: 8000)')
    parser.add_argument('--verbose', action='store_true', help='Stream server output to the console')
    parser.add_argument('--kill-port', action='store_true', help='Kill any process currently using the port')
    
    args = parser.parse_args()
    
    success = start_server(args.port, verbose=args.verbose, kill_port=args.kill_port)
    sys.exit(0 if success else 1)