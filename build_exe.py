#!/usr/bin/env python3
"""
Build script to create .exe file for SecurePass Password Manager
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is already installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install PyInstaller: {e}")
            return False

def create_spec_file():
    """Create a custom spec file for better control over the build"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['tkinter', 'cryptography', 'bcrypt', 'pyperclip'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SecurePass',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon='icon.ico'
)
'''
    
    with open('SecurePass.spec', 'w') as f:
        f.write(spec_content)
    print("✓ Spec file created")

def create_version_info():
    """Create version info file for the executable"""
    version_info = '''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'SecurePass'),
        StringStruct(u'FileDescription', u'SecurePass Password Manager'),
        StringStruct(u'FileVersion', u'1.0.0'),
        StringStruct(u'InternalName', u'SecurePass'),
        StringStruct(u'LegalCopyright', u'Copyright (C) 2024'),
        StringStruct(u'OriginalFilename', u'SecurePass.exe'),
        StringStruct(u'ProductName', u'SecurePass Password Manager'),
        StringStruct(u'ProductVersion', u'1.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w') as f:
        f.write(version_info)
    print("✓ Version info created")

def create_icon():
    """Create a simple icon file or use default"""
    # For now, we'll skip the icon creation
    # You can add a custom icon.ico file to the directory
    print("ⓘ Icon file not created - you can add 'icon.ico' for a custom icon")

def build_exe():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    try:
        # Clean previous builds
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        if os.path.exists('build'):
            shutil.rmtree('build')
        
        # Build with spec file if it exists, otherwise use simple command
        if os.path.exists('SecurePass.spec'):
            cmd = [sys.executable, "-m", "PyInstaller", "--clean", "SecurePass.spec"]
        else:
            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--onefile",
                "--windowed",
                "--name=SecurePass",
                "--add-data=passwords.db;." if os.path.exists('passwords.db') else "",
                "main.py"
            ]
            # Remove empty strings
            cmd = [c for c in cmd if c]
        
        subprocess.check_call(cmd)
        print("✓ Executable built successfully!")
        print(f"✓ Find your .exe file in: {os.path.abspath('dist')}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False

def main():
    """Main build process"""
    print("SecurePass Password Manager - EXE Builder")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("✗ main.py not found. Please run this script from the project directory.")
        return False
    
    # Install PyInstaller
    if not install_pyinstaller():
        return False
    
    # Create build files
    create_spec_file()
    create_version_info()
    create_icon()
    
    # Build the executable
    if build_exe():
        print("\n" + "=" * 50)
        print("🎉 Build completed successfully!")
        print("Your SecurePass.exe is ready in the 'dist' folder")
        print("\nTo distribute your app:")
        print("1. Copy the entire 'dist' folder")
        print("2. Or just copy SecurePass.exe (standalone)")
        print("3. Make sure target computers have Visual C++ Redistributable")
        return True
    else:
        print("\n✗ Build failed. Check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
