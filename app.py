from flask import Flask, render_template, request
import os
from custom import perform_ocr  # Import OCR function from custom.py

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    dynamic_text = "This is dynamic text."
    
    if request.method == 'POST':
        uploaded_image = request.files['image']
        if uploaded_image:
            # Ensure that the uploads directory exists
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
                
            image_path = os.path.join('uploads', uploaded_image.filename)
            uploaded_image.save(image_path)
            
            # Perform OCR on the uploaded image
            processed_text = perform_ocr(image_path)
            
            dynamic_text = f"{processed_text}"

    return render_template('index.html', dynamic_text=dynamic_text)

if __name__ == '__main__':
    app.run(debug=True)
