import os
import requests
import io
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ttkbootstrap import Styl

root = tk.Tk()
root.title("ArtfinityPix")
root.geometry("700x500")
image_url = "https://img.freepik.com/free-photo/vivid-blurred-colorful-background_58702-2655.jpg?w=2000&t=st=1690629280~exp=1690629880~hmac=dfb9c890b8dddaae59b504a6561778dab1f821d824c38ca83f8dfcb5342ba7f9"
image_data = requests.get(image_url).content
image = ImageTk.PhotoImage(Image.open(io.BytesIO(image_data)))
background_label = ttk.Label(root, image=image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
root.resizable(False, False)

style = Style(theme="flatly")

def display_image(category):
    url = f"https://api.unsplash.com/photos/random?query={category}&orientation=landscape&client_id=1n7sSMtCh8Hs_MrBOjhQ1SygTDA-BJ550UdX3rwLYZQ"
    data = requests.get(url).json()
    img_data = requests.get(data["urls"]["regular"]).content

    photo = ImageTk.PhotoImage(Image.open(io.BytesIO(img_data)).resize((700, 400), resample=Image.LANCZOS))
    label.config(image=photo)
    label.image = photo

    global download_img_data
    download_img_data = img_data

def enable_button(*args):
    generate_button.config(state="normal" if category_var.get() != "Choose Category" else "disabled")

def download_image():
    if 'download_img_data' in globals():
        try:
            download_path = os.path.join(os.path.expanduser("~"), "Downloads", "generated_image.jpg")
            with open(download_path, "wb") as f:
                f.write(download_img_data)
            messagebox.showinfo("Download Successful", f"Image downloaded successfully to {download_path}!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while downloading the image: {e}")

def create_gui():
    global category_var, generate_button, label

    category_var = tk.StringVar(value="Choose Category")
    category_options = ["Choose Category", "Food", "Animals", "People", "Music", "Art", "Vehicles", "Random"]
    category_dropdown = ttk.OptionMenu(root, category_var, *category_options, command=enable_button, style="Category.TMenubutton")
    category_dropdown.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    category_dropdown.config(width=14)

    generate_button = ttk.Button(root, text="Generate Image", state="disabled", command=lambda: display_image(category_var.get()), style="Generate.TButton")
    generate_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    label = tk.Label(root, background="white")
    label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    download_button = ttk.Button(root, text="Download", command=download_image, style="Download.TButton")
    download_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    root.columnconfigure([0, 1], weight=1)
    root.rowconfigure(1, weight=1)
    root.mainloop()

if __name__ == '__main__':
    style.configure("Category.TMenubutton", font=("Helvetica", 14), foreground=style.colors.dark, background=style.colors.primary)
    style.configure("Generate.TButton", font=("Helvetica", 14), foreground=style.colors.light, background=style.colors.success)
    style.configure("Download.TButton", font=("Helvetica", 14), foreground=style.colors.light, background=style.colors.warning)

    create_gui()
