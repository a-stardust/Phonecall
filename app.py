import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# Constants for file paths
CSS_FILE = 'styles.css'
JS_FILE = 'script.js'
OUTPUT_DIR = 'webpages'

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Generate index.html with links to employee-specific directories
def generate_index_page(file_names):
    index_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Phone Directories</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Poppins', sans-serif; background-color: #f3f6fb; padding: 40px; }
            h1 { text-align: center; font-size: 32px; color: #333; }
            .employee-list { margin-top: 20px; }
            .employee-link { display: block; margin: 10px 0; font-size: 25px; text-align: center;color: #007BFF; text-decoration: none; }
            .employee-link:hover { color: #0056b3; }
        </style>
    </head>
    <body>
        <h1>Phone Directories</h1>
        <div class="employee-list">
    """
    for file_name in file_names:
        name_without_extension = os.path.splitext(file_name)[0]
        link = f"{OUTPUT_DIR}/{name_without_extension}.html"
        index_content += f'<a href="{link}" class="employee-link">{name_without_extension}</a>\n'

    index_content += """
        </div>
    </body>
    </html>
    """

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(index_content)

# Function to generate a webpage for each CSV file
def generate_webpage_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        if 'School Name' not in df.columns or 'Phone Number' not in df.columns:
            raise ValueError('The CSV file must have "School Name" and "Phone Number" columns')
        
        file_name = os.path.basename(file_path)
        name_without_extension = os.path.splitext(file_name)[0]
        output_path = os.path.join(OUTPUT_DIR, f"{name_without_extension}.html")

        # Generate HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{name_without_extension} Phone Directory</title>
            <link rel="stylesheet" href="../{CSS_FILE}">
            <script src="../{JS_FILE}" defer></script>
        </head>
        <body>
            <header>     
                <h1>{name_without_extension}'s Phone Directory</h1>
            </header>
           <div class="container">
                <div class="school-list">
        """
        for i, row in df.iterrows():
            school_name = row['School Name']
            phone_number = row['Phone Number']
            html_content += f"""
            <div class="school-item" id="school-{i}">
                <input type="checkbox" id="checkbox-{i}" class="call-checkbox" data-index="{i}">
                <label for="checkbox-{i}" class="school-label">
                    <a href="tel:{phone_number}">{school_name}</a>
                </label>
            </div>
            """

        html_content += """
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print(f"Generated webpage: {output_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Create the Python UI for uploading CSV files
def upload_csv_files():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_paths = filedialog.askopenfilenames(title="Select CSV files", filetypes=[("CSV files", "*.csv")])
    if not file_paths:
        messagebox.showinfo("No file selected", "Please select at least one CSV file.")
        return

    file_names = []
    for file_path in file_paths:
        file_names.append(os.path.basename(file_path))
        generate_webpage_from_csv(file_path)

    if file_names:
        generate_index_page(file_names)
        messagebox.showinfo("Success", "Webpages and index page generated successfully!")

# Run the script in VS Code or as a standalone
if __name__ == "__main__":
    upload_csv_files()
