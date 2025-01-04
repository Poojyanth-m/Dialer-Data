import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import csv
import json
import tkinter as tk
from tkinter import filedialog

# Global variable to store phone number history
phone_history = []

# Save phone number details to a CSV file
def save_to_csv(data, filename="phone_details.csv"):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Phone Number', 'Timezone', 'Service Provider', 'Country'])
            writer.writerows(data)
        return filename
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return None

# Save phone number details to a JSON file
def save_to_json(data, filename="phone_details.json"):
    try:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        return filename
    except Exception as e:
        print(f"Error saving to JSON: {e}")
        return None

# Validate phone number input (starts with country code and is valid)
def validate_input(input_number):
    try:
        if not input_number.startswith('+'):
            raise ValueError("Phone number should start with a country code, e.g., +1")
        parsed_no = phonenumbers.parse(input_number)
        if not phonenumbers.is_valid_number(parsed_no):
            raise ValueError("Invalid phone number format")
        return parsed_no
    except ValueError as e:
        print(f"Error: {e}")
        return None

# Display phone number details (timezone, carrier, country)
def display_phone_info(parsed_no):
    timezones = timezone.time_zones_for_number(parsed_no)
    service_provider = carrier.name_for_number(parsed_no, "en")
    country = geocoder.description_for_number(parsed_no, "en")
    
    phone_details = {
        "Phone Number": str(parsed_no),
        "Timezone": ", ".join(timezones),
        "Service Provider": service_provider if service_provider else "Unknown",
        "Country": country if country else "Unknown"
    }
    
    return phone_details

# Handle the submission from the GUI
def on_submit():
    phone_number = entry.get()
    parsed_no = validate_input(phone_number)
    
    if parsed_no:
        phone_info = display_phone_info(parsed_no)
        phone_history.append(phone_info)
        
        output_text.insert(tk.END, f"Phone Number: {phone_info['Phone Number']}\n")
        output_text.insert(tk.END, f"Timezone(s): {phone_info['Timezone']}\n")
        output_text.insert(tk.END, f"Service Provider: {phone_info['Service Provider']}\n")
        output_text.insert(tk.END, f"Country: {phone_info['Country']}\n\n")
        
        status_label.config(text="Phone number details added successfully!", fg="green")
    else:
        status_label.config(text="Invalid phone number!", fg="red")

# Save the details to the selected file format and display the file path
def save_to_file():
    file_type = file_format.get()
    file_path = None
    
    if file_type == "CSV":
        file_path = save_to_csv(phone_history)
    elif file_type == "JSON":
        file_path = save_to_json(phone_history)
    
    if file_path:
        file_path_label.config(text=f"Details saved to: {file_path}", fg="blue")
    else:
        file_path_label.config(text="Error saving details. Try again.", fg="red")

# Allow user to choose a custom file path and save the file
def save_custom_file():
    file_type = file_format.get()
    
    file_path = filedialog.asksaveasfilename(defaultextension=f".{file_type.lower()}", 
                                             filetypes=[(f"{file_type} files", f"*.{file_type.lower()}")])
    if not file_path:
        return  # User canceled the save operation

    if file_type == "CSV":
        file_path = save_to_csv(phone_history, file_path)
    elif file_type == "JSON":
        file_path = save_to_json(phone_history, file_path)
    
    if file_path:
        file_path_label.config(text=f"Details saved to: {file_path}", fg="blue")
    else:
        file_path_label.config(text="Error saving details. Try again.", fg="red")

# Run the GUI interface
def run_gui():
    global entry, output_text, phone_history, status_label, file_format, file_path_label
    
    phone_history = []  # List to store valid phone details
    
    root = tk.Tk()
    root.title("Phone Number Details")

    label = tk.Label(root, text="Enter Phone Number with Country Code:")
    label.pack()
    
    entry = tk.Entry(root)
    entry.pack()
    
    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack()

    output_text = tk.Text(root, height=10, width=50)
    output_text.pack()

    file_format_label = tk.Label(root, text="Select Output Format:")
    file_format_label.pack()

    file_format = tk.StringVar(root)
    file_format.set("CSV")  # Default format is CSV

    file_format_menu = tk.OptionMenu(root, file_format, "CSV", "JSON")
    file_format_menu.pack()

    save_button = tk.Button(root, text="Save to File", command=save_to_file)
    save_button.pack()

    save_custom_button = tk.Button(root, text="Save to Custom Location", command=save_custom_file)
    save_custom_button.pack()

    status_label = tk.Label(root, text="", fg="blue")
    status_label.pack()

    file_path_label = tk.Label(root, text="", fg="blue")
    file_path_label.pack()

    root.mainloop()

if __name__ == "__main__":
    run_gui()
