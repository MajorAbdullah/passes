# SecurePass Password Manager - EXE Distribution

## Building the Executable

### Method 1: Quick Build (Recommended)
1. Double-click `build.bat`
2. Wait for the build process to complete
3. Find your `SecurePass.exe` in the `dist` folder

### Method 2: Manual Build
1. Install requirements:
   ```
   pip install -r requirements.txt
   ```

2. Run the build script:
   ```
   python build_exe.py
   ```

3. Or use PyInstaller directly:
   ```
   pyinstaller --onefile --windowed --name=SecurePass main.py
   ```

## Distribution

### Single File Distribution
- Copy `SecurePass.exe` from the `dist` folder
- This is a standalone executable that doesn't require Python installation
- Size: ~20-30 MB (includes Python runtime and all dependencies)

### What's Included
- Complete Python runtime
- All required libraries (tkinter, cryptography, bcrypt, pyperclip)
- Your password manager application
- Database handling (creates passwords.db automatically)

## System Requirements

### For Running the EXE
- Windows 7/8/10/11 (64-bit recommended)
- ~50 MB disk space
- Visual C++ Redistributable (usually already installed)

### For Building the EXE
- Python 3.7+
- pip (Python package manager)
- Internet connection (for downloading PyInstaller)

## Security Features
- Offline operation (no internet required)
- Local database storage
- Strong encryption for passwords
- No data transmitted externally

## Installation for Users
1. Download `SecurePass.exe`
2. Place it in a folder of your choice
3. Double-click to run
4. The application will create its database file automatically

## Troubleshooting

### Build Issues
- Make sure Python is in your PATH
- Run as administrator if permission issues occur
- Check internet connection for PyInstaller download

### Runtime Issues
- Windows Defender might flag unknown executables
- Add exception in antivirus if needed
- Ensure Visual C++ Redistributable is installed

### Performance
- First startup might be slower (extracting runtime)
- Subsequent runs are faster
- Database operations are very fast

## Advanced Options

### Custom Icon
1. Add `icon.ico` file to the project directory
2. Rebuild using the build script

### Smaller Executable
- Use `--exclude-module` flags for unused modules
- Consider using virtual environment for cleaner builds

### Code Signing (Optional)
- For professional distribution
- Reduces Windows security warnings
- Requires code signing certificate

## File Structure After Build
```
YourProject/
├── dist/
│   └── SecurePass.exe        # Your standalone executable
├── build/                    # Temporary build files (can delete)
├── main.py                   # Source code
├── database.py
├── password_generator.py
├── requirements.txt
├── build_exe.py              # Build script
└── build.bat                 # Quick build batch file
```
