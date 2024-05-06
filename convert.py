from PIL import Image

def convert_png_to_pcx(png_file_path, pcx_file_path):
    # Open the PNG file
    with Image.open(png_file_path) as img:
        # Convert the image to 'P' mode which is required for PCX format
        if img.mode != 'P':
            img = img.convert('P')
        
        # Save the image as PCX
        img.save(pcx_file_path, 'PCX')

# Example usage
convert_png_to_pcx('qr_code.png', 'qr_code.pcx')
