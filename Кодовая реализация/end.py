from math import *
from matplotlib import pyplot as plt
import numpy as np
from graphksp import Timetable


class Stage1():
    def __init__(self,Data_fly,speed_x,speed_y,coord_y,coord_x):
        self.Data_fly = Data_fly
        self.g = 9.8
        self.S = ((1.7**2 * pi)/4)*5
        self.m0 = 71_000
        self.c = 0.3
        self.flight_time = 93
        self.angle = (55 * pi / 180) / self.flight_time
        self.F = (130*1000 * 5) + (32*1000*8) + (32*1000*4) 
        self.F_min = (123*1000 * 5) + (28*1000*8) + (28*1000*4)
        self.F_increase = (self.F - self.F_min) / self.flight_time
        self.m_release = 340
        self.hundredth = 0.0001

        self.density0 = 1.225
        self.e = 2.7128
        self.Mmol = 0.029
        self.R = 8.31
        self.T_air = 290 

        self.speed_x = speed_x
        self.speed_y = speed_y 
        self.coord_x = 0
        self.coord_y = 600_000

        self.big_data = []


    def calculate_gravity(self,h):
        g0 = 9.8
        R = 600000  
        g = g0 * (R / (R + h))**2
        return 9.8

    
    def p_env(self,h):
        """Расчет плотности среды"""
        return self.density0 * e**((-self.Mmol * h * self.g) / (self.R * self.T_air))
    

    def F_Resistance(self, v1,v2, y,x):
        """Расчет силы споротивления"""
        return (self.c * self.S * self.p_env(sqrt(x**2+y**2)-600_000) * (sqrt(v1**2+v2**2) ** 2)) / 2
    
    def correct_gy(self,x,y):
        mod_g = sqrt(x**2 + y**2)
        sin_phi = y/mod_g
        return sin_phi
    
    def correct_gx(self,x,y):
        mod_g = sqrt((x)**2 + (y)**2)
        cos_phi = x/mod_g
        return cos_phi
    

    def f1_x(self,t, v1,v2, y,x):
        """Ускорение по оси x"""
        return (((self.F_min + self.F_increase * t) - self.F_Resistance(v1,v2, y,x))* sin(self.angle * t)) / (self.m0 - self.m_release * t)- self.calculate_gravity((sqrt(self.coord_x**2+self.coord_y**2)-600_000))*self.correct_gx(x,y)

    def f2_y(self,t,v1,v2,y,x):
        """Ускорение по оси y"""
        return (((self.F_min + self.F_increase * t) - self.F_Resistance(v1,v2,y,x))* cos(self.angle * t)) / (self.m0 - self.m_release * t) - self.calculate_gravity((sqrt(self.coord_x**2+self.coord_y**2)-600_000))*self.correct_gy(x,y)
    
    def ret(self):
        return self.big_data
    
    def simulating(self):
        """Расчет данных полета ракеты"""
        global speed_x
        global coord_x
        global coord_y
        global speed_y
        d = 0.0001


        for i in range(1,int(self.flight_time / self.hundredth)):
            self.time = i/10000

            self.a_x = self.f1_x(self.time,self.speed_x,self.speed_y,self.coord_y,self.coord_x)
            self.a_y = self.f2_y(self.time,self.speed_x,self.speed_y,self.coord_y,self.coord_x)

            delta_vx = self.a_x * 0.0001
            self.speed_x = self.Data_fly[-1][1][0] + delta_vx

            delta_vy = self.a_y * 0.0001
            self.speed_y = self.Data_fly[-1][1][1] + delta_vy

            delta_x  =   self.speed_x*0.0001 
            self.coord_x = self.Data_fly[-1][-1][0] + delta_x

            delta_y =  self.speed_y*0.0001 
            self.coord_y = self.Data_fly[-1][-1][-1] + delta_y

            self.Data_fly.append([[self.a_x, self.a_y], [self.speed_x, self.speed_y], [self.coord_x, self.coord_y]]) 
            self.big_data.append(sqrt(self.coord_x**2+self.coord_y**2)-600_000)
        
        print(sqrt(self.coord_x**2+self.coord_y**2)-600_000)
        print(sqrt(self.speed_x**2+self.speed_y**2))
        print(self.big_data[-1],'mas')
        return self.Data_fly
            

class Stage2():
    def __init__(self,Data_fly):
        """Аналогично первому классу"""
        self.speed_x = Data_fly[-1][-2][0]
        self.speed_y = Data_fly[-1][-2][1]
        self.coord_x = Data_fly[-1][-1][0]
        self.coord_y = Data_fly[-1][-1][1]
        print(self.speed_x,self.speed_y,self.coord_x,self.coord_y)
        self.Data_fly = Data_fly 
        self.flight_time = 64
        self.g = 9.8
        self.m_release = 75
        self.hundredth = 0.0001
        self.angle_past = (55* pi / 180)
        self.angle = (17 * pi / 180) / self.flight_time
        self.F = (130*1000) + (4*32*1000) 
        self.F_min = (123*1000) +(28*1000*4)
        self.F_increase = (self.F - self.F_min) / self.flight_time
        self.m0 = 27_600
        self.c = 0.3
        self.S = 2.9**2*pi/4
        self.density0 = 1.225
        self.e = 2.7128
        self.Mmol = 0.029
        self.R = 8.31
        self.T_air = 290 
        self.big_data = []


    def calculate_gravity(self,h):
        g0 = 9.81 
        R = 600000  
        g = g0 * (R / (R + h))**2
        return g


    def p_env(self,h):
        return self.density0 * e**((-self.Mmol * h * self.g) / (self.R * self.T_air))

    def F_Resistance(self, v1,v2, y,x):
        return (self.c * self.S * self.p_env(sqrt(x**2+y**2)-600_000) * (sqrt(v1**2+v2**2) ** 2)) / 2
       
    def correct_gy(self,x,y):
        mod_g = sqrt(x**2 + y**2)
        sin_phi = y/mod_g
        return sin_phi
    
    def correct_gx(self,x,y):
        mod_g = sqrt((x)**2 + (y)**2)
        cos_phi = x/mod_g
        return cos_phi

    def ret(self):
        return self.big_data

    def f1_x(self,t, v1,v2, y,x):
        return (self.F_min+self.F_increase * t-self.F_Resistance(v1,v2,y,x))* sin(self.angle*t + self.angle_past) / (self.m0 - self.m_release * t)-  self.calculate_gravity((sqrt(self.coord_x**2+self.coord_y**2)-600_000))*self.correct_gx(x,y)
    
    def f2_y(self,t,v1,v2,y,x):
        return (self.F_min +self.F_increase * t-self.F_Resistance(v1,v2,y,x))*cos(self.angle_past + self.angle*t) / (self.m0 - self.m_release * t) -  self.calculate_gravity((sqrt(self.coord_x**2+self.coord_y**2)-600_000))*self.correct_gy(x,y)
    
    def simulating(self):
        d = 0.0001
        for i in range(1,int(self.flight_time / self.hundredth)):
            self.time = i/10000
            self.a_x = self.f1_x(self.time,self.speed_x,self.speed_y,self.coord_y,self.coord_x)
            self.a_y = self.f2_y(self.time,self.speed_x,self.speed_y,self.coord_y,self.coord_x)

            delta_vx = self.a_x * 0.0001
            self.speed_x = self.Data_fly[-1][1][0] + delta_vx

            delta_vy = self.a_y * 0.0001
            self.speed_y = self.Data_fly[-1][1][1] + delta_vy

            delta_x  =   self.speed_x*0.0001 + (self.a_x*(d**2))/2
            self.coord_x = self.Data_fly[-1][-1][0] + delta_x
            
            delta_y =  self.speed_y*0.0001 + (self.a_y*(d**2))/2
            self.coord_y = self.Data_fly[-1][-1][-1] + delta_y
            self.Data_fly.append([[self.a_x, self.a_y], [self.speed_x, self.speed_y], [self.coord_x, self.coord_y]]) 
            self.big_data.append(sqrt(self.coord_x**2+self.coord_y**2)-600_000)
        print(sqrt(self.coord_x**2+self.coord_y**2)-600_000)
        print(sqrt(self.speed_x**2+self.speed_y**2))
        print(self.big_data[-1],'mas')
        return self.Data_fly


class Stage3():
    def __init__(self,Data_fly):
        """Аналогично первому классу"""
        self.Data_fly = Data_fly
        self.speed_x = Data_fly[-1][-2][0]
        self.speed_y = Data_fly[-1][-2][1]
        self.coord_x = Data_fly[-1][-1][0]
        self.coord_y = Data_fly[-1][-1][1]
        self.flight_time = 39
        self.g = 9.8
        self.m_release = 153
        self.hundredth = 0.0001
        self.angle_past = (72 * pi / 180)
        self.angle = (5 * pi / 180) / self.flight_time
        self.F = (260*1000) + (4*32*1000)
        self.m0 = 17_600
        self.c = 0.3
        self.S = 2.9**2*pi/4
        self.density0 = 1.225
        self.e = 2.7128
        self.Mmol = 0.029
        self.R = 8.31
        self.T_air = 290 
        self.big_data = []

    def p_env(self,h):
        return self.density0 * e**((-self.Mmol * h * self.g) / (self.R * self.T_air))

    def F_Resistance(self, v1,v2, y,x):
        return (self.c * self.S * self.p_env(sqrt(x**2+y**2)-600_000) * (sqrt(v1**2+v2**2) ** 2)) / 2

    def calculate_gravity(self,h):
        g0 = 9.81 
        R = 600000  
        g = g0 * (R / (R + h))**2
        return g
           
    def correct_gy(self,x,y):
        mod_g = sqrt(x**2 + y**2)
        sin_phi = y/mod_g
        return sin_phi
        
    
    def correct_gx(self,x,y):
        mod_g = sqrt(x**2 + y**2)
        cos_phi = x/mod_g
        return cos_phi

    def f1_x(self,t, v1,v2, y,x):
        return ((self.F-self.F_Resistance(v1,v2,y,x))* sin(self.angle_past+self.angle*t)) / (self.m0 - self.m_release * t) - self.calculate_gravity((sqrt(self.coord_x**2+self.coord_y**2)-600_000))*self.correct_gx(x,y)
    
    def f2_y(self,t,v1,v2,y,x):
        return (self.F-self.F_Resistance(v1,v2,y,x))*cos(self.angle_past+self.angle*t) / (self.m0 - self.m_release * t) - self.calculate_gravity((sqrt(self.coord_x**2+self.coord_y**2)-600_000))*self.correct_gy(x,y)
    
    def ret(self):
        return self.big_data
    def simulating(self):
        d = 0.0001
        for i in range(1,int(self.flight_time / self.hundredth)):
            self.time = i/10000
            self.a_x = self.f1_x(self.time,self.speed_x,self.speed_y,self.coord_y,self.coord_x)
            self.a_y = self.f2_y(self.time,self.speed_x,self.speed_y,self.coord_y,self.coord_x)

            delta_vx = self.a_x * 0.0001
            self.speed_x = self.Data_fly[-1][1][0] + delta_vx

            delta_vy = self.a_y * 0.0001
            self.speed_y = self.Data_fly[-1][1][1] + delta_vy

            delta_x  =   self.speed_x*0.0001 + (self.a_x*(d**2))/2
            self.coord_x = self.Data_fly[-1][-1][0] + delta_x

            delta_y =  self.speed_y*0.0001 + (self.a_y*(d**2))/2
            self.coord_y = self.Data_fly[-1][-1][-1] + delta_y

            self.Data_fly.append([[self.a_x, self.a_y], [self.speed_x, self.speed_y], [self.coord_x, self.coord_y]]) 
            self.big_data.append(sqrt(self.coord_x**2+self.coord_y**2)-600_000)
        print(sqrt(self.coord_x**2+self.coord_y**2)-600_000)
        print(sqrt(self.speed_x**2+self.speed_y**2))
        print(self.big_data[-1],'mas')
        return self.Data_fly
    
if __name__ == '__main__':
    """Запуск мат модели"""
       
    P1 = Stage1([[[0, 0], [0, 0], [0, 600_000]]],0,0,0,0)
    Data_fly = P1.simulating()
    check1= sqrt(Data_fly[-1][1][0]**2+Data_fly[-1][1][1]**2)
    check2 = len(Data_fly)/10000
    end = P1.ret()


    P2 = Stage2(Data_fly)
    Data_fly = P2.simulating()
    check3 = sqrt(Data_fly[-1][1][0]**2+Data_fly[-1][1][1]**2)
    check4 = len(Data_fly)/10000
    end += P2.ret()
   
    P3 = Stage3(Data_fly)
    Data_fly = P3.simulating()
    check5 = sqrt(Data_fly[-1][1][0]**2+Data_fly[-1][1][1]**2)
    check6 = len(Data_fly)/10000
    end += P3.ret()
  
    sp,y,x = [],[],[]
    for i in range(len(Data_fly)):
        sp.append(sqrt(Data_fly[i][1][0]**2 + Data_fly[i][1][1]**2))
        y.append(Data_fly[i][-1][-1]/1000)
        x.append(Data_fly[i][-1][0]/1000)

    f = open(r"KSP_fly.txt").readlines()
    f1 = []
    for i in range(len(f)):
        if f[i]=='\n':
            pass
        else:
            f1.append(float(f[i][0:-1]))
    plt.plot([i/4 for i in range(len(f1))],f1,label = 'KSP')
    plt.plot([i/10_000 for i in range(len(sp))],sp,label = 'Мат модель')
    plt.xlabel("Время (сек)")
    plt.ylabel("Скорость (м/с)") 
    plt.legend()
    plt.show()
    d = Timetable(x,y,0,0,0,0,0,0,0).trajectory()