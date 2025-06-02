import sqlite3
import json
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import bcrypt
from datetime import datetime

class SecurityManager:
    def __init__(self, db_path="passwords.db"):
        self.db_path = db_path
        self.key = None
        self.fernet = None
        
    def generate_salt(self):
        """Generate a random salt for password hashing"""
        return os.urandom(32)
    
    def derive_key_from_password(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key from master password"""
        password_bytes = password.encode('utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        return key
    
    def hash_master_password(self, password: str) -> tuple:
        """Hash master password with bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed, salt
    
    def verify_master_password(self, password: str, hashed: bytes) -> bool:
        """Verify master password"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    
    def setup_encryption(self, master_password: str, salt: bytes):
        """Setup encryption with master password"""
        self.key = self.derive_key_from_password(master_password, salt)
        self.fernet = Fernet(self.key)
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt string data"""
        if not self.fernet:
            raise ValueError("Encryption not initialized")
        encrypted = self.fernet.encrypt(data.encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted).decode('utf-8')
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        if not self.fernet:
            raise ValueError("Encryption not initialized")
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
        decrypted = self.fernet.decrypt(encrypted_bytes)
        return decrypted.decode('utf-8')

class DatabaseManager:
    def __init__(self, db_path="passwords.db", security_manager=None):
        self.db_path = db_path
        self.security = security_manager
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Master password table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS master_auth (
                id INTEGER PRIMARY KEY,
                password_hash BLOB,
                salt BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Passwords table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        # Activity log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                details TEXT
            )
        ''')
        
        self.conn.commit()
    
    def set_master_password(self, password: str):
        """Set initial master password"""
        hashed, salt = self.security.hash_master_password(password)
        encryption_salt = self.security.generate_salt()
        
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM master_auth')  # Remove any existing
        cursor.execute(
            'INSERT INTO master_auth (password_hash, salt) VALUES (?, ?)',
            (hashed, encryption_salt)
        )
        self.conn.commit()
        
        # Setup encryption
        self.security.setup_encryption(password, encryption_salt)
        self.log_activity("Master password set", "Initial setup")
    
    def verify_master_password(self, password: str) -> bool:
        """Verify master password and setup encryption"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT password_hash, salt FROM master_auth LIMIT 1')
        result = cursor.fetchone()
        
        if not result:
            return False
        
        hashed, salt = result
        if self.security.verify_master_password(password, hashed):
            self.security.setup_encryption(password, salt)
            self.log_activity("Successful login", "Master password verified")
            return True
        else:
            self.log_activity("Failed login attempt", "Invalid master password")
            return False
    
    def has_master_password(self) -> bool:
        """Check if master password is set"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM master_auth')
        return cursor.fetchone()[0] > 0
    
    def add_password(self, service: str, username: str, password: str, notes: str = ""):
        """Add new password entry"""
        encrypted_service = self.security.encrypt_data(service)
        encrypted_username = self.security.encrypt_data(username)
        encrypted_password = self.security.encrypt_data(password)
        encrypted_notes = self.security.encrypt_data(notes)
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO passwords (service, username, password, notes)
            VALUES (?, ?, ?, ?)
        ''', (encrypted_service, encrypted_username, encrypted_password, encrypted_notes))
        
        self.conn.commit()
        self.log_activity("Password added", f"Service: {service}")
        return cursor.lastrowid
    
    def get_all_passwords(self):
        """Get all password entries"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, service, username, password, notes, created_at, updated_at FROM passwords')
        results = cursor.fetchall()
        
        decrypted_results = []
        for row in results:
            id_, service, username, password, notes, created_at, updated_at = row
            decrypted_results.append({
                'id': id_,
                'service': self.security.decrypt_data(service),
                'username': self.security.decrypt_data(username),
                'password': self.security.decrypt_data(password),
                'notes': self.security.decrypt_data(notes),
                'created_at': created_at,
                'updated_at': updated_at
            })
        
        return decrypted_results
    
    def search_passwords(self, query: str):
        """Search passwords by service or username"""
        all_passwords = self.get_all_passwords()
        query_lower = query.lower()
        
        filtered = []
        for entry in all_passwords:
            if (query_lower in entry['service'].lower() or 
                query_lower in entry['username'].lower()):
                filtered.append(entry)
        
        return filtered
    
    def update_password(self, id_: int, service: str, username: str, password: str, notes: str = ""):
        """Update existing password entry"""
        encrypted_service = self.security.encrypt_data(service)
        encrypted_username = self.security.encrypt_data(username)
        encrypted_password = self.security.encrypt_data(password)
        encrypted_notes = self.security.encrypt_data(notes)
        
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE passwords 
            SET service=?, username=?, password=?, notes=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        ''', (encrypted_service, encrypted_username, encrypted_password, encrypted_notes, id_))
        
        self.conn.commit()
        self.log_activity("Password updated", f"ID: {id_}, Service: {service}")
        return cursor.rowcount > 0
    
    def delete_password(self, id_: int):
        """Delete password entry"""
        # Get service name for logging before deletion
        cursor = self.conn.cursor()
        cursor.execute('SELECT service FROM passwords WHERE id=?', (id_,))
        result = cursor.fetchone()
        
        if result:
            service = self.security.decrypt_data(result[0])
            cursor.execute('DELETE FROM passwords WHERE id=?', (id_,))
            self.conn.commit()
            self.log_activity("Password deleted", f"ID: {id_}, Service: {service}")
            return True
        return False
    
    def log_activity(self, action: str, details: str = ""):
        """Log activity to database"""
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO activity_log (action, details) VALUES (?, ?)',
            (action, details)
        )
        self.conn.commit()
    
    def get_activity_log(self, limit: int = 50):
        """Get recent activity log"""
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT action, details, timestamp FROM activity_log ORDER BY timestamp DESC LIMIT ?',
            (limit,)
        )
        return cursor.fetchall()
    
    def export_data(self, file_path: str):
        """Export encrypted data to file"""
        passwords = self.get_all_passwords()
        # Re-encrypt for export (passwords are already decrypted in get_all_passwords)
        export_data = {
            'passwords': [],
            'exported_at': datetime.now().isoformat()
        }
        
        for entry in passwords:
            export_data['passwords'].append({
                'service': entry['service'],
                'username': entry['username'],
                'password': entry['password'],
                'notes': entry['notes'],
                'created_at': entry['created_at'],
                'updated_at': entry['updated_at']
            })
        
        encrypted_export = self.security.encrypt_data(json.dumps(export_data))
        
        with open(file_path, 'w') as f:
            json.dump({'data': encrypted_export}, f)
        
        self.log_activity("Data exported", f"File: {file_path}")
    
    def import_data(self, file_path: str):
        """Import encrypted data from file"""
        try:
            with open(file_path, 'r') as f:
                encrypted_data = json.load(f)
            
            decrypted_data = json.loads(self.security.decrypt_data(encrypted_data['data']))
            
            imported_count = 0
            for entry in decrypted_data['passwords']:
                self.add_password(
                    entry['service'],
                    entry['username'],
                    entry['password'],
                    entry.get('notes', '')
                )
                imported_count += 1
            
            self.log_activity("Data imported", f"File: {file_path}, Entries: {imported_count}")
            return imported_count
        except Exception as e:
            self.log_activity("Import failed", f"File: {file_path}, Error: {str(e)}")
            raise e
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
