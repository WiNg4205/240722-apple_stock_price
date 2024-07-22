import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

data = pd.read_csv('AAPL.csv')
data['Date'] = pd.to_datetime(data['Date'])
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

ax.set_xlabel('Date')
ax.set_ylabel('Share Price ($USD)')
ax.set_title('Apple stock price over time')

fig.autofmt_xdate()


def round_to_sigfigs(x, sigfigs):
    """Round a number to a specified number of significant figures."""
    if x == 0:
        return 0
    return round(x, sigfigs - int(np.floor(np.log10(abs(x)))) - 1)


def init():
    line, = ax.plot([], [], lw=2)
    ax.set_xlim(data['Date'].min(), data['Date'].max())
    ax.set_ylim(0, data['Adj Close'].min())
    yticks = np.linspace(0, data['Adj Close'].min(), num=10)
    yticks = np.array([round_to_sigfigs(tick, 2) for tick in yticks])
    ax.set_yticks(yticks)
    line.set_data([], [])
    return line,

def update(frame):
    x = data['Date'][:frame]
    y = data['Adj Close'][:frame]
    current_ylim = ax.get_ylim()
    new_max = max(current_ylim[1], data['Adj Close'][frame])
    ax.set_ylim(0, new_max)
    yticks = np.linspace(0, 2*data['Adj Close'].min(), num=10)
    yticks = np.array([round_to_sigfigs(tick, 2) for tick in yticks])
    ax.set_yticks(yticks)
    line.set_data(x, y)
    return line,
    
ani = animation.FuncAnimation(fig, update, frames=len(data), init_func=init, blit=True, interval=0.001)
plt.show()
