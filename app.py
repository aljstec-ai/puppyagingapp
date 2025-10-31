from flask import Flask, request, send_file
from io import BytesIO
from PIL import Image
import model_stub

app = Flask(__name__)

@app.route('/api/age', methods=['POST'])
def age_image():
    if 'photo' not in request.files:
        return 'photo file missing', 400
    f = request.files['photo']
    target_years = int(request.form.get('target_years', 2))
    img = Image.open(f.stream).convert('RGB')
    try:
        aged = model_stub.apply_aging(img, target_years)
    except Exception as e:
        return str(e), 500
    buf = BytesIO()
    aged.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
