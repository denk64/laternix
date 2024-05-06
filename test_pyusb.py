import qrcode
from PIL import Image, ImageWin
import win32print
import win32ui

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
        # count 14 numbers
        if len(alias_label) != 14:
            print("Alias is not 14 numbers")
            return
        # Check if the input is a number
        if not alias_label.isnumeric():
            print("Alias is not a number")
            return
        # Take first 8 numbers as Identifier
        identifier = alias_label[:8]

        # Data to be encoded in QR Code
        data = "Example data for QR Code"
        line_1 = f"Alias: {alias_label}"
        line_2 = f"Identifier: {identifier}"
        line_3 = f"200mA"

        # Generate QR code image
        img = generate_qr_code(identifier, qr_size)
        print("Printing QR code...")
        print("Identifier: ", identifier)

        for i in range(3):
            # Print QR Code
            print(f"Label {i+1}")
            print_qr_code(printer_name, img, label_width_px, label_height_px, line_1, line_2, line_3)

if __name__ == "__main__":
    main()
