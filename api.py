from flask import Flask, request, jsonify
import qrcode
from PIL import Image, ImageWin, ImageDraw, ImageFont
import win32print
import win32ui
from datetime import datetime
import csv
import time
import os

app = Flask(__name__)

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
    img = img.resize((size, size), Image.BILINEAR)
    return img


def print_qr_code(printer_name, img, label_width_px, label_height_px, line1, line2, line3, save_path_without_offsets):
    # Calculate the size of the QR code
    qr_width, qr_height = img.size

    # Create a new image with the same dimensions as the label (without offsets)
    label_image_without_offsets = Image.new("RGB", (label_width_px, label_height_px), "white")
    draw_without_offsets = ImageDraw.Draw(label_image_without_offsets)

    # Calculate positions for QR code and text (without offsets)
    x_position_without_offsets = (label_width_px - qr_width) // 2 + 390
    y_position_without_offsets = (label_height_px - qr_height) // 2
    text_x_position_without_offsets = 10  # Adjust as needed

    # Load a font
    font = ImageFont.truetype("arial.ttf", 75)

    # Draw the QR code and text on the label image (without offsets)
    label_image_without_offsets.paste(img, (x_position_without_offsets, y_position_without_offsets))
    draw_without_offsets.text((text_x_position_without_offsets, y_position_without_offsets + 10), line1, fill="black", font=font)
    draw_without_offsets.text((text_x_position_without_offsets, y_position_without_offsets + 110), line2, fill="black", font=font)
    draw_without_offsets.text((text_x_position_without_offsets, y_position_without_offsets + 210), line3, fill="black", font=font)

    # Save the label images to files if the file does not exist
    if not os.path.exists(save_path_without_offsets):
        label_image_without_offsets.save(save_path_without_offsets)


    try:
        
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)
        hDC.StartDoc("QR Code Print")
        hDC.StartPage()

        dib = ImageWin.Dib(img)
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
    except Exception as e:
        print(f"Drucker Godex RT860i GZPL nicht gefunden")

    return save_path_without_offsets
    
def get_serial(identifier):
    return identifier[1:-1]

def write_to_csv(data, filename):
    current_date = datetime.now().strftime('%Y-%m-%d')
    try:
        with open(filename, 'r', newline='') as file:
            last_line = list(csv.reader(file))[-1]
            last_date = last_line[1] if last_line[0] == 'Date' else None
    except FileNotFoundError:
        last_date = None

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['Alias', 'Identifier', 'Serial Number', 'Date'])

        for alias, identifier, serial_number in data:
            formatted_alias = f'="{alias}"'
            writer.writerow([formatted_alias, identifier, serial_number, current_date])

@app.route('/print_qr_code', methods=['POST'])
def print_qr_code_api():
    data = request.json
    alias_label = data.get('alias_label')
    alias_label = alias_label.strip()
    print(f"\nPayload:\n    Alias:    {alias_label}")
    printer_name = data.get('printer_name', "Godex RT860i GZPL")


    if len(alias_label) != 14:
        return jsonify({"error": "Alias is not 14 digits long"}), 400

    if not alias_label.isnumeric():
        return jsonify({"error": "Alias is not numeric"}), 400

    identifier = alias_label[:8]
    serial = get_serial(identifier)
    version_ident = alias_label[-3:]

    version = None
    if version_ident[:2] == "12":
        version = "200mA"
    elif version_ident[:2] == "18":
        version = "300mA"
    elif version_ident[:2] == "24":
        version = "400mA"
    elif version_ident[:2] == "30":
        version = "600mA"
    else:
        version = "Unknown"
    label_width_mm = 50
    label_height_mm = 18
    dpi = 600
    label_width_px = int(label_width_mm / 25.4 * dpi)
    label_height_px = int(label_height_mm / 25.4 * dpi)
    qr_size = int(label_height_mm / 25.4 * dpi * 0.8)

    line_1 = f"Alias: {alias_label}"
    line_2 = f"Serial: {serial}"
    line_3 = version

    img = generate_qr_code(alias_label, qr_size)
    #img.save(f"qr_codes/{alias_label}.png")
    for i in range(3):
        time.sleep(0.3)
        response_img_path = print_qr_code(printer_name, img, label_width_px, label_height_px, line_1, line_2, line_3, f"qr_codes/{alias_label}.png")
        write_to_csv([[alias_label, identifier, serial]], "data.csv")

    # return the image path
    response_img_path = f"image path: H:\\Projects\\laternix\\print_api\\laternix\\qr_codes\\{alias_label}.png"
    return jsonify({"image_path": response_img_path}), 200

if __name__ == '__main__':
    app.run(debug=True)
