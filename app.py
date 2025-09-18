import os
import requests
import zipfile
import tempfile
from flask import Flask, render_template, request, send_file
from PIL import Image
from io import BytesIO
from werkzeug.utils import secure_filename

app = Flask(__name__)
RESIZED_FOLDER = 'resized_images'
app.config['RESIZED_FOLDER'] = RESIZED_FOLDER

# Create the folder if it doesn't exist
os.makedirs(RESIZED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

def process_image(image_source, new_width, filename_prefix="image", index=0):
    """Process a single image from either file upload or URL"""
    try:
        if isinstance(image_source, str):  # URL
            response = requests.get(image_source, timeout=10)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            original_filename = image_source.split('/')[-1] or f"{filename_prefix}_{index+1}.jpg"
        else:  # File upload
            image = Image.open(image_source)
            original_filename = getattr(image_source, 'filename', f"{filename_prefix}_{index+1}.jpg")
        
        # Calculate new height while maintaining aspect ratio
        original_width, original_height = image.size
        new_height = int(original_height * (new_width / original_width))
        
        # Resize the image
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Create filename with dimensions
        name, ext = os.path.splitext(original_filename)
        if not ext:
            ext = '.jpg'
        resized_filename = f"{secure_filename(name)}_{new_width}x{new_height}{ext}"
        
        return resized_image, resized_filename
        
    except Exception as e:
        print(f"Failed to process image: {e}")
        return None, None

@app.route('/resize_batch', methods=['POST'])
def resize_batch():
    urls_string = request.form.get('image_urls', '')
    urls = [url.strip() for url in urls_string.split('\n') if url.strip()]
    
    # Get uploaded files
    uploaded_files = request.files.getlist('files')
    uploaded_files = [f for f in uploaded_files if f.filename]
    
    # Check if we have any images
    total_images = len(urls) + len(uploaded_files)
    if total_images == 0:
        return 'No images provided.', 400

    new_width_str = request.form.get('new_width', '300')
    try:
        new_width = int(new_width_str)
    except ValueError:
        return 'Invalid width provided.', 400

    processed_images = []
    
    # Process URLs
    for i, url in enumerate(urls):
        resized_image, filename = process_image(url, new_width, "url_image", i)
        if resized_image and filename:
            processed_images.append((resized_image, filename))
    
    # Process uploaded files
    for i, file in enumerate(uploaded_files):
        resized_image, filename = process_image(file, new_width, "uploaded_image", i)
        if resized_image and filename:
            processed_images.append((resized_image, filename))
    
    if not processed_images:
        return 'No images could be processed.', 400
    
    # If only one image, return it directly
    if len(processed_images) == 1:
        resized_image, filename = processed_images[0]
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        try:
            resized_image.save(temp_file.name, format='JPEG', quality=95)
            return send_file(temp_file.name, as_attachment=True, download_name=filename, mimetype='image/jpeg')
        finally:
            # Clean up temp file after sending
            def remove_file(response):
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
                return response
            
    # Multiple images - create zip file
    temp_zip_file = os.path.join(app.config['RESIZED_FOLDER'], 'resized_images.zip')
    
    try:
        with zipfile.ZipFile(temp_zip_file, 'w') as zf:
            for resized_image, filename in processed_images:
                # Save the resized image to a buffer and add to the zip file
                img_buffer = BytesIO()
                resized_image.save(img_buffer, format='JPEG', quality=95)
                img_buffer.seek(0)
                zf.writestr(filename, img_buffer.getvalue())

        # Send the created zip file to the user
        return send_file(temp_zip_file, as_attachment=True, download_name='resized_images.zip')

    except Exception as e:
        return f"An error occurred during processing: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)