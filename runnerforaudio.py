import librosa
from tensorflow.keras.models import load_model
import numpy as np
# import numpy as np

def runner(filepath):
   y,sr=librosa.load(filepath)
   zcr=librosa.feature.zero_crossing_rate(y)
   average_zcr=np.mean(zcr)
   mfc=librosa.feature.mfcc(y=y, sr=sr)
   avg_mfc=np.mean(mfc)
   speccentroid=librosa.feature.spectral_centroid(y=y, sr=sr)
   avg_speccentroid=np.mean(speccentroid)
   specrolloff=librosa.feature.spectral_rolloff(y=y, sr=sr)
   avg_specrolloff=np.mean(specrolloff)
   tempo=librosa.feature.tempo(y=y,sr=sr)[0]
   beats=librosa.onset.onset_detect(y=y, sr=sr).sum()
   model1= load_model('Backup.h5')
   all_features = np.array([average_zcr, avg_mfc, avg_speccentroid, avg_specrolloff, tempo, beats])
   all_features = np.expand_dims(all_features, axis=0)
   prediction= model1.predict(all_features)
   emotion=prediction.argmax()
   return emotion

output=runner("C:/Users/Siddhi/Downloads/runner/1001_DFA_DIS_XX.wav")
print(output)