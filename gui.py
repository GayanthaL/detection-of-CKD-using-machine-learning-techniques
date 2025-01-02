import tkinter as tk
from tkinter import messagebox
import pandas as pd
import requests

def save_and_upload():
    # Collect user input
    data = {
        'Age': entry_age.get(),
        'Creatinine': entry_creatinine.get(),
        'Albumin': entry_albumin.get(),
        'Sodium': entry_sodium.get(),
        'Calcium': entry_calcium.get(),
        'Potassium': entry_potassium.get(),
        'Chloride': entry_chloride.get(),
        'White_Blood_Cell_Count': entry_white_blood_cell.get(),
        'Red_Blood_Cell_Count': entry_red_blood_cell.get(),
        'Hemoglobin': entry_hemoglobin.get(),
    }

    # Check if any field is empty
    for key, value in data.items():
        if not value:
            messagebox.showerror("Input Error", f"The {key} field cannot be empty!")
            return  # Return and do not proceed with submission if any field is empty

    # Validate if all inputs are positive numbers
    for key, value in data.items():
        try:
            if float(value) < 0:
                messagebox.showerror("Input Error", f"The {key} field cannot have a negative value!")
                return
        except ValueError:
            messagebox.showerror("Input Error", f"The {key} field must be a valid number!")
            return

    # Convert data into a DataFrame
    df = pd.DataFrame([data])

    # Save the DataFrame as a CSV file
    df.to_csv('user_data.csv', index=False)

    # Send CSV file to FastAPI server
    try:
        files = {'file': open('user_data.csv', 'rb')}
        response = requests.post("http://localhost:8000/CKD_predict", files=files)

        # Check the response from the API
        if response.status_code == 200:
            prediction = response.json().get("prediction", "No prediction received")
            messagebox.showinfo("Prediction Result", f"The prediction is: {prediction}")
        else:
            messagebox.showerror("Error", "Failed to get prediction")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def clear_fields():
    # Clear all the input fields
    entry_age.delete(0, tk.END)
    entry_creatinine.delete(0, tk.END)
    entry_albumin.delete(0, tk.END)
    entry_sodium.delete(0, tk.END)
    entry_calcium.delete(0, tk.END)
    entry_potassium.delete(0, tk.END)
    entry_chloride.delete(0, tk.END)
    entry_white_blood_cell.delete(0, tk.END)
    entry_red_blood_cell.delete(0, tk.END)
    entry_hemoglobin.delete(0, tk.END)

# Create the main window
window = tk.Tk()
window.title("CKD Prediction")
window.configure(bg="#f0f0f0")  # Set background color for the window

# Set the window size and position
window.geometry("500x600")

# Configure the grid
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1, minsize=200)
window.grid_columnconfigure(1, weight=2, minsize=250)

# Main topic label (title)
main_topic_label = tk.Label(window, text="Predict CKD or Not", font=("Arial", 16, "bold"), bg="#f0f0f0")
main_topic_label.grid(row=0, column=0, columnspan=2, pady=20)

# Labels and input fields for each parameter with larger font and padding
font = ("Arial", 12)

tk.Label(window, text="Age", font=font, bg="#f0f0f0").grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_age = tk.Entry(window, font=font)
entry_age.grid(row=1, column=1, padx=10, pady=5)

tk.Label(window, text="Creatinine", font=font, bg="#f0f0f0").grid(row=2, column=0, sticky="w", padx=10, pady=5)
entry_creatinine = tk.Entry(window, font=font)
entry_creatinine.grid(row=2, column=1, padx=10, pady=5)

tk.Label(window, text="Albumin", font=font, bg="#f0f0f0").grid(row=3, column=0, sticky="w", padx=10, pady=5)
entry_albumin = tk.Entry(window, font=font)
entry_albumin.grid(row=3, column=1, padx=10, pady=5)

tk.Label(window, text="Sodium", font=font, bg="#f0f0f0").grid(row=4, column=0, sticky="w", padx=10, pady=5)
entry_sodium = tk.Entry(window, font=font)
entry_sodium.grid(row=4, column=1, padx=10, pady=5)

tk.Label(window, text="Calcium", font=font, bg="#f0f0f0").grid(row=5, column=0, sticky="w", padx=10, pady=5)
entry_calcium = tk.Entry(window, font=font)
entry_calcium.grid(row=5, column=1, padx=10, pady=5)

tk.Label(window, text="Potassium", font=font, bg="#f0f0f0").grid(row=6, column=0, sticky="w", padx=10, pady=5)
entry_potassium = tk.Entry(window, font=font)
entry_potassium.grid(row=6, column=1, padx=10, pady=5)

tk.Label(window, text="Chloride", font=font, bg="#f0f0f0").grid(row=7, column=0, sticky="w", padx=10, pady=5)
entry_chloride = tk.Entry(window, font=font)
entry_chloride.grid(row=7, column=1, padx=10, pady=5)

tk.Label(window, text="White Blood Cell Count", font=font, bg="#f0f0f0").grid(row=8, column=0, sticky="w", padx=10, pady=5)
entry_white_blood_cell = tk.Entry(window, font=font)
entry_white_blood_cell.grid(row=8, column=1, padx=10, pady=5)

tk.Label(window, text="Red Blood Cell Count", font=font, bg="#f0f0f0").grid(row=9, column=0, sticky="w", padx=10, pady=5)
entry_red_blood_cell = tk.Entry(window, font=font)
entry_red_blood_cell.grid(row=9, column=1, padx=10, pady=5)

tk.Label(window, text="Hemoglobin", font=font, bg="#f0f0f0").grid(row=10, column=0, sticky="w", padx=10, pady=5)
entry_hemoglobin = tk.Entry(window, font=font)
entry_hemoglobin.grid(row=10, column=1, padx=10, pady=5)

# Submit button with larger font
submit_button = tk.Button(window, text="Submit", command=save_and_upload, font=("Arial", 14), bg="#4CAF50", fg="white")
submit_button.grid(row=11, column=0, columnspan=2, pady=10)

# Clear button to reset fields
clear_button = tk.Button(window, text="Clear", command=clear_fields, font=("Arial", 14), bg="#f44336", fg="white")
clear_button.grid(row=12, column=0, columnspan=2, pady=10)

# Start the GUI
window.mainloop()
