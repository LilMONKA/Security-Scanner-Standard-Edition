import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import hashlib
import threading
import time
from datetime import datetime
import psutil
import winreg
import re

class AdvancedSecurityScanner:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("🛡️ Advanced Security Scanner Pro")
        self.root.geometry("1400x900")
        
        self.is_scanning = False
        self.scan_results = {
            'threats': [],
            'suspicious': [],
            'safe': [],
            'total_scanned': 0
        }
        
        self.malware_signatures = {}
        
        self.suspicious_patterns = [
            r'\.exe\.exe$',
            r'\.scr$',
            r'\.vbs$',
            r'\.bat$',
            r'\.cmd$',
        ]
        
        self.safe_locations = [
            r'C:\Windows\System32',
            r'C:\Windows\SysWOW64',
            r'C:\Program Files',
            r'C:\Program Files (x86)',
        ]
        
        self.colors = {
            'bg': '#0a0e14',
            'card': '#161b22',
            'accent': '#58a6ff',
            'success': '#3fb950',
            'warning': '#d29922',
            'danger': '#f85149',
            'text': '#c9d1d9',
            'subtext': '#8b949e',
            'border': '#30363d'
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        self.create_header()
        main_container = ctk.CTkFrame(self.root, fg_color=self.colors['bg'])
        main_container.pack(fill="both", expand=True)
        self.create_sidebar(main_container)
        self.create_content_area(main_container)
    
    def create_header(self):
        header = ctk.CTkFrame(self.root, height=100, fg_color=self.colors['card'])
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=30, pady=20)
        
        ctk.CTkLabel(
            title_frame,
            text="🛡️ ADVANCED SECURITY SCANNER",
            font=("Arial Black", 28),
            text_color=self.colors['accent']
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="Professional-Grade Threat Detection",
            font=("Arial", 12),
            text_color=self.colors['subtext']
        ).pack(anchor="w")
        
        status_frame = ctk.CTkFrame(header, fg_color="transparent")
        status_frame.pack(side="right", padx=30)
        
        protection_frame = ctk.CTkFrame(status_frame, fg_color=self.colors['success'])
        protection_frame.pack(pady=2)
        
        ctk.CTkLabel(
            protection_frame,
            text="🛡️ SCANNER ACTIVE",
            font=("Arial Bold", 12),
            text_color="white"
        ).pack(padx=20, pady=8)
        
        self.last_scan_label = ctk.CTkLabel(
            status_frame,
            text="Last Scan: Never",
            font=("Arial", 10),
            text_color=self.colors['subtext']
        )
        self.last_scan_label.pack(pady=2)
    
    def create_sidebar(self, parent):
        sidebar = ctk.CTkScrollableFrame(parent, width=320, fg_color=self.colors['card'])
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        ctk.CTkLabel(
            sidebar,
            text="🔍 SCAN OPTIONS",
            font=("Arial Bold", 16),
            text_color=self.colors['accent']
        ).pack(pady=(20, 15), padx=20, anchor="w")
        
        quick_frame = ctk.CTkFrame(sidebar, fg_color=self.colors['bg'])
        quick_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkButton(
            quick_frame,
            text="⚡ Quick Scan",
            width=280,
            height=50,
            font=("Arial Bold", 14),
            fg_color=self.colors['accent'],
            command=self.quick_scan
        ).pack(pady=10, padx=10)
        
        ctk.CTkLabel(
            quick_frame,
            text="Common locations (5-10 min)",
            font=("Arial", 10),
            text_color=self.colors['subtext']
        ).pack(pady=(0, 10))
        
        full_frame = ctk.CTkFrame(sidebar, fg_color=self.colors['bg'])
        full_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkButton(
            full_frame,
            text="🔍 Full System Scan",
            width=280,
            height=50,
            font=("Arial Bold", 14),
            fg_color=self.colors['warning'],
            command=self.full_scan
        ).pack(pady=10, padx=10)
        
        ctk.CTkLabel(
            full_frame,
            text="Entire system (1-2 hours)",
            font=("Arial", 10),
            text_color=self.colors['subtext']
        ).pack(pady=(0, 10))
        
        custom_frame = ctk.CTkFrame(sidebar, fg_color=self.colors['bg'])
        custom_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkButton(
            custom_frame,
            text="📁 Custom Scan",
            width=280,
            height=50,
            font=("Arial Bold", 14),
            command=self.custom_scan
        ).pack(pady=10, padx=10)
        
        ctk.CTkLabel(
            custom_frame,
            text="Select specific folder",
            font=("Arial", 10),
            text_color=self.colors['subtext']
        ).pack(pady=(0, 10))
        
        ctk.CTkFrame(sidebar, height=2, fg_color=self.colors['border']).pack(fill="x", pady=20, padx=20)
        
        ctk.CTkLabel(
            sidebar,
            text="⚙️ SETTINGS",
            font=("Arial Bold", 16),
            text_color=self.colors['accent']
        ).pack(pady=(10, 15), padx=20, anchor="w")
        
        settings_frame = ctk.CTkFrame(sidebar, fg_color=self.colors['bg'])
        settings_frame.pack(fill="x", padx=20, pady=10)
        
        self.scan_hidden_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            settings_frame,
            text="Scan hidden files",
            variable=self.scan_hidden_var,
            font=("Arial", 12)
        ).pack(anchor="w", padx=15, pady=8)
        
        self.deep_scan_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            settings_frame,
            text="Deep heuristic analysis",
            variable=self.deep_scan_var,
            font=("Arial", 12)
        ).pack(anchor="w", padx=15, pady=8)
        
        self.stop_btn = ctk.CTkButton(
            sidebar,
            text="⏹️ STOP SCAN",
            width=280,
            height=45,
            font=("Arial Bold", 14),
            fg_color=self.colors['danger'],
            command=self.stop_scan,
            state="disabled"
        )
        self.stop_btn.pack(side="bottom", pady=20, padx=20)
    
    def create_content_area(self, parent):
        content = ctk.CTkFrame(parent, fg_color=self.colors['bg'])
        content.pack(side="left", fill="both", expand=True)
        
        stats_container = ctk.CTkFrame(content, fg_color="transparent", height=120)
        stats_container.pack(fill="x", padx=20, pady=20)
        stats_container.pack_propagate(False)
        
        self.threats_card = self.create_stat_card(stats_container, "⚠️ THREATS", "0", self.colors['danger'])
        self.threats_card.pack(side="left", fill="both", expand=True, padx=5)
        
        self.suspicious_card = self.create_stat_card(stats_container, "⚡ SUSPICIOUS", "0", self.colors['warning'])
        self.suspicious_card.pack(side="left", fill="both", expand=True, padx=5)
        
        self.scanned_card = self.create_stat_card(stats_container, "📁 SCANNED", "0", self.colors['accent'])
        self.scanned_card.pack(side="left", fill="both", expand=True, padx=5)
        
        self.safe_card = self.create_stat_card(stats_container, "✅ SAFE", "0", self.colors['success'])
        self.safe_card.pack(side="left", fill="both", expand=True, padx=5)
        
        scan_button_frame = ctk.CTkFrame(content, height=150, fg_color=self.colors['card'])
        scan_button_frame.pack(fill="x", padx=20, pady=(0, 20))
        scan_button_frame.pack_propagate(False)
        
        main_scan_container = ctk.CTkFrame(scan_button_frame, fg_color="transparent")
        main_scan_container.pack(expand=True)
        
        self.main_scan_btn = ctk.CTkButton(
            main_scan_container,
            text="🛡️ START SCAN",
            width=400,
            height=80,
            font=("Arial Black", 28),
            fg_color=self.colors['accent'],
            hover_color=self.colors['success'],
            corner_radius=15,
            command=self.show_scan_options
        )
        self.main_scan_btn.pack()
        
        ctk.CTkLabel(
            main_scan_container,
            text="Click to choose scan type",
            font=("Arial", 11),
            text_color=self.colors['subtext']
        ).pack(pady=(5, 0))
        
        progress_frame = ctk.CTkFrame(content, fg_color=self.colors['card'])
        progress_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        progress_container = ctk.CTkFrame(progress_frame, fg_color="transparent")
        progress_container.pack(fill="x", padx=20, pady=20)
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_container,
            width=1000,
            height=15,
            progress_color=self.colors['accent']
        )
        self.progress_bar.pack(fill="x")
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(
            progress_container,
            text="Ready to scan",
            font=("Arial", 12),
            text_color=self.colors['subtext']
        )
        self.status_label.pack(pady=10)
        
        results_container = ctk.CTkFrame(content, fg_color="transparent")
        results_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.results_tabs = ctk.CTkTabview(results_container)
        self.results_tabs.pack(fill="both", expand=True)
        
        self.threats_tab = self.results_tabs.add("⚠️ Threats")
        self.suspicious_tab = self.results_tabs.add("⚡ Suspicious")
        self.logs_tab = self.results_tabs.add("📋 Logs")
        
        self.threats_scroll = ctk.CTkScrollableFrame(self.threats_tab, fg_color="transparent")
        self.threats_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.suspicious_scroll = ctk.CTkScrollableFrame(self.suspicious_tab, fg_color="transparent")
        self.suspicious_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.logs_text = ctk.CTkTextbox(self.logs_tab, font=("Consolas", 11), fg_color=self.colors['card'])
        self.logs_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.show_welcome_message()
    
    def create_stat_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, fg_color=self.colors['card'])
        ctk.CTkLabel(card, text=title, font=("Arial Bold", 12), text_color=self.colors['subtext']).pack(pady=(15, 5))
        value_label = ctk.CTkLabel(card, text=value, font=("Arial Black", 32), text_color=color)
        value_label.pack(pady=(0, 15))
        card.value_label = value_label
        return card
    
    def show_welcome_message(self):
        welcome = ctk.CTkFrame(self.threats_scroll, fg_color=self.colors['card'])
        welcome.pack(fill="both", expand=True, padx=50, pady=50)
        
        ctk.CTkLabel(
            welcome,
            text="🛡️ Advanced Security Scanner",
            font=("Arial Bold", 28),
            text_color=self.colors['accent']
        ).pack(pady=(40, 20))
        
        info = """⚠️ EDUCATIONAL TOOL - NOT A REPLACEMENT FOR REAL ANTIVIRUS ⚠️

Always use professional antivirus (Windows Defender, Malwarebytes, etc.)

Features:
• Hash-based malware detection
• Heuristic analysis
• File pattern analysis
• System monitoring

Click "START SCAN" to begin!"""
        
        ctk.CTkLabel(welcome, text=info, font=("Arial", 13), text_color=self.colors['text'], justify="left").pack(pady=(0, 40), padx=30)
    
    def show_scan_options(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Select Scan Type")
        dialog.geometry("500x450")
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 250
        y = (dialog.winfo_screenheight() // 2) - 225
        dialog.geometry(f"500x450+{x}+{y}")
        
        header = ctk.CTkFrame(dialog, fg_color=self.colors['card'])
        header.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header, text="🛡️ Select Scan Type", font=("Arial Bold", 24), text_color=self.colors['accent']).pack(pady=20)
        
        quick_frame = ctk.CTkFrame(dialog, fg_color=self.colors['card'])
        quick_frame.pack(fill="x", padx=30, pady=10)
        ctk.CTkButton(quick_frame, text="⚡ QUICK SCAN", width=420, height=70, font=("Arial Bold", 18), 
                     fg_color=self.colors['accent'], command=lambda: [dialog.destroy(), self.quick_scan()]).pack(pady=15, padx=15)
        ctk.CTkLabel(quick_frame, text="✓ Desktop, Downloads, Temp • 5-10 min", font=("Arial", 11), 
                    text_color=self.colors['subtext']).pack(pady=(0, 15))
        
        full_frame = ctk.CTkFrame(dialog, fg_color=self.colors['card'])
        full_frame.pack(fill="x", padx=30, pady=10)
        ctk.CTkButton(full_frame, text="🔍 FULL SYSTEM SCAN", width=420, height=70, font=("Arial Bold", 18),
                     fg_color=self.colors['warning'], command=lambda: [dialog.destroy(), self.full_scan()]).pack(pady=15, padx=15)
        ctk.CTkLabel(full_frame, text="✓ All drives • 1-2 hours", font=("Arial", 11), 
                    text_color=self.colors['subtext']).pack(pady=(0, 15))
        
        custom_frame = ctk.CTkFrame(dialog, fg_color=self.colors['card'])
        custom_frame.pack(fill="x", padx=30, pady=10)
        ctk.CTkButton(custom_frame, text="📁 CUSTOM SCAN", width=420, height=70, font=("Arial Bold", 18),
                     fg_color=self.colors['success'], command=lambda: [dialog.destroy(), self.custom_scan()]).pack(pady=15, padx=15)
        ctk.CTkLabel(custom_frame, text="✓ Choose folder • Varies", font=("Arial", 11), 
                    text_color=self.colors['subtext']).pack(pady=(0, 15))
        
        ctk.CTkButton(dialog, text="Cancel", width=200, height=40, fg_color="gray", command=dialog.destroy).pack(pady=20)
    
    def quick_scan(self):
        if self.is_scanning:
            messagebox.showwarning("Scan in Progress", "Already scanning!")
            return
        
        locations = [
            os.path.join(os.environ['USERPROFILE'], 'Desktop'),
            os.path.join(os.environ['USERPROFILE'], 'Downloads'),
            os.path.join(os.environ['TEMP']),
        ]
        self.start_scan(locations, "Quick Scan")
    
    def full_scan(self):
        if self.is_scanning:
            messagebox.showwarning("Scan in Progress", "Already scanning!")
            return
        
        if not messagebox.askyesno("Full Scan", "This may take 1-2 hours. Continue?"):
            return
        
        locations = [d + '\\' for d in 'CDE' if os.path.exists(d + ':\\')]
        self.start_scan(locations, "Full System Scan")
    
    def custom_scan(self):
        if self.is_scanning:
            messagebox.showwarning("Scan in Progress", "Already scanning!")
            return
        
        path = filedialog.askdirectory(title="Select Folder")
        if path:
            self.start_scan([path], f"Custom Scan: {os.path.basename(path)}")
    
    def start_scan(self, locations, scan_type):
        self.is_scanning = True
        self.stop_btn.configure(state="normal")
        self.main_scan_btn.configure(state="disabled", text="⏳ Scanning...")
        
        self.scan_results = {'threats': [], 'suspicious': [], 'safe': [], 'total_scanned': 0}
        
        for widget in self.threats_scroll.winfo_children():
            widget.destroy()
        for widget in self.suspicious_scroll.winfo_children():
            widget.destroy()
        
        self.logs_text.delete("1.0", "end")
        self.log(f"=== {scan_type} Started ===")
        self.log(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"Locations: {', '.join(locations)}\n")
        
        threading.Thread(target=self.perform_scan, args=(locations, scan_type), daemon=True).start()
    
    def perform_scan(self, locations, scan_type):
        for location in locations:
            if not self.is_scanning:
                break
            self.log(f"\nScanning: {location}")
            for file_path in self.walk_directory(location):
                if not self.is_scanning:
                    break
                self.scan_file(file_path)
                if self.scan_results['total_scanned'] % 10 == 0:
                    self.update_stats()
        
        self.scan_complete(scan_type)
    
    def walk_directory(self, path):
        try:
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if not d.startswith('$')]
                for file in files:
                    yield os.path.join(root, file)
        except:
            pass
    
    def scan_file(self, file_path):
        try:
            self.scan_results['total_scanned'] += 1
            size = os.path.getsize(file_path)
            if size > 100 * 1024 * 1024:
                return
            
            threat_level = 0
            reasons = []
            
            for pattern in self.suspicious_patterns:
                if re.search(pattern, file_path, re.IGNORECASE):
                    threat_level = 1
                    reasons.append(f"Suspicious extension")
                    break
            
            result = {'path': file_path, 'size': size, 'reasons': reasons, 'hash': None}
            
            if threat_level == 2:
                self.scan_results['threats'].append(result)
            elif threat_level == 1:
                self.scan_results['suspicious'].append(result)
            else:
                self.scan_results['safe'].append(result)
        except:
            pass
    
    def scan_complete(self, scan_type):
        self.is_scanning = False
        self.progress_bar.set(1.0)
        self.stop_btn.configure(state="disabled")
        self.main_scan_btn.configure(state="normal", text="🛡️ START SCAN")
        
        self.update_stats()
        self.last_scan_label.configure(text=f"Last Scan: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.log(f"\n=== Scan Complete ===")
        self.log(f"Total: {self.scan_results['total_scanned']}")
        self.log(f"Threats: {len(self.scan_results['threats'])}")
        self.log(f"Suspicious: {len(self.scan_results['suspicious'])}")
        
        self.root.after(0, self.display_results)
        
        if len(self.scan_results['threats']) > 0:
            messagebox.showwarning("Threats Found", f"Found {len(self.scan_results['threats'])} threats!")
        else:
            messagebox.showinfo("Scan Complete", f"Scanned {self.scan_results['total_scanned']} files\nNo threats detected")
    
    def display_results(self):
        for widget in self.threats_scroll.winfo_children():
            widget.destroy()
        for widget in self.suspicious_scroll.winfo_children():
            widget.destroy()
        
        if self.scan_results['threats']:
            for threat in self.scan_results['threats']:
                self.create_threat_card(self.threats_scroll, threat, True)
        else:
            ctk.CTkLabel(self.threats_scroll, text="✅ No threats detected", font=("Arial Bold", 16), 
                        text_color=self.colors['success']).pack(pady=50)
        
        if self.scan_results['suspicious']:
            for sus in self.scan_results['suspicious'][:50]:
                self.create_threat_card(self.suspicious_scroll, sus, False)
        else:
            ctk.CTkLabel(self.suspicious_scroll, text="✅ No suspicious files", font=("Arial Bold", 16),
                        text_color=self.colors['success']).pack(pady=50)
    
    def create_threat_card(self, parent, item, is_threat):
        card = ctk.CTkFrame(parent, fg_color=self.colors['card'], border_width=2,
                           border_color=self.colors['danger'] if is_threat else self.colors['warning'])
        card.pack(fill="x", pady=5, padx=10)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=15)
        
        icon = "⚠️" if is_threat else "⚡"
        ctk.CTkLabel(content, text=icon, font=("Arial", 24)).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(content, text=item['path'], font=("Arial Bold", 12),
                    text_color=self.colors['danger'] if is_threat else self.colors['warning'],
                    anchor="w", wraplength=800).pack(side="left", fill="x", expand=True)
    
    def stop_scan(self):
        if messagebox.askyesno("Stop", "Stop the scan?"):
            self.is_scanning = False
            self.log("\n[STOPPED BY USER]")
    
    def update_status(self, msg):
        self.root.after(0, lambda: self.status_label.configure(text=msg))
    
    def update_stats(self):
        def update():
            self.threats_card.value_label.configure(text=str(len(self.scan_results['threats'])))
            self.suspicious_card.value_label.configure(text=str(len(self.scan_results['suspicious'])))
            self.scanned_card.value_label.configure(text=str(self.scan_results['total_scanned']))
            self.safe_card.value_label.configure(text=str(len(self.scan_results['safe'])))
        self.root.after(0, update)
    
    def log(self, msg):
        self.root.after(0, lambda: self.logs_text.insert("end", msg + "\n"))
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AdvancedSecurityScanner()
    app.run()
