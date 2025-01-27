import tkinter as tk
from tkinter import filedialog, ttk
import pyautogui
from PIL import Image
import json
import os

class ImageClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Auto Clicker")
        self.setup_style()

        self.image_paths = []
        self.running = False
        self.current_index = 0
        self.drag_start_index = None
        
        # Configuration variables
        self.mode = tk.StringVar(value="parallel")
        self.delay = tk.DoubleVar(value=1.0)
        self.confidence = tk.DoubleVar(value=0.8)
        self.click_type = tk.StringVar(value="Left")
        self.status_var = tk.StringVar()

        self.setup_gui()
        self.setup_traces()
        self.load_settings()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_style(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # GitHub Dark Theme Colors
        self.bg_color = '#0d1117'
        self.fg_color = '#c9d1d9'
        self.accent_color = '#161b22'
        self.active_color = '#238636'  # GitHub green
        self.hover_color = '#2ea043'    # GitHub hover green
        self.selected_color = '#1f6feb' # GitHub blue
        self.danger_color = '#da3633'   # GitHub red
        self.danger_hover = '#f85149'   # GitHub hover red
        
        # Base style
        self.style.configure('.', 
                           background=self.bg_color,
                           foreground=self.fg_color,
                           relief='flat',
                           borderwidth=0,
                           focuscolor=self.bg_color)
        
        # Radio button style updates
        self.style.configure('TRadiobutton',
                    background=self.bg_color,
                    foreground=self.fg_color,  # Normal text color
                    indicatorbackground=self.accent_color,
                    indicatorcolor='white',  # Selected dot color
                    selectcolor=self.bg_color,
                    activebackground=self.bg_color,
                    activeforeground=self.fg_color,  # Hover text color
                    borderwidth=0,
                    padding=5)
    
        self.style.map('TRadiobutton',
                    indicatorbackground=[('selected', self.active_color),
                                        ('active', self.active_color)],
                    indicatorcolor=[('selected', 'white'),
                                    ('active', 'white')],
                    # Add these to control text colors
                    foreground=[('active', self.fg_color),  # Hover state
                                ('!active', self.fg_color)],  # Normal state
                    background=[('active', self.bg_color),
                                ('!active', self.bg_color)])
        
        # Combobox style updates
        self.style.configure('TCombobox',
                           fieldbackground=self.accent_color,
                           selectbackground=self.selected_color,
                           arrowsize=12,
                           padding=6,
                           arrowcolor=self.fg_color)  # Arrow color
        
        # Configure combobox dropdown listbox colors
        self.root.option_add('*TCombobox*Listbox*background', self.accent_color)
        self.root.option_add('*TCombobox*Listbox*foreground', self.fg_color)
        self.root.option_add('*TCombobox*Listbox*selectBackground', self.selected_color)
        self.root.option_add('*TCombobox*Listbox*selectForeground', self.fg_color)
        
        # Frame styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabelframe', 
                           background=self.bg_color,
                           borderwidth=2,
                           relief='flat',
                           foreground=self.fg_color)
        
        # Button styles
        self.style.configure('Primary.TButton', 
                           background=self.active_color,
                           foreground=self.fg_color,
                           borderwidth=0,
                           padding=6,
                           focusthickness=0)
        self.style.map('Primary.TButton',
                      background=[('active', self.hover_color),
                                  ('disabled', self.accent_color)])
        
        self.style.configure('Danger.TButton', 
                           background=self.danger_color,
                           foreground=self.fg_color,
                           borderwidth=0,
                           padding=6)
        self.style.map('Danger.TButton',
                      background=[('active', self.danger_hover),
                                  ('disabled', self.accent_color)])

        # Listbox style
        self.listbox = tk.Listbox(
            self.root,
            bg=self.accent_color,
            fg=self.fg_color,
            borderwidth=0,
            highlightthickness=0,
            selectbackground=self.selected_color,
            selectforeground=self.fg_color,
            activestyle='none',
            font=('Segoe UI', 10)
        )
        
        # Scrollbar style
        self.style.configure('TScrollbar', 
                           troughcolor=self.accent_color,
                           background=self.accent_color)
        self.style.map('TScrollbar',
                     background=[('active', self.active_color)])
        
        # Combobox style
        self.style.configure('TCombobox',
                           fieldbackground=self.accent_color,
                           selectbackground=self.selected_color,
                           arrowsize=12,
                           padding=6)
        self.style.map('TCombobox',
                     fieldbackground=[('readonly', self.accent_color)],
                     selectbackground=[('readonly', self.selected_color)])
        
        # Radiobutton style
        self.style.configure('TRadiobutton',
                           background=self.bg_color,
                           indicatorbackground=self.accent_color,
                           indicatorcolor=self.active_color,
                           selectcolor=self.selected_color)
        
        # Label styles
        self.style.configure('TLabel', 
                           background=self.bg_color, 
                           foreground=self.fg_color)
        self.style.configure('Status.TLabel', 
                           foreground=self.danger_color,
                           font=('Segoe UI', 9, 'italic'))
        
        # Scale (slider) style
        self.style.configure('Horizontal.TScale',
                           background=self.bg_color,
                           troughcolor=self.accent_color,
                           sliderthickness=12,
                           sliderrelief='flat',
                           slidercolor=self.fg_color,
                           gripcount=0)
        self.style.map('Horizontal.TScale',
                     slidercolor=[('active', self.active_color)])
        
        # Scrollbar style
        self.style.configure('TScrollbar', 
                        troughcolor='#808080',  # Grey color
                        background='#808080', 
                        gripcount=0)   # Grey color
        
        self.style.map('TScrollbar',
                    background=[('active', '#a0a0a0')])  # Slightly darker grey when clicked

        # Remove grip indicators (lines)
        self.style.configure('Vertical.Scrollbar.thumb', gripcount=0)
        self.style.configure('Horizontal.Scrollbar.thumb', gripcount=0)
        
        # Configure root background
        self.root.configure(background=self.bg_color)
        self.root.option_add('*TEntry*background', self.accent_color)
        self.root.option_add('*TEntry*foreground', self.fg_color)
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Image list
        list_frame = ttk.LabelFrame(main_frame, text="Image Paths", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.listbox = tk.Listbox(
            list_frame, 
            height=6, 
            selectmode=tk.SINGLE,
            bg=self.accent_color,
            fg=self.fg_color,
            selectbackground=self.selected_color,
            activestyle='none',
            font=('Segoe UI', 10)
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind('<ButtonPress-1>', self.on_drag_start)
        self.listbox.bind('<B1-Motion>', self.on_drag_motion)
        self.listbox.bind('<ButtonRelease-1>', self.on_drag_release)

        scrollbar = ttk.Scrollbar(list_frame, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Controls
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=5)

        self.add_btn = ttk.Button(controls_frame, text="+ Add Images", 
                                command=self.add_image_paths, style='Primary.TButton')
        self.add_btn.pack(side=tk.LEFT, padx=5)

        self.remove_btn = ttk.Button(controls_frame, text="- Remove Selected", 
                                   command=self.remove_selected, style='Danger.TButton')
        self.remove_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = ttk.Button(controls_frame, text="Clear All", 
                                  command=self.clear_all, style='Danger.TButton')
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # Click type selection
        click_frame = ttk.LabelFrame(main_frame, text="Click Type", padding=10)
        click_frame.pack(fill=tk.X, pady=5)

        self.click_combo = ttk.Combobox(
            click_frame, 
            textvariable=self.click_type, 
            values=('Left', 'Right', 'Middle', 'Double'),
            state='readonly'
        )
        self.click_combo.pack(fill=tk.X)

        # Delay slider
        self.delay_frame = ttk.LabelFrame(main_frame, text="Check Delay (seconds)", padding=10)
        self.delay_frame.pack(fill=tk.X, pady=5)

        self.delay_slider = ttk.Scale(
            self.delay_frame,
            from_=0.1,
            to=5.0,
            variable=self.delay,
            orient=tk.HORIZONTAL
        )
        self.delay_slider.pack(fill=tk.X)
        self.delay_label = ttk.Label(self.delay_frame, text=f"{self.delay.get():.2f}")
        self.delay_label.pack()

        # Confidence slider
        self.confidence_frame = ttk.LabelFrame(main_frame, text="Confidence Threshold (%)", padding=10)
        self.confidence_frame.pack(fill=tk.X, pady=5)

        self.confidence_slider = ttk.Scale(
            self.confidence_frame,
            from_=0.1,
            to=1.0,
            variable=self.confidence,
            orient=tk.HORIZONTAL
        )
        self.confidence_slider.pack(fill=tk.X)
        self.confidence_label = ttk.Label(self.confidence_frame, text=f"{self.confidence.get()*100:.2f}%")
        self.confidence_label.pack()

        # Mode selection
        mode_frame = ttk.LabelFrame(main_frame, text="Mode", padding=10)
        mode_frame.pack(fill=tk.X, pady=5)

        self.parallel_rb = ttk.Radiobutton(
            mode_frame,
            text="Parallel (Click first found image)",
            variable=self.mode,
            value="parallel"
        )
        self.parallel_rb.pack(anchor=tk.W)

        self.sequential_rb = ttk.Radiobutton(
            mode_frame,
            text="Sequential (Click in order)",
            variable=self.mode,
            value="sequential"
        )
        self.sequential_rb.pack(anchor=tk.W)

        # Start/Stop button
        self.start_btn = ttk.Button(main_frame, text="Start", 
                                  command=self.start_stop, style='Primary.TButton')
        self.start_btn.pack(pady=10)

        # Status label
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, style='Status.TLabel')
        self.status_label.pack(pady=5)

    def setup_traces(self):
        self.delay.trace_add("write", lambda *_: self.delay_label.config(
            text=f"{self.delay.get():.2f}"))
        self.confidence.trace_add("write", lambda *_: self.confidence_label.config(
            text=f"{self.confidence.get()*100:.2f}%"))

    def on_drag_start(self, event):
        self.drag_start_index = self.listbox.nearest(event.y)

    def on_drag_motion(self, event):
        current_index = self.listbox.nearest(event.y)
        if current_index != self.drag_start_index and self.drag_start_index is not None:
            item = self.listbox.get(self.drag_start_index)
            self.listbox.delete(self.drag_start_index)
            self.listbox.insert(current_index, item)
            self.drag_start_index = current_index

    def on_drag_release(self, event):
        self.drag_start_index = None
        self.image_paths = list(self.listbox.get(0, tk.END))

    def remove_selected(self):
        selected = self.listbox.curselection()
        if selected:
            self.listbox.delete(selected[0])
            self.image_paths = list(self.listbox.get(0, tk.END))

    def clear_all(self):
        self.listbox.delete(0, tk.END)
        self.image_paths = []

    def add_image_paths(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*"))
        )
        for path in file_paths:
            self.listbox.insert(tk.END, path)
        self.image_paths = list(self.listbox.get(0, tk.END))

    def start_stop(self):
        if self.running:
            self.running = False
            self.start_btn.config(text="Start", style='Primary.TButton')
            self.enable_controls(True)
            self.status_var.set("Stopped")
        else:
            self.image_paths = list(self.listbox.get(0, tk.END))
            if not self.image_paths:
                self.status_var.set("Error: Add at least one image path")
                return
            self.running = True
            self.current_index = 0
            self.start_btn.config(text="Stop", style='Danger.TButton')
            self.enable_controls(False)
            self.status_var.set("Running...")
            self.check_images()

    def enable_controls(self, enable):
        state = "normal" if enable else "disabled"
        self.add_btn.config(state=state)
        self.remove_btn.config(state=state)
        self.clear_btn.config(state=state)
        self.delay_slider.config(state=state)
        self.confidence_slider.config(state=state)
        self.parallel_rb.config(state=state)
        self.sequential_rb.config(state=state)
        self.click_combo.config(state=state)
        self.listbox.config(state=state)

    def check_images(self):
        if not self.running:
            return

        try:
            click_type = self.click_type.get().lower()
            if self.mode.get() == "sequential":
                if self.current_index >= len(self.image_paths):
                    self.current_index = 0
                path = self.image_paths[self.current_index]
                location = pyautogui.locateOnScreen(path, confidence=self.confidence.get())
                if location:
                    x, y = pyautogui.center(location)
                    if click_type == "double":
                        pyautogui.doubleClick(x, y)
                    else:
                        pyautogui.click(x, y, button=click_type)
                    self.current_index += 1
                    self.status_var.set(f"Clicked: {os.path.basename(path)}")
                else:
                    self.status_var.set(f"Waiting for: {os.path.basename(path)}")
            else:
                clicked = False
                for path in self.image_paths:
                    try:
                        location = pyautogui.locateOnScreen(
                            path,
                            confidence=self.confidence.get()
                        )
                    except pyautogui.ImageNotFoundException:
                        continue

                    if location:
                        x, y = pyautogui.center(location)
                        if click_type == "double":
                            pyautogui.doubleClick(x, y)
                        else:
                            pyautogui.click(x, y, button=click_type)
                        clicked = True
                        self.status_var.set(f"Clicked: {os.path.basename(path)}")
                        break

                if not clicked:
                    self.status_var.set("No images found")
        except pyautogui.ImageNotFoundException as e:
            self.status_var.set(f"Image not found: {os.path.basename(str(e))}")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            self.running = False
            self.start_btn.config(text="Start", style='Primary.TButton')
            self.enable_controls(True)

        self.root.after(int(self.delay.get() * 1000), self.check_images)

    def save_settings(self):
        settings = {
            "image_paths": self.image_paths,
            "mode": self.mode.get(),
        }
        with open("settings.json", "w") as f:
            json.dump(settings, f)

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
                self.listbox.delete(0, tk.END)
                for path in settings.get("image_paths", []):
                    self.listbox.insert(tk.END, path)
                self.delay.set(settings.get("delay", 1.0))
                self.confidence.set(settings.get("confidence", 0.8))
                self.mode.set(settings.get("mode", "parallel"))
                self.click_type.set(settings.get("click_type", "Left"))
        except FileNotFoundError:
            pass

    def on_close(self):
        self.save_settings()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x800")  # Set initial size
    root.minsize(600, 400)  # Set minimum size
    app = ImageClickerApp(root)
    root.mainloop()