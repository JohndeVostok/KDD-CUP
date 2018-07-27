import numpy
import pickle

from keras.models import Sequential, Model
from keras.layers.core import Dense, Activation
from keras.layers import LSTM, Input, Flatten, Merge,Bidirectional
from keras.layers.wrappers import TimeDistributed
from keras.optimizers import SGD, Adam, RMSprop
from keras.layers.normalization import BatchNormalization

from sklearn.preprocessing import MinMaxScaler

with open("../data/netdata.pkl", "rb") as f:
    tmp = pickle.load(f)

trainx = tmp[0]
trainy = tmp[1]
testx = tmp[2]
testy = tmp[3]

model = Sequential()
model.add(LSTM(64, return_sequences=True, input_shape=(48, 5)))
model.add(LSTM(32, return_sequences=True))
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dense(1))
#model.add(Activation('softmax'))

model.compile(loss="binary_crossentropy", optimizer='adam')
model.summary()

hist = model.fit(trainx, trainy, batch_size = 64, epochs = 8, verbose = 1, shuffle = True)

model.save("../data/model")
