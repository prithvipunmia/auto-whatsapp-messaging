import tkinter as tk
from tkinter import messagebox
import pywhatkit as kit
import time
from datetime import datetime, timedelta

import sys, os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # Used by PyInstaller when bundled
    except Exception:
        base_path = os.path.abspath(".")  # Fallback for script mode
    return os.path.join(base_path, relative_path)

# === Message Template Builder ===
def generate_message(name, model, executive, inquiry_type, include_image, inquiry_date):
    date_str = inquiry_date

    if inquiry_type == "BW":
        message = f"""Hello {name},
Thank you for your interest in Honda {model} on the Bikewala website. Our Sales Executive {executive} will be in touch with you soon. 

Exclusive Offers at Surya Honda:
• Cashback offer upto ₹5,000 on your favourite Honda models   
• Insurance free (on select models)  
• Leading finance partners with low cost EMI options

You can find the complete catalogue of Honda vehicles here on Whatsapp. 

Contact Us:Kattapakkam/Porur:
Sales: 9884492386/ 7823944304
Service: 7823944795/ 7823944306

–  Team Surya Honda"""
    
    elif inquiry_type == "Delivery":
        message = f"""Hello {name},
Thank you for choosing Honda {model}. We hope you had a great delivery experience with Sales Executive {executive}.  
We’re thrilled to have you as part of the Surya Honda family!

Contact Us:Kattapakkam/Porur:
Sales: 9884492386/ 7823944304
Service: 7823944795/ 7823944306

We’re always here to help.

– Team Surya Honda"""

    else:  # Retail Inquiry
        message = f"""Hello {name},
Thank you for visiting Surya Honda Porur on {date_str} and enquiring about {model} with Sales Executive {executive}. We look forward to serving you.

Exclusive Offers:
• Cashback offer upto ₹5,000 on your favourite Honda models   
• Insurance free (on select models)  
• Leading finance partners with low cost EMI options

You can find the complete catalogue of Honda vehicles here on Whatsapp.

We are available on WhatsApp or phone for your convenience.  

Contact Us:Kattapakkam/Porur:
Sales: 9884492386/ 7823944304
Service: 7823944795/ 7823944306

– Team Surya Honda"""

    return message

# === WhatsApp Sender ===
def send_messages():
    inquiry_dates = date_text.get("1.0", tk.END).strip().splitlines()
    names = name_text.get("1.0", tk.END).strip().splitlines()
    numbers = number_text.get("1.0", tk.END).strip().splitlines()
    models = model_text.get("1.0", tk.END).strip().splitlines()
    executives = executive_text.get("1.0", tk.END).strip().splitlines()
    inquiry_type = inquiry_var.get()
    include_image = image_var.get()

    count = min(len(names), len(numbers), len(models), len(executives))
    if count == 0:
        messagebox.showerror("Error", "Please enter valid customer data.")
        return

    wait_time_image = 30
    wait_time_text = 10

    for i in range(count):
        try:
            inquiry_date = inquiry_dates[i].strip()
            name = names[i].strip()
            phone = "+91" + numbers[i].strip()
            model = models[i].strip()
            executive = executives[i].strip()
            message = generate_message(name, model, executive, inquiry_type, include_image, inquiry_date)

            print(f"📤 Sending to {name} ({phone})")

            if include_image == "Yes":
                kit.sendwhats_image(phone, "Creatives.png", caption=message, wait_time=wait_time_image, tab_close=True)
            else:
                kit.sendwhatmsg_instantly(phone, message, wait_time=wait_time_text, tab_close=True)

            time.sleep(40)
        except Exception as e:
            print(f"❌ Failed for {name}: {e}")

    messagebox.showinfo("Done", f"Sent messages to {count} customers")


# === GUI Setup ===
root = tk.Tk()
root.title("Surya Honda WhatsApp Messenger")
root.geometry("1200x720")

# === Inquiry Type Selection ===
inquiry_var = tk.StringVar(value="Retail")
image_var = tk.StringVar(value="Yes")

tk.Label(root, text="Surya Honda Message Sender", font=("Arial", 16)).pack(pady=10)

form_frame = tk.Frame(root)
form_frame.pack(pady=10)

# === Utility to Create Inputs ===
def build_input(label_text):
    frame = tk.Frame(form_frame)
    tk.Label(frame, text=label_text, font=("Arial", 10)).pack(anchor="w")
    txt = tk.Text(frame, height=30, width=25, font=("Courier New", 10))
    txt.pack()
    frame.pack(side="left", padx=10)
    return txt

# === Fields for Bulk Input ===
date_text = build_input("Inquiry Date")
name_text = build_input("Customer Name")
number_text = build_input("Contact Number")
model_text = build_input("Model Enquired")
executive_text = build_input("Sales Executive")

# === Inquiry Type Radio Buttons ===
inquiry_frame = tk.Frame(root)
tk.Label(inquiry_frame, text="Inquiry Type:", font=("Arial", 10)).pack(side="left")
tk.Radiobutton(inquiry_frame, text="Retail", variable=inquiry_var, value="Retail").pack(side="left", padx=10)
tk.Radiobutton(inquiry_frame, text="BW", variable=inquiry_var, value="BW").pack(side="left", padx=10)
tk.Radiobutton(inquiry_frame, text="Delivery", variable=inquiry_var, value="Delivery").pack(side="left", padx=10)
inquiry_frame.pack(pady=5)

# === Image Include Option ===
image_frame = tk.Frame(root)
tk.Label(image_frame, text="Include Image?", font=("Arial", 10)).pack(side="left")
tk.Radiobutton(image_frame, text="Yes", variable=image_var, value="Yes").pack(side="left", padx=10)
tk.Radiobutton(image_frame, text="No", variable=image_var, value="No").pack(side="left", padx=10)
image_frame.pack(pady=5)

# === Submit Button ===
tk.Button(root, text="Send WhatsApp Messages", bg="green", fg="white", font=("Arial", 12), command=send_messages).pack(pady=20)

root.mainloop()
