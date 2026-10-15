'''
DQN 模型
'''

from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D

def build_dqn(input_shape, actions):
    model = Sequential()
    model.add(Conv2D(32, (8, 8), strides=(4, 4), activation='relu', input_shape=input_shape))
    model.add(Conv2D(64, (4, 4), strides=(2, 2), activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dense(actions, activation='linear'))
    model.compile(optimizer='adam', loss='mse')
    return model