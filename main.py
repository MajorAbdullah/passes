import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyperclip
from database import DatabaseManager, SecurityManager
from password_generator import PasswordGenerator
import threading
import time
from datetime import datetime, timedelta

class ModernStyle:
    """Modern color scheme and styling"""
    
    # Color schemes
    LIGHT_THEME = {
        'bg': '#ffffff',
        'fg': '#333333',
        'accent': '#0078d4',
        'accent_hover': '#106ebe',
        'secondary': '#f5f5f5',
        'border': '#e1e1e1',
        'success': '#16a085',
        'warning': '#f39c12',
        'danger': '#e74c3c',
        'text_light': '#6c757d'
    }
    
    DARK_THEME = {
        'bg': '#2b2b2b',
        'fg': '#ffffff',
        'accent': '#0078d4',
        'accent_hover': '#106ebe',
        'secondary': '#3c3c3c',
        'border': '#555555',
        'success': '#27ae60',
        'warning': '#f39c12',
        'danger': '#e74c3c',
        'text_light': '#cccccc'
    }
    
    def __init__(self, theme='light'):
        self.current_theme = self.LIGHT_THEME if theme == 'light' else self.DARK_THEME

class PasswordManagerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SecurePass - Password Manager")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Initialize components
        self.security = SecurityManager()
        self.db = DatabaseManager(security_manager=self.security)
        self.password_gen = PasswordGenerator()
        
        # State variables
        self.is_locked = True
        self.auto_lock_time = 300  # 5 minutes (default)
        self.last_activity = time.time()
        self.passwords_data = []
        self.filtered_data = []
        self.current_theme = 'light'  # default theme
        
        # Load user preferences
        self.load_user_preferences()
        
        # Initialize style with loaded theme
        self.style = ModernStyle(self.current_theme)
        
        # Setup GUI
        self.setup_styles()
        self.create_login_screen()
        
        # Start auto-lock timer
        self.check_auto_lock()
          # Bind activity tracking
        self.root.bind('<Button-1>', self.track_activity)
        self.root.bind('<Key>', self.track_activity)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Setup modern styling for ttk widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'),
                       foreground=self.style.current_theme['accent'])
        
        style.configure('Heading.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=self.style.current_theme['fg'])
        
        style.configure('Modern.TButton',
                       font=('Segoe UI', 10),
                       borderwidth=0,
                       focuscolor='none')
        
        style.configure('Accent.TButton',
                       background=self.style.current_theme['accent'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('Accent.TButton',
                 background=[('active', self.style.current_theme['accent_hover'])])
        
        # Apply theme to root window
        self.apply_theme_to_widget(self.root)
    
    def apply_theme_to_widget(self, widget):
        """Apply current theme to a widget and all its children recursively"""
        try:
            # Apply theme to the widget itself
            if isinstance(widget, tk.Tk) or isinstance(widget, tk.Toplevel):
                widget.configure(bg=self.style.current_theme['bg'])
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=self.style.current_theme['bg'])
            elif isinstance(widget, tk.Label):
                widget.configure(bg=self.style.current_theme['bg'], 
                               fg=self.style.current_theme['fg'])
            elif isinstance(widget, tk.Text):
                widget.configure(bg=self.style.current_theme['secondary'], 
                               fg=self.style.current_theme['fg'],
                               insertbackground=self.style.current_theme['fg'])
            elif isinstance(widget, tk.Entry):
                widget.configure(bg=self.style.current_theme['secondary'], 
                               fg=self.style.current_theme['fg'],
                               insertbackground=self.style.current_theme['fg'])
            elif isinstance(widget, tk.Listbox):
                widget.configure(bg=self.style.current_theme['secondary'], 
                               fg=self.style.current_theme['fg'],
                               selectbackground=self.style.current_theme['accent'])
        except tk.TclError:
            # Some widgets might not support certain configuration options
            pass
        
        # Apply theme to all children
        try:
            for child in widget.winfo_children():
                self.apply_theme_to_widget(child)
        except tk.TclError:
            pass
    
    def track_activity(self, event=None):
        """Track user activity for auto-lock"""
        self.last_activity = time.time()
    
    def check_auto_lock(self):
        """Check if app should auto-lock"""
        if not self.is_locked and time.time() - self.last_activity > self.auto_lock_time:
            self.lock_application()
        
        # Schedule next check
        self.root.after(30000, self.check_auto_lock)  # Check every 30 seconds
    
    def lock_application(self):
        """Lock the application"""
        self.is_locked = True
        self.clear_main_window()
        self.create_login_screen()
        messagebox.showinfo("Auto Lock", "Application has been locked due to inactivity.")
    
    def save_user_preferences(self):
        """Save user preferences to a configuration file"""
        import json
        import os
        
        preferences = {
            'theme': self.current_theme,
            'auto_lock_minutes': self.auto_lock_time // 60,
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            config_file = os.path.join(os.path.dirname(__file__), 'user_config.json')
            with open(config_file, 'w') as f:
                json.dump(preferences, f, indent=2)
        except Exception as e:
            print(f"Failed to save preferences: {e}")
    
    def load_user_preferences(self):
        """Load user preferences from configuration file"""
        import json
        import os
        
        try:
            config_file = os.path.join(os.path.dirname(__file__), 'user_config.json')
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    preferences = json.load(f)
                
                # Apply loaded preferences
                self.current_theme = preferences.get('theme', 'light')
                self.auto_lock_time = preferences.get('auto_lock_minutes', 5) * 60
                self.style = ModernStyle(self.current_theme)
                
                return True
        except Exception as e:
            print(f"Failed to load preferences: {e}")
        
        return False

    def clear_main_window(self):
        """Clear all widgets from main window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_login_screen(self):
        """Create the login/setup screen"""
        self.clear_main_window()
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Center frame
        center_frame = ttk.Frame(main_frame)
        center_frame.pack(expand=True)
        
        # Title
        title_label = ttk.Label(center_frame, text="🔐 SecurePass", style='Title.TLabel')
        title_label.pack(pady=(0, 30))
        
        subtitle = ttk.Label(center_frame, text="Your Personal Password Manager", 
                            font=('Segoe UI', 12), foreground=self.style.current_theme['text_light'])
        subtitle.pack(pady=(0, 40))
        
        # Login form
        form_frame = ttk.Frame(center_frame)
        form_frame.pack(pady=20)
        
        # Check if master password exists
        if self.db.has_master_password():
            # Login mode
            ttk.Label(form_frame, text="Enter Master Password:", style='Heading.TLabel').pack(pady=(0, 10))
            
            self.master_password_var = tk.StringVar()
            password_entry = ttk.Entry(form_frame, textvariable=self.master_password_var, 
                                     show="*", font=('Segoe UI', 12), width=30)
            password_entry.pack(pady=(0, 20))
            password_entry.bind('<Return>', lambda e: self.login())
            password_entry.focus()
            
            login_btn = ttk.Button(form_frame, text="Unlock", command=self.login, style='Accent.TButton')
            login_btn.pack(pady=(0, 10))
            
        else:
            # Setup mode
            ttk.Label(form_frame, text="Create Master Password:", style='Heading.TLabel').pack(pady=(0, 10))
            
            ttk.Label(form_frame, text="This will be used to encrypt all your passwords.", 
                     foreground=self.style.current_theme['text_light']).pack(pady=(0, 15))
            
            self.master_password_var = tk.StringVar()
            password_entry = ttk.Entry(form_frame, textvariable=self.master_password_var, 
                                     show="*", font=('Segoe UI', 12), width=30)
            password_entry.pack(pady=(0, 10))
            
            self.confirm_password_var = tk.StringVar()
            confirm_entry = ttk.Entry(form_frame, textvariable=self.confirm_password_var, 
                                    show="*", font=('Segoe UI', 12), width=30)
            confirm_entry.pack(pady=(0, 20))
            
            password_entry.bind('<Return>', lambda e: confirm_entry.focus())
            confirm_entry.bind('<Return>', lambda e: self.setup_master_password())
            password_entry.focus()
            
            setup_btn = ttk.Button(form_frame, text="Create & Setup", 
                                 command=self.setup_master_password, style='Accent.TButton')
            setup_btn.pack(pady=(0, 10))
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(side='bottom', fill='x', pady=(20, 0))
        
        footer_text = ttk.Label(footer_frame, 
                               text="All data is encrypted and stored locally on your device",
                               font=('Segoe UI', 9), 
                               foreground=self.style.current_theme['text_light'])
        footer_text.pack()
    
    def login(self):
        """Handle login process"""
        password = self.master_password_var.get()
        
        if not password:
            messagebox.showerror("Error", "Please enter your master password")
            return
        
        if self.db.verify_master_password(password):
            self.is_locked = False
            self.track_activity()
            self.create_main_interface()
        else:
            messagebox.showerror("Error", "Invalid master password")
            self.master_password_var.set("")
    
    def setup_master_password(self):
        """Setup initial master password"""
        password = self.master_password_var.get()
        confirm = self.confirm_password_var.get()
        
        if not password or not confirm:
            messagebox.showerror("Error", "Please fill in both password fields")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 8:
            messagebox.showerror("Error", "Master password must be at least 8 characters long")
            return
        
        try:
            self.db.set_master_password(password)
            self.is_locked = False
            self.track_activity()
            messagebox.showinfo("Success", "Master password created successfully!")
            self.create_main_interface()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create master password: {str(e)}")
    
    def create_main_interface(self):
        """Create the main password manager interface"""
        self.clear_main_window()
        
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True)
        
        # Header
        self.create_header(main_container)
        
        # Content area
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Left panel (controls)
        self.create_left_panel(content_frame)
        
        # Right panel (password list)
        self.create_right_panel(content_frame)
        
        # Load passwords
        self.refresh_password_list()
    
    def create_header(self, parent):
        """Create header with title and controls"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill='x', padx=20, pady=20)
        
        # Title
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side='left')
        
        ttk.Label(title_frame, text="🔐 SecurePass", font=('Segoe UI', 18, 'bold')).pack(side='left')
        
        # Header controls
        controls_frame = ttk.Frame(header_frame)
        controls_frame.pack(side='right')
        
        # Search
        ttk.Label(controls_frame, text="Search:").pack(side='left', padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(controls_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side='left', padx=(0, 10))
        search_entry.bind('<KeyRelease>', self.on_search)
        
        # Lock button
        ttk.Button(controls_frame, text="🔒 Lock", command=self.lock_application).pack(side='right', padx=(10, 0))
        
        # Theme toggle
        ttk.Button(controls_frame, text="🌙", command=self.toggle_theme).pack(side='right', padx=(10, 0))
    
    def create_left_panel(self, parent):
        """Create left control panel"""
        left_frame = ttk.LabelFrame(parent, text="Controls", padding=15)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Add Password button
        ttk.Button(left_frame, text="➕ Add Password", 
                  command=self.show_add_password_dialog, style='Accent.TButton').pack(fill='x', pady=(0, 10))
        
        # Password Generator button
        ttk.Button(left_frame, text="🎲 Generate Password", 
                  command=self.show_password_generator).pack(fill='x', pady=(0, 10))
        
        # Separator
        ttk.Separator(left_frame, orient='horizontal').pack(fill='x', pady=15)
        
        # Import/Export
        ttk.Label(left_frame, text="Backup & Restore", font=('Segoe UI', 10, 'bold')).pack(pady=(0, 10))
        
        ttk.Button(left_frame, text="📤 Export Data", 
                  command=self.export_data).pack(fill='x', pady=(0, 5))
        
        ttk.Button(left_frame, text="📥 Import Data", 
                  command=self.import_data).pack(fill='x', pady=(0, 10))
        
        # Separator
        ttk.Separator(left_frame, orient='horizontal').pack(fill='x', pady=15)
        
        # Activity Log
        ttk.Button(left_frame, text="📋 Activity Log", 
                  command=self.show_activity_log).pack(fill='x', pady=(0, 10))
        
        # Settings
        ttk.Button(left_frame, text="⚙️ Settings", 
                  command=self.show_settings).pack(fill='x')
    
    def create_right_panel(self, parent):
        """Create right panel with password list"""
        right_frame = ttk.LabelFrame(parent, text="Saved Passwords", padding=15)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Treeview for password list
        columns = ('Service', 'Username', 'Created', 'Updated')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='tree headings')
        
        # Configure columns
        self.tree.heading('#0', text='ID')
        self.tree.column('#0', width=50, minwidth=50)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == 'Service':
                self.tree.column(col, width=200, minwidth=150)
            elif col == 'Username':
                self.tree.column(col, width=150, minwidth=100)
            else:
                self.tree.column(col, width=100, minwidth=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Context menu
        self.create_context_menu()
        
        # Bind events
        self.tree.bind('<Double-1>', self.on_item_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu)  # Right click
    
    def create_context_menu(self):
        """Create context menu for password list"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="📋 Copy Username", command=self.copy_username)
        self.context_menu.add_command(label="🔑 Copy Password", command=self.copy_password)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="👁️ View Details", command=self.view_password_details)
        self.context_menu.add_command(label="✏️ Edit", command=self.edit_password)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🗑️ Delete", command=self.delete_password)
    
    def show_context_menu(self, event):
        """Show context menu"""
        # Select item under cursor
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def on_item_double_click(self, event):
        """Handle double click on item"""
        self.view_password_details()
    
    def on_search(self, event=None):
        """Handle search input"""
        query = self.search_var.get().strip()
        if query:
            self.filtered_data = self.db.search_passwords(query)
        else:
            self.filtered_data = self.passwords_data
        self.update_tree_view()
    
    def refresh_password_list(self):
        """Refresh the password list from database"""
        try:
            self.passwords_data = self.db.get_all_passwords()
            self.filtered_data = self.passwords_data
            self.update_tree_view()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load passwords: {str(e)}")
    
    def update_tree_view(self):
        """Update the treeview with current data"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add items
        for entry in self.filtered_data:
            created = entry['created_at'][:10] if entry['created_at'] else 'N/A'
            updated = entry['updated_at'][:10] if entry['updated_at'] else 'N/A'
            
            self.tree.insert('', 'end', 
                           text=str(entry['id']),
                           values=(entry['service'], entry['username'], created, updated))
    
    def get_selected_password(self):
        """Get currently selected password entry"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a password entry")
            return None
        
        item = self.tree.item(selection[0])
        entry_id = int(item['text'])
        
        for entry in self.filtered_data:
            if entry['id'] == entry_id:
                return entry
        return None
    
    def copy_username(self):
        """Copy username to clipboard"""
        entry = self.get_selected_password()
        if entry:
            pyperclip.copy(entry['username'])
            messagebox.showinfo("Copied", f"Username for {entry['service']} copied to clipboard")
    
    def copy_password(self):
        """Copy password to clipboard"""
        entry = self.get_selected_password()
        if entry:
            pyperclip.copy(entry['password'])
            messagebox.showinfo("Copied", f"Password for {entry['service']} copied to clipboard")
    
    def view_password_details(self):
        """Show password details in a dialog"""
        entry = self.get_selected_password()
        if not entry:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Password Details - {entry['service']}")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Service
        ttk.Label(main_frame, text="Service:", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        ttk.Label(main_frame, text=entry['service'], wraplength=350).pack(anchor='w', pady=(0, 10))
        
        # Username
        ttk.Label(main_frame, text="Username:", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        username_frame = ttk.Frame(main_frame)
        username_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(username_frame, text=entry['username']).pack(side='left')
        ttk.Button(username_frame, text="Copy", 
                  command=lambda: self.copy_to_clipboard(entry['username'])).pack(side='right')
        
        # Password
        ttk.Label(main_frame, text="Password:", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill='x', pady=(0, 10))
        
        self.password_visible = tk.BooleanVar()
        password_var = tk.StringVar()
        password_var.set("*" * len(entry['password']))
        
        password_entry = ttk.Entry(password_frame, textvariable=password_var, state='readonly', width=30)
        password_entry.pack(side='left', padx=(0, 5))
        
        def toggle_password():
            if self.password_visible.get():
                password_var.set(entry['password'])
            else:
                password_var.set("*" * len(entry['password']))
        
        ttk.Checkbutton(password_frame, text="Show", variable=self.password_visible, 
                       command=toggle_password).pack(side='left', padx=(0, 5))
        ttk.Button(password_frame, text="Copy", 
                  command=lambda: self.copy_to_clipboard(entry['password'])).pack(side='left')
        
        # Notes
        if entry['notes']:
            ttk.Label(main_frame, text="Notes:", font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(10, 0))
            notes_text = tk.Text(main_frame, height=3, wrap='word', state='normal')
            notes_text.pack(fill='x', pady=(0, 10))
            notes_text.insert('1.0', entry['notes'])
            notes_text.config(state='disabled')
        
        # Dates
        date_frame = ttk.Frame(main_frame)
        date_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Label(date_frame, text=f"Created: {entry['created_at'][:19] if entry['created_at'] else 'N/A'}", 
                 font=('Segoe UI', 9)).pack(side='left')
        ttk.Label(date_frame, text=f"Updated: {entry['updated_at'][:19] if entry['updated_at'] else 'N/A'}", 
                 font=('Segoe UI', 9)).pack(side='right')
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Button(button_frame, text="Edit", 
                  command=lambda: [dialog.destroy(), self.edit_password()]).pack(side='left')
        ttk.Button(button_frame, text="Close", 
                  command=dialog.destroy).pack(side='right')
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard with feedback"""
        pyperclip.copy(text)
        messagebox.showinfo("Copied", "Copied to clipboard!")
    
    def show_add_password_dialog(self):
        """Show add password dialog"""
        self.show_password_dialog()
    
    def edit_password(self):
        """Edit selected password"""
        entry = self.get_selected_password()
        if entry:
            self.show_password_dialog(entry)
    
    def show_password_dialog(self, entry=None):
        """Show add/edit password dialog"""
        is_edit = entry is not None
        title = "Edit Password" if is_edit else "Add New Password"
        
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("450x500")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Service
        ttk.Label(main_frame, text="Service/Website:", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        service_var = tk.StringVar(value=entry['service'] if is_edit else "")
        service_entry = ttk.Entry(main_frame, textvariable=service_var, width=50)
        service_entry.pack(fill='x', pady=(0, 15))
        service_entry.focus()
        
        # Username
        ttk.Label(main_frame, text="Username/Email:", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        username_var = tk.StringVar(value=entry['username'] if is_edit else "")
        username_entry = ttk.Entry(main_frame, textvariable=username_var, width=50)
        username_entry.pack(fill='x', pady=(0, 15))
        
        # Password
        ttk.Label(main_frame, text="Password:", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill='x', pady=(0, 15))
        
        password_var = tk.StringVar(value=entry['password'] if is_edit else "")
        password_entry = ttk.Entry(password_frame, textvariable=password_var, show="*", width=35)
        password_entry.pack(side='left', padx=(0, 5))
        
        show_password_var = tk.BooleanVar()
        def toggle_password_visibility():
            password_entry.config(show="" if show_password_var.get() else "*")
        
        ttk.Checkbutton(password_frame, text="Show", variable=show_password_var, 
                       command=toggle_password_visibility).pack(side='left', padx=(0, 5))
        
        ttk.Button(password_frame, text="Generate", 
                  command=lambda: self.generate_password_for_dialog(password_var)).pack(side='left')
        
        # Password strength indicator
        strength_frame = ttk.Frame(main_frame)
        strength_frame.pack(fill='x', pady=(0, 15))
        
        strength_label = ttk.Label(strength_frame, text="Password Strength:")
        strength_label.pack(side='left')
        
        strength_indicator = ttk.Label(strength_frame, text="", font=('Segoe UI', 9, 'bold'))
        strength_indicator.pack(side='left', padx=(10, 0))
        
        def update_strength(*args):
            password = password_var.get()
            if password:
                strength = self.password_gen.check_password_strength(password)
                strength_indicator.config(text=strength['strength'], foreground=strength['color'])
            else:
                strength_indicator.config(text="")
        
        password_var.trace('w', update_strength)
        
        # Notes
        ttk.Label(main_frame, text="Notes (optional):", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        notes_text = tk.Text(main_frame, height=4, wrap='word')
        notes_text.pack(fill='x', pady=(0, 20))
        if is_edit and entry['notes']:
            notes_text.insert('1.0', entry['notes'])
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x')
        
        def save_password():
            service = service_var.get().strip()
            username = username_var.get().strip()
            password = password_var.get()
            notes = notes_text.get('1.0', 'end-1c').strip()
            
            if not service or not username or not password:
                messagebox.showerror("Error", "Service, username, and password are required")
                return
            
            try:
                if is_edit:
                    self.db.update_password(entry['id'], service, username, password, notes)
                    messagebox.showinfo("Success", "Password updated successfully!")
                else:
                    self.db.add_password(service, username, password, notes)
                    messagebox.showinfo("Success", "Password added successfully!")
                
                dialog.destroy()
                self.refresh_password_list()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save password: {str(e)}")
        
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side='right', padx=(10, 0))
        ttk.Button(button_frame, text="Save", command=save_password, style='Accent.TButton').pack(side='right')
    
    def generate_password_for_dialog(self, password_var):
        """Generate password for dialog"""
        generated = self.password_gen.generate_password(length=16, use_symbols=True)
        password_var.set(generated)
    
    def delete_password(self):
        """Delete selected password"""
        entry = self.get_selected_password()
        if not entry:
            return
        
        result = messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete the password for {entry['service']}?\n\nThis action cannot be undone.")
        
        if result:
            try:
                self.db.delete_password(entry['id'])
                messagebox.showinfo("Success", "Password deleted successfully!")
                self.refresh_password_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete password: {str(e)}")
    
    def show_password_generator(self):
        """Show password generator dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Password Generator")
        dialog.geometry("450x600")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Generated password display
        ttk.Label(main_frame, text="Generated Password:", font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill='x', pady=(5, 20))
        
        generated_password_var = tk.StringVar()
        password_display = ttk.Entry(password_frame, textvariable=generated_password_var, 
                                   font=('Consolas', 12), state='readonly', width=40)
        password_display.pack(side='left', padx=(0, 10))
        
        ttk.Button(password_frame, text="Copy", 
                  command=lambda: self.copy_to_clipboard(generated_password_var.get())).pack(side='left')
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding=15)
        options_frame.pack(fill='x', pady=(0, 20))
        
        # Length
        length_frame = ttk.Frame(options_frame)
        length_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(length_frame, text="Length:").pack(side='left')
        length_var = tk.IntVar(value=16)
        length_scale = ttk.Scale(length_frame, from_=8, to=64, variable=length_var, orient='horizontal')
        length_scale.pack(side='left', fill='x', expand=True, padx=(10, 10))
        length_label = ttk.Label(length_frame, text="16")
        length_label.pack(side='left')
        
        def update_length_label(*args):
            length_label.config(text=str(length_var.get()))
        length_var.trace('w', update_length_label)
        
        # Character options
        use_lowercase = tk.BooleanVar(value=True)
        use_uppercase = tk.BooleanVar(value=True)
        use_digits = tk.BooleanVar(value=True)
        use_symbols = tk.BooleanVar(value=True)
        exclude_ambiguous = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(options_frame, text="Lowercase letters (a-z)", 
                       variable=use_lowercase).pack(anchor='w', pady=2)
        ttk.Checkbutton(options_frame, text="Uppercase letters (A-Z)", 
                       variable=use_uppercase).pack(anchor='w', pady=2)
        ttk.Checkbutton(options_frame, text="Numbers (0-9)", 
                       variable=use_digits).pack(anchor='w', pady=2)
        ttk.Checkbutton(options_frame, text="Symbols (!@#$%^&*)", 
                       variable=use_symbols).pack(anchor='w', pady=2)
        ttk.Checkbutton(options_frame, text="Exclude ambiguous characters (0, O, l, I)", 
                       variable=exclude_ambiguous).pack(anchor='w', pady=2)
        
        # Password strength
        strength_frame = ttk.Frame(main_frame)
        strength_frame.pack(fill='x', pady=(0, 20))
        
        strength_label = ttk.Label(strength_frame, text="Strength:", font=('Segoe UI', 10, 'bold'))
        strength_label.pack(side='left')
        
        strength_indicator = ttk.Label(strength_frame, text="", font=('Segoe UI', 10, 'bold'))
        strength_indicator.pack(side='left', padx=(10, 0))
        
        strength_progress = ttk.Progressbar(strength_frame, length=200, mode='determinate')
        strength_progress.pack(side='right')
        
        # Passphrase option
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=15)
        
        passphrase_frame = ttk.Frame(main_frame)
        passphrase_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Button(passphrase_frame, text="Generate Passphrase", 
                  command=lambda: self.generate_passphrase(generated_password_var, strength_indicator, strength_progress)).pack(side='left')
        
        ttk.Label(passphrase_frame, text="(e.g., Apple-Mountain-River-89)", 
                 foreground=self.style.current_theme['text_light']).pack(side='left', padx=(10, 0))
        
        def generate_new_password():
            try:
                password = self.password_gen.generate_password(
                    length=int(length_var.get()),
                    use_lowercase=use_lowercase.get(),
                    use_uppercase=use_uppercase.get(),
                    use_digits=use_digits.get(),
                    use_symbols=use_symbols.get(),
                    exclude_ambiguous=exclude_ambiguous.get()
                )
                generated_password_var.set(password)
                
                # Update strength indicator
                strength = self.password_gen.check_password_strength(password)
                strength_indicator.config(text=strength['strength'], foreground=strength['color'])
                strength_progress['value'] = (strength['score'] / strength['max_score']) * 100
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate password: {str(e)}")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, text="Generate New", command=generate_new_password, 
                  style='Accent.TButton').pack(side='left')
        ttk.Button(button_frame, text="Close", command=dialog.destroy).pack(side='right')
        
        # Generate initial password
        generate_new_password()
    
    def generate_passphrase(self, password_var, strength_indicator, strength_progress):
        """Generate a passphrase"""
        passphrase = self.password_gen.generate_passphrase()
        password_var.set(passphrase)
        
        # Update strength indicator
        strength = self.password_gen.check_password_strength(passphrase)
        strength_indicator.config(text=strength['strength'], foreground=strength['color'])
        strength_progress['value'] = (strength['score'] / strength['max_score']) * 100
    
    def export_data(self):
        """Export encrypted data"""
        file_path = filedialog.asksaveasfilename(
            title="Export Password Data",
            defaultextension=".spx",
            filetypes=[("SecurePass Export", "*.spx"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                self.db.export_data(file_path)
                messagebox.showinfo("Success", f"Data exported successfully to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {str(e)}")
    
    def import_data(self):
        """Import encrypted data"""
        file_path = filedialog.askopenfilename(
            title="Import Password Data",
            filetypes=[("SecurePass Export", "*.spx"), ("All Files", "*.*")]
        )
        
        if file_path:
            result = messagebox.askyesno("Confirm Import", 
                                       "This will add imported passwords to your existing data. Continue?")
            if result:
                try:
                    count = self.db.import_data(file_path)
                    messagebox.showinfo("Success", f"Successfully imported {count} passwords")
                    self.refresh_password_list()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to import data: {str(e)}")
    
    def show_activity_log(self):
        """Show activity log dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Activity Log")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Treeview for log
        columns = ('Action', 'Details', 'Timestamp')
        log_tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        
        for col in columns:
            log_tree.heading(col, text=col)
            if col == 'Action':
                log_tree.column(col, width=150)
            elif col == 'Details':
                log_tree.column(col, width=250)
            else:
                log_tree.column(col, width=150)
        
        # Scrollbar
        log_scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=log_tree.yview)
        log_tree.configure(yscrollcommand=log_scrollbar.set)
        
        # Pack
        log_tree.pack(side='left', fill='both', expand=True)
        log_scrollbar.pack(side='right', fill='y')
        
        # Load log data
        try:
            log_data = self.db.get_activity_log()
            for action, details, timestamp in log_data:
                log_tree.insert('', 'end', values=(action, details, timestamp))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load activity log: {str(e)}")
        
        # Close button
        ttk.Button(main_frame, text="Close", command=dialog.destroy).pack(pady=(20, 0))
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Settings")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Auto-lock setting
        ttk.Label(main_frame, text="Auto-lock timeout (minutes):", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        
        timeout_frame = ttk.Frame(main_frame)
        timeout_frame.pack(fill='x', pady=(5, 20))
        
        timeout_var = tk.IntVar(value=self.auto_lock_time // 60)
        timeout_spinbox = ttk.Spinbox(timeout_frame, from_=1, to=60, textvariable=timeout_var, width=10)
        timeout_spinbox.pack(side='left')
        
        ttk.Label(timeout_frame, text="minutes").pack(side='left', padx=(10, 0))
        
        # Theme setting
        ttk.Label(main_frame, text="Theme:", font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(20, 0))
        
        theme_var = tk.StringVar(value=self.current_theme)
        theme_frame = ttk.Frame(main_frame)
        theme_frame.pack(fill='x', pady=(5, 20))
        
        ttk.Radiobutton(theme_frame, text="Light", variable=theme_var, value='light').pack(side='left')
        ttk.Radiobutton(theme_frame, text="Dark", variable=theme_var, value='dark').pack(side='left', padx=(20, 0))
        
        # Change master password
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=20)
        
        ttk.Label(main_frame, text="Security:", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        
        ttk.Button(main_frame, text="Change Master Password", 
                  command=lambda: [dialog.destroy(), self.change_master_password()]).pack(anchor='w', pady=(10, 0))
          # Save settings
        def save_settings():
            # Save auto-lock timeout
            old_auto_lock = self.auto_lock_time
            self.auto_lock_time = timeout_var.get() * 60
            
            # Apply theme immediately if changed
            if theme_var.get() != self.current_theme:
                self.current_theme = theme_var.get()
                self.style = ModernStyle(self.current_theme)
                self.setup_styles()
                
                # Save theme preference to config file
                self.save_user_preferences()
                
                messagebox.showinfo("Settings", f"Theme changed to {self.current_theme} mode successfully!")
            else:
                # Save other settings if theme didn't change
                if old_auto_lock != self.auto_lock_time:
                    self.save_user_preferences()
                    messagebox.showinfo("Settings", "Settings saved successfully!")
                else:
                    messagebox.showinfo("Settings", "No changes made.")
            
            dialog.destroy()
        
        def apply_settings():
            """Apply settings without closing dialog"""
            # Save auto-lock timeout
            self.auto_lock_time = timeout_var.get() * 60
            
            # Apply theme immediately if changed
            if theme_var.get() != self.current_theme:
                self.current_theme = theme_var.get()
                self.style = ModernStyle(self.current_theme)
                self.setup_styles()
                messagebox.showinfo("Settings", f"Theme applied: {self.current_theme} mode")
            
            # Save preferences
            self.save_user_preferences()
          # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(30, 0))
        
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side='right', padx=(10, 0))
        ttk.Button(button_frame, text="Apply", command=apply_settings).pack(side='right', padx=(10, 0))
        ttk.Button(button_frame, text="Save", command=save_settings, style='Accent.TButton').pack(side='right')
    
    def change_master_password(self):
        """Change master password dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Change Master Password")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        messagebox.showwarning("Important", 
                             "Changing your master password will require you to re-enter all stored passwords. "
                             "Make sure you have a backup of your data.")
        
        # Current password
        ttk.Label(main_frame, text="Current Master Password:", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        current_var = tk.StringVar()
        current_entry = ttk.Entry(main_frame, textvariable=current_var, show="*", width=40)
        current_entry.pack(fill='x', pady=(5, 15))
        current_entry.focus()
        
        # New password
        ttk.Label(main_frame, text="New Master Password:", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        new_var = tk.StringVar()
        new_entry = ttk.Entry(main_frame, textvariable=new_var, show="*", width=40)
        new_entry.pack(fill='x', pady=(5, 15))
        
        # Confirm new password
        ttk.Label(main_frame, text="Confirm New Password:", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        confirm_var = tk.StringVar()
        confirm_entry = ttk.Entry(main_frame, textvariable=confirm_var, show="*", width=40)
        confirm_entry.pack(fill='x', pady=(5, 20))
        
        def change_password():
            current = current_var.get()
            new_password = new_var.get()
            confirm = confirm_var.get()
            
            if not all([current, new_password, confirm]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            if new_password != confirm:
                messagebox.showerror("Error", "New passwords do not match")
                return
            
            if len(new_password) < 8:
                messagebox.showerror("Error", "New password must be at least 8 characters long")
                return
            
            if not self.db.verify_master_password(current):
                messagebox.showerror("Error", "Current password is incorrect")
                return
            
            try:
                # This is a simplified implementation
                # In a real scenario, you'd need to re-encrypt all data with the new password
                messagebox.showinfo("Notice", 
                                  "Master password change is not fully implemented in this demo. "
                                  "In a production version, this would re-encrypt all stored data.")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to change master password: {str(e)}")
          # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side='right', padx=(10, 0))
        ttk.Button(button_frame, text="Change Password", command=change_password, 
                  style='Accent.TButton').pack(side='right')
    
    def toggle_theme(self):
        """Toggle between light and dark theme with immediate effect"""
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.style = ModernStyle(self.current_theme)
        self.setup_styles()
        self.save_user_preferences()
        messagebox.showinfo("Theme", f"Switched to {self.current_theme} theme")
    
    def on_closing(self):
        """Handle application closing with automatic export"""
        if messagebox.askokcancel("Quit", "Do you want to quit SecurePass?"):
            try:
                # Perform automatic export before closing
                self.auto_export_on_logout()
                
                # Close database connection
                self.db.close()
            except Exception as e:
                print(f"Error during closing: {e}")
            finally:
                self.root.destroy()
    
    def auto_export_on_logout(self):
        """Automatically export password data to a backup file on logout"""
        try:
            import os
            from datetime import datetime
            
            # Define auto-backup file path (overwrites each time)
            backup_filename = "auto_backup_latest.spx"
            backup_path = os.path.join(os.path.dirname(__file__), backup_filename)
            
            # Check if we have any passwords to export
            if not self.is_locked and hasattr(self, 'db'):
                passwords = self.db.get_all_passwords()
                
                if passwords:  # Only export if there are passwords
                    # Export data (this will overwrite the existing file)
                    self.db.export_data(backup_path)
                    
                    # Log the auto-export
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{timestamp}] Auto-backup created: {backup_path}")
                    
                    # Show brief notification (non-blocking)
                    try:
                        self.root.after(100, lambda: messagebox.showinfo(
                            "Auto Backup", 
                            f"Passwords automatically backed up to:\n{backup_filename}", 
                            parent=self.root
                        ))
                    except:
                        # If window is already destroyed, skip notification
                        pass
                        
        except Exception as e:
            print(f"Auto-export failed: {e}")
            # Don't block closing if auto-export fails
    
    def create_timestamped_backup(self):
        """Create a timestamped backup file that won't be overwritten"""
        try:
            import os
            from datetime import datetime
            
            # Create timestamped backup filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"password_backup_{timestamp}.spx"
            backup_path = os.path.join(os.path.dirname(__file__), backup_filename)
            
            # Export data to timestamped file
            self.db.export_data(backup_path)
            
            messagebox.showinfo("Backup Created", 
                              f"Timestamped backup created:\n{backup_filename}")
            return backup_path
            
        except Exception as e:
            messagebox.showerror("Backup Failed", f"Failed to create backup: {str(e)}")
            return None

    # ...existing code...
    
    def run(self):
        """Start the application"""
        # Load user preferences
        self.load_user_preferences()
        
        # Apply loaded theme
        self.style = ModernStyle(self.current_theme)
        self.setup_styles()
        
        self.root.mainloop()

# Check if pyperclip is available, install it if needed
try:
    import pyperclip
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
    import pyperclip

if __name__ == "__main__":
    app = PasswordManagerGUI()
    app.run()
