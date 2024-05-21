
# QR Code Labeling and Printing API

This Flask application provides endpoints to generate, save, and print QR code labels. It includes two main endpoints:

- `/save_qr_code_image`: Generates a QR code, saves it as an image, and returns the image path.
- `/print_qr_code`: Generates a QR code and sends it to a specified printer.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
  - [POST /save_qr_code_image](#post-save_qr_code_image)
  - [POST /print_qr_code](#post-print_qr_code)
- [Functions](#functions)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/yourusername/qr-code-labeling.git
   cd qr-code-labeling
   \`\`\`

2. Create and activate a virtual environment:
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows use \`venv\Scripts\activate\`
   \`\`\`

3. Install the required packages:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. Run the Flask application:
   \`\`\`bash
   python app.py
   \`\`\`

## Usage

- Ensure your Flask application is running.
- Use an HTTP client (like Postman) to interact with the API endpoints.

## API Endpoints

### POST /save_qr_code_image

Generates a QR code from the provided alias label, saves the QR code image, and returns the path to the saved image.

**Request:**

- \`alias_label\` (string, required): A 14-digit numeric string used to generate the QR code.

**Response:**

- \`image_path\` (string): The path to the saved QR code image.

**Example:**

\`\`\`json
{
  "alias_label": "12345678901234"
}
\`\`\`

**Response:**

\`\`\`json
{
  "image_path": "image path: H:\\Projects\\laternix\\print_api\\laternix\\qr_codes\\12345678901234.png"
}
\`\`\`

### POST /print_qr_code

Generates a QR code from the provided alias label and sends it to the specified printer.

**Request:**

- \`alias_label\` (string, required): A 14-digit numeric string used to generate the QR code.
- \`printer_name\` (string, optional): The name of the printer. Default is "Godex RT860i GZPL".

**Response:**

- \`message\` (string): A success message indicating that the QR code has been printed.

**Example:**

\`\`\`json
{
  "alias_label": "12345678901234",
  "printer_name": "Godex RT860i GZPL"
}
\`\`\`

**Response:**

\`\`\`json
{
  "message": "QR code printed successfully"
}
\`\`\`

## Functions

### generate_qr_code(data, size)

Generates a QR code image from the provided data.

- \`data\` (string): The data to encode in the QR code.
- \`size\` (int): The size of the generated QR code image.

### save_qr_code_image(img, label_width_px, label_height_px, line1, line2, line3, save_path)

Saves the QR code image with additional label information.

- \`img\` (PIL.Image): The QR code image.
- \`label_width_px\` (int): The width of the label in pixels.
- \`label_height_px\` (int): The height of the label in pixels.
- \`line1\`, \`line2\`, \`line3\` (string): The text lines to add to the label.
- \`save_path\` (string): The file path to save the label image.

### print_qr_code(printer_name, img, label_width_px, label_height_px, line1, line2, line3)

Prints the QR code image with additional label information.

- \`printer_name\` (string): The name of the printer.
- \`img\` (PIL.Image): The QR code image.
- \`label_width_px\` (int): The width of the label in pixels.
- \`label_height_px\` (int): The height of the label in pixels.
- \`line1\`, \`line2\`, \`line3\` (string): The text lines to add to the label.

### get_serial(identifier)

Extracts the serial number from the identifier.

- \`identifier\` (string): The identifier from which to extract the serial number.

### write_to_csv(data, filename)

Writes the provided data to a CSV file.

- \`data\` (list): The data to write to the CSV file.
- \`filename\` (string): The name of the CSV file.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
