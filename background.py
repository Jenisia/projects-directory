import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class BackgroundApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI with Background Image")

        # Load and resize the background image
        image_path = "fitness.png"  # Replace with the path to your image file
        original_image = Image.open(image_path)
        resized_image = original_image.resize((400, 300), Image.ANTIALIAS)
        self.background_photo = ImageTk.PhotoImage(resized_image)

        # Set the size of the canvas to match the resized image
        self.canvas = tk.Canvas(root, width=resized_image.width, height=resized_image.height)
        self.canvas.pack()

        # Place the resized background image on the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_photo)

        # Create a frame on top of the canvas
        self.frame = ttk.Frame(self.canvas, padding="20")
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Add widgets to the frame
        self.label = ttk.Label(self.frame, text="Welcome to the GUI!")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.button = ttk.Button(self.frame, text="Click Me", command=self.on_button_click)
        self.button.grid(row=1, column=0, padx=10, pady=10)

    def on_button_click(self):
        self.label["text"] = "Button Clicked!"

if __name__ == "__main__":
    root = tk.Tk()
    app = BackgroundApp(root)
    root.mainloop()
