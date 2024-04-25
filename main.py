from face_run import run_emotion_detection as face_runner
from voice_run import runner as voice_runner
from moviepy.editor import VideoFileClip, AudioClip
import os


def extract_audio(input_file, output_file):
	video = VideoFileClip(input_file)
	audio = video.audio
	audio.write_audiofile(output_file)

	print(f"Audio successfully extracted to {output_file}")


def run(path):
	face_dict = face_runner(path)
	face_value = max(face_dict, key=face_dict.get)
	audio_path = 'audios/' + (path.split('.')[0] + '.mp3').split('/')[1]
	extract_audio(path, audio_path)
	voice_value = voice_runner(audio_path)
	final_value = face_value if face_value == voice_value else 'Undetermined'
	return face_value, voice_value, final_value


if __name__ == '__main__':
	for file in os.listdir('videos'):
		print(file, run(f'videos/{file}'))
		# break

	# extract_audio('videos/recording2.mp4', 'audios/recording2.mp3')
