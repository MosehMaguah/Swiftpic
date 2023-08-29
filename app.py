from flask import Flask, render_template, request, send_file
from PIL import Image
import io

app = Flask(__name__)

# Function to compress the uploaded image
def compress_image(image, quality=90):
    img = Image.open(image)

    # Compress the image by reducing the quality
    img = img.convert("RGB")
    img.save(image, format='JPEG', quality=quality)

    return img

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return render_template('index.html', message='No selected file')

        try:
            # Get the quality value from the form data
            quality = int(request.form['quality'])

            # Validate the quality value (0-100 range)
            if quality < 0 or quality > 100:
                return render_template('index.html', message='Quality must be between 0 and 100')

            # Compress the uploaded image using the specified quality
            img = compress_image(file, quality=quality)

            # Create an in-memory file to send as a response
            output = io.BytesIO()
            img.save(output, format='JPEG')
            output.seek(0)

            # Send the compressed image as a response
            return send_file(output, mimetype='image/jpeg', as_attachment=True, download_name='compressed_image.jpg')

        except Exception as e:
            return render_template('index.html', message=f'Error: {str(e)}')

    return render_template('index.html', message=None)

if __name__ == '__main__':
    app.run(debug=True)