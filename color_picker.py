import threading
import tkinter as tk
from tkinter import messagebox, colorchooser
from tkinter import ttk
from PIL import ImageGrab, ImageTk

class ColorPickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Picker")
        self.root.geometry("600x600")
        self.root.configure(bg="#f0f0f0")

        self._init_ui()

        self.selected_color = None
        self.screenshot = None
        self.original_size = (0, 0)

    def _init_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)

        self.color_label = ttk.Label(main_frame, text="Click to pick a color", width=30, anchor="w", style="TLabel")
        self.color_label.grid(row=0, column=0, pady=20, sticky="w")

        self.capture_button = ttk.Button(main_frame, text="Capture Color from Screen", command=self.start_capture, style="TButton")
        self.capture_button.grid(row=1, column=0, pady=10, sticky="w")

        self.palette_button = ttk.Button(main_frame, text="Pick Color from Palette", command=self.open_color_palette, style="TButton")
        self.palette_button.grid(row=2, column=0, pady=10, sticky="w")

        self.save_button = ttk.Button(main_frame, text="Save Color", command=self.save_color, style="TButton")
        self.save_button.grid(row=3, column=0, pady=10, sticky="w")

        self.image_label = ttk.Label(main_frame)
        self.image_label.grid(row=4, column=0, pady=10)

        self._apply_styles()

    def _apply_styles(self):
        style = ttk.Style()
        style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12, "bold"), foreground="#333")
        style.configure("TButton", font=("Helvetica", 12), padding=10, relief="flat")
        style.map("TButton", background=[("active", "#4CAF50"), ("pressed", "#45a049")])

    def start_capture(self):
        threading.Thread(target=self.capture_color, daemon=True).start()

    def capture_color(self):
        self.root.withdraw()
        messagebox.showinfo("Capture Color", "Click anywhere on the screen to pick a color!")

        screenshot = ImageGrab.grab()
        self.screenshot = screenshot
        self.original_size = screenshot.size

        self.display_screenshot(screenshot)

        self.root.deiconify()

        self.image_label.bind("<Button-1>", self.on_image_click)

    def display_screenshot(self, screenshot):
        resized_screenshot = screenshot.resize((500, 500))
        screenshot_tk = ImageTk.PhotoImage(resized_screenshot)
        self.image_label.config(image=screenshot_tk)
        self.image_label.image = screenshot_tk

    def on_image_click(self, event):
        if self.screenshot:
            x, y = event.x, event.y
            scale_x = self.original_size[0] / 500
            scale_y = self.original_size[1] / 500
            original_x, original_y = int(x * scale_x), int(y * scale_y)

            color = self.screenshot.getpixel((original_x, original_y))
            self.selected_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
            self.update_color_label(self.selected_color)

    def update_color_label(self, color):
        self.color_label.config(background=color, text=f"Color: {color}")

    def open_color_palette(self):
        color_code = colorchooser.askcolor(title="Choose a color")[1]
        if color_code:
            self.selected_color = color_code
            self.update_color_label(self.selected_color)

    def save_color(self):
        if self.selected_color:
            with open("colors.txt", "a") as file:
                file.write(self.selected_color + "\n")
            messagebox.showinfo("Saved", f"Saved color: {self.selected_color}")
        else:
            messagebox.showwarning("No Color", "No color selected!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorPickerApp(root)
    root.mainloop()
