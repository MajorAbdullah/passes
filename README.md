# 🔐 SecurePass - Personal Password Manager

A minimalistic, secure, and offline password manager built with Python and Tkinter. All your passwords are encrypted and stored locally on your device - no cloud, no internet required.

## ✨ Features

### 🔐 Security
- **AES-256 encryption** for all stored passwords
- **Master password protection** with bcrypt hashing
- **Password masking** in input fields
- **Auto-lock** after inactivity (configurable)
- **Local encrypted database** (SQLite + encryption)
- **Activity logging** for security audit

### 📋 Password Management
- ➕ **Add new password entries** (service, username, password, notes)
- 👁️ **View stored passwords** with copy-to-clipboard functionality
- ✏️ **Update existing entries**
- 🗑️ **Delete password entries**
- 🔍 **Search/filter** functionality for quick access

### 🖥️ User Interface
- **Minimalist GUI** built with Tkinter
- **Responsive layout** for window resizing
- **Modern styling** with clean design
- **Context menus** for easy access to actions
- **Intuitive navigation** and user experience
- **Theme support** (light/dark modes)

### 📂 Data Management
- 💾 **Local encrypted storage** (SQLite database)
- 📤 **Export encrypted data** for backup
- 📥 **Import encrypted data** for restore
- 📋 **Activity logging** for security auditing
- **Automatic export on logout** with file overwriting

### 🧰 Additional Tools
- 🎲 **Password generator** with customizable options
- 📊 **Password strength indicator**
- 🔗 **Passphrase generator** for memorable passwords
- ⚙️ **Settings panel** for customization
- 🌙 **Real-time theme toggle** (light/dark mode support)

## 🚀 Quick Start & Installation

### Prerequisites
- Python 3.7 or higher
- Windows, macOS, or Linux

### Installation Options

1. **Clone or download** this repository to your computer

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application** (choose any method):

   **Option 1: Windows Batch File (Recommended)**
   ```
   Double-click: run.bat
   ```

   **Option 2: Python Command**
   ```bash
   python main.py
   ```

   **Option 3: Using Launcher**
   ```bash
   python launcher.py
   ```

### First Time Setup
1. **Start the application** using any of the methods above
2. **Create your master password** when prompted:
   - Choose a strong, memorable password
   - This password encrypts ALL your data
   - **IMPORTANT**: If you forget this password, your data cannot be recovered
3. **Start adding your passwords** using the "➕ Add Password" button

## 🔧 Usage Guide

### Adding Passwords
1. Click **"➕ Add Password"** in the left panel
2. Fill in the service name, username, and password
3. Optionally add notes for additional information
4. Click **"Save"** to store the encrypted entry

### Viewing & Managing Passwords
- **Double-click** any entry in the list to view full details
- **Right-click** for context menu options:
  - Copy username/password to clipboard
  - View full details
  - Edit entry
  - Delete entry
- **Search functionality**: Use the search box to filter by service names and usernames

### Password Generator
Access via **"🎲 Generate Password"** button:
- **Customizable length** (8-64 characters)
- **Character type selection** (uppercase, lowercase, numbers, symbols)
- **Passphrase generation** for memorable passwords
- **Strength indicator** to evaluate password security
- **Copy directly** to clipboard or password fields

### Backup & Restore System
**Export Data** (📤):
- Creates encrypted backup files (.spx format)
- Maintains full encryption security
- **Automatic export on logout** with file overwriting

**Import Data** (📥):
- Restores passwords from backup files
- Requires same master password for decryption
- Easy restore process

### Activity Log
Access via **"📋 Activity Log"** button:
- View all password operations
- Monitor login attempts (successful/failed)
- Security audit trail for monitoring access

## 🛡️ Security Best Practices

### Master Password Guidelines
- **Use at least 12 characters**
- Include uppercase, lowercase, numbers, and symbols
- Avoid common words or personal information
- Consider using a passphrase (generated in-app)
- **Remember it well** - recovery is impossible if forgotten

### General Usage Best Practices
- **Lock the application** when not in use
- **Create regular backups** using the export feature
- **Keep the application updated** along with your system
- **Use the built-in password generator** for new accounts
- **Use unique passwords** for each service
- **Update passwords regularly**
- **Review activity log periodically**

## 📁 File Structure & Components

```
passes/
├── main.py                 # Main GUI application
├── database.py            # Database and encryption management  
├── password_generator.py   # Password generation utilities
├── config.py              # Configuration settings
├── launcher.py            # Application launcher with checks
├── backup_utility.py      # Backup management tools
├── requirements.txt       # Python dependencies
├── run.bat                # Windows startup script
├── README.md              # Complete documentation
└── passwords.db           # Encrypted database (created on first run)
```

### Core Components
| File | Purpose |
|------|---------|
| `main.py` | Main application with GUI interface |
| `database.py` | Database operations and encryption management |
| `password_generator.py` | Password and passphrase generation utilities |
| `config.py` | Application configuration and settings |
| `launcher.py` | Application launcher with dependency checks |
| `backup_utility.py` | Command-line backup and restore tools |
| `requirements.txt` | Python package dependencies |

## 🛡️ Security Features

### Encryption
- Uses **AES-256** encryption for all password data
- Master password is hashed with **bcrypt** (100,000 iterations)
- Each encryption uses a unique salt for maximum security

### Auto-Lock
- Automatically locks after inactivity (default: 5 minutes)
- Configurable timeout in settings
- Protects against unauthorized access

### Activity Logging
- Tracks all password operations
- Logs successful/failed login attempts
- View activity history in the log panel

## 📁 File Structure

```
passes/
├── main.py                 # Main GUI application
├── database.py            # Database and encryption management
├── password_generator.py   # Password generation utilities
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── passwords.db           # Encrypted database (created on first run)
```

## ⚙️ Settings & Configuration

### Settings Panel
Access via **"⚙️ Settings"** button to configure:
- **Auto-lock timeout**: Configure inactivity timer (1-60 minutes)
- **Theme selection**: Choose light or dark mode with real-time application
- **Master password**: Change your master password securely

### Advanced Features

**Auto-lock Configuration**:
- Default: 5 minutes of inactivity
- Configurable in Settings (1-60 minutes)
- Protects against unauthorized access
- Requires master password to unlock

**Real-time Theme Support**:
- Light and dark themes available
- **Instant theme switching** without restart
- Theme preference automatically saved
- Toggle via settings panel or header button

**Search Functionality**:
- Searches service names and usernames
- Real-time filtering as you type
- Case-insensitive matching
- Quick access to specific entries

### Command Line Tools

**Backup Utility** (`backup_utility.py`):
```bash
# Create backup
python backup_utility.py create

# List available backups  
python backup_utility.py list

# Restore from backup
python backup_utility.py restore --backup-file backup_file.db
```

**Application Launcher** (`launcher.py`):
```bash
# Launch with dependency verification
python launcher.py
```

## 💡 Tips & Keyboard Shortcuts

### Keyboard Shortcuts
- **Enter**: Confirm login or save in dialogs
- **Escape**: Cancel dialogs and operations
- **Ctrl+C**: Copy selected text (when supported)
- **Double-click**: View password entry details
- **Right-click**: Access context menus

### Pro Tips
- **Test restore process** occasionally to ensure backups work
- **Create backups before major changes** or updates
- **Use unique passwords** for every service/account
- **Review activity log** regularly for security monitoring
- **Keep the application updated** for latest security improvements

## 🛡️ Advanced Security Features

### Encryption Details
- **AES-256 encryption** for all password data
- **PBKDF2 key derivation** with 100,000 iterations
- **Unique salt** for each encryption operation
- **bcrypt password hashing** for master password
- **Local storage only** - no cloud or internet dependency

### Security Monitoring
- **Activity logging** tracks all operations
- **Failed login attempt** monitoring
- **Auto-lock protection** during inactivity
- **Secure clipboard operations** with automatic clearing
- **Memory protection** for sensitive data

## 🔒 Security Notes

1. **Master Password**: Choose a strong, unique master password. If you forget it, your data cannot be recovered.

2. **Backup Regularly**: Use the export feature to create encrypted backups of your data.

3. **Keep Software Updated**: Regularly update the application and its dependencies.

4. **Secure Environment**: Run the application on a secure, malware-free computer.

## 🐛 Troubleshooting & Support

### Common Issues & Solutions

**Application Won't Start**:
1. Ensure Python 3.7+ is installed: `python --version`
2. Install dependencies: `pip install -r requirements.txt`
3. Check for error messages in the console output
4. Try running with: `python launcher.py` for dependency verification

**"Module not found" errors**:
```bash
# Install all required dependencies
pip install -r requirements.txt

# Install individual packages if needed
pip install cryptography bcrypt pyperclip
```

**Password Database Issues**:
1. Check if `passwords.db` file exists in application directory
2. Ensure you have write permissions in the folder
3. Verify master password is correct
4. Try creating a backup and starting fresh if corrupted
5. Check for sufficient disk space

**Import/Export Problems**:
1. Verify the backup file (.spx) isn't corrupted
2. Ensure you're using the same master password used for export
3. Check file permissions and paths
4. Confirm file format is correct (.spx extension)

**Clipboard Not Working**:
1. Install pyperclip: `pip install pyperclip`
2. On Linux, install xclip or xsel: `sudo apt-get install xclip`
3. Check system clipboard permissions
4. Try restarting the application

**Theme/Display Issues**:
1. Update Tkinter if using older Python version
2. Check display scaling settings
3. Try different theme in Settings panel
4. Restart application if theme doesn't apply

**Performance Issues**:
1. Check available system memory
2. Review activity log for excessive operations
3. Consider creating backup and fresh database start
4. Ensure antivirus isn't interfering with database operations

### Getting Help

If you encounter persistent issues:

1. **Check this README** for detailed documentation
2. **Run launcher verification**: `python launcher.py`
3. **Review activity log** in the application for error patterns
4. **Create a backup** before any troubleshooting
5. **Check Python and dependency versions** for compatibility
6. **Test with fresh database** by temporarily renaming `passwords.db`

### System Requirements

**Minimum Requirements**:
- Python 3.7 or higher
- 50MB available disk space
- 256MB RAM
- Modern operating system (Windows 7+, macOS 10.12+, Linux with Tk support)

**Recommended**:
- Python 3.9 or higher
- 100MB available disk space
- 512MB RAM
- Regular backup storage location

## 🔒 Security Notes & Warnings

### Critical Security Information

1. **Master Password**: 
   - Choose a strong, unique master password
   - **If forgotten, data cannot be recovered** - there's no backdoor
   - Consider writing it down and storing in a secure physical location

2. **Backup Strategy**: 
   - **Create regular encrypted backups** using the export feature
   - Test restore process to ensure backups work
   - Store backups in secure, separate locations
   - **Automatic backup on logout** helps maintain current backups

3. **Software Updates**: 
   - Keep SecurePass and its dependencies updated
   - Update your operating system regularly
   - Monitor for security patches

4. **Secure Environment**: 
   - Run only on secure, malware-free computers
   - Use up-to-date antivirus software
   - Avoid using on public or shared computers
   - Log out when leaving computer unattended

5. **Data Protection**:
   - The `passwords.db` file contains your encrypted data
   - **Never share** this file without encryption
   - Regular backups protect against file corruption
   - Consider additional file-level encryption for extra security

### Best Practices for Maximum Security

- **Use unique, strong passwords** for every account
- **Enable auto-lock** and set appropriate timeout
- **Monitor activity log** for suspicious activity  
- **Create backups before** making major changes
- **Test restore process** periodically
- **Keep master password secure** and memorable
- **Use secure physical environment** when accessing passwords

## 🤝 Contributing & Customization

This is a personal password manager project designed for individual use. You're welcome to:

- **Report bugs or issues** you encounter
- **Suggest new features** for future versions
- **Fork and customize** according to your specific needs
- **Submit improvements** to the codebase
- **Share security feedback** to improve the application

### Customization Options
- Modify themes and colors in `main.py`
- Adjust security settings in `config.py`
- Extend password generation options in `password_generator.py`
- Add custom backup formats in `backup_utility.py`

## 📄 License & Disclaimer

**License**: This project is provided as-is for personal use and educational purposes. Feel free to modify and customize according to your needs.

**Disclaimer**: This password manager is designed for personal use and educational purposes. While it implements strong encryption and security practices, use it at your own discretion and risk. The authors are not responsible for any data loss or security breaches. Always maintain backups of your important data and follow security best practices.

## 🔮 Future Enhancements

Potential features for future versions:
- **Browser integration** for automatic form filling
- **Mobile companion app** for cross-platform access
- **Biometric authentication** support
- **Secure password sharing** capabilities
- **Cloud sync options** with end-to-end encryption
- **Two-factor authentication** integration
- **Password breach monitoring**
- **Advanced audit reports**
- **Group/category management**
- **Import from other password managers**

---

**Stay secure! 🔐**

*SecurePass - Your passwords, your device, your security.*
