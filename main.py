import pywhatkit as kit
import pandas as pd
import time
from datetime import datetime

# Helper to format date like "13th December"
def format_date_with_suffix(date_obj):
    day = date_obj.day
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return f"{day}{suffix} {date_obj.strftime('%B')}"

# Load your Excel file (first 10 rows only for safety)
df = pd.read_excel("EnquiryList.xlsx", sheet_name="EnquiryList").head(10)

# Add a 'Status' column if it 
#  doesn’t exist
if 'Status' not in df.columns:
    df['Status'] = ""

# Loop through each customer
for index, row in df.iterrows():
    name = row['Customer Name']
    date_raw = pd.to_datetime(row['Date'])
    formatted_date = format_date_with_suffix(date_raw)
    model = row['Model Enquired']
    exec_name = row['Executive Name']
    phone = str(row['Customer Contact']).strip()
    formatted_phone = f"+91{phone}"

    # Message body
    message = f"""Hello {name},
Thank you for visiting Surya Honda Porur on {formatted_date} and enquiring about {model} with Sales Executive {exec_name}.

Surya Honda is committed to delivering a seamless experience from enquiry to after-sales support, ensuring your journey with us is smooth and satisfying.

Exclusive Offers:
• Cashback offer upto ₹5,000 on your favourite Honda Activa   
• Insurance free (on select models)  
• Leading finance partners with low cost EMI options

For any sales queries, contact us at 7823944301 / 04  
For service queries, contact us at 7823944302 / 06

We are available on WhatsApp or phone for your convenience.  
– Team Surya Honda"""

    try:
        print(f"📤 Attempting to send message to {name} ({formatted_phone})...")

        kit.sendwhats_image(
            receiver=formatted_phone,
            img_path="Creatives.png",
            caption=message,
            wait_time=15,
            tab_close=True
        )

        print(f"✅ Message sent to {name} at {datetime.now().strftime('%H:%M:%S')}")
        df.at[index, 'Status'] = "Sent"
    except Exception as e:
        print(f"❌ Failed to send to {name}: {e}")
        df.at[index, 'Status'] = f"Failed: {str(e)}"

    time.sleep(40)  # Wait extra time for photo delivery

# Save updated sheet
df.to_excel("EnquiryList_updated.xlsx", index=False)
print("📝 All done. Status saved to 'EnquiryList_updated.xlsx'")