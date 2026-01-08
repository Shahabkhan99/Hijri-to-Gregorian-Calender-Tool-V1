# Version: 1.2.0 (Internal Ref: SGAI-Theme-Footer-Update)
import tkinter as tk
from tkinter import ttk, messagebox
from hijri_converter import convert
import calendar
from datetime import datetime, date

class DualCalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hijri & Gregorian Calendar Tool")
        self.root.geometry("700x700")
        
        # Theme State (Default: Dark Mode)
        self.is_dark_mode = True
        
        # Color Palettes
        self.colors = {
            'light': {
                'bg': '#f0f0f0', 'fg': '#000000', 
                'frame_bg': '#ffffff', 'cal_bg': '#ffffff',
                'cal_text': '#000000', 'header_bg': '#e0e0e0',
                'today_bg': '#e3f2fd', 'h_text': '#d81b60',
                'input_bg': '#ffffff', 'input_fg': '#000000',
                'footer': '#555555'
            },
            'dark': {
                'bg': '#2d2d2d', 'fg': '#ffffff', 
                'frame_bg': '#3d3d3d', 'cal_bg': '#3d3d3d',
                'cal_text': '#ffffff', 'header_bg': '#505050',
                'today_bg': '#1a4e6e', 'h_text': '#ff80ab',
                'input_bg': '#505050', 'input_fg': '#ffffff',
                'footer': '#bbbbbb'
            }
        }

        # Initialize Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Main Container
        self.main_container = tk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Header with Theme Toggle
        header_frame = tk.Frame(self.main_container)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Button text logic inverted because default is now Dark
        btn_text = "☀️ Day Mode" if self.is_dark_mode else "🌙 Night Mode"
        self.theme_btn = tk.Button(header_frame, text=btn_text, command=self.toggle_theme, 
                                   font=("Helvetica", 10), cursor="hand2")
        self.theme_btn.pack(side=tk.RIGHT)

        # --- SECTION 1: CONVERTER ---
        self.convert_frame = ttk.LabelFrame(self.main_container, text="Date Converter", padding="15")
        self.convert_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Gregorian to Hijri
        ttk.Label(self.convert_frame, text="Gregorian (dd-mmm-yyyy):").grid(row=0, column=0, padx=5, sticky="w")
        self.g_entry = ttk.Entry(self.convert_frame, width=15)
        # Default to today
        self.g_entry.insert(0, datetime.today().strftime('%d-%b-%Y'))
        self.g_entry.grid(row=0, column=1, padx=5)
        
        btn_g2h = ttk.Button(self.convert_frame, text="Convert to Hijri >", command=self.convert_g_to_h)
        btn_g2h.grid(row=0, column=2, padx=5)
        
        self.res_h = ttk.Label(self.convert_frame, text="Result: -", font=("Helvetica", 11, "bold"))
        self.res_h.grid(row=0, column=3, padx=10)

        # Hijri to Gregorian
        ttk.Label(self.convert_frame, text="Hijri (dd-mm-yyyy):").grid(row=1, column=0, padx=5, sticky="w", pady=10)
        self.h_entry = ttk.Entry(self.convert_frame, width=15)
        self.h_entry.grid(row=1, column=1, padx=5, pady=10)
        
        btn_h2g = ttk.Button(self.convert_frame, text="Convert to Gregorian >", command=self.convert_h_to_g)
        btn_h2g.grid(row=1, column=2, padx=5, pady=10)
        
        self.res_g = ttk.Label(self.convert_frame, text="Result: -", font=("Helvetica", 11, "bold"))
        self.res_g.grid(row=1, column=3, padx=10, pady=10)

        # --- SECTION 2: CALENDAR ---
        self.cal_frame = ttk.LabelFrame(self.main_container, text="Current Month Dual Calendar", padding="10")
        self.cal_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        # Navigation
        nav_frame = ttk.Frame(self.cal_frame)
        nav_frame.pack(fill=tk.X, pady=5)
        
        self.current_view_date = datetime.today()
        
        self.lbl_month = ttk.Label(nav_frame, text="", font=("Helvetica", 14, "bold"))
        self.lbl_month.pack(side=tk.LEFT, padx=10)
        
        btn_next = ttk.Button(nav_frame, text="Next >", command=lambda: self.change_month(1))
        btn_next.pack(side=tk.RIGHT)
        
        btn_prev = ttk.Button(nav_frame, text="< Prev", command=lambda: self.change_month(-1))
        btn_prev.pack(side=tk.RIGHT, padx=5)

        # Calendar Grid Frame
        self.cal_grid = tk.Frame(self.cal_frame)
        self.cal_grid.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # --- FOOTER ---
        self.footer_lbl = tk.Label(self.main_container, text="Power by SGAI... Ver 01.00", 
                                   font=("Arial", 9, "italic"))
        self.footer_lbl.pack(side=tk.BOTTOM, pady=(0, 10))

        # Apply initial theme
        self.apply_theme()
        self.draw_calendar()

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.theme_btn.config(text="☀️ Day Mode" if self.is_dark_mode else "🌙 Night Mode")
        self.apply_theme()
        self.draw_calendar() 

    def apply_theme(self):
        mode = 'dark' if self.is_dark_mode else 'light'
        c = self.colors[mode]
        
        # Root and Main Container
        self.root.configure(bg=c['bg'])
        self.main_container.configure(bg=c['bg'])
        self.cal_grid.configure(bg=c['bg'])
        header_bg_current = c['header_bg'] if 'header_bg' in c else c['bg'] # Fallback
        
        # Footer
        self.footer_lbl.configure(bg=c['bg'], fg=c['footer'])

        # TTK Styles
        self.style.configure("TLabel", background=c['frame_bg'], foreground=c['fg'])
        self.style.configure("Header.TLabel", background=c['frame_bg'], foreground=c['fg'])
        self.style.configure("TLabelframe", background=c['frame_bg'], foreground=c['fg'])
        self.style.configure("TLabelframe.Label", background=c['frame_bg'], foreground=c['fg'])
        self.style.configure("TFrame", background=c['frame_bg'])
        self.style.configure("TEntry", fieldbackground=c['input_bg'], foreground=c['input_fg'])
        
        # Standard TK Widgets 
        self.theme_btn.configure(bg=c['header_bg'], fg=c['fg'])
        
        # Result Labels specific colors
        self.res_h.configure(foreground="#007BFF" if not self.is_dark_mode else "#4eaeff")
        self.res_g.configure(foreground="#007BFF" if not self.is_dark_mode else "#4eaeff")

    def convert_g_to_h(self):
        try:
            d_str = self.g_entry.get()
            # Parse dd-mmm-yyyy (e.g., 01-Jan-2026)
            dt = datetime.strptime(d_str, '%d-%b-%Y')
            h_date = convert.Gregorian(dt.year, dt.month, dt.day).to_hijri()
            self.res_h.config(text=f"{h_date.day}-{h_date.month_name()}-{h_date.year}")
        except ValueError:
            self.res_h.config(text="Format Error")
        except Exception:
            self.res_h.config(text="Error")

    def convert_h_to_g(self):
        try:
            d_str = self.h_entry.get()
            # Expecting dd-mm-yyyy for input simplicity
            d, m, y = map(int, d_str.split('-'))
            g_date = convert.Hijri(y, m, d).to_gregorian()
            dt = date(g_date.year, g_date.month, g_date.day)
            self.res_g.config(text=dt.strftime('%d-%b-%Y'))
        except ValueError:
            self.res_g.config(text="Format Error")
        except Exception:
            self.res_g.config(text="Error")

    def change_month(self, step):
        m = self.current_view_date.month + step
        y = self.current_view_date.year
        if m > 12:
            m = 1
            y += 1
        elif m < 1:
            m = 12
            y -= 1
        self.current_view_date = self.current_view_date.replace(year=y, month=m, day=1)
        self.draw_calendar()

    def draw_calendar(self):
        mode = 'dark' if self.is_dark_mode else 'light'
        c = self.colors[mode]

        # Clear grid
        for widget in self.cal_grid.winfo_children():
            widget.destroy()

        # Update Header
        month_name = calendar.month_name[self.current_view_date.month]
        year = self.current_view_date.year
        self.lbl_month.config(text=f"{month_name} {year}")

        # Days of Week Headers
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            lbl = tk.Label(self.cal_grid, text=day, bg=c['header_bg'], fg=c['fg'], 
                           font=("Arial", 10, "bold"), pady=5)
            lbl.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        cal = calendar.monthcalendar(year, self.current_view_date.month)
        
        for r, week in enumerate(cal):
            for col, day in enumerate(week):
                if day == 0:
                    bg_color = c['bg']
                    txt = ""
                    h_txt = ""
                    border = 0
                else:
                    bg_color = c['cal_bg']
                    border = 1
                    
                    g_date_obj = date(year, self.current_view_date.month, day)
                    h_date_obj = convert.Gregorian(year, self.current_view_date.month, day).to_hijri()
                    
                    txt = str(day)
                    h_txt = f"{h_date_obj.day}/{h_date_obj.month}"
                    
                    # Highlight today
                    if g_date_obj == date.today():
                        bg_color = c['today_bg']

                cell = tk.Frame(self.cal_grid, bg=bg_color, borderwidth=border, relief="solid")
                cell.grid(row=r+1, column=col, sticky="nsew", padx=1, pady=1)
                
                if day != 0:
                    tk.Label(cell, text=txt, bg=bg_color, fg=c['cal_text'], 
                             font=("Arial", 12, "bold")).pack(anchor="nw", padx=2)
                    tk.Label(cell, text=h_txt, bg=bg_color, fg=c['h_text'], 
                             font=("Arial", 9)).pack(anchor="se", padx=2)

        for i in range(7):
            self.cal_grid.columnconfigure(i, weight=1)
        for i in range(len(cal) + 1):
            self.cal_grid.rowconfigure(i, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = DualCalendarApp(root)
    root.mainloop()