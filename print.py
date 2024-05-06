import socket

def send_to_printer(ip, port, data):
    # Create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to printer
        sock.connect((ip, port))
        # Send data
        sock.sendall(data)

# Printer IP and port (example values, replace with actual printer IP and port)
printer_ip = '192.168.54.138'
printer_port = 9100

# Command to print QR code (This is an illustrative example; check your printer's manual for exact commands)
# You would need to convert your image to a format like PCX or GRF and load it here as binary data
print_command = b'\nN\nGW100,100,1,1,qr_code.pcx\nP1\n'

# Send print command to printer
send_to_printer(printer_ip, printer_port, print_command)
