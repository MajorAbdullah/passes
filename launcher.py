#!/usr/bin/env python3
"""
SecurePass Password Manager
A minimalistic, secure offline password manager

Usage: python main.py
"""

import sys
import os

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'cryptography',
        'bcrypt',
        'pyperclip'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def main():
    """Main entry point with dependency checking"""
    print("🔐 SecurePass Password Manager")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("\n🚀 Starting SecurePass...")
    print("=" * 40)
    
    # Import and run the main application
    try:
        from main import PasswordManagerGUI
        app = PasswordManagerGUI()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 SecurePass closed by user")
    except Exception as e:
        print(f"\n❌ Error starting SecurePass: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
