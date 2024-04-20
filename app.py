from flask import Flask, render_template, request
import os

app = Flask(__name__)
recordings_dir = os.path.join(app.root_path, 'videos')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/record')
def record():
    directory = os.path.join(app.root_path, 'videos')
    return render_template('record.html')


@app.route('/save-video', methods=['POST'])
def save_video():
    if 'video' in request.files:
        video = request.files['video']
        if video:
            video_path = os.path.join(recordings_dir, 'recording.mp4')
            video.save(video_path)
            return 'Video saved successfully', 200
    return 'Error saving video', 400


if __name__ == '__main__':
    app.run(debug=True)
