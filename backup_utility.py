#!/usr/bin/env python3
"""
Backup utility for SecurePass Password Manager
Creates timestamped backups of the password database
"""

import os
import shutil
from datetime import datetime
import argparse

def create_backup(source_db="passwords.db", backup_dir="backups"):
    """Create a timestamped backup of the password database"""
    
    # Check if source database exists
    if not os.path.exists(source_db):
        print(f"❌ Database file '{source_db}' not found")
        return False
    
    # Create backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"📁 Created backup directory: {backup_dir}")
    
    # Generate timestamp for backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"passwords_backup_{timestamp}.db"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    try:
        # Copy the database file
        shutil.copy2(source_db, backup_path)
        
        # Get file sizes
        original_size = os.path.getsize(source_db)
        backup_size = os.path.getsize(backup_path)
        
        print(f"✅ Backup created successfully!")
        print(f"   Source: {source_db} ({original_size} bytes)")
        print(f"   Backup: {backup_path} ({backup_size} bytes)")
        print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Backup failed: {str(e)}")
        return False

def list_backups(backup_dir="backups"):
    """List all available backups"""
    
    if not os.path.exists(backup_dir):
        print(f"📁 No backup directory found: {backup_dir}")
        return
    
    backup_files = [f for f in os.listdir(backup_dir) if f.startswith("passwords_backup_") and f.endswith(".db")]
    
    if not backup_files:
        print(f"📄 No backups found in {backup_dir}")
        return
    
    print(f"📋 Available backups in {backup_dir}:")
    print("=" * 50)
    
    backup_files.sort(reverse=True)  # Most recent first
    
    for backup_file in backup_files:
        backup_path = os.path.join(backup_dir, backup_file)
        file_size = os.path.getsize(backup_path)
        
        # Extract timestamp from filename
        try:
            timestamp_str = backup_file.replace("passwords_backup_", "").replace(".db", "")
            timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            formatted_date = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        except:
            formatted_date = "Unknown date"
        
        print(f"   {backup_file}")
        print(f"   └── Date: {formatted_date}")
        print(f"   └── Size: {file_size} bytes")
        print()

def restore_backup(backup_file, target_db="passwords.db"):
    """Restore a backup to the main database file"""
    
    if not os.path.exists(backup_file):
        print(f"❌ Backup file '{backup_file}' not found")
        return False
    
    # Warn user about overwriting
    if os.path.exists(target_db):
        response = input(f"⚠️  This will overwrite the existing database '{target_db}'. Continue? (y/N): ")
        if response.lower() != 'y':
            print("❌ Restore cancelled by user")
            return False
    
    try:
        # Create a backup of current database before restoring
        if os.path.exists(target_db):
            backup_current = f"{target_db}.pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(target_db, backup_current)
            print(f"💾 Current database backed up to: {backup_current}")
        
        # Restore the backup
        shutil.copy2(backup_file, target_db)
        
        print(f"✅ Database restored successfully!")
        print(f"   From: {backup_file}")
        print(f"   To: {target_db}")
        
        return True
        
    except Exception as e:
        print(f"❌ Restore failed: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="SecurePass Backup Utility")
    parser.add_argument("action", choices=["create", "list", "restore"], 
                       help="Action to perform")
    parser.add_argument("--source", default="passwords.db", 
                       help="Source database file (default: passwords.db)")
    parser.add_argument("--backup-dir", default="backups", 
                       help="Backup directory (default: backups)")
    parser.add_argument("--backup-file", 
                       help="Specific backup file to restore")
    
    args = parser.parse_args()
    
    print("🔐 SecurePass Backup Utility")
    print("=" * 40)
    
    if args.action == "create":
        create_backup(args.source, args.backup_dir)
    
    elif args.action == "list":
        list_backups(args.backup_dir)
    
    elif args.action == "restore":
        if not args.backup_file:
            print("❌ --backup-file is required for restore action")
            return
        restore_backup(args.backup_file, args.source)

if __name__ == "__main__":
    main()
