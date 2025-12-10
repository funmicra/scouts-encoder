from flask import Flask, render_template, request, redirect, url_for
from encoders import ENCODERS, DECODERS, encode, decode

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    input_text = ''
    result = None
    mode = 'encode'
    encoding = next(iter(ENCODERS.keys()))
    error_msg = None

    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        mode = request.form.get('mode', 'encode')
        encoding = request.form.get('encoding_type', encoding)

        try:
            if mode == 'encode':
                result = encode(encoding, input_text)
            else:
                result = decode(encoding, input_text)
        except Exception as e:
            error_msg = str(e)

    return render_template('index.html',
                           input_text=input_text,
                           result=result,
                           mode=mode,
                           encoding_type=encoding,
                           encodings=ENCODERS.keys(),
                           error_msg=error_msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)