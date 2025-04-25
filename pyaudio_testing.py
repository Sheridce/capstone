import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import time

CHUNK = 1024 *4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = CHUNK
)

plt.ion()

fig, ax = plt.subplots()

x = np.arange(0, 2 * CHUNK, 2)
line, = ax.plot(x, np.random.rand(CHUNK))
ax.set_ylim(-1500, 1500)
ax.set_xlim(0, CHUNK)

silence_start = None
wc = 0

while True:
    data = stream.read(CHUNK)
    data_int = np.array(struct.unpack( str( CHUNK ) + 'h', data ))

    line.set_ydata(data_int)
    fig.canvas.draw()
    fig.canvas.flush_events()

    rms = np.sqrt(np.mean(data_int**2))