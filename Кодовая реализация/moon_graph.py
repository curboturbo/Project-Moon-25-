import numpy as np
import matplotlib.pyplot as plt
class Timetable():

    def __init__(self,data_x,data_y):
        self.data_x = np.array(data_x)
        self.data_y = np.array(data_y)
        


    def trajectory(self):
        fig, ax = plt.subplots()
        ax.set_xlim(-240, 240)   # -240 240
        ax.set_ylim(-240, 240)
        ax.axhline(0, color='black', linewidth=0.5, ls='--')  
        ax.axvline(0, color='black', linewidth=0.5, ls='--')
        ax.set_xticks(range(-220, 220, 30))   #-220 220 100
        ax.set_yticks(range(-220, 220, 30))
        ax.grid()
        radius = 200                         #200
        theta = np.linspace(0, np.pi, 100)
        x_circle = radius * np.cos(theta)
        y_circle = radius * np.sin(theta)
        ax.plot(x_circle, y_circle, color='blue', linewidth=2, label='Муна')
        ax.plot(self.data_x, self.data_y, color='red', label='Траектория Луна-25')
        ax.legend()
        ax.set_aspect('equal', adjustable='box')
        plt.show()
    
    