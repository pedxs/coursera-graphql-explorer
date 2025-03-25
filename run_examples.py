#!/usr/bin/env python3
"""
Coursera GraphQL API Explorer - Example Runner

This script provides a menu-based interface for running the various
example scripts and exploring the Coursera GraphQL API capabilities.
"""

import os
import subprocess
import sys
import time

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the program header"""
    print("=" * 60)
    print("           COURSERA GRAPHQL API EXPLORER           ")
    print("=" * 60)
    print()

def run_command(command):
    """Run a shell command and print output"""
    print(f"\nRunning: {command}\n")
    print("-" * 60)
    
    process = subprocess.Popen(
        command, 
        shell=True, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    
    # Print output in real-time
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    
    # Check for errors
    stderr = process.stderr.read()
    if stderr:
        print("\nErrors:")
        print(stderr)
    
    print("-" * 60)
    print("\nCommand completed with return code:", process.returncode)
    
    return process.returncode

def menu():
    """Display the main menu"""
    print_header()
    print("Available Examples:")
    print()
    print("1. Reverse-engineered GraphQL query examples (example.py)")
    print("2. Actual GraphQL query structure (coursera_api_final.py)")
    print("3. Extract structured course information (coursera_api_final.py --extract)")
    print("4. Debug mode with request details (coursera_api_final.py --debug)")
    print("5. Simple test query (test_query.py)")
    print()
    print("Documentation:")
    print("7. View README.md")
    print("8. View API Analysis")
    print("9. View Project Summary")
    print()
    print("0. Exit")
    print()

def get_query_input():
    """Get search query from user"""
    default = "python"
    query = input(f"Enter search query [{default}]: ").strip()
    if not query:
        return default
    return query

def get_limit_input():
    """Get result limit from user"""
    default = "5"
    limit = input(f"Enter result limit [{default}]: ").strip()
    if not limit or not limit.isdigit():
        return default
    return limit

def view_file(filename):
    """View a file with pagination"""
    clear_screen()
    print_header()
    print(f"Viewing: {filename}\n")
    
    try:
        with open(filename, 'r') as f:
            content = f.readlines()
        
        page_size = 20
        for i in range(0, len(content), page_size):
            page = content[i:i+page_size]
            print(''.join(page))
            
            if i + page_size < len(content):
                input("\nPress Enter for next page...")
            else:
                input("\nEnd of file. Press Enter to continue...")
    
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        input("\nPress Enter to continue...")

def main():
    """Main application loop"""
    while True:
        clear_screen()
        menu()
        
        try:
            choice = input("Enter your choice (0-9): ").strip()
            
            if choice == '0':
                print("\nExiting...\n")
                sys.exit(0)
            
            elif choice == '1':
                query = get_query_input()
                limit = get_limit_input()
                run_command(f"python3 example.py --query \"{query}\" --limit {limit}")
            
            elif choice == '2':
                query = get_query_input()
                limit = get_limit_input()
                run_command(f"python3 coursera_api_final.py --query \"{query}\" --limit {limit}")
            
            elif choice == '3':
                query = get_query_input()
                run_command(f"python3 coursera_api_final.py --query \"{query}\" --extract")
            
            elif choice == '4':
                query = get_query_input()
                run_command(f"python3 coursera_api_final.py --query \"{query}\" --debug")
            
            elif choice == '5':
                run_command("python3 test_query.py")
            
            elif choice == '7':
                view_file("README.md")
            
            elif choice == '8':
                view_file("coursera_api_analysis.md")
            
            elif choice == '9':
                view_file("SUMMARY.md")
            
            else:
                print("\nInvalid choice. Please try again.")
            
            if choice not in ['7', '8', '9']:
                input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            input("\nPress Enter to continue...")
        
        except Exception as e:
            print(f"\nError: {str(e)}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...\n")
        sys.exit(0)