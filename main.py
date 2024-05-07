import qrcode
from PIL import Image, ImageWin
import win32print
import win32ui
from datetime import datetime
import csv
import time
import os

def clear_screen():
    # Check if the operating system is Windows
    if os.name == 'nt':
        os.system('cls')  # For Windows
    else:
        os.system('clear')  # For Unix/Linux/Mac

def generate_qr_code(data, size):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white').convert('RGB')
    img = img.resize((size, size), Image.BILINEAR)  # Resize the image
    return img


def print_qr_code(printer_name, img, label_width_px, label_height_px, line1, line2, line3):
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)
    hDC.StartDoc("QR Code Print")
    hDC.StartPage()

    dib = ImageWin.Dib(img)

    # Calculate the position to align the QR code to the right
    qr_width, qr_height = img.size
    margin_right = 500  # Margin from the right edge in pixels
    x_position = label_width_px - qr_width + margin_right
    y_position = (label_height_px - qr_height) // 1  # Center vertically

    text_x_position = label_width_px - label_width_px + 600
    # text_x_position = 10
    # text_y_position = 10

    # Create and select the font
    font = win32ui.CreateFont({
        "name": "Arial",
        "height": 75,  # Height in logical units; adjust size as needed
    })
    hDC.SelectObject(font)

    # Write from left to right 3 lines of text
    hDC.TextOut(text_x_position, y_position+10, line1)
    hDC.TextOut(text_x_position, y_position+110, line2)
    hDC.TextOut(text_x_position, y_position+210, line3)


    # Draw the image at the calculated position
    dib.draw(hDC.GetHandleOutput(), (x_position, y_position, x_position + qr_width, y_position + qr_height))


    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()

# Function to take identifier, remove first and last number and return the remaining 6 numbers
def get_serial(identifier):
    return identifier[1:-1]

def write_to_csv(data, filename):
    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Attempt to determine the last written date
    try:
        with open(filename, 'r', newline='') as file:
            # Read all content and check the last date entry
            last_line = list(csv.reader(file))[-1]
            last_date = last_line[1] if last_line[0] == 'Date' else None
    except FileNotFoundError:
        last_date = None  # File does not exist yet

    # Open the file in append mode, create if doesn't exist
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        
        # Write the headers if the file is newly created or empty
        if file.tell() == 0:
            writer.writerow(['Alias', 'Identifier', 'Serial Number', 'Date'])

        # Write the data
        for alias, identifier, serial_number in data:
            # Ensure alias is treated as a full string, not a number
            formatted_alias = f'="{alias}"'
            writer.writerow([formatted_alias, identifier, serial_number, current_date])

def main():
    # Printer name as seen in Windows Printers and Devices. Replace with your printer name.
    printer_name = "Godex RT860i GZPL"  # Change this to the exact name of your printer in Windows

    # Label dimensions in pixels (600 DPI printer)
    label_width_mm = 50  # width in millimeters
    label_height_mm = 18  # height in millimeters
    dpi = 600
    label_width_px = int(label_width_mm / 25.4 * dpi)
    label_height_px = int(label_height_mm / 25.4 * dpi)

    # QR code size (approximately 80% of label height)
    qr_size = int(label_height_mm / 25.4 * dpi * 0.8)


    while True:
        # Take an input from the user
        alias_label = input("Etiket einscannen: ")

        # Clear the screen
        try:
            clear_screen()
        except:
            pass
        # count 14 numbers
        if len(alias_label) != 14:
            print("Alias ist nicht 14 Zahlen lang")
            continue
        # Check if the input is a number
        if not alias_label.isnumeric():
            print("Alias ist nicht numerisch")
            continue


        # Take first 8 numbers as Identifier
        identifier = alias_label[:8]

        # Serial number
        serial = get_serial(identifier)


        # Data to be encoded in QR Code
        data = "Example data for QR Code"
        line_1 = f"Alias: {alias_label}"
        line_2 = f"Identifier: {identifier}"
        line_3 = f"200mA"

        print(f"Alias: {alias_label}\nIdentifier: {identifier}\nSerial: {serial}\nVersion: 200mA\n")


        # Generate QR code image
        img = generate_qr_code(identifier, qr_size)
        print("Drucke QR Code...")

        for i in range(3):
            # Print QR Code
            print(f"Label {i+1}")
            print_qr_code(printer_name, img, label_width_px, label_height_px, line_1, line_2, line_3)
            time.sleep(0.3)

        print("QR Code gedruckt.")
        write_to_csv([[alias_label, identifier, serial]], "data.csv")
        print("Die Daten wurden in data.csv gespeichert.\n\n")

if __name__ == "__main__":
    main()
