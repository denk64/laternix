from flask import Flask, request, jsonify
import qrcode
from PIL import Image, ImageWin
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

def print_qr_code(printer_name, img, label_width_px, label_height_px, line1, line2, line3):
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)
    hDC.StartDoc("QR Code Print")
    hDC.StartPage()

    dib = ImageWin.Dib(img)

    qr_width, qr_height = img.size
    margin_right = 500
    x_position = label_width_px - qr_width + margin_right
    y_position = (label_height_px - qr_height) // 1

    text_x_position = label_width_px - label_width_px + 600

    font = win32ui.CreateFont({
        "name": "Arial",
        "height": 75,
    })
    hDC.SelectObject(font)

    hDC.TextOut(text_x_position, y_position + 10, line1)
    hDC.TextOut(text_x_position, y_position + 110, line2)
    hDC.TextOut(text_x_position, y_position + 210, line3)

    dib.draw(hDC.GetHandleOutput(), (x_position, y_position, x_position + qr_width, y_position + qr_height))

    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()

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
    printer_name = data.get('printer_name', "Godex RT860i GZPL")

    if alias_label in ["61599645", "61599635", "61599605"]:
        alias_label += "040186"
    elif alias_label in ["61599625", "61599655", "61599615"]:
        alias_label += "040244"

    if len(alias_label) == 8:
        alias_label = alias_label.strip() + "040126"

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

    for i in range(3):
        print_qr_code(printer_name, img, label_width_px, label_height_px, line_1, line_2, line_3)
        time.sleep(0.3)

    write_to_csv([[alias_label, identifier, serial]], "data.csv")

    return jsonify({"message": "QR Code printed and data saved"}), 200

if __name__ == '__main__':
    app.run(debug=True)


# Example request:
# payload = {
#     "alias_label": "61599645",
#     "printer_name": "Godex RT860i GZPL"
# }
# response = requests.post('http://127.0.0.1:5000/print_qr_code', json=payload)
# print(response.json())
# Example response:
# {
#     "message": "QR Code printed and data saved"
# }
# Example error response:
# {
#     "error": "Alias is not 14 digits long"
# }