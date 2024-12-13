import numpy as np
import matplotlib.pyplot as plt
class Timetable():
    """Класс для отрисовки графиков"""

    def __init__(self,data_x,data_y,speed,check1,check2,check3,check4,check5,check6):
        self.data_x = np.array(data_x)
        self.data_y = np.array(data_y)
        self.speed = speed
        self.check1 = check1
        self.check2 = check2
        self.check3 = check3
        self.check4 = check4
        self.check5 = check5
        self.check6 = check6

    def trajectory(self):
        fig, ax = plt.subplots()
        ax.set_xlim(-5000, 5000)
        ax.set_ylim(-5000, 5000)
        ax.axhline(0, color='black', linewidth=0.5, ls='--')  
        ax.axvline(0, color='black', linewidth=0.5, ls='--')
        ax.set_xticks(range(-5000, 5000, 500))
        ax.set_yticks(range(-5000, 5000, 500))
        ax.grid()

        radius = 600  # Радиус окружности
        theta = np.linspace(0, 2 * np.pi, 100)  # Параметризация окружности от 0 до 2π
        x_circle = radius * np.cos(theta)  # x-координаты окружности
        y_circle = radius * np.sin(theta)  # y-координаты окружности

        ax.plot(x_circle, y_circle, color='blue', linewidth=2, label='Земля')  # Рисуем окружность
        ax.plot(self.data_x, self.data_y, color='red', label='Траектория союз2.1б')  # Рисуем траекторию

        ax.legend()
        ax.set_aspect('equal', adjustable='box')  # Сохраняем равные масштабы осей
        plt.show()

    def speed_graph(self):
        time =[i/10000 for i in range(len(self.speed))]
        plt.grid(color='gray', linestyle='--', linewidth=0.8)
        plt.plot(time,self.speed)
        plt.title('Phase(1-3)')
        plt.scatter(self.check6, self.check5, color='red', s=100, label='Point (5, sin(5))')
        plt.scatter(self.check2, self.check1, color='red', s=100)
        plt.scatter(self.check4,self.check3,color='red',s=100)
        plt.xlabel('time', fontsize=16)
        plt.ylabel(r'Speed', fontsize=16)