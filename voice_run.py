import librosa
import os
from sklearn.preprocessing import StandardScaler
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from keras.models import Sequential
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout
import numpy as np


def noise(data):
    noise_amp = 0.035*np.random.uniform()*np.amax(data)
    data = data + noise_amp*np.random.normal(size=data.shape[0])
    return data


def stretch(data, rate=0.8):
    return librosa.effects.time_stretch(data, rate=rate)


def shift(data):
    shift_range = int(np.random.uniform(low=-5, high = 5)*1000)
    return np.roll(data, shift_range)


def pitch(data, sampling_rate, pitch_factor=0.7):
    return librosa.effects.pitch_shift(data, sr=sampling_rate, n_steps=pitch_factor)


def extract_features(data,sample_rate):
	# ZCR
	result = np.array([])
	zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
	result = np.hstack((result, zcr))  # stacking horizontally

	# Chroma_stft
	stft = np.abs(librosa.stft(data))
	chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
	result = np.hstack((result, chroma_stft))  # stacking horizontally

	# MFCC
	mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate).T, axis=0)
	result = np.hstack((result, mfcc))  # stacking horizontally

	# Root Mean Square Value
	rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
	result = np.hstack((result, rms))  # stacking horizontally

	# MelSpectogram
	mel = np.mean(librosa.feature.melspectrogram(y=data, sr=sample_rate).T, axis=0)
	result = np.hstack((result, mel))  # stacking horizontally

	return result


def get_features(path):
	# duration and offset are used to take care of the no audio in start and the ending of each audio files as seen above.
	data, sample_rate = librosa.load(path, duration=2.5, offset=0.6)

	# without augmentation
	res1 = extract_features(data, sample_rate)
	result = np.array(res1)

	# data with noise
	noise_data = noise(data)
	res2 = extract_features(noise_data, sample_rate)
	result = np.vstack((result, res2))  # stacking vertically

	# data with stretching and pitching
	new_data = stretch(data)
	data_stretch_pitch = pitch(new_data, sample_rate)
	res3 = extract_features(data_stretch_pitch, sample_rate)
	result = np.vstack((result, res3))  # stacking vertically

	return result


def create_model():
	model = Sequential()
	model.add(Conv1D(256, kernel_size=5, strides=1, padding='same', activation='relu', input_shape=(162, 1)))
	model.add(MaxPooling1D(pool_size=5, strides=2, padding='same'))

	model.add(Conv1D(256, kernel_size=5, strides=1, padding='same', activation='relu'))
	model.add(MaxPooling1D(pool_size=5, strides=2, padding='same'))

	model.add(Conv1D(128, kernel_size=5, strides=1, padding='same', activation='relu'))
	model.add(MaxPooling1D(pool_size=5, strides=2, padding='same'))
	model.add(Dropout(0.2))

	model.add(Conv1D(64, kernel_size=5, strides=1, padding='same', activation='relu'))
	model.add(MaxPooling1D(pool_size=5, strides=2, padding='same'))

	model.add(Flatten())
	model.add(Dense(units=32, activation='relu'))
	model.add(Dropout(0.3))

	model.add(Dense(units=8, activation='softmax'))
	model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

	return model


def runner(filepath):
	fts = get_features(filepath)
	scaler = StandardScaler()
	fts = scaler.fit_transform(fts)
	fts = np.expand_dims(fts, axis=2)
	fts = fts[0]
	fts = np.expand_dims(fts, axis=0)
	model = create_model()
	model.load_weights('saved_weights.h5')
	prediction = model.predict(fts, verbose=0)
	emotion = prediction.argmax()
	dictt = [['angry'], ['calm'], ['disgust'], ['fear'], ['happy'], ['neutral'], ['sad'], ['surprise']]
	return dictt[emotion]


if __name__ == '__main__':
	output = runner("audios/happytest.mp3")
	print(output)
