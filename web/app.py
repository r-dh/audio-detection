import os

from flask import Flask
from flask import render_template
from flask import request

from werkzeug.utils import secure_filename

from module.audio_classifier import ClassifyAudio
app = Flask(__name__)


audio_classifier = ClassifyAudio()

@app.route("/")
def index():
    return render_template('index.html')

# TODO: handle requests
@app.route('/upload_audio', methods=['GET', 'POST'])
def upload_audio():
    if request.method == 'POST' and len(request.files) == 1:

        file = request.files['the_file']
        # file.save(f"/uploads/{secure_filename(file.filename)}")
        filename = secure_filename(file.filename)
        file_path = "./temp/" + filename[:-3] + "wav" # hardcoded
        if not file_path.exists():
            filetype = filename[-3:]
            st.audio(uploaded_file.getvalue(), format=f'audio/{filetype}')
            sound = AudioSegment.from_file(io.BytesIO(file.read()), format=filetype)
            sound = sound.set_channels(1)
            sound.export(file_path, format="wav")
        analysis, pred_class = audio_classifier.analyse(str(file_path))
        return 'success' #{ "analysis": analysis, "pred_class": pred_class }
    return render_template('index.html')

# TODO: accept downloaded file

# TODO: split downloaded file

# TODO: analyse pieces of downloaded file


if __name__ == '__main__':
  app.run(debug=True)
  app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 10 # max 10MB audio files
  app.config['UPLOAD_EXTENSIONS'] = ['.wav', '.mp3']
