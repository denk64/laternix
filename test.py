import qrcode
from PIL import Image
import socket

def generate_qr_code(data, file_path):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill='black', back_color='white')

    # Save the QR code to a temporary PNG file
    img.save(file_path)
    return file_path

def convert_png_to_pcx(png_file_path, pcx_file_path):
    # Open the PNG file
    with Image.open(png_file_path) as img:
        # Convert the image to 'P' mode which is required for PCX format
        if img.mode != 'P':
            img = img.convert('P')
        
        # Save the image as PCX
        img.save(pcx_file_path, 'PCX')
    return pcx_file_path

def send_to_printer(ip, port, data):
    # Create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to printer
        sock.connect((ip, port))
        # Send data
        sock.sendall(data)

def main():
    # Settings for the QR code and printer
    data = "https://example.com"
    printer_ip = '192.168.54.138'
    printer_port = 9100

    # Generate and convert QR code
    png_file_path = generate_qr_code(data, 'temp_qr.png')
    pcx_file_path = convert_png_to_pcx(png_file_path, 'qr_code.pcx')

    # Load PCX file into memory
    with open(pcx_file_path, 'rb') as f:
        pcx_data = f.read()

    # Construct command to print QR code
    # Convert string parts to bytes and properly format the print command
    length_data = str(len(pcx_data)).encode()  # Convert the length to bytes
    print_command = b'\nN\nGW100,100,' + length_data + b',' + pcx_data + b'\nP1\n'

    # Send print command to printer
    send_to_printer(printer_ip, printer_port, print_command)


if __name__ == '__main__':
    main()