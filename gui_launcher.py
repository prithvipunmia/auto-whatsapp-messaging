import tkinter as tk
from tkinter import messagebox
import pywhatkit as kit
import time
from datetime import datetime


def generate_message(name, model, executive, inquiry_type):
    date_str = datetime.now().strftime("%d %B %Y")
    if inquiry_type == "Walk-in":
        return f"""Hello {name},
Thank you for visiting Surya Honda Porur on {date_str} as a Walk-in Customer, and enquiring about {model} with Sales Executive {executive}.
We look forward to assisting you further with your vehicle selection and purchase.
– Team Surya Honda"""
    else:  # BW Inquiry
        return f"""Hello {name},
Thank you for your BW inquiry about the {model} with Sales Executive {executive} at Surya Honda Porur on {date_str}.
We appreciate your interest and will be glad to assist you throughout your buying journey.
– Team Surya Honda"""

def send_messages():
    names = name_text.get("1.0", tk.END).strip().splitlines()
    numbers = number_text.get("1.0", tk.END).strip().splitlines()
    models = model_text.get("1.0", tk.END).strip().splitlines()
    executives = executive_text.get("1.0", tk.END).strip().splitlines()
    inquiry_type = inquiry_var.get()
    send_image = send_image_var.get()

    count = min(len(names), len(numbers), len(models), len(executives))
    for i in range(count):
        try:
            message = generate_message(names[i], models[i], executives[i], inquiry_type)
            phone = f"+91{numbers[i].strip()}"
            print(f"📤 Sending to {names[i]} ({phone})")

            if send_image:
                kit.sendwhats_image(phone, "Creatives.png", caption=message, wait_time=40, tab_close=True)
            else:
                kit.sendwhatsmsg(phone, message, time.localtime().tm_hour, time.localtime().tm_min + 2, tab_close=True)
            
            time.sleep(15)

        except Exception as e:
            print(f"❌ Failed for {names[i]}: {e}")

    messagebox.showinfo("Done", f"Sent messages to {count} customers")

# ==== UI ====
root = tk.Tk()
root.title("Surya Honda WhatsApp Sender")
root.geometry("1200x900")

send_image_var = tk.BooleanVar(value=True)  # default: send image

inquiry_var = tk.StringVar(value="Walk-in")

form_frame = tk.Frame(root)
form_frame.pack(pady=20)

def build_input(label_text):
    frame = tk.Frame(form_frame)
    tk.Label(frame, text=label_text, font=("Arial", 10)).pack(anchor="w")
    txt = tk.Text(frame, height=30, width=25, font=("Courier New", 10))
    txt.pack()
    frame.pack(side="left", padx=10)
    return txt

name_text = build_input("Customer Name")
number_text = build_input("Contact Number")
model_text = build_input("Model Enquired")
executive_text = build_input("Sales Executive")

# ==== Add This Below inquiry_frame ====
image_frame = tk.Frame(root)
tk.Label(image_frame, text="Upload Image:").pack(side="left")
tk.Radiobutton(image_frame, text="Yes", variable=send_image_var, value=True).pack(side="left")
tk.Radiobutton(image_frame, text="No", variable=send_image_var, value=False).pack(side="left")
image_frame.pack(pady=10)

inquiry_frame = tk.Frame(root)
tk.Label(inquiry_frame, text="Inquiry Type:").pack(side="left")
tk.Radiobutton(inquiry_frame, text="Walk-in", variable=inquiry_var, value="Walk-in").pack(side="left")
tk.Radiobutton(inquiry_frame, text="BW Inquiry", variable=inquiry_var, value="BW").pack(side="left")
inquiry_frame.pack(pady=10)

tk.Button(root, text="Send WhatsApp Messages", bg="green", fg="white", font=("Arial", 12), command=send_messages).pack(pady=20)

root.mainloop()
