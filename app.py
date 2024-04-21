from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
recordings_dir = os.path.join(app.root_path, 'videos')
q = 0


def make_data():
    data = []
    for file in os.listdir(recordings_dir):
        video = 'Positive'  # Placeholder
        audio = '75%'  # Placeholder
        final = 'Yes'  # Placeholder
        data.append({'file': file, 'video': video, 'audio': audio, 'final': final})
    return data


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/question/<int:question_no>')  # Route with parameter
def question(question_no):
    # Assuming you have a list of questions (modify as needed)
    questions = [
        {"question_no": 1, "question": "What is your opinion on video games?"},
        {"question_no": 2, "question": "What are your hobbies?"},
    ]
    # Validate question number within your question list range
    if question_no == len(questions) + 1:
        return render_template('fin.html')

    if question_no < 1 or question_no > len(questions):
        return "Invalid question number", 404  # Handle invalid question number

    selected_question = questions[question_no - 1]  # Access by index (0-based)
    global q
    q = question_no
    return render_template('question.html', question_no=selected_question["question_no"],
                           question=selected_question["question"])


@app.route('/record')
def record():
    return render_template('record.html')


@app.route('/save-video', methods=['POST'])
def save_video():
    if 'video' in request.files:
        video = request.files['video']
        if video:
            video_path = os.path.join(recordings_dir, f'recording{q}.mp4')
            video.save(video_path)
            return 'Video saved successfully', 200
    return 'Error saving video', 400


@app.route('/get_data')
def get_data():
    data = make_data()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
