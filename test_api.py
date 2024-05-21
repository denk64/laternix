import win32print
import win32ui
from PIL import Image, ImageWin, ImageDraw, ImageFont

def create_test_image(label_width_px, label_height_px, dpi):
    # Create a new image with the specified dimensions
    test_image = Image.new("RGB", (label_width_px, label_height_px), "white")
    draw = ImageDraw.Draw(test_image)
    
    # Load a font
    font = ImageFont.truetype("arial.ttf", 50)

    # Draw horizontal lines
    for y in range(0, label_height_px, dpi // 2):  # Every 0.5 inch
        draw.line((0, y, label_width_px, y), fill="black", width=5)
        draw.text((10, y + 5), f"Y={y // dpi} in", fill="black", font=font)

    # Draw vertical lines
    for x in range(0, label_width_px, dpi // 2):  # Every 0.5 inch
        draw.line((x, 0, x, label_height_px), fill="black", width=5)
        draw.text((x + 5, 10), f"X={x // dpi} in", fill="black", font=font)

    return test_image

def print_test_page(printer_name, test_image):
    try:
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)
        hDC.StartDoc("Test Print")
        hDC.StartPage()

        dib = ImageWin.Dib(test_image)
        dib.draw(hDC.GetHandleOutput(), (0, 0, test_image.width, test_image.height))

        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC()
    except Exception as e:
        print(f"Printer {printer_name} not found: {e}")

def main():
    printer_name = "Godex RT863i"  # Replace with your printer name

    label_width_mm = 50
    label_height_mm = 18
    dpi = 600
    label_width_px = int(label_width_mm / 25.4 * dpi)
    label_height_px = int(label_height_mm / 25.4 * dpi)

    test_image = create_test_image(label_width_px, label_height_px, dpi)
    
    print_test_page(printer_name, test_image)
    print("Test page printed successfully")

if __name__ == '__main__':
    main()
