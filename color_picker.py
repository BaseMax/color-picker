import threading
import tkinter as tk
from tkinter import messagebox, colorchooser
from PIL import ImageGrab, ImageTk

class ColorPickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Picker")

        self._init_ui()

        self.selected_color = None
        self.screenshot = None
        self.original_size = (0, 0)

    def _init_ui(self):
        """Initialize the UI components."""
        self.color_label = tk.Label(self.root, text="Click to pick a color", width=30, height=5)
        self.color_label.pack(pady=10)

        self.capture_button = tk.Button(self.root, text="Capture Color from Screen", command=self.start_capture)
        self.capture_button.pack(pady=10)

        self.palette_button = tk.Button(self.root, text="Pick Color from Palette", command=self.open_color_palette)
        self.palette_button.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Save Color", command=self.save_color)
        self.save_button.pack(pady=10)

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

    def start_capture(self):
        """Start a thread to capture screen and display it in the window."""
        threading.Thread(target=self.capture_color, daemon=True).start()

    def capture_color(self):
        """Capture the screen and allow the user to pick a color."""
        self.root.withdraw()
        messagebox.showinfo("Capture Color", "Click anywhere on the screen to pick a color!")

        screenshot = ImageGrab.grab()
        self.screenshot = screenshot
        self.original_size = screenshot.size

        self.display_screenshot(screenshot)

        self.root.deiconify()

        self.image_label.bind("<Button-1>", self.on_image_click)

    def display_screenshot(self, screenshot):
        """Display the captured screenshot resized to fit the window."""
        resized_screenshot = screenshot.resize((500, 500))
        screenshot_tk = ImageTk.PhotoImage(resized_screenshot)
        self.image_label.config(image=screenshot_tk)
        self.image_label.image = screenshot_tk

    def on_image_click(self, event):
        """Handle click event on the image to pick a color."""
        if self.screenshot:
            x, y = event.x, event.y
            scale_x = self.original_size[0] / 500
            scale_y = self.original_size[1] / 500
            original_x, original_y = int(x * scale_x), int(y * scale_y)

            color = self.screenshot.getpixel((original_x, original_y))
            self.selected_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
            self.update_color_label(self.selected_color)

    def update_color_label(self, color):
        """Update the label with the selected color."""
        self.color_label.config(bg=color, text=f"Color: {color}")

    def open_color_palette(self):
        """Open the color picker dialog to choose a color."""
        color_code = colorchooser.askcolor(title="Choose a color")[1]
        if color_code:
            self.selected_color = color_code
            self.update_color_label(self.selected_color)

    def save_color(self):
        """Save the selected color to a file."""
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
