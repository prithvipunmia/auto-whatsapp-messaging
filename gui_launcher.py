import tkinter as tk
from tkinter import messagebox
import pywhatkit as kit
import time
from datetime import datetime

# === Message Template Builder ===
def generate_message(name, model, executive, inquiry_type, include_image):
    date_str = datetime.now().strftime("%d %B %Y")

    if inquiry_type == "BW":
        message = f"""Hello {name},
Thank you for your interest in Honda {model} on the Bikewala website. Sales Executive {executive} will be in touch with you soon.

– Team Surya Honda"""
    else:  # Retail Inquiry
        message = f"""Hello {name},
Thank you for visiting Surya Honda Porur on {date_str} and enquiring about {model} with Sales Executive {executive}. We look forward to serving you.

– Team Surya Honda"""

    return message

# === WhatsApp Sender ===
def send_messages():
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

    for i in range(count):
        try:
            name = names[i].strip()
            phone = "+91" + numbers[i].strip()
            model = models[i].strip()
            executive = executives[i].strip()
            message = generate_message(name, model, executive, inquiry_type, include_image)

            print(f"📤 Sending to {name} ({phone})")

            if include_image == "Yes":
                kit.sendwhats_image(phone, "Creatives.png", caption=message, wait_time=15, tab_close=True)
            else:
                from datetime import datetime
                from datetime import datetime, timedelta

                now = datetime.now() + timedelta(minutes=1)
                hour_now = now.hour
                minute_now = now.minute

                kit.sendwhatmsg(phone, message, hour_now, minute_now, 15, True, True)

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
name_text = build_input("Customer Name")
number_text = build_input("Contact Number")
model_text = build_input("Model Enquired")
executive_text = build_input("Sales Executive")

# === Inquiry Type Radio Buttons ===
inquiry_frame = tk.Frame(root)
tk.Label(inquiry_frame, text="Inquiry Type:", font=("Arial", 10)).pack(side="left")
tk.Radiobutton(inquiry_frame, text="Retail", variable=inquiry_var, value="Retail").pack(side="left", padx=10)
tk.Radiobutton(inquiry_frame, text="BW", variable=inquiry_var, value="BW").pack(side="left", padx=10)
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
