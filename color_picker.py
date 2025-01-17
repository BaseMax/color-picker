import threading
import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab, ImageTk

class ColorPickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Picker")

        self.color_label = tk.Label(root, text="Click to pick a color", width=30, height=5)
        self.color_label.pack(pady=10)

        self.capture_button = tk.Button(root, text="Capture Color from Screen", command=self.start_capture)
        self.capture_button.pack(pady=10)

        self.save_button = tk.Button(root, text="Save Color", command=self.save_color)
        self.save_button.pack(pady=10)

        self.selected_color = None

        self.screenshot = None
        self.image_label = tk.Label(root)
        self.image_label.pack()

    def start_capture(self):
        """Start a new thread to capture the screen and display it in the window"""
        capture_thread = threading.Thread(target=self.capture_color)
        capture_thread.daemon = True
        capture_thread.start()

    def capture_color(self):
        """Capture the color of the pixel where the user clicks"""
        self.root.withdraw()

        messagebox.showinfo("Capture Color", "Click anywhere on the screen to pick a color!")

        screenshot = ImageGrab.grab()
        self.screenshot = screenshot
        self.display_screenshot(screenshot)

        self.root.deiconify()

        self.image_label.bind("<Button-1>", self.on_image_click)

    def display_screenshot(self, screenshot):
        """Display the captured screenshot in the tkinter window"""
        screenshot = screenshot.resize((500, 500))
        screenshot_tk = ImageTk.PhotoImage(screenshot)
        self.image_label.config(image=screenshot_tk)
        self.image_label.image = screenshot_tk

    def on_image_click(self, event):
        """Capture the color of the pixel at the point the user clicks"""
        if self.screenshot:
            x, y = event.x, event.y

            color = self.screenshot.getpixel((x, y))
            self.selected_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'

            self.update_color_label(self.selected_color)

    def update_color_label(self, color):
        """Update the label to show the selected color"""
        self.color_label.config(bg=color, text=f"Color: {color}")

    def save_color(self):
        """Save the selected color to a file"""
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
