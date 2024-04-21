from face_run import run_emotion_detection
import os


def run(path):
	return run_emotion_detection(path), {'angry': 0.9609064598416173, 'sad': 0.32430961693442145}, 'Happy'
	# return path, {'angry': 0.9609064598416173, 'sad': 0.32430961693442145}, 'Happy'

if __name__ == '__main__':
	for file in os.listdir('videos'):
		print(run(f'videos/{file}'))
		break
