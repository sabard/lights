import matplotlib.pyplot as plt

channels = [1]
window = 200
samplerate = 48000
downsample = 10

length = int(window * samplerate / (1000 * downsample))
plotdata = np.zeros((length, len(channels)))

# fig, ax = plt.subplots()
# lines = ax.plot(plotdata)
# if len(channels) > 1:
#     ax.legend([f'channel {c}' for c in channels],
#               loc='lower left', ncol=len(channels))
# ax.axis((0, len(plotdata), -1, 1))
# ax.set_yticks([0])
# ax.yaxis.grid(True)
# ax.tick_params(bottom=False, top=False, labelbottom=False,
#                right=False, left=False, labelleft=False)
# fig.tight_layout(pad=0)


plt.ion()
plt.show()


plt.plot(plotdata)
plt.draw()
plt.pause(0.001)
