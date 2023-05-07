import os
import fnmatch
from matplotlib import pyplot as plt
from os import path
import numpy as np
from matplotlib.animation import FuncAnimation

def find_files(pattern, directory):
    matches = []
    for filename in fnmatch.filter(os.listdir(directory), pattern):
        matches.append(os.path.join(directory, filename))
    return matches
def read_data_from_etafiles(eta_files_no , root_dir):
    lines_no = sum(1 for line in open(path.join(root_dir, "eta0")))
    x= np.empty(lines_no)
    y = np.empty((eta_files_no,lines_no))
    for i in range(0,eta_files_no):
        file_path = path.join(root_dir, "eta" + str(i))
        with open(file_path, 'r') as file:
            line = file.readline()
            j = 0
            while line:
                float_strings = line.split()
                x[j] = float_strings[0]
                y[i,j] = float_strings[1]
                line  = file.readline()
                j += 1
    return x,y

def get_coord(root_dir):
    eta_n = len(find_files('eta*', root_dir))
    return read_data_from_etafiles(eta_n, root_dir)

root_dir1 = '/home/anna/annaCode/UiO/waves/Obligatorisk2/ex1/LBoussinesq/delta_x_0.5'
root_dir2 = '/home/anna/annaCode/UiO/waves/Obligatorisk2/ex1/LBoussinesq/delta_x_1'
root_dir3 = '/home/anna/annaCode/UiO/waves/Obligatorisk2/ex1/LBoussinesq/delta_x_2'
eta_n = len(find_files('eta*', root_dir3))
x1,y1 = get_coord(root_dir1)
x2,y2 = get_coord(root_dir2)
x3,y3 = get_coord(root_dir3)


fig, ax = plt.subplots()
fig.set_figheight(8)
fig.set_figwidth(24)
y_max = max(y1.max(), y2.max(), y3.max())
y_min = min(y1.min(), y2.min(), y3.min())
y_tank_wall = np.arange(0, y_max + 0.1, 0.01)
x_0 = np.empty(len(y_tank_wall))
x_100 = np.empty(len(y_tank_wall))
x_0.fill(0)
x_100.fill(100)

def update(frame):
    ax.clear()
    ax.set_ylim([y_min, y_max])
    ax.plot(x_0, y_tank_wall, color = 'darkblue')
    ax.plot(x_100, y_tank_wall, color = 'darkblue')

    y_1 = y1[frame]
    ax.plot(x1, y_1, color = 'red', label= "Δx = 0.5")
    ax.fill_between(x1, y_min, y_1, where = y_1 > y_min, facecolor ='red', alpha = 0.2)
    y_2 = y2[frame]
    ax.plot(x2, y_2, color = 'green', label= "Δx = 1")
    ax.fill_between(x2, y_min, y_2, where = y_2 > y_min, facecolor ='green', alpha = 0.2)
    y_3 = y3[frame]
    ax.plot(x3, y_3, color = 'blue', label= "Δx = 2")
    ax.fill_between(x3, y_min, y_3, where = y_3 > y_min, facecolor ='blue', alpha = 0.2)
    ax.legend(loc = 'upper right')
anim= FuncAnimation(fig, update, frames=eta_n, interval=200)
anim.save("/home/anna/LBoussinesq.mp4")