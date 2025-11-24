import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime, timedelta
import json
import os

class DesktopClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Clock")
        self.root.geometry("900x300")
        self.root.configure(bg='black')

        # Config file for saving window position
        self.config_file = os.path.join(os.path.expanduser("~"), ".countdownclock_config.json")

        # Remove window frame and keep on top
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", 0.8)  # Slight transparency

        # Variables
        self.countdown_time = 0
        self.time_str = tk.StringVar()
        self.flash_state = False  # For blinking effect
        self.target_time = None  # Store target datetime
        self.last_update_time = None  # Track time for millisecond precision

        # UI Elements - use absolute positioning for precise layout
        # Current time display (top, 20px from top)
        self.current_time_str = tk.StringVar()
        self.current_time_label = tk.Label(self.root, textvariable=self.current_time_str, font=("Helvetica", 28, "bold"), fg="#666666", bg="black")
        self.current_time_label.place(relx=0.5, y=20, anchor='n')

        # Main countdown display (vertically centered)
        self.label = tk.Label(self.root, textvariable=self.time_str, font=("Helvetica", 120, "bold"), fg="white", bg="black")
        self.label.place(relx=0.5, rely=0.5, anchor='center')

        # Target time display (bottom, 20px from bottom)
        self.target_str = tk.StringVar()
        self.target_label = tk.Label(self.root, textvariable=self.target_str, font=("Helvetica", 28, "bold"), fg="yellow", bg="black", cursor="hand2")
        self.target_label.place(relx=0.5, rely=1.0, y=-20, anchor='s')
        self.target_label.bind("<Button-1>", lambda e: self.set_countdown())

        # Bindings for window dragging
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)
        self.root.bind("<B1-Motion>", self.do_move)

        # ESC key to exit - bind to root and all labels
        self.root.bind("<Escape>", lambda e: self.root.quit())
        self.label.bind("<Escape>", lambda e: self.root.quit())
        self.current_time_label.bind("<Escape>", lambda e: self.root.quit())
        self.target_label.bind("<Escape>", lambda e: self.root.quit())

        # Ensure window gets focus
        self.root.focus_force()

        # Set default countdown to 11:29 AFTER UI is created
        self._set_default_countdown()

        # Load and apply saved configuration (window position and target time)
        self.load_config()

        # Save config when window is moved or closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Configure>", self.on_window_configure)

        self.update_clock()

    def _set_default_countdown(self):
        """Set default countdown to 11:29"""
        try:
            now = datetime.now()
            target = now.replace(hour=11, minute=29, second=0, microsecond=0)

            # If 11:29 has passed today, set for tomorrow
            if target <= now:
                target += timedelta(days=1)

            self.target_time = target  # Store target time
            self.countdown_time = int((target - now).total_seconds())
            self.last_update_time = datetime.now()  # Initialize last update time
            self.update_display_countdown()
            self.update_target_display()
        except Exception:
            self.countdown_time = 0
            self.target_time = None

    def load_config(self):
        """Load saved configuration from config file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)

                    # Load window position
                    x = config.get('x', 100)
                    y = config.get('y', 100)
                    self.root.geometry(f"+{x}+{y}")

                    # Load target time
                    saved_time = config.get('target_time')
                    if saved_time:
                        try:
                            # Parse HH:MM:SS
                            h, m, s = map(int, saved_time.split(':'))
                            now = datetime.now()
                            target = now.replace(hour=h, minute=m, second=s, microsecond=0)

                            # If target is earlier than now, assume it's for tomorrow
                            if target <= now:
                                target += timedelta(days=1)

                            self.target_time = target
                            self.countdown_time = int((target - now).total_seconds())
                            self.update_display_countdown()
                            self.update_target_display()
                        except ValueError:
                            pass # Invalid time format in config
        except Exception:
            pass

    def save_config(self):
        """Save current configuration to config file"""
        try:
            x = self.root.winfo_x()
            y = self.root.winfo_y()

            config = {
                'x': x,
                'y': y
            }

            # Save target time if set
            if self.target_time:
                config['target_time'] = self.target_time.strftime("%H:%M:%S")

            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception:
            pass

    def on_window_configure(self, event):
        """Called when window is moved or resized"""
        # Only save if it's a move event (not resize)
        if event.widget == self.root:
            self.save_config()

    def on_closing(self):
        """Called when window is closed"""
        self.save_config()
        self.root.quit()


    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")


    def set_countdown(self):
        # Dialog to get target time in HH:MM or HH:MM:SS format
        def set_time():
            try:
                target_time_str = entry.get().strip()
                # Parse HH:MM or HH:MM:SS format
                time_parts = target_time_str.split(':')

                if len(time_parts) == 2:
                    # HH:MM format
                    target_hour, target_min = map(int, time_parts)
                    target_sec = 0
                elif len(time_parts) == 3:
                    # HH:MM:SS format
                    target_hour, target_min, target_sec = map(int, time_parts)
                else:
                    raise ValueError("Invalid format")

                # Get current time
                now = datetime.now()

                # Create target datetime for today
                target = now.replace(hour=target_hour, minute=target_min, second=target_sec, microsecond=0)

                # If target time is earlier than now, assume it's for tomorrow
                if target <= now:
                    target += timedelta(days=1)

                # Calculate seconds difference
                self.countdown_time = int((target - now).total_seconds())
                self.target_time = target  # Store target time
                self.countdown_running = True  # Auto-start countdown
                self.save_config()  # Save new target time
                top.destroy()
                self.update_display_countdown()
                self.update_target_display()
            except (ValueError, AttributeError):
                messagebox.showerror("Invalid Format", "Please enter time in HH:MM or HH:MM:SS format (24-hour)")

        top = tk.Toplevel(self.root)
        top.title("Set Target Time")
        top.geometry("250x120")

        # Fix focus issue: make sure the dialog can receive focus
        top.attributes("-topmost", True)
        top.focus_force()

        tk.Label(top, text="Enter target time:").pack(pady=5)
        tk.Label(top, text="(HH:MM or HH:MM:SS)", font=("Helvetica", 10), fg="gray").pack()
        entry = tk.Entry(top, font=("Helvetica", 14))
        entry.pack(pady=5)
        entry.insert(0, "11:29")  # Default example
        entry.focus_set()  # Set focus to entry field
        entry.select_range(0, tk.END)  # Select all text for easy editing

        tk.Button(top, text="Set", command=set_time).pack(pady=5)

        # Allow Enter key to submit
        entry.bind("<Return>", lambda e: set_time())


    def update_display_countdown(self):
        """Update countdown display with milliseconds"""
        if self.target_time:
            # Calculate precise time remaining including milliseconds
            now = datetime.now()
            time_remaining = (self.target_time - now).total_seconds()
            if time_remaining < 0:
                time_remaining = 0

            total_ms = int(time_remaining * 1000)
            hours = total_ms // 3600000
            mins = (total_ms % 3600000) // 60000
            secs = (total_ms % 60000) // 1000
            ms = total_ms % 1000

            self.time_str.set(f"{hours:02}:{mins:02}:{secs:02}.{ms:03}")
        else:
            # No target time set
            mins, secs = divmod(self.countdown_time, 60)
            hours, mins = divmod(mins, 60)
            self.time_str.set(f"{hours:02}:{mins:02}:{secs:02}.000")

    def update_target_display(self):
        """Update the target time display"""
        if self.target_time:
            target_str = self.target_time.strftime("%H:%M:%S")
            self.target_str.set(target_str)
        else:
            self.target_str.set("")

    def update_clock(self):
        # Always update current time display
        current_time = time.strftime("%H:%M:%S")
        self.current_time_str.set(current_time)

        # Update countdown
        if self.countdown_time > 0 and self.target_time:
            # Update countdown with millisecond precision
            now = datetime.now()
            time_remaining = (self.target_time - now).total_seconds()

            if time_remaining > 0:
                self.countdown_time = int(time_remaining)
                self.update_display_countdown()

                # Visual alert: Blinking red/white text for last 10 seconds
                if time_remaining <= 10:
                    # Toggle between red and white every 500ms
                    if int(time_remaining * 2) % 2 == 0:
                        self.label.config(fg="red")
                    else:
                        self.label.config(fg="white")
                else:
                    self.label.config(fg="white")
                    self.flash_state = False
            else:
                # Countdown finished - show 00:00:00.000
                self.countdown_time = 0
                self.time_str.set("00:00:00.000")
                self.label.config(fg="white")
                self.root.update() # Ensure UI updates before blocking message box
                messagebox.showinfo("Time's up!", "Countdown finished!")
        else:
            self.update_display_countdown()

        self.root.after(100, self.update_clock)  # Update every 100ms for millisecond precision

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopClock(root)
    root.mainloop()
