# Batch Image Resizer

A simple web application that allows you to resize multiple images at once with drag & drop functionality.

## Features

- **Drag & Drop**: Simply drag images from your computer onto the interface
- **Multiple Upload Methods**: Choose files via browser or paste image URLs
- **Batch Processing**: Resize multiple images simultaneously
- **Smart Downloads**: 
  - Single image: Downloads directly as JPEG
  - Multiple images: Downloads as ZIP file
- **Aspect Ratio Preservation**: Maintains original image proportions
- **File Naming**: Automatically adds dimensions to filename (e.g., `photo_300x200.jpg`)

## Supported Formats

- JPEG/JPG
- PNG
- GIF
- WebP

## Installation

1. Clone or download this project
2. Navigate to the project directory:
   ```bash
   cd "300-px resizer"
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your web browser and go to:
   ```
   http://localhost:5000
   ```

## How to Use

### Method 1: Drag & Drop
1. Drag image files from your computer directly onto the drop area
2. Selected files will appear in a list below
3. Set your desired width (height is calculated automatically)
4. Click "Resize & Download"

### Method 2: File Browser
1. Click on the drag & drop area to open file browser
2. Select one or multiple image files
3. Set your desired width
4. Click "Resize & Download"

### Method 3: Image URLs
1. Paste image URLs in the textarea (one per line)
2. Set your desired width
3. Click "Resize & Download"

### Mixed Method
You can combine file uploads and URLs in the same batch!

## Output

- **Single Image**: Downloads as `originalname_WIDTHxHEIGHT.jpg`
- **Multiple Images**: Downloads as `resized_images.zip` containing all resized images

## Technical Details

- Built with Flask (Python web framework)
- Uses Pillow (PIL) for image processing
- Maintains aspect ratios automatically
- LANCZOS resampling for high-quality resizing
- Secure filename handling
- Error handling for invalid images/URLs

## File Structure

```
300-px resizer/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.txt         # This documentation
├── templates/
│   └── index.html     # Web interface
├── uploads/           # Temporary upload storage
└── resized_images/    # Output directory
```

## Requirements

- Python 3.6+
- Flask 2.3.3+
- Pillow 10.0.1+
- requests 2.31.0+

## Troubleshooting

**Common Issues:**

1. **Module not found**: Make sure you've installed requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. **Permission errors**: Ensure the app has write permissions in the project directory

3. **Large files**: Very large images may take longer to process

4. **Network timeouts**: URLs may fail if the image server is slow or unreachable

## Development

This is a development server. For production deployment, use a WSGI server like Gunicorn.

## License

Free to use and modify for personal and commercial projects.

---

Enjoy resizing your images! 🖼️✨
