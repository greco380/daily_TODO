from __future__ import annotations

from flask import Flask, render_template_string, request, jsonify

from . import config
from .voice_intake import transcribe_audio, extract_tasks

app = Flask(__name__)

INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>Voice Task Capture</title>
</head>
<body>
<h1>Record Your Tasks</h1>
<button id='record'>Record</button>
<button id='stop' disabled>Stop</button>
<ul id='tasks'></ul>
<script>
let recorder;
let chunks = [];

const recordBtn = document.getElementById('record');
const stopBtn = document.getElementById('stop');

recordBtn.onclick = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({audio: true});
    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = e => chunks.push(e.data);
    recorder.onstop = async () => {
        const blob = new Blob(chunks, {type: 'audio/webm'});
        chunks = [];
        const form = new FormData();
        form.append('audio', blob, 'recording.webm');
        const res = await fetch('/submit', {method: 'POST', body: form});
        const data = await res.json();
        const ul = document.getElementById('tasks');
        ul.innerHTML = '';
        data.tasks.forEach(t => {
            const li = document.createElement('li');
            li.textContent = t;
            ul.appendChild(li);
        });
    };
    recorder.start();
    recordBtn.disabled = true;
    stopBtn.disabled = false;
};

stopBtn.onclick = () => {
    recorder.stop();
    recordBtn.disabled = false;
    stopBtn.disabled = true;
};
</script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(INDEX_HTML)


@app.route('/submit', methods=['POST'])
def submit():
    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({'error': 'no audio'}), 400

    audio_bytes = audio_file.read()
    cfg = config.load_config()
    transcript = transcribe_audio(audio_bytes, cfg.openai_api_key or '')
    tasks = extract_tasks(transcript, cfg.openai_api_key or '') if transcript else []
    return jsonify({'transcript': transcript, 'tasks': tasks})


if __name__ == '__main__':
    app.run(debug=True)
