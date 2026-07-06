import json
import customtkinter as ctk
import sqlite3
from tkinter import ttk, messagebox, filedialog
import os
import threading 
import payslip_engine 
from datetime import datetime

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
try:
    import win32com.client
    OUTLOOK_AVAILABLE = True
except ImportError:
    OUTLOOK_AVAILABLE = False

# --- THE MILLION-DOLLAR COLOR PALETTE ---
BG_MAIN = "#0F172A"       
BG_SIDEBAR = "#020617"    
BG_CARD = "#1E293B"       
BG_CARD_HOVER = "#25344A" 
BG_CARD_ALT = "#162032"   
ACCENT = "#3B82F6"        
SUCCESS = "#10B981"       
WARNING_ORANGE = "#F59E0B"
TEXT_MAIN = "#F8FAFC"     
TEXT_SUB = "#94A3B8"      
WARNING_RED = "#EF4444"   

ctk.set_appearance_mode("dark")
APP_FONT = "Helvetica" 
YEAR_RANGE = [str(y) for y in range(2019, 2031)] 

class PayrollDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 🔥 SELF-HEALING PROTOCOL
        self.initialize_database()

        self.title("Enterprise Payroll Vault v4.6.2 - Secured")
        self.geometry("1400x850") 
        self.configure(fg_color=BG_MAIN) 
        self.month_map = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1) 

        # --- PREMIUM SIDEBAR ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=BG_SIDEBAR)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        # Pushes everything below row 9 to the bottom
        self.sidebar_frame.grid_rowconfigure(9, weight=1) 
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="PAYROLL VAULT", font=ctk.CTkFont(family=APP_FONT, size=18, weight="bold"), text_color=TEXT_MAIN)
        self.logo_label.grid(row=0, column=0, padx=20, pady=(35, 30))

        self.btn_dashboard = ctk.CTkButton(self.sidebar_frame, text="📊 Executive Dash", font=ctk.CTkFont(family=APP_FONT, size=13), fg_color="transparent", text_color=TEXT_MAIN, anchor="w", command=lambda: self.select_frame("dashboard"))
        self.btn_dashboard.grid(row=1, column=0, padx=15, pady=8, sticky="ew")
        
        self.btn_employees = ctk.CTkButton(self.sidebar_frame, text="👥 Staff Directory", font=ctk.CTkFont(family=APP_FONT, size=13), fg_color="transparent", text_color=TEXT_MAIN, anchor="w", command=lambda: self.select_frame("employees"))
        self.btn_employees.grid(row=2, column=0, padx=15, pady=8, sticky="ew")
        
        self.btn_batch = ctk.CTkButton(self.sidebar_frame, text="🎯 HR Requests", font=ctk.CTkFont(family=APP_FONT, size=13), fg_color="transparent", text_color=TEXT_MAIN, anchor="w", command=lambda: self.select_frame("batch"))
        self.btn_batch.grid(row=3, column=0, padx=15, pady=8, sticky="ew")

        # Admin Sidebar Button 
        self.btn_admin = ctk.CTkButton(self.sidebar_frame, text="🛡️ Admin Settings", font=ctk.CTkFont(family=APP_FONT, size=13), fg_color="transparent", text_color=TEXT_MAIN, anchor="w", command=lambda: self.select_frame("admin"))
        self.btn_admin.grid(row=4, column=0, padx=15, pady=8, sticky="ew")
        
       # Data Importers
        self.btn_import_emails = ctk.CTkButton(self.sidebar_frame, text="📥 Import Emails", font=ctk.CTkFont(family=APP_FONT, size=13), fg_color="transparent", text_color=TEXT_MAIN, anchor="w")
        self.btn_import_emails.grid(row=5, column=0, padx=15, pady=8, sticky="ew")

        self.btn_import_payroll = ctk.CTkButton(self.sidebar_frame, text="📤 Import Payroll", font=ctk.CTkFont(family=APP_FONT, size=13, weight="bold"), fg_color="transparent", text_color=SUCCESS, anchor="w", command=self.trigger_smart_import)
        self.btn_import_payroll.grid(row=6, column=0, padx=15, pady=8, sticky="ew")

        self.btn_db_admin = ctk.CTkButton(self.sidebar_frame, text="⚙️ Database Admin", font=ctk.CTkFont(family=APP_FONT, size=13, weight="bold"), fg_color="transparent", text_color=WARNING_ORANGE, anchor="w", command=self.open_db_admin_modal)
        self.btn_db_admin.grid(row=7, column=0, padx=15, pady=8, sticky="ew")

        # LOGOUT BUTTON (NEW)
        self.btn_logout = ctk.CTkButton(self.sidebar_frame, text="🚪 Secure Logout", font=ctk.CTkFont(family=APP_FONT, size=13, weight="bold"), fg_color="transparent", hover_color="#7F1D1D", text_color=WARNING_RED, anchor="w", command=self.logout_user)
        self.btn_logout.grid(row=10, column=0, padx=15, pady=(0, 10), sticky="ew")

        self.brand_label = ctk.CTkLabel(self.sidebar_frame, text="Powered by\nHawea Heritage", font=ctk.CTkFont(family=APP_FONT, size=12, weight="bold"), text_color="#38BDF8") 
        self.brand_label.grid(row=11, column=0, pady=(0, 30), sticky="s")

        # --- EXECUTIVE DASHBOARD MODULE ---
        self.dashboard_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.dashboard_frame.grid_columnconfigure(0, weight=1)
        
        self.dash_header_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.dash_header_frame.grid(row=0, column=0, padx=35, pady=(35, 5), sticky="ew")
        
        self.label_welcome = ctk.CTkLabel(self.dash_header_frame, text="Executive Overview", font=ctk.CTkFont(family=APP_FONT, size=28, weight="bold"), text_color=TEXT_MAIN)
        self.label_welcome.pack(side="left")

        self.label_missing_emails = ctk.CTkLabel(self.dash_header_frame, text="⚠️ 0 Staff Missing Emails", font=ctk.CTkFont(family=APP_FONT, size=12, weight="bold"), text_color=WARNING_ORANGE, fg_color=BG_CARD, corner_radius=6, padx=10, pady=5)
        self.label_missing_emails.pack(side="right", padx=10)
        
        self.filter_frame = ctk.CTkFrame(self.dashboard_frame, fg_color=BG_CARD, corner_radius=12)
        self.filter_frame.grid(row=1, column=0, padx=35, pady=(15, 0), sticky="w")
        
        ctk.CTkLabel(self.filter_frame, text="Start:", font=ctk.CTkFont(family=APP_FONT, weight="bold")).grid(row=0, column=0, padx=(15, 5), pady=15)
        self.dash_start_m = ctk.CTkComboBox(self.filter_frame, font=ctk.CTkFont(family=APP_FONT), values=list(self.month_map.keys()), width=110, fg_color=BG_MAIN, border_color=BG_SIDEBAR)
        self.dash_start_m.grid(row=0, column=1, padx=5)
        self.dash_start_y = ctk.CTkComboBox(self.filter_frame, font=ctk.CTkFont(family=APP_FONT), values=YEAR_RANGE, width=80, fg_color=BG_MAIN, border_color=BG_SIDEBAR)
        self.dash_start_y.grid(row=0, column=2, padx=5)

        ctk.CTkLabel(self.filter_frame, text="End:", font=ctk.CTkFont(family=APP_FONT, weight="bold")).grid(row=0, column=3, padx=(20, 5), pady=15)
        self.dash_end_m = ctk.CTkComboBox(self.filter_frame, font=ctk.CTkFont(family=APP_FONT), values=list(self.month_map.keys()), width=110, fg_color=BG_MAIN, border_color=BG_SIDEBAR)
        self.dash_end_m.grid(row=0, column=4, padx=5)
        self.dash_end_y = ctk.CTkComboBox(self.filter_frame, font=ctk.CTkFont(family=APP_FONT), values=YEAR_RANGE, width=80, fg_color=BG_MAIN, border_color=BG_SIDEBAR)
        self.dash_end_y.grid(row=0, column=5, padx=5)

        self.btn_calc_range = ctk.CTkButton(self.filter_frame, text="🔄 Calculate", font=ctk.CTkFont(family=APP_FONT, weight="bold"), fg_color=ACCENT, width=100, command=self.update_metrics_event)
        self.btn_calc_range.grid(row=0, column=6, padx=(15, 5))

        self.btn_export_report = ctk.CTkButton(self.filter_frame, text="📥 Export Excel Report", font=ctk.CTkFont(family=APP_FONT, weight="bold"), fg_color=SUCCESS, hover_color="#047857", width=150, command=self.export_board_report)
        self.btn_export_report.grid(row=0, column=7, padx=5)

        self.btn_delete_month = ctk.CTkButton(self.filter_frame, text="🗑️ Purge", font=ctk.CTkFont(family=APP_FONT, weight="bold"), fg_color=WARNING_RED, hover_color="#991B1B", width=90, command=self.delete_month_data)
        self.btn_delete_month.grid(row=0, column=8, padx=(5, 15))

        # --- THE 9-CARD INTERACTIVE GRID ---
        self.metrics_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.metrics_frame.grid(row=2, column=0, padx=25, pady=25, sticky="nsew")
        
        card_w = 320
        card_h = 105

        self.card_staff = self.create_interactive_card(self.metrics_frame, 0, 0, card_w, card_h, "TOTAL ACTIVE STAFF", "0", TEXT_MAIN)
        self.card_gross = self.create_interactive_card(self.metrics_frame, 0, 1, card_w, card_h, "GROSS PAYROLL (Total Obligation)", "₦ 0.00", TEXT_MAIN)
        self.card_net = self.create_interactive_card(self.metrics_frame, 0, 2, card_w, card_h, "NET PAYROLL (Cash Outflow)", "₦ 0.00", SUCCESS)

        self.card_tax = self.create_interactive_card(self.metrics_frame, 1, 0, card_w, card_h, "TOTAL PAYE (Tax)", "₦ 0.00", WARNING_RED)
        self.card_pen = self.create_interactive_card(self.metrics_frame, 1, 1, card_w, card_h, "TOTAL PENSIONS", "₦ 0.00", WARNING_RED)
        self.card_c1_sav = self.create_interactive_card(self.metrics_frame, 1, 2, card_w, card_h, "COOP 1: CONTR/SPEC SAVINGS", "₦ 0.00", ACCENT)

        self.card_c1_loan = self.create_interactive_card(self.metrics_frame, 2, 0, card_w, card_h, "COOP 1: LOAN RECOVERY", "₦ 0.00", ACCENT)
        self.card_c2_sav = self.create_interactive_card(self.metrics_frame, 2, 1, card_w, card_h, "COOP 2: CONTR/SPEC SAVINGS", "₦ 0.00", "#8B5CF6") 
        self.card_c2_loan = self.create_interactive_card(self.metrics_frame, 2, 2, card_w, card_h, "COOP 2: LOAN RECOVERY", "₦ 0.00", "#8B5CF6") 

        # --- EMPLOYEES MODULE ---
        self.employees_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.employees_frame.grid_columnconfigure(0, weight=1)
        self.employees_frame.grid_rowconfigure(1, weight=1) 
        self.emp_header_frame = ctk.CTkFrame(self.employees_frame, fg_color="transparent")
        self.emp_header_frame.grid(row=0, column=0, padx=35, pady=(35, 10), sticky="ew")
        self.emp_header_frame.grid_columnconfigure(0, weight=1) 
        self.emp_header = ctk.CTkLabel(self.emp_header_frame, text="Staff Directory", font=ctk.CTkFont(family=APP_FONT, size=28, weight="bold"), text_color=TEXT_MAIN)
        self.emp_header.grid(row=0, column=0, sticky="w")
        self.search_entry = ctk.CTkEntry(self.emp_header_frame, placeholder_text="🔍 Search Name...", font=ctk.CTkFont(family=APP_FONT), width=300, height=40, fg_color=BG_CARD, border_color=BG_SIDEBAR, corner_radius=8)
        self.search_entry.grid(row=0, column=1, sticky="e")
        self.search_entry.bind("<KeyRelease>", self.update_search_event)

        self.table_frame = ctk.CTkFrame(self.employees_frame, corner_radius=12, fg_color=BG_CARD)
        self.table_frame.grid(row=1, column=0, padx=35, pady=10, sticky="nsew")
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=BG_CARD, foreground=TEXT_MAIN, rowheight=42, fieldbackground=BG_CARD, borderwidth=0, font=(APP_FONT, 10))
        style.map('Treeview', background=[('selected', ACCENT)])
        style.configure("Treeview.Heading", background=BG_SIDEBAR, foreground=TEXT_SUB, relief="flat", font=(APP_FONT, 10, "bold"), padding=10)
        
        self.tree_scroll = ctk.CTkScrollbar(self.table_frame, fg_color="transparent", button_color=BG_SIDEBAR)
        self.tree_scroll.grid(row=0, column=1, sticky="ns", pady=10, padx=(0, 10))
        self.staff_tree = ttk.Treeview(self.table_frame, yscrollcommand=self.tree_scroll.set, selectmode="extended")
        self.staff_tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.tree_scroll.configure(command=self.staff_tree.yview)
        self.staff_tree.bind("<Double-1>", lambda event: self.open_employee_profile())

        self.staff_tree.tag_configure('evenrow', background=BG_CARD)
        self.staff_tree.tag_configure('oddrow', background=BG_CARD_ALT)

        self.staff_tree['columns'] = ("Name", "Designation", "Grade", "Net Pay")
        self.staff_tree.column("#0", width=0, stretch="no") 
        self.staff_tree.column("Name", anchor="w", width=250)
        self.staff_tree.column("Designation", anchor="w", width=200)
        self.staff_tree.column("Grade", anchor="center", width=100)
        self.staff_tree.column("Net Pay", anchor="e", width=150)
        self.staff_tree.heading("Name", text="STAFF NAME", anchor="w")
        self.staff_tree.heading("Designation", text="DESIGNATION", anchor="w")
        self.staff_tree.heading("Grade", text="GRADE LEVEL", anchor="center")
        self.staff_tree.heading("Net Pay", text="LATEST NET PAY", anchor="e")

        self.action_frame = ctk.CTkFrame(self.employees_frame, fg_color="transparent")
        self.action_frame.grid(row=2, column=0, padx=35, pady=(10, 30), sticky="e")
        self.btn_edit = ctk.CTkButton(self.action_frame, text="View/Edit Profile", font=ctk.CTkFont(family=APP_FONT, weight="bold"), height=40, corner_radius=8, command=self.open_employee_profile, fg_color=ACCENT, text_color=TEXT_MAIN)
        self.btn_edit.grid(row=0, column=0, padx=10)

        # --- HR SNIPER & BATCH MODULE ---
        self.batch_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.batch_frame.grid_columnconfigure(0, weight=2) 
        self.batch_frame.grid_columnconfigure(1, weight=1) 
        self.batch_frame.grid_rowconfigure(1, weight=1)

        self.batch_header = ctk.CTkLabel(self.batch_frame, text="HR Requests & Batch Engine", font=ctk.CTkFont(family=APP_FONT, size=28, weight="bold"), text_color=TEXT_MAIN)
        self.batch_header.grid(row=0, column=0, columnspan=2, padx=35, pady=(35, 20), sticky="w")

        self.left_batch_panel = ctk.CTkFrame(self.batch_frame, fg_color="transparent")
        self.left_batch_panel.grid(row=1, column=0, padx=(35, 10), sticky="nsew")
        self.left_batch_panel.grid_columnconfigure(0, weight=1)
        self.left_batch_panel.grid_rowconfigure(1, weight=1)

        self.range_panel = ctk.CTkFrame(self.left_batch_panel, fg_color=BG_CARD, corner_radius=12)
        self.range_panel.grid(row=0, column=0, pady=(0, 15), sticky="ew")
        ctk.CTkLabel(self.range_panel, text="Start Period:", font=ctk.CTkFont(family=APP_FONT, weight="bold")).grid(row=0, column=0, padx=15, pady=25)
        self.batch_start_m = ctk.CTkComboBox(self.range_panel, font=ctk.CTkFont(family=APP_FONT), values=list(self.month_map.keys()), width=120, fg_color=BG_MAIN, border_color=BG_SIDEBAR)
        self.batch_start_m.grid(row=0, column=1, padx=5)
        self.batch_start_y = ctk.CTkComboBox(self.range_panel, font=ctk.CTkFont(family=APP_FONT), values=YEAR_RANGE, width=90, fg_color=BG_MAIN, border_color=BG_SIDEBAR)
        self.batch_start_y.grid(row=0, column=2, padx=5)
        
        ctk.CTkLabel(self.range_panel, text="End Period:", font=ctk.CTkFont(family=APP_FONT, weight="bold")).grid(row=0, column=3, padx=(30, 15), pady=25)
        self.batch_end_m = ctk.CTkComboBox(self.range_panel, font=ctk.CTkFont(family=APP_FONT), values=list(self.month_map.keys()), width=120, fg_color=BG_MAIN, border_color=BG_SIDEBAR)
        self.batch_end_m.grid(row=0, column=4, padx=5)
        self.batch_end_y = ctk.CTkComboBox(self.range_panel, font=ctk.CTkFont(family=APP_FONT), values=YEAR_RANGE, width=90, fg_color=BG_MAIN, border_color=BG_SIDEBAR)
        self.batch_end_y.grid(row=0, column=5, padx=5)

        self.log_panel = ctk.CTkFrame(self.left_batch_panel, fg_color=BG_CARD, corner_radius=12)
        self.log_panel.grid(row=1, column=0, sticky="nsew")
        self.log_panel.grid_columnconfigure(0, weight=1)
        self.log_panel.grid_rowconfigure(1, weight=1)
        self.progress_bar = ctk.CTkProgressBar(self.log_panel, progress_color=ACCENT, height=12)
        self.progress_bar.grid(row=0, column=0, padx=25, pady=25, sticky="ew")
        self.progress_bar.set(0)
        self.log_box = ctk.CTkTextbox(self.log_panel, font=ctk.CTkFont(family="Courier", size=12), fg_color=BG_MAIN, text_color=TEXT_SUB, state="disabled", corner_radius=8)
        self.log_box.grid(row=1, column=0, padx=25, pady=(0, 25), sticky="nsew")

        self.right_batch_panel = ctk.CTkFrame(self.batch_frame, fg_color=BG_CARD, corner_radius=12)
        self.right_batch_panel.grid(row=1, column=1, padx=(10, 35), sticky="nsew")
        self.right_batch_panel.grid_rowconfigure(2, weight=1)
        self.right_batch_panel.grid_columnconfigure(0, weight=1)
        self.chk_header = ctk.CTkLabel(self.right_batch_panel, text="🎯 Target Selection", font=ctk.CTkFont(family=APP_FONT, weight="bold", size=16), text_color=TEXT_MAIN)
        self.chk_header.grid(row=0, column=0, pady=15)
        self.chk_search = ctk.CTkEntry(self.right_batch_panel, placeholder_text="🔍 Quick Search...", font=ctk.CTkFont(family=APP_FONT), height=35, fg_color=BG_MAIN, border_color=BG_SIDEBAR, corner_radius=8)
        self.chk_search.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        self.chk_search.bind("<KeyRelease>", self.filter_checklist_ui)
        
        self.staff_checklist_frame = ctk.CTkScrollableFrame(self.right_batch_panel, fg_color=BG_MAIN, corner_radius=8)
        self.staff_checklist_frame.grid(row=2, column=0, padx=15, pady=5, sticky="nsew")
        
        self.chk_actions = ctk.CTkFrame(self.right_batch_panel, fg_color="transparent")
        self.chk_actions.grid(row=3, column=0, pady=15)
        ctk.CTkButton(self.chk_actions, text="Select All", font=ctk.CTkFont(family=APP_FONT), width=110, corner_radius=6, command=self.select_all_staff, fg_color=BG_SIDEBAR, hover_color=ACCENT).grid(row=0, column=0, padx=5)
        ctk.CTkButton(self.chk_actions, text="Clear All", font=ctk.CTkFont(family=APP_FONT), width=110, corner_radius=6, command=self.clear_all_staff, fg_color=BG_SIDEBAR, hover_color=WARNING_RED).grid(row=0, column=1, padx=5)

        self.master_staff_vars = {} 

        self.batch_action_panel = ctk.CTkFrame(self.batch_frame, fg_color="transparent")
        self.batch_action_panel.grid(row=2, column=0, columnspan=2, padx=35, pady=25, sticky="e")

        self.dispatch_mode = ctk.StringVar(value="Draft (Review)")
        self.dispatch_dropdown = ctk.CTkComboBox(self.batch_action_panel, font=ctk.CTkFont(family=APP_FONT, weight="bold"), values=["Draft (Review)", "Send Immediately 🚀"], variable=self.dispatch_mode, fg_color=BG_CARD, border_color=ACCENT, height=40, width=200)
        self.dispatch_dropdown.grid(row=0, column=0, padx=15)

        self.btn_stop_batch = ctk.CTkButton(self.batch_action_panel, text="🛑 HALT", font=ctk.CTkFont(family=APP_FONT, weight="bold"), fg_color=WARNING_RED, hover_color="#B91C1C", state="disabled", command=self.stop_batch, height=40, corner_radius=8)
        self.btn_stop_batch.grid(row=0, column=1, padx=10)

        self.btn_start_batch = ctk.CTkButton(self.batch_action_panel, text="🚀 Execute Operation", font=ctk.CTkFont(family=APP_FONT, weight="bold"), fg_color=SUCCESS, hover_color="#059669", command=self.start_batch_thread, height=40, corner_radius=8)
        self.btn_start_batch.grid(row=0, column=2, padx=10)

        self.batch_running = False

        # --- ADMIN FRAME (NEW FEATURE UI) ---
        self.admin_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.admin_frame.grid_columnconfigure(0, weight=1)
        self.admin_frame.grid_rowconfigure(1, weight=1)
        
        self.admin_header = ctk.CTkLabel(self.admin_frame, text="System Administration & Access", font=ctk.CTkFont(family=APP_FONT, size=28, weight="bold"), text_color=TEXT_MAIN)
        self.admin_header.grid(row=0, column=0, padx=35, pady=(35, 20), sticky="w")

        self.admin_content = ctk.CTkFrame(self.admin_frame, fg_color="transparent")
        self.admin_content.grid(row=1, column=0, padx=35, sticky="nsew")
        self.admin_content.grid_columnconfigure(0, weight=2)
        self.admin_content.grid_columnconfigure(1, weight=1)

        self.user_list_card = ctk.CTkFrame(self.admin_content, fg_color=BG_CARD, corner_radius=12)
        self.user_list_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        ctk.CTkLabel(self.user_list_card, text="Authorized Vault Users", font=ctk.CTkFont(family=APP_FONT, size=16, weight="bold")).pack(pady=15)

        self.user_tree = ttk.Treeview(self.user_list_card, columns=("User", "Access", "Last Login"), show='headings', height=15)
        self.user_tree.heading("User", text="USERNAME")
        self.user_tree.heading("Access", text="ACCESS LEVEL")
        self.user_tree.heading("Last Login", text="LAST LOGIN")
        self.user_tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.user_ctrl_card = ctk.CTkFrame(self.admin_content, fg_color=BG_CARD_ALT, corner_radius=12)
        self.user_ctrl_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        ctk.CTkLabel(self.user_ctrl_card, text="User Controls", font=ctk.CTkFont(family=APP_FONT, size=16, weight="bold")).pack(pady=15)

        self.new_username = ctk.CTkEntry(self.user_ctrl_card, placeholder_text="New Username", height=40, fg_color=BG_MAIN)
        self.new_username.pack(fill="x", padx=20, pady=5)
        
        self.new_password = ctk.CTkEntry(self.user_ctrl_card, placeholder_text="Set Password", height=40, show="*", fg_color=BG_MAIN)
        self.new_password.pack(fill="x", padx=20, pady=5)

        self.access_lvl = ctk.CTkComboBox(self.user_ctrl_card, values=["Admin", "Viewer"], height=40, fg_color=BG_MAIN)
        self.access_lvl.pack(fill="x", padx=20, pady=5)

        ctk.CTkButton(self.user_ctrl_card, text="Grant Access", fg_color=SUCCESS, command=self.add_system_user).pack(fill="x", padx=20, pady=20)
        ctk.CTkButton(self.user_ctrl_card, text="Revoke Access", fg_color=WARNING_RED, command=self.delete_system_user).pack(fill="x", padx=20, pady=5)


        # INITIALIZATION
        self.select_frame("dashboard")
        self.load_dashboard_metrics()
        self.load_staff_directory() 
        self.init_batch_checklist()

    # --- 🔥 SELF-HEALING DATABASE PROTOCOL (V4.6 UPGRADED) ---
    def initialize_database(self):
        conn = sqlite3.connect("payroll_vault.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 1. Master Payroll Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS master_payroll (
                Txn_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                "STAFF NAME" TEXT,
                "Payroll_Month" INTEGER,
                "Payroll_Year" INTEGER,
                "DESIGNATION" TEXT,
                "GRADE LEVEL" TEXT,
                "GROSS SALARY" REAL DEFAULT 0.0,
                "NET PAY" REAL DEFAULT 0.0,
                "PAYE" REAL DEFAULT 0.0,
                "EMPLOYEE PENSIONS" REAL DEFAULT 0.0,
                "COOP 1 CONTR/SPEC SAVINGS" REAL DEFAULT 0.0,
                "COOP 1 LOAN RECOVERY" REAL DEFAULT 0.0,
                "COOP 2 CONTR/SPEC SAVINGS" REAL DEFAULT 0.0,
                "COOP 2 LOAN RECOVERY" REAL DEFAULT 0.0
            )
        ''')
        
        # 2. Staff Profiles Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tbl_Staff_Profiles (
                "STAFF NAME" TEXT PRIMARY KEY,
                "EMAIL" TEXT,
                "BANK" TEXT,
                "ACCT NO" TEXT,
                "PFA" TEXT,
                "PENSION NO" TEXT
            )
        ''')

        # 3. User Admin Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tbl_Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                access_level TEXT DEFAULT 'Admin',
                last_login TEXT
            )
        ''')

        # 4. Header Mapping Table (THE NEW AUDIT UPGRADE)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS header_mapping (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                messy_header TEXT UNIQUE NOT NULL,
                clean_standard TEXT NOT NULL
            );
        """)

        # 5. Immutable Audit Vault (THE NEW AUDIT UPGRADE)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payroll_month TEXT,
                payroll_year TEXT,
                raw_json_data TEXT, 
                upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 6. Auto-Load the Mapping Coordinates
        cursor.execute("SELECT COUNT(*) FROM header_mapping")
        if cursor.fetchone()[0] == 0:
            default_mappings = [
                ("COOP 1 CONTR/SPEC SAVINGS", "Cooperative Society 1"),
                ("COOP 2 CONTR/SPEC SAVINGS", "Cooperative Society 2"),
                ("COOP. LOAN RECOVERY", "Cooperative Loan Recovery"),
                ("TOTAL DEDUCTION", "Total Deduction"),
                ("NET PAY", "Net Pay")
            ]
            cursor.executemany("INSERT INTO header_mapping (messy_header, clean_standard) VALUES (?, ?)", default_mappings)

        conn.commit()
        conn.close()

   # --- DATABASE ADMIN MODULE (V4.6.3 UPDATED) ---
    def open_db_admin_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Database Structure Admin")
        modal.geometry("500x650")
        modal.configure(fg_color=BG_MAIN)
        modal.grab_set() 
        
        ctk.CTkLabel(modal, text="⚙️ Schema Admin", font=ctk.CTkFont(family=APP_FONT, size=22, weight="bold"), text_color=WARNING_ORANGE).pack(pady=(20, 5))
        ctk.CTkLabel(modal, text="Manage columns. Core financial columns are\nlocked to prevent dashboard errors.", text_color=TEXT_SUB, font=ctk.CTkFont(family=APP_FONT)).pack(pady=(0, 15))

        # UPDATED: Added TOTAL DEDUCTION, AUCTION, and NHF DED. to the locked core
        core_cols = [
            "Txn_ID", "STAFF NAME", "Payroll_Month", "Payroll_Year", 
            "DESIGNATION", "GRADE LEVEL", "GROSS SALARY", "NET PAY", 
            "PAYE", "EMPLOYEE PENSIONS", "COOP 1 CONTR/SPEC SAVINGS", 
            "COOP 1 LOAN RECOVERY", "COOP 2 CONTR/SPEC SAVINGS", 
            "COOP 2 LOAN RECOVERY", "TOTAL DEDUCTION", "AUCTION", "NHF DED."
        ]
        
        scroll_frame = ctk.CTkScrollableFrame(modal, fg_color=BG_CARD, corner_radius=8)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        def refresh_list():
            for widget in scroll_frame.winfo_children(): widget.destroy()
            try:
                conn = sqlite3.connect("payroll_vault.db")
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(master_payroll)")
                columns = [row[1] for row in cursor.fetchall()]
                conn.close()

                for col in columns:
                    # Case-insensitive comparison for safety
                    is_core = col.upper() in [c.upper() for c in core_cols]
                    row_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
                    row_frame.pack(fill="x", pady=5)
                    
                    ctk.CTkLabel(row_frame, text=col, font=ctk.CTkFont(family=APP_FONT, weight="bold" if is_core else "normal"), text_color=TEXT_SUB if is_core else TEXT_MAIN).pack(side="left", padx=10)
                    
                    if not is_core:
                        btn_del = ctk.CTkButton(row_frame, text="Drop", width=60, height=24, fg_color=WARNING_RED, hover_color="#991B1B", command=lambda c=col: drop_column(c))
                        btn_del.pack(side="right", padx=10)
                    else:
                        ctk.CTkLabel(row_frame, text="Locked", text_color=SUCCESS, font=ctk.CTkFont(size=10)).pack(side="right", padx=10)
            except Exception as e:
                ctk.CTkLabel(scroll_frame, text=f"Error reading DB: {e}").pack()

        def drop_column(col_name):
            if messagebox.askyesno("Confirm Drop", f"PERMANENTLY delete column:\n\n'{col_name}'?\n\nThis will destroy the data inside it.", parent=modal):
                try:
                    conn = sqlite3.connect("payroll_vault.db")
                    cursor = conn.cursor()
                    cursor.execute(f'ALTER TABLE master_payroll DROP COLUMN "{col_name}"')
                    conn.commit()
                    conn.close()
                    refresh_list()
                    self.load_dashboard_metrics()
                    messagebox.showinfo("Success", f"Column '{col_name}' eradicated.", parent=modal)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed: {e}", parent=modal)

        refresh_list()
        ctk.CTkButton(modal, text="Close Admin", command=modal.destroy, fg_color=BG_SIDEBAR).pack(pady=15)

    # --- 📤 V4.6 THE "DATA-FIRST" IMPORTER WITH AUDIT GLASS ---
    def trigger_smart_import(self):
        if not PANDAS_AVAILABLE: 
            messagebox.showerror("System Error", "The engine is missing Pandas.", parent=self)
            return
            
        filepath = filedialog.askopenfilename(parent=self, filetypes=[("Data Files", "*.xlsx *.xls *.csv")])
        if not filepath: return

        try:
            if filepath.endswith('.csv'): df = pd.read_csv(filepath)
            else: df = pd.read_excel(filepath)

            df.columns = [str(c).upper().strip() for c in df.columns]
            cols_to_drop = [col for col in df.columns if col in ["TXN_ID", "S/N"] or "UNNAMED" in col]
            if cols_to_drop: df.drop(columns=cols_to_drop, inplace=True, errors='ignore')

            conn = sqlite3.connect('payroll_vault.db')
            cursor = conn.cursor()
            cursor.execute("SELECT messy_header, clean_standard FROM header_mapping")
            raw_rules = cursor.fetchall()
            conn.close()

            mapping_rules = {messy.upper().strip(): clean.upper().strip() for messy, clean in raw_rules}
            df.rename(columns=mapping_rules, inplace=True)
            df = df.loc[:, ~df.columns.duplicated()]

            if "STAFF NAME" not in df.columns:
                messagebox.showerror("Format Error", "File MUST contain a 'STAFF NAME' column.", parent=self)
                return

            def safe_sum(col_name):
                col_upper = col_name.upper()
                if col_upper in df.columns:
                    return pd.to_numeric(df[col_upper], errors='coerce').fillna(0).sum()
                return 0.0

            total_gross = safe_sum("GROSS SALARY")
            total_deductions = safe_sum("TOTAL DEDUCTION")
            total_net = safe_sum("NET PAY")

            audit_window = ctk.CTkToplevel(self)
            audit_window.title("Audit Glass - Verify Payroll Data")
            audit_window.geometry("1100x750")
            audit_window.grab_set()

            summary_frame = ctk.CTkFrame(audit_window, fg_color="#1E293B")
            summary_frame.pack(fill="x", padx=20, pady=(20, 10))

            ctk.CTkLabel(summary_frame, text=f"Gross Expected: ₦{total_gross:,.2f}", font=("Helvetica", 16, "bold"), text_color="#3B82F6").pack(side="left", padx=20, pady=15)
            ctk.CTkLabel(summary_frame, text=f"Total Deductions: ₦{total_deductions:,.2f}", font=("Helvetica", 16, "bold"), text_color="#EF4444").pack(side="left", padx=20, pady=15)
            ctk.CTkLabel(summary_frame, text=f"NET PAYOUT: ₦{total_net:,.2f}", font=("Helvetica", 18, "bold"), text_color="#10B981").pack(side="right", padx=20, pady=15)

            grid_frame = ctk.CTkFrame(audit_window)
            grid_frame.pack(fill="both", expand=True, padx=20, pady=0)

            columns = list(df.columns)
            tree = ttk.Treeview(grid_frame, columns=columns, show="headings", height=15)
            vsb = ttk.Scrollbar(grid_frame, orient="vertical", command=tree.yview)
            hsb = ttk.Scrollbar(grid_frame, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

            tree.grid(column=0, row=0, sticky='nsew')
            vsb.grid(column=1, row=0, sticky='ns')
            hsb.grid(column=0, row=1, sticky='ew')
            grid_frame.grid_columnconfigure(0, weight=1)
            grid_frame.grid_rowconfigure(0, weight=1)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=130, anchor="center")

            for _, row in df.iterrows():
                tree.insert("", "end", values=list(row))

            def approve_and_continue():
                audit_window.destroy()
                cols_check = [str(c).upper().strip() for c in df.columns]
                is_bulk = "PAYROLL_MONTH" in cols_check and "PAYROLL_YEAR" in cols_check
                if is_bulk: self.execute_payroll_import(df, None, None, True)
                else: self.open_date_selector_modal(df)

            btn_frame = ctk.CTkFrame(audit_window, fg_color="transparent")
            btn_frame.pack(fill="x", pady=20)
            ctk.CTkButton(btn_frame, text="❌ Reject", fg_color="#EF4444", height=45, command=audit_window.destroy).pack(side="left", padx=50)
            ctk.CTkButton(btn_frame, text="✅ Approve & Upload", fg_color="#10B981", font=("Helvetica", 15, "bold"), height=45, command=approve_and_continue).pack(side="right", padx=50)

        except Exception as e:
            messagebox.showerror("Read Error", f"Failed to analyze file: {e}", parent=self)

    def open_date_selector_modal(self, df):
        modal = ctk.CTkToplevel(self)
        modal.title("Target Month Selection")
        modal.geometry("400x320")
        modal.configure(fg_color=BG_MAIN)
        modal.grab_set()
        
        ctk.CTkLabel(modal, text="📅 Select Payroll Period", font=ctk.CTkFont(family=APP_FONT, size=22, weight="bold"), text_color=SUCCESS).pack(pady=(30, 10))
        ctk.CTkLabel(modal, text="Data verified! Please specify the target month.", text_color=TEXT_SUB, font=ctk.CTkFont(family=APP_FONT)).pack(pady=10)
        
        frame = ctk.CTkFrame(modal, fg_color="transparent")
        frame.pack(pady=15)
        
        m_var = ctk.StringVar(value="March")
        ctk.CTkComboBox(frame, font=ctk.CTkFont(family=APP_FONT), values=list(self.month_map.keys()), variable=m_var, fg_color=BG_CARD, border_color=BG_SIDEBAR).grid(row=0, column=0, padx=5)
        y_var = ctk.StringVar(value="2026")
        ctk.CTkComboBox(frame, font=ctk.CTkFont(family=APP_FONT), values=YEAR_RANGE, variable=y_var, fg_color=BG_CARD, border_color=BG_SIDEBAR, width=90).grid(row=0, column=1, padx=5)
        
        def confirm():
            m, y = m_var.get(), y_var.get()
            modal.destroy()
            self.execute_payroll_import(df, m, y, False)
            
        ctk.CTkButton(modal, text="Confirm & Import 🚀", font=ctk.CTkFont(family=APP_FONT, weight="bold"), height=40, corner_radius=8, fg_color=SUCCESS, command=confirm).pack(pady=15)

    def execute_payroll_import(self, df, month_str, year_str, is_bulk_mode):
        try:
            self.title("Enterprise Payroll Vault - ⚙️ IMPORTING DATA... PLEASE WAIT")
            self.update()

            # --- THE TRANSLATOR (Forces Excel headers to match the Database/PDF) ---
            rename_map = {
                "RESEARCH ALLOW.": "RESEARCH ALLOWANCE",
                "HARDSHIP ALLOW.": "HARDSHIP ALLOWANCE",
                "DUTY ALLCE": "LEGISLATIVE DUTY ALLOWANCE",
                "DUTY ALLOWANCE": "LEGISLATIVE DUTY ALLOWANCE",
                "RENT": "RENT ALLOWANCE",
                "UTILITY": "UTILITY ALLOWANCE",
                "DOMESTIC": "DOMESTIC ALLOWANCE",
                "ENTERT.": "ENTERTAINMENT ALLOWANCE",
                "FURNIT.": "FURNITURE ALLOWANCE",
                "FUEL": "MOTOR/FUEL ALLOWANCE"
            }
            df.rename(columns=rename_map, inplace=True)
            # -----------------------------------------------------------------------

                       # 🛡️ THE EVIL TWIN SHIELD: Force perfect, uniform names
            df["STAFF NAME"] = df["STAFF NAME"].astype(str).str.upper().str.strip().str.replace(r'\s+', ' ', regex=True)

            conn = sqlite3.connect("payroll_vault.db", timeout=10.0)
            cursor = conn.cursor()

            ui_target_month = self.month_map[month_str] if not is_bulk_mode else None
            ui_target_year = int(year_str) if not is_bulk_mode else None

            # 🛡️ THE DOUBLE-ENTRY SHIELD
            if ui_target_month and ui_target_year:
                cursor.execute('DELETE FROM master_payroll WHERE "Payroll_Month" = ? AND "Payroll_Year" = ?', (ui_target_month, ui_target_year))
                conn.commit()

            # THE GATEKEEPER (Checking for new columns)
            cursor.execute("PRAGMA table_info(master_payroll)")
            db_cols = [info[1] for info in cursor.fetchall()]
            new_cols_found = [col for col in df.columns if col not in db_cols and col not in ["PAYROLL_MONTH", "PAYROLL_YEAR"]]

            if new_cols_found:
                col_list = "\n- ".join(new_cols_found)
                msg = f"The engine found NEW columns in your Excel file:\n\n- {col_list}\n\nDo you want to permanently add these to the Database schema?"
                if messagebox.askyesno("Gatekeeper: New Columns Detected", msg, parent=self):
                    for col in new_cols_found:
                        try: cursor.execute(f'ALTER TABLE master_payroll ADD COLUMN "{col}" REAL DEFAULT 0.00')
                        except: pass
                else:
                    df.drop(columns=new_cols_found, inplace=True, errors='ignore')

            df = df.fillna(0)
            cols_to_insert = [c for c in df.columns if c not in ["PAYROLL_MONTH", "PAYROLL_YEAR"]]
            placeholders = ", ".join(["?"] * (len(cols_to_insert) + 2))
            col_names_str = ", ".join([f'"{c}"' for c in cols_to_insert]) + ', "Payroll_Month", "Payroll_Year"'
            insert_query = f"INSERT INTO master_payroll ({col_names_str}) VALUES ({placeholders})"

            records_to_insert = []
            for _, row in df.iterrows():
                staff_name = str(row.get("STAFF NAME", "")).strip()
                if not staff_name or staff_name.lower() in ["nan", "none", "s/n", "0", "0.0"]: continue

                clean_row = []
                for col_name in cols_to_insert:
                    val = row.get(col_name, 0)
                    if pd.isna(val):
                        clean_row.append("" if col_name in ["STAFF NAME", "DESIGNATION", "GRADE LEVEL"] else 0.0)
                    else:
                        if col_name in ["STAFF NAME", "DESIGNATION", "GRADE LEVEL"]:
                            clean_row.append(str(val).strip())
                        else:
                            try: clean_row.append(float(str(val).replace(",", "").strip()))
                            except: clean_row.append(0.0)

                if is_bulk_mode:
                    try:
                        m_val = str(row["PAYROLL_MONTH"]).strip().capitalize()
                        if m_val in self.month_map: r_month = self.month_map[m_val]
                        else: r_month = int(float(row["PAYROLL_MONTH"]))
                        r_year = int(float(row["PAYROLL_YEAR"]))
                    except: continue
                    clean_row.extend([r_month, r_year])
                else:
                    clean_row.extend([ui_target_month, ui_target_year])

                records_to_insert.append(tuple(clean_row))

            cursor.executemany(insert_query, records_to_insert)

            for name in df["STAFF NAME"]:
                name = str(name).strip()
                if name and name.lower() not in ["nan", "none", "0", "0.0", "s/n"]:
                    try: cursor.execute('INSERT OR IGNORE INTO tbl_Staff_Profiles ("STAFF NAME") VALUES (?)', (name,))
                    except: pass

            # 🛡️ THE AUDIT VAULT: Save the raw immutable JSON backup
            try:
                import json
                json_data = df.to_json(orient='records')
                target_m = month_str if not is_bulk_mode else "Bulk Mode"
                target_y = str(year_str) if not is_bulk_mode else "Bulk Mode"
                cursor.execute("INSERT INTO audit_vault (payroll_month, payroll_year, raw_json_data) VALUES (?, ?, ?)", (target_m, target_y, json_data))
            except Exception as e:
                print(f"Audit Vault warning: {e}")

            conn.commit()
            conn.close()

            self.load_dashboard_metrics()
            self.load_staff_directory()
            self.init_batch_checklist()

            self.title("Enterprise Payroll Vault v4.6 - Secured")
            messagebox.showinfo("Import Successful", f"Gbosa! Successfully imported {len(records_to_insert)} clean records into the Vault.", parent=self)

        except Exception as e:
            self.title("Enterprise Payroll Vault v4.6 - Secured")
            messagebox.showerror("Import Error", f"Failed to import data: {e}", parent=self)

# --- 📥 DATA-FIRST EMAIL IMPORTER ---
# ... [Your existing email success message is here] ...
        
        # 🛡️ UX POLISH: Auto-clear the search bar
        try:
            # Note: Replace 'self.search_entry' with your actual search bar variable name!
            self.search_entry.delete(0, 'end') 
            
            # If you have a function that resets the visual list, uncomment the line below:
            # self.refresh_staff_list() 
        except Exception as e: 
            pass

        # 🛡️ UX POLISH: Auto-deselect all checkboxes
        try:
            # Note: Replace 'self.checkbox_vars' with your actual list of Tkinter variables!
            for var in self.checkbox_vars: 
                var.set(0)
        except Exception as e: 
            pass

# --- THE QUICK FIX: AUTO-DESELECT CHECKBOXES ---
        try:
            # Flips all the checkbox IntVars back to 0 (unchecked)
            if hasattr(self, 'checkbox_vars'):
                for var in self.checkbox_vars: 
                    var.set(0)
            
            # Show the final success message to the user
            messagebox.showinfo("Task Complete", "Gbosa! Emails dispatched successfully and all selections have been cleared.", parent=self)
        except Exception as e: 
            print(f"Error clearing checkboxes: {e}")

# --- TACTILE CARD GENERATOR ---
    def create_interactive_card(self, parent, row, col, w, h, title, default_val, val_color):
        card = ctk.CTkFrame(parent, width=w, height=h, corner_radius=12, fg_color=BG_CARD)
        card.grid(row=row, column=col, padx=10, pady=10)
        card.grid_propagate(False)
        
        lbl_title = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(family=APP_FONT, size=11, weight="bold"), text_color=TEXT_SUB)
        lbl_title.place(relx=0.08, rely=0.2)
        
        lbl_val = ctk.CTkLabel(card, text=default_val, font=ctk.CTkFont(family=APP_FONT, size=24, weight="bold"), text_color=val_color)
        lbl_val.place(relx=0.08, rely=0.5)

        def on_enter(e): card.configure(fg_color=BG_CARD_HOVER)
        def on_leave(e): card.configure(fg_color=BG_CARD)
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        lbl_title.bind("<Enter>", on_enter)
        lbl_title.bind("<Leave>", on_leave)
        lbl_val.bind("<Enter>", on_enter)
        lbl_val.bind("<Leave>", on_leave)

        return lbl_val
        
   # --- 👑 1-CLICK EXCEL BOARD REPORT ---
    def export_board_report(self):
        if not PANDAS_AVAILABLE: return
        start_m, start_y = self.month_map[self.dash_start_m.get()], int(self.dash_start_y.get())
        end_m, end_y = self.month_map[self.dash_end_m.get()], int(self.dash_end_y.get())
        start_val, end_val = (start_y * 12) + start_m, (end_y * 12) + end_m
        period_string = f"{self.dash_start_m.get()} {start_y} to {self.dash_end_m.get()} {end_y}"

        if start_val > end_val:
            messagebox.showerror("Date Error", "Start period cannot be after End period.", parent=self); return

        save_path = filedialog.asksaveasfilename(parent=self, defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")], initialfile=f"Hawea_Board_Report_{self.dash_start_m.get()}_{start_y}_to_{self.dash_end_m.get()}_{end_y}.xlsx")
        if not save_path: return

        try:
            conn = sqlite3.connect("payroll_vault.db")
            # 🚨 BUG FIX 1: This magic line allows us to use row["nickname"]
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()
            
            # 🚨 BUG FIX 2: Added the missing staff count query!
            cursor.execute('''SELECT COUNT(DISTINCT "STAFF NAME") AS staff_count FROM master_payroll WHERE (CAST("Payroll_Year" AS INTEGER) * 12 + CAST("Payroll_Month" AS INTEGER)) >= ? AND (CAST("Payroll_Year" AS INTEGER) * 12 + CAST("Payroll_Month" AS INTEGER)) <= ?''', (start_val, end_val))
            staff_count = cursor.fetchone()["staff_count"]

            # The Upgraded SQL Query with Aliases (Nicknames)
            cursor.execute('''
                SELECT 
                    SUM(IFNULL("GROSS SALARY", 0)) AS total_gross, 
                    SUM(IFNULL("NET PAY", 0)) AS total_net, 
                    SUM(IFNULL("PAYE", 0)) AS total_paye, 
                    SUM(IFNULL("EMPLOYEE PENSIONS", 0)) AS total_pension, 
                    SUM(IFNULL("NHF DED.", 0)) AS total_nhf, 
                    SUM(IFNULL("AUCTION", 0)) AS total_auction, 
                    SUM(IFNULL("COOP 1 CONTR/SPEC SAVINGS", 0)) AS coop1_sav, 
                    SUM(IFNULL("COOP 1 LOAN RECOVERY", 0)) AS coop1_loan, 
                    SUM(IFNULL("COOP 2 CONTR/SPEC SAVINGS", 0)) AS coop2_sav, 
                    SUM(IFNULL("COOP 2 LOAN RECOVERY", 0)) AS coop2_loan 
                FROM master_payroll 
                WHERE (CAST("Payroll_Year" AS INTEGER) * 12 + CAST("Payroll_Month" AS INTEGER)) >= ? 
                AND (CAST("Payroll_Year" AS INTEGER) * 12 + CAST("Payroll_Month" AS INTEGER)) <= ?
            ''', (start_val, end_val))
            
            row = cursor.fetchone()
            
            # Using the Dictionary Method with our new nicknames!
            total_gross = row["total_gross"] or 0
            total_net = row["total_net"] or 0
            total_deductions = total_gross - total_net 

            summary_data = {
                "Metric": [
                    "REPORTING PERIOD", "Total Active Staff", "Gross Payroll (Total Obligation)", 
                    "Total Deductions", "Net Payroll (Cash Outflow)", "Total PAYE (Tax)", 
                    "Total Pensions", "Total NHF", "Total Auction", "Coop 1: Savings", 
                    "Coop 1: Loan Recovery", "Coop 2: Savings", "Coop 2: Loan Recovery"
                ],
                "Value": [
                    period_string, staff_count, total_gross, total_deductions, total_net, 
                    row["total_paye"] or 0, 
                    row["total_pension"] or 0, 
                    row["total_nhf"] or 0, 
                    row["total_auction"] or 0, 
                    row["coop1_sav"] or 0, 
                    row["coop1_loan"] or 0, 
                    row["coop2_sav"] or 0, 
                    row["coop2_loan"] or 0
                ]
            }
            df_summary = pd.DataFrame(summary_data)

            query = '''SELECT "STAFF NAME", "DESIGNATION", "GRADE LEVEL", SUM(IFNULL("GROSS SALARY", 0)) as "TOTAL GROSS", (SUM(IFNULL("GROSS SALARY", 0)) - SUM(IFNULL("NET PAY", 0))) as "TOTAL DEDUCTIONS", SUM(IFNULL("NET PAY", 0)) as "TOTAL NET" FROM master_payroll WHERE (CAST("Payroll_Year" AS INTEGER) * 12 + CAST("Payroll_Month" AS INTEGER)) >= ? AND (CAST("Payroll_Year" AS INTEGER) * 12 + CAST("Payroll_Month" AS INTEGER)) <= ? GROUP BY "STAFF NAME" ORDER BY "STAFF NAME" ASC'''
            df_staff = pd.read_sql_query(query, conn, params=(start_val, end_val))
            conn.close()

            with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
                df_summary.to_excel(writer, sheet_name='Executive Summary', index=False)
                df_staff.to_excel(writer, sheet_name='Staff Breakdown', index=False)
            
            messagebox.showinfo("Report Generated", "Export successful!", parent=self); os.startfile(save_path) 
            
        except Exception as e: messagebox.showerror("Export Error", f"Failed: {e}", parent=self)

    # --- DATA ROLLBACK (PURGE MENU) ---
    def delete_month_data(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Purge Monthly Data")
        modal.geometry("400x300")
        modal.configure(fg_color=BG_MAIN)
        modal.grab_set()

        ctk.CTkLabel(modal, text="⚠️ Purge Payroll Data", font=ctk.CTkFont(family=APP_FONT, size=22, weight="bold"), text_color=WARNING_RED).pack(pady=(30, 10))
        ctk.CTkLabel(modal, text="Select the exact month to permanently delete.", text_color=TEXT_SUB, font=ctk.CTkFont(family=APP_FONT)).pack(pady=10)

        frame = ctk.CTkFrame(modal, fg_color="transparent")
        frame.pack(pady=10)

        m_var = ctk.StringVar(value="March")
        ctk.CTkComboBox(frame, font=ctk.CTkFont(family=APP_FONT), values=list(self.month_map.keys()), variable=m_var, fg_color=BG_CARD, border_color=BG_SIDEBAR).grid(row=0, column=0, padx=5)
        y_var = ctk.StringVar(value="2026")
        ctk.CTkComboBox(frame, font=ctk.CTkFont(family=APP_FONT), values=YEAR_RANGE, variable=y_var, fg_color=BG_CARD, border_color=BG_SIDEBAR, width=90).grid(row=0, column=1, padx=5)

        def execute_purge():
            m_val, y_val = self.month_map[m_var.get()], int(y_var.get())
            if messagebox.askyesno("Confirm", f"Permanently delete {m_var.get()} {y_val}?", parent=modal):
                conn = sqlite3.connect("payroll_vault.db"); cursor = conn.cursor()
                cursor.execute('DELETE FROM master_payroll WHERE "Payroll_Month" = ? AND "Payroll_Year" = ?', (m_val, y_val))
                deleted = cursor.rowcount; conn.commit(); conn.close()
                self.load_dashboard_metrics(); self.load_staff_directory()
                messagebox.showinfo("Purged", f"Deleted {deleted} records.", parent=modal); modal.destroy()

        ctk.CTkButton(modal, text="Permanently Delete Data", font=ctk.CTkFont(family=APP_FONT, weight="bold"), fg_color=WARNING_RED, hover_color="#991B1B", command=execute_purge).pack(pady=20)

    # --- ROUTERS & LOGIC ---
    def select_frame(self, name):
        self.dashboard_frame.grid_forget()
        self.employees_frame.grid_forget()
        self.batch_frame.grid_forget()
        
        # FIX: Check if admin_frame exists before trying to hide it
        if hasattr(self, 'admin_frame'):
            self.admin_frame.grid_forget()

        self.btn_dashboard.configure(fg_color="transparent", text_color=TEXT_MAIN)
        self.btn_employees.configure(fg_color="transparent", text_color=TEXT_MAIN)
        self.btn_batch.configure(fg_color="transparent", text_color=TEXT_MAIN)
        
        if hasattr(self, 'btn_admin'):
            self.btn_admin.configure(fg_color="transparent", text_color=TEXT_MAIN)

        if name == "dashboard":
            self.dashboard_frame.grid(row=0, column=1, sticky="nsew")
            self.btn_dashboard.configure(fg_color=BG_CARD_ALT, text_color=ACCENT)
        elif name == "employees":
            self.employees_frame.grid(row=0, column=1, sticky="nsew")
            self.btn_employees.configure(fg_color=BG_CARD_ALT, text_color=ACCENT)
        elif name == "batch":
            self.batch_frame.grid(row=0, column=1, sticky="nsew")
            self.btn_batch.configure(fg_color=BG_CARD_ALT, text_color=ACCENT)
        elif name == "admin":
            self.admin_frame.grid(row=0, column=1, sticky="nsew")
            self.btn_admin.configure(fg_color=BG_CARD_ALT, text_color=ACCENT)
            self.refresh_user_list()

    def update_metrics_event(self, choice=None):
        self.load_dashboard_metrics()
        self.load_staff_directory() 

    def update_search_event(self, event):
        self.load_staff_directory()

    # --- DASHBOARD METRICS ENGINE ---
    def load_dashboard_metrics(self):
        try:
            start_m = str(self.month_map[self.dash_start_m.get()])
            start_y = str(self.dash_start_y.get())
            end_m = str(self.month_map[self.dash_end_m.get()])
            end_y = str(self.dash_end_y.get())
            start_val, end_val = (int(start_y) * 12) + int(start_m), (int(end_y) * 12) + int(end_m)

            if start_val > end_val: return

            conn = sqlite3.connect("payroll_vault.db")
            conn.row_factory = sqlite3.Row  
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) AS missing_count FROM tbl_Staff_Profiles WHERE "EMAIL" IS NULL OR "EMAIL" = ""')
            missing_emails = cursor.fetchone()["missing_count"]
            self.label_missing_emails.configure(text=f"⚠️ {missing_emails} Staff Missing Emails")

         # Solid integer casting for the board summary
            cursor.execute('''SELECT COUNT(DISTINCT "STAFF NAME") AS staff_count FROM master_payroll WHERE (CAST("Payroll_Year" AS INTEGER) * 12 + CAST("Payroll_Month" AS INTEGER)) >= ? AND (CAST("Payroll_Year" AS INTEGER) * 12 + CAST("Payroll_Month" AS INTEGER)) <= ?''', (start_val, end_val))
            staff_count = cursor.fetchone()["staff_count"]
            
            cursor.execute('''
                SELECT 
                    SUM(IFNULL("GROSS SALARY", 0)) AS total_gross, 
                    SUM(IFNULL("TOTAL DEDUCTION", 0)) AS total_deduction,
                    SUM(IFNULL("NET PAY", 0)) AS total_net, 
                    SUM(IFNULL("PAYE", 0)) AS total_paye, 
                    SUM(IFNULL("EMPLOYEE PENSIONS", 0)) AS total_pension, 
                    SUM(IFNULL("NHF DED.", 0)) AS total_nhf, 
                    SUM(IFNULL("AUCTION", 0)) AS total_auction,
                    SUM(IFNULL("COOP 1 CONTR/SPEC SAVINGS", 0)) AS coop1_sav, 
                    SUM(IFNULL("COOP 1 LOAN RECOVERY", 0)) AS coop1_loan, 
                    SUM(IFNULL("COOP 2 CONTR/SPEC SAVINGS", 0)) AS coop2_sav, 
                    SUM(IFNULL("COOP 2 LOAN RECOVERY", 0)) AS coop2_loan 
                FROM master_payroll 
                WHERE (CAST("Payroll_Year" AS INTEGER) * 12 + CAST("Payroll_Month" AS INTEGER)) >= ? 
                AND (CAST("Payroll_Year" AS INTEGER) * 12 + CAST("Payroll_Month" AS INTEGER)) <= ?
            ''', (start_val, end_val))
            
            row = cursor.fetchone()
            conn.close()

            # --- EXISTING UI CARDS ---
            self.card_staff.configure(text=str(staff_count))
            self.card_gross.configure(text=f"₦ {row['total_gross'] if row['total_gross'] else 0:,.2f}")
            self.card_net.configure(text=f"₦ {row['total_net'] if row['total_net'] else 0:,.2f}")
            self.card_tax.configure(text=f"₦ {row['total_paye'] if row['total_paye'] else 0:,.2f}")
            self.card_pen.configure(text=f"₦ {row['total_pension'] if row['total_pension'] else 0:,.2f}")
            self.card_c1_sav.configure(text=f"₦ {row['coop1_sav'] if row['coop1_sav'] else 0:,.2f}")
            self.card_c1_loan.configure(text=f"₦ {row['coop1_loan'] if row['coop1_loan'] else 0:,.2f}")
            self.card_c2_sav.configure(text=f"₦ {row['coop2_sav'] if row['coop2_sav'] else 0:,.2f}")
            self.card_c2_loan.configure(text=f"₦ {row['coop2_loan'] if row['coop2_loan'] else 0:,.2f}")

            # --- NEW UI CARDS (Uncomment these if you add them to the Dashboard UI later!) ---
            # self.card_nhf.configure(text=f"₦ {row['total_nhf'] if row['total_nhf'] else 0:,.2f}")
            # self.card_auction.configure(text=f"₦ {row['total_auction'] if row['total_auction'] else 0:,.2f}")
            # self.card_total_deduction.configure(text=f"₦ {row['total_deduction'] if row['total_deduction'] else 0:,.2f}")
            
        except Exception as e: 
            print(f"Error in Dashboard Metrics: {e}")

# --- STAFF DIRECTORY ENGINE ---
    def load_staff_directory(self):
        try:
            for item in self.staff_tree.get_children(): self.staff_tree.delete(item)
            
            # Convert UI inputs to strict integers
            target_month = int(self.month_map[self.dash_end_m.get()])
            target_year = int(self.dash_end_y.get())
            search_text = self.search_entry.get().strip()

            conn = sqlite3.connect("payroll_vault.db")
            conn.row_factory = sqlite3.Row  
            cursor = conn.cursor()
            
            # The bulletproof query: Forces SQLite to treat the month/year columns as numbers
            query = '''
                SELECT "STAFF NAME", "DESIGNATION", "GRADE LEVEL", "NET PAY" 
                FROM master_payroll 
                WHERE CAST("Payroll_Month" AS INTEGER) = ? 
                AND CAST("Payroll_Year" AS INTEGER) = ?
            '''
            params = [target_month, target_year]

            if search_text:
                query += ' AND ("STAFF NAME" LIKE ? OR "DESIGNATION" LIKE ?)'
                params.extend([f'%{search_text}%', f'%{search_text}%'])

            query += ' GROUP BY "STAFF NAME" ORDER BY "STAFF NAME" ASC'
            cursor.execute(query, tuple(params))
            
            for i, row in enumerate(cursor.fetchall()):
                name = row["STAFF NAME"]
                desig = row["DESIGNATION"]
                grade = row["GRADE LEVEL"]
                net_pay = row["NET PAY"]
                
                try: formatted_pay = f"₦ {float(net_pay):,.2f}"
                except: formatted_pay = "₦ 0.00"
                
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.staff_tree.insert(parent='', index='end', values=(name, desig, grade, formatted_pay), tags=(tag,))
            conn.close()

            # NOTICE: The auto-clear command has been completely removed from here!

        except Exception as e: 
            print(f"Error in Staff Directory: {e}")
    
# --- SPLIT-VIEW PROFILE MANAGER & COMMAND CENTER ---
    def open_employee_profile(self):
        selected = self.staff_tree.selection()
        if not selected: return
        item = self.staff_tree.item(selected[0])
        staff_name = item['values'][0]

        target_month, target_year = self.month_map[self.dash_end_m.get()], int(self.dash_end_y.get())

        conn = sqlite3.connect("payroll_vault.db")
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM master_payroll WHERE "STAFF NAME" = ? AND "Payroll_Month" = ? AND "Payroll_Year" = ? LIMIT 1', (staff_name, target_month, target_year))
        fin_record = cursor.fetchone()
        
        cursor.execute('SELECT * FROM tbl_Staff_Profiles WHERE "STAFF NAME" = ?', (staff_name,))
        profile_record = cursor.fetchone()
        conn.close()

        if not fin_record or not profile_record: return
        full_staff_data = dict(fin_record)

        profile_window = ctk.CTkToplevel(self)
        profile_window.title(f"Enterprise Profile - {staff_name}")
        profile_window.geometry("900x750") 
        profile_window.configure(fg_color=BG_MAIN)
        profile_window.grab_set()

        header_frame = ctk.CTkFrame(profile_window, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(25, 15))
        
        ctk.CTkLabel(header_frame, text=staff_name, font=ctk.CTkFont(family=APP_FONT, size=26, weight="bold"), text_color=TEXT_MAIN).pack(side="left")
        ctk.CTkLabel(header_frame, text=f"| {fin_record['DESIGNATION']}", font=ctk.CTkFont(family=APP_FONT, size=16), text_color=TEXT_SUB).pack(side="left", padx=10)

        content_frame = ctk.CTkFrame(profile_window, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

        # --- LEFT CARD: IDENTITY ---
        left_card = ctk.CTkFrame(content_frame, fg_color=BG_CARD, corner_radius=12)
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(left_card, text="💳 Identity & Bank Details", font=ctk.CTkFont(family=APP_FONT, size=16, weight="bold"), text_color=SUCCESS).pack(pady=(20, 15), anchor="w", padx=20)
        
        left_scroll = ctk.CTkScrollableFrame(left_card, fg_color="transparent")
        left_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.editable_entries = {}
        row_idx = 0
        editable_keys = ["EMAIL", "BANK", "ACCT NO", "PFA", "PENSION NO"]
        for key in editable_keys:
            val = profile_record[key] if key in profile_record.keys() else ""
            lbl = ctk.CTkLabel(left_scroll, text=f"{key}:", font=ctk.CTkFont(family=APP_FONT, weight="bold"), text_color=TEXT_MAIN) 
            lbl.grid(row=row_idx, column=0, padx=10, pady=10, sticky="w")
            
            entry = ctk.CTkEntry(left_scroll, width=220, height=35, font=ctk.CTkFont(family=APP_FONT), fg_color=BG_MAIN, border_color=ACCENT, text_color=TEXT_MAIN, corner_radius=6)
            entry.grid(row=row_idx, column=1, padx=10, pady=10, sticky="w")
            entry.insert(0, str(val) if val is not None else "")
            
            self.editable_entries[key] = entry
            row_idx += 1

        # --- RIGHT CARD: FINANCIALS ---
        right_card = ctk.CTkFrame(content_frame, fg_color=BG_CARD, corner_radius=12)
        right_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ctk.CTkLabel(right_card, text="📊 Monthly Financials (Locked)", font=ctk.CTkFont(family=APP_FONT, size=16, weight="bold"), text_color=TEXT_SUB).pack(pady=(20, 15), anchor="w", padx=20)

        right_scroll = ctk.CTkScrollableFrame(right_card, fg_color="transparent")
        right_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        row_idx = 0
        for key in fin_record.keys():
            if key in ["STAFF NAME", "Txn_ID", "Payroll_Month", "Payroll_Year", "DESIGNATION", "GRADE LEVEL"]: continue
            val = fin_record[key]
            
            if isinstance(val, (int, float)): display_val = f"₦ {val:,.2f}"
            else: display_val = str(val) if val is not None else ""

            lbl = ctk.CTkLabel(right_scroll, text=f"{key}:", font=ctk.CTkFont(family=APP_FONT, size=11), text_color=TEXT_SUB)
            lbl.grid(row=row_idx, column=0, padx=10, pady=6, sticky="w")
            
            entry = ctk.CTkEntry(right_scroll, width=180, height=28, font=ctk.CTkFont(family=APP_FONT, size=11, weight="bold"), fg_color=BG_MAIN, border_color=BG_SIDEBAR, text_color=TEXT_MAIN)
            entry.grid(row=row_idx, column=1, padx=10, pady=6, sticky="w")
            entry.insert(0, display_val)
            entry.configure(state="disabled")
            
            row_idx += 1

        # --- COMMAND CENTER FRAME ---
        command_frame = ctk.CTkFrame(profile_window, fg_color=BG_CARD, corner_radius=8)
        command_frame.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(command_frame, text="⚙️ Payslip Command Center", font=ctk.CTkFont(family=APP_FONT, weight="bold"), text_color=WARNING_ORANGE).pack(pady=(5,0))

        selectors_frame = ctk.CTkFrame(command_frame, fg_color="transparent")
        selectors_frame.pack(pady=5)
        
        ctk.CTkLabel(selectors_frame, text="From:").grid(row=0, column=0, padx=5)
        cmd_start_m = ctk.CTkComboBox(selectors_frame, values=list(self.month_map.keys()), width=100)
        cmd_start_m.grid(row=0, column=1, padx=5)
        cmd_start_m.set(self.dash_start_m.get()) 
        
        cmd_start_y = ctk.CTkComboBox(selectors_frame, values=YEAR_RANGE, width=80)
        cmd_start_y.grid(row=0, column=2, padx=5)
        cmd_start_y.set(self.dash_start_y.get())

        ctk.CTkLabel(selectors_frame, text="To:").grid(row=0, column=3, padx=5)
        cmd_end_m = ctk.CTkComboBox(selectors_frame, values=list(self.month_map.keys()), width=100)
        cmd_end_m.grid(row=0, column=4, padx=5)
        cmd_end_m.set(self.dash_end_m.get())
        
        cmd_end_y = ctk.CTkComboBox(selectors_frame, values=YEAR_RANGE, width=80)
        cmd_end_y.grid(row=0, column=5, padx=5)
        cmd_end_y.set(self.dash_end_y.get())

        popup_action_frame = ctk.CTkFrame(profile_window, fg_color="transparent")
        popup_action_frame.pack(pady=10, side="bottom")

        btn_save = ctk.CTkButton(popup_action_frame, text="💾 Save Identity", font=ctk.CTkFont(family=APP_FONT, weight="bold"), height=35, fg_color=SUCCESS, hover_color="#047857", command=lambda: self.save_staff_profile(staff_name, profile_window))
        btn_save.grid(row=0, column=0, padx=10)

        # 🛡️ THE VISUAL LOCK: Passing the actual button into the function to disable it immediately
        btn_smart_print = ctk.CTkButton(popup_action_frame, text="🖨️ Print Payslip(s)", font=ctk.CTkFont(family=APP_FONT, weight="bold"), height=35, fg_color=WARNING_ORANGE)
        btn_smart_print.configure(command=lambda b=btn_smart_print: self.cmd_smart_action(staff_name, cmd_start_m.get(), cmd_start_y.get(), cmd_end_m.get(), cmd_end_y.get(), "print", profile_window, b))
        btn_smart_print.grid(row=0, column=1, padx=10)

        btn_smart_email = ctk.CTkButton(popup_action_frame, text="📧 Email Payslip(s)", font=ctk.CTkFont(family=APP_FONT, weight="bold"), height=35, fg_color="#3B82F6")
        btn_smart_email.configure(command=lambda b=btn_smart_email: self.cmd_smart_action(staff_name, cmd_start_m.get(), cmd_start_y.get(), cmd_end_m.get(), cmd_end_y.get(), "email", profile_window, b))
        btn_smart_email.grid(row=0, column=2, padx=10)

    # --- COMMAND CENTER: SMART ACTION ENGINE ---
    def cmd_smart_action(self, staff_name, start_m_str, start_y_str, end_m_str, end_y_str, action, window, clicked_button=None):
        """Intelligently processes payslips with a physical UI lock and duplicate destruction."""
        
        # 🛡️ PHYSICAL UI LOCK: Immediately gray out the button so it literally cannot be clicked twice
        if clicked_button:
            clicked_button.configure(state="disabled", text="Processing...")
            self.update() # Force the UI to visually update the button instantly
        
        try:
            start_val = (int(start_y_str) * 12) + self.month_map[start_m_str]
            end_val = (int(end_y_str) * 12) + self.month_map[end_m_str]

            if start_val > end_val:
                messagebox.showerror("Date Error", "Oga, the Start Date cannot be after the End Date.", parent=window)
                return

            is_single_month = (start_val == end_val)

            conn = sqlite3.connect("payroll_vault.db")
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM tbl_Staff_Profiles WHERE "STAFF NAME" = ?', (staff_name,))
            profile = cursor.fetchone()
            
            cursor.execute('''
                SELECT * FROM master_payroll 
                WHERE "STAFF NAME" = ? 
                AND (CAST("Payroll_Year" AS INTEGER) * 12 + CAST("Payroll_Month" AS INTEGER)) >= ? 
                AND (CAST("Payroll_Year" AS INTEGER) * 12 + CAST("Payroll_Month" AS INTEGER)) <= ?
            ''', (staff_name, start_val, end_val))
            raw_records = cursor.fetchall()
            conn.close()

            if not raw_records:
                messagebox.showerror("No Data", f"No records found for {staff_name} in that date range.", parent=window)
                return
                
            # 🛡️ THE TWIN KILLER: Ruthlessly destroy duplicate months
            unique_records = {}
            for rec in raw_records:
                month_key = f"{rec['Payroll_Year']}_{rec['Payroll_Month']}"
                unique_records[month_key] = rec 
                
            records = list(unique_records.values())
            
            generated_pdfs = []
            for rec in records:
                staff_data = dict(rec)
                if profile: staff_data.update(dict(profile))
                
                m_num = rec["Payroll_Month"]
                month_name = list(self.month_map.keys())[list(self.month_map.values()).index(m_num)]
                year_val = str(rec["Payroll_Year"])
                
                pdf_path = payslip_engine.generate_live_payslip(staff_data, month_name, year_val)
                generated_pdfs.append(pdf_path)
                
            if action == "print":
                for path in set(generated_pdfs): 
                    os.startfile(path)
                
                # 🎯 TRACER BULLET MESSAGE
                if is_single_month:
                    messagebox.showinfo("Success", "Gbosa! THE VAULT IS SECURE! Printed 1 single payslip.", parent=window)
                else:
                    messagebox.showinfo("Success", f"Gbosa! THE VAULT IS SECURE! Printed {len(generated_pdfs)} payslips.", parent=window)
                    
            elif action == "email":
                email_addr = profile["EMAIL"] if profile and profile["EMAIL"] else ""
                if not email_addr or "@" not in email_addr:
                    messagebox.showerror("Email Error", f"Valid email not found in profile for {staff_name}.", parent=window)
                    return
                    
                try:
                    outlook_app = win32com.client.Dispatch("Outlook.Application")
                    mail = outlook_app.CreateItem(0)
                    mail.To = email_addr
                    
                    if is_single_month:
                        mail.Subject = f"NILDS Payslip: {start_m_str} {start_y_str}"
                        mail.Body = f"Dear {staff_name},\n\nPlease find attached your payslip for {start_m_str} {start_y_str}.\n\nRegards,\nFinance & Accounts\nNILDS"
                    else:
                        mail.Subject = f"NILDS Payslips: {start_m_str} {start_y_str} - {end_m_str} {end_y_str}"
                        mail.Body = f"Dear {staff_name},\n\nPlease find attached your payslips for the requested period.\n\nRegards,\nFinance & Accounts\nNILDS"
                    
                    for path in set(generated_pdfs): mail.Attachments.Add(path)
                    mail.Send()
                    
                    try:
                        namespace = outlook_app.GetNamespace("MAPI")
                        for i in range(1, namespace.SyncObjects.Count + 1):
                            namespace.SyncObjects.Item(i).Start()
                    except: pass 
                    
                    # 🎯 TRACER BULLET MESSAGE
                    qty_text = "1 payslip" if is_single_month else f"{len(generated_pdfs)} payslips"
                    messagebox.showinfo("Success", f"Gbosa! THE VAULT IS SECURE! Pushed {qty_text} to Outlook for {email_addr}.", parent=window)
                except Exception as e:
                    messagebox.showerror("Outlook Error", f"Failed to send email: {e}", parent=window)
                    
        except Exception as e:
            print(f"Error in Smart Action: {e}")
            
        finally:
            # 🛡️ UNLOCK THE UI
            if clicked_button:
                original_text = "🖨️ Print Payslip(s)" if action == "print" else "📧 Email Payslip(s)"
                clicked_button.configure(state="normal", text=original_text)       
        # 5. Generate the PDFs in the background
        generated_pdfs = []
        for rec in records:
            staff_data = dict(rec)
            if profile: staff_data.update(dict(profile))
            
            m_num = rec["Payroll_Month"]
            month_name = list(self.month_map.keys())[list(self.month_map.values()).index(m_num)]
            year_val = str(rec["Payroll_Year"])
            
            pdf_path = payslip_engine.generate_live_payslip(staff_data, month_name, year_val)
            generated_pdfs.append(pdf_path)
            
        # 6. Execute the Requested Action (Print or Email)
        if action == "print":
            for path in generated_pdfs:
                os.startfile(path)
                
            if not is_single_month:
                messagebox.showinfo("Success", f"Generated and opened {len(generated_pdfs)} payslips for printing.", parent=window)
                
        elif action == "email":
            email_addr = profile["EMAIL"] if profile and profile["EMAIL"] else ""
            if not email_addr or "@" not in email_addr:
                messagebox.showerror("Email Error", f"Valid email not found in profile for {staff_name}.", parent=window)
                return
                
            try:
                outlook_app = win32com.client.Dispatch("Outlook.Application")
                mail = outlook_app.CreateItem(0)
                mail.To = email_addr
                
                # Smart Subject & Body based on context
                if is_single_month:
                    mail.Subject = f"NILDS Payslip: {start_m_str} {start_y_str}"
                    mail.Body = f"Dear {staff_name},\n\nPlease find attached your payslip for {start_m_str} {start_y_str}.\n\nRegards,\nFinance & Accounts\nNILDS"
                else:
                    mail.Subject = f"NILDS Payslips: {start_m_str} {start_y_str} - {end_m_str} {end_y_str}"
                    mail.Body = f"Dear {staff_name},\n\nPlease find attached your payslips for the requested period.\n\nRegards,\nFinance & Accounts\nNILDS"
                
                for path in generated_pdfs:
                    mail.Attachments.Add(path)
                    
                mail.Send()
                
                # Smart Success Message
                qty_text = "1 payslip" if is_single_month else f"{len(generated_pdfs)} payslips"
                messagebox.showinfo("Success", f"Gbosa! Emailed {qty_text} to {email_addr}.", parent=window)
            except Exception as e:
                messagebox.showerror("Outlook Error", f"Failed to send email: {e}", parent=window)
                               
    def save_staff_profile(self, staff_name, window):
        email = self.editable_entries["EMAIL"].get()
        bank = self.editable_entries["BANK"].get()
        acct = self.editable_entries["ACCT NO"].get()
        pfa = self.editable_entries["PFA"].get()
        pen_no = self.editable_entries["PENSION NO"].get()
        
        try:
            conn = sqlite3.connect("payroll_vault.db")
            cursor = conn.cursor()
            cursor.execute('UPDATE tbl_Staff_Profiles SET "EMAIL" = ?, "BANK" = ?, "ACCT NO" = ?, "PFA" = ?, "PENSION NO" = ? WHERE "STAFF NAME" = ?', (email, bank, acct, pfa, pen_no, staff_name))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Profile updated globally for {staff_name}!", parent=window)
            window.destroy()
            self.load_dashboard_metrics()
        except Exception as e:
            messagebox.showerror("Error", f"Could not save profile: {e}", parent=window)

    def trigger_pdf_print(self, staff_data, month_name, year):
        try: 
            os.startfile(payslip_engine.generate_live_payslip(staff_data, month_name, year))
        except Exception as e: 
            print(f"Error: {e}")
    # --- BATCH LOGIC ---
    def init_batch_checklist(self):
        self.master_staff_vars.clear()
        try:
            conn = sqlite3.connect("payroll_vault.db")
            cursor = conn.cursor()
            cursor.execute('SELECT "STAFF NAME" FROM tbl_Staff_Profiles ORDER BY "STAFF NAME" ASC')
            for row in cursor.fetchall(): self.master_staff_vars[row[0]] = ctk.BooleanVar(value=False)
            conn.close()
            self.filter_checklist_ui(None) 
        except: pass

    def filter_checklist_ui(self, event):
        for widget in self.staff_checklist_frame.winfo_children(): widget.destroy()
        search_query = self.chk_search.get().strip().lower()
        for name, var in self.master_staff_vars.items():
            if search_query in name.lower():
                ctk.CTkCheckBox(self.staff_checklist_frame, text=name, font=ctk.CTkFont(family=APP_FONT), variable=var, fg_color=ACCENT).pack(anchor="w", pady=4, padx=5)

    def select_all_staff(self):
        q = self.chk_search.get().strip().lower()
        for name, var in self.master_staff_vars.items():
            if q in name.lower(): var.set(True)

    def clear_all_staff(self):
        for var in self.master_staff_vars.values(): var.set(False)

    def log_msg(self, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
        self.update()

    def stop_batch(self):
        self.batch_running = False
        self.log_msg("⚠️ EMERGENCY STOP INITIATED...")

    def start_batch_thread(self):
        if self.batch_running: return
        self.batch_running = True
        self.btn_start_batch.configure(state="disabled")
        self.btn_stop_batch.configure(state="normal")
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
        self.progress_bar.set(0)
        threading.Thread(target=self.run_batch_process).start()

    def run_batch_process(self):
        try:
            start_m, start_y = self.month_map[self.batch_start_m.get()], int(self.batch_start_y.get())
            end_m, end_y = self.month_map[self.batch_end_m.get()], int(self.batch_end_y.get())
            start_val, end_val = (start_y * 12) + start_m, (end_y * 12) + end_m

            if start_val > end_val:
                self.log_msg("❌ Error: Start Date after End Date."); self.finish_batch(); return

            selected_staff = [name for name, var in self.master_staff_vars.items() if var.get()]
            if not selected_staff:
                self.log_msg("❌ Error: Select a staff member."); self.finish_batch(); return

            mode = self.dispatch_mode.get()
            self.log_msg(f"🎯 SNIPER MODE: {len(selected_staff)} Staff Selected.")
            
            outlook_app = win32com.client.Dispatch("Outlook.Application") if OUTLOOK_AVAILABLE else None
            
            conn = sqlite3.connect("payroll_vault.db")
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()
            placeholders = ','.join(['?'] * len(selected_staff))
            query = f'''SELECT m.*, p."EMAIL" FROM master_payroll m LEFT JOIN tbl_Staff_Profiles p ON m."STAFF NAME" = p."STAFF NAME" WHERE (m."Payroll_Year" * 12 + m."Payroll_Month") >= ? AND (m."Payroll_Year" * 12 + m."Payroll_Month") <= ? AND m."STAFF NAME" IN ({placeholders})'''
            cursor.execute(query, tuple([start_val, end_val] + selected_staff))
            records = cursor.fetchall()
            conn.close()

            total_records = len(records)
            if total_records == 0:
                self.log_msg("⚠️ No records found."); self.finish_batch(); return

            count_success = 0
            for i, row in enumerate(records):
                if not self.batch_running: break
                data = dict(row)
                staff_name, email = data.get("STAFF NAME", "Unknown"), str(data.get("EMAIL", "")).strip()
                if email == "None" or email == "nan": email = ""
                month_name, year = list(self.month_map.keys())[list(self.month_map.values()).index(data["Payroll_Month"])], data["Payroll_Year"]

                pdf_path = payslip_engine.generate_live_payslip(data, month_name, year)

                if outlook_app:
                    if "@" in email:
                        mail = outlook_app.CreateItem(0)
                        mail.To, mail.Subject = email, f"NILDS Payslip - {month_name} {year}"
                        mail.Body = f"Dear {staff_name},\n\nPlease find attached your payslip for {month_name} {year}.\n\nRegards,\nFinance & Accounts\nNILDS"
                        mail.Attachments.Add(pdf_path)
                        if mode == "Send Immediately 🚀": mail.Send()
                        else: mail.Save() 
                        self.log_msg(f"✅ [{i+1}/{total_records}] Processed: {staff_name}"); count_success += 1
                    else: self.log_msg(f"📄 [{i+1}/{total_records}] PDF ONLY (No Email): {staff_name}")

                self.progress_bar.set((i + 1) / total_records)
                self.update_idletasks() 

            self.log_msg(f"🎉 COMPLETE! Processed {count_success} emails."); self.finish_batch()
        except Exception as e: self.log_msg(f"❌ ERROR: {e}"); self.finish_batch()

    def finish_batch(self):
        self.batch_running = False
        self.btn_start_batch.configure(state="normal")
        self.btn_stop_batch.configure(state="disabled")

    # --- ADMIN SETTINGS LOGIC ---
    def refresh_user_list(self):
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        conn = sqlite3.connect("payroll_vault.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, access_level, last_login FROM tbl_Users")
        for row in cursor.fetchall():
            self.user_tree.insert("", "end", values=row)
        conn.close()

    def add_system_user(self):
        u = self.new_username.get().strip()
        p = self.new_password.get().strip()
        a = self.access_lvl.get()
        if u and p:
            try:
                conn = sqlite3.connect("payroll_vault.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO tbl_Users (username, password, access_level) VALUES (?, ?, ?)", (u, p, a))
                conn.commit()
                conn.close()
                self.refresh_user_list()
                self.new_username.delete(0, 'end')
                self.new_password.delete(0, 'end')
                messagebox.showinfo("Success", f"User {u} added successfully!", parent=self)
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists!", parent=self)
        else:
            messagebox.showwarning("Input Error", "Please provide both Username and Password.", parent=self)

    def delete_system_user(self):
        selected = self.user_tree.selection()
        if not selected: return
        user_to_del = self.user_tree.item(selected[0])['values'][0]
        if user_to_del == "admin":
            messagebox.showerror("Denied", "You cannot delete the Master Admin account.", parent=self)
            return
        
        if messagebox.askyesno("Confirm", f"Delete access for {user_to_del}?", parent=self):
            conn = sqlite3.connect("payroll_vault.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tbl_Users WHERE username=?", (user_to_del,))
            conn.commit()
            conn.close()
            self.refresh_user_list()

    # --- SESSION MANAGEMENT ---
    def logout_user(self):
        if messagebox.askyesno("Secure Logout", "Oga Chief, are you sure you want to lock the vault and log out?", parent=self):
            self.destroy()  # Close the dashboard and kill its mainloop
            login_screen = LoginGate()  # Re-initialize the login gate
            login_screen.mainloop()


# --- 🔐 THE SECURITY GATE (NEW IN V4.6) ---
class LoginGate(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 🔥 FIX: Ensure table exists before anything else happens
        self.ensure_user_table_exists()

        self.title("Vault Security")
        self.geometry("400x500")
        self.configure(fg_color=BG_MAIN)
        self.eval('tk::PlaceWindow . center') 
        
        # Center the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # UI Elements
        self.logo = ctk.CTkLabel(self, text="🛡️\nHAWEA SECURE", font=ctk.CTkFont(family=APP_FONT, size=24, weight="bold"), text_color=SUCCESS)
        self.logo.grid(row=1, column=0, pady=(0, 30))

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Admin Username", width=250, height=45, font=ctk.CTkFont(family=APP_FONT, size=14), fg_color=BG_CARD, border_color=BG_SIDEBAR, corner_radius=8)
        self.username_entry.grid(row=2, column=0, pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Master Password", width=250, height=45, show="*", font=ctk.CTkFont(family=APP_FONT, size=14), fg_color=BG_CARD, border_color=BG_SIDEBAR, corner_radius=8)
        self.password_entry.grid(row=3, column=0, pady=10)
        self.password_entry.bind("<Return>", lambda event: self.verify_credentials())

        self.btn_login = ctk.CTkButton(self, text="AUTHORIZE ACCESS", font=ctk.CTkFont(family=APP_FONT, weight="bold"), width=250, height=45, corner_radius=8, fg_color=ACCENT, command=self.verify_credentials)
        self.btn_login.grid(row=4, column=0, pady=30)

    def ensure_user_table_exists(self):
        """Self-healing specifically for the login gate before Dashboard loads."""
        conn = sqlite3.connect("payroll_vault.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tbl_Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                access_level TEXT DEFAULT 'Admin',
                last_login TEXT
            )
        ''')
        cursor.execute("SELECT COUNT(*) FROM tbl_Users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO tbl_Users (username, password, access_level) VALUES (?, ?, ?)", 
                           ('admin', 'hawea2026', 'SuperAdmin'))
        conn.commit()
        conn.close()

    def verify_credentials(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()

        try:
            conn = sqlite3.connect("payroll_vault.db")
            cursor = conn.cursor()
            
            # Check if user exists with that password
            cursor.execute("SELECT * FROM tbl_Users WHERE username=? AND password=?", (user, pwd))
            result = cursor.fetchone()

            if result:
                # Update last login time
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                cursor.execute("UPDATE tbl_Users SET last_login=? WHERE username=?", (now, user))
                conn.commit()
                conn.close()
                
                self.destroy() 
                launch_dashboard() 
            else:
                conn.close()
                self.username_entry.configure(border_color=WARNING_RED)
                self.password_entry.configure(border_color=WARNING_RED)
                messagebox.showerror("Access Denied", "Invalid Credentials. The Vault remains locked.", parent=self)
        except Exception as e:
            messagebox.showerror("System Error", f"Login Gate failed: {e}")
            
def launch_dashboard():
    app = PayrollDashboard()
    app.mainloop()

if __name__ == "__main__":
    login_screen = LoginGate()
    login_screen.mainloop()