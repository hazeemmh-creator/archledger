import customtkinter as ctk

# Set the appearance and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class PayrollDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Configure Window
        self.title("Hawea Heritage - Payroll Vault v2.0")
        self.geometry("1100x600")

        # 2. Create Grid Layout (4 columns, 4 rows)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # 3. Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        
        # Sidebar Title
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="PAYROLL VAULT", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # 4. Navigation Buttons
        self.btn_dashboard = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.sidebar_button_event)
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=10)

        self.btn_employees = ctk.CTkButton(self.sidebar_frame, text="Employees", command=self.sidebar_button_event)
        self.btn_employees.grid(row=2, column=0, padx=20, pady=10)

        # 5. Main Content Area (Welcome Greeting)
        self.label_welcome = ctk.CTkLabel(self, text="Welcome, Oga Chief!", font=ctk.CTkFont(size=30, weight="bold"))
        self.label_welcome.grid(row=0, column=1, padx=20, pady=20)

    def sidebar_button_event(self):
        print("Sidebar button clicked")

if __name__ == "__main__":
    app = PayrollDashboard()
    app.mainloop()