import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time

data_list = []
theta = np.array(np.arange(0, 1.5 * np.pi, 1.5 * np.pi / 1081))

def read():
    f = open('./positions/shadow/2019-11-24-16-27-46-lsr1.csv', 'r')
    f.readline()
    while True:
        temp = f.readline()
        if not temp:
            break
        data = []
        info = temp.split(',')[2:]
        for i in range(len(info) - 1):
            data.append(float(info[i]))
        data_list.append(data)


def animate():
    def update(frame):
        print(frame)
        dots.set_data(theta, data_list[frame])
        return dots,

    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    ax.set_ylim(0, 20)
    dots, = ax.plot([], [], 'o', c='b', markersize=1.2)

    ani = FuncAnimation(fig=fig, func=update, frames=[i for i in range(2769)], blit=True,
                        interval=1, repeat=True)

    plt.show()


if __name__ == '__main__':
    print(time.perf_counter())
    read()
    print(time.perf_counter())
    animate()
