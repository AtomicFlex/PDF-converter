from flask import Flask, render_template, request, send_file
import os
import img2pdf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'files' not in request.files:
        return "No files uploaded", 400

    files = request.files.getlist('files')
    if not files:
        return "No files selected", 400

    image_paths = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_paths.append(filepath)

    if not image_paths:
        return " No valid images uploaded", 400

    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.pdf')
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(image_paths))

    for image_path in image_paths:
        os.remove(image_path)

    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)