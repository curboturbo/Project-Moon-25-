import math
from moon_graph import Timetable
import test

class Landing_Force():
    def __init__(self,Data,time):
        """Инициализация данных"""
        self.alpha = (90 * math.pi / 180) 
        self.Data_fly = Data
        self.flight_time = time
        G = 6.67430e-11  
        M_moon = 9.7599066*10**20 
        R_moon = 200_000
        height = 13769
        r_orbit = R_moon + height
        self.speed_x = 610
        self.speed_y = 12
        self.coord_x = 0  
        self.coord_y = 200_000 + 13900 
        self.F_1 = 60*1000 * 0.1235 + 1300     
        self.Luna_25 = 2889
        self.g = 1.63    
        self.hundredth = 0.0001
        self.Data_fly  =[[[0,0],[self.speed_x,self.speed_y],[self.coord_x,self.coord_y]]]
        self.Data_lost = []
        self.cnt = 0
        self.big_data = []

    def fuel_consumption(self,t):
        """Расход топлива"""
        return (self.Luna_25  - t*0.438)

    def correct_gy(self,x,y):
        """Проеция силы тяжести"""
        mod_g = math.sqrt(x**2 + y**2)
        sin_phi = y/mod_g
        return sin_phi
    
    def correct_gx(self,x,y):
        """Проеция силы тяжести"""
        mod_g = math.sqrt((x)**2 + (y)**2)
        cos_phi = x/mod_g
        return cos_phi
    
 
    def f2_y_zero(self,vx,vy,x,y,t,alpha):
        return (-self.F_1*math.sin(alpha))/self.fuel_consumption(t) - self.correct_gy(x,y)*self.g
    
    def f1_x_zero(self,vx,vy,x,y,t,alpha):
        return (-self.F_1*math.cos(alpha))/self.fuel_consumption(t) - self.correct_gx(x,y)*self.g

    def f2_y(self,vx,vy,x,y,t,alpha):
        """Расчет сил"""
        return (self.F_1*math.cos(alpha))/self.fuel_consumption(t) - self.correct_gy(x,y)*self.g
    
    def f1_x(self,vx,vy,x,y,t,alpha):
        """Расчет сил"""
        return (-self.F_1*math.sin(alpha))/self.fuel_consumption(t) - self.correct_gx(x,y)*self.g
    
    def pre_landing_start_condition(self,vx,vy):
        if vy <= 0: return True
        else: False

    def data(self):
        """возврат некоторых данных"""
        return self.big_data

    def simulating(self):
        """математичсекое моделирования"""
        d = 0.0001
        for i in range(1,int(self.flight_time / self.hundredth)):
            self.time = i/10000
            if self.pre_landing_start_condition(self.speed_x,self.speed_y):
                tang = (abs(self.speed_x) / abs(self.speed_y))
                self.alpha = math.atan(tang)  # Угол в радинах
                self.a_x = self.f1_x(self.speed_x,self.speed_y,self.coord_x,self.coord_y,self.time,self.alpha)
                self.a_y = self.f2_y(self.speed_x,self.speed_y,self.coord_x,self.coord_y,self.time,self.alpha)

                delta_vx = self.a_x * 0.0001
                self.speed_x = self.Data_fly[-1][1][0] + delta_vx

                delta_vy = self.a_y * 0.0001
                self.speed_y = self.Data_fly[-1][1][1] + delta_vy
                
                delta_x  =   self.Data_fly[-1][1][0]*0.0001 + (self.a_x*(d**2))/2
                self.coord_x = self.Data_fly[-1][-1][0] + delta_x
                delta_y =  self.Data_fly[-1][1][-1]*0.0001 + (self.a_y*(d**2))/2
                self.coord_y = self.Data_fly[-1][-1][-1] + delta_y
                self.Data_fly.append([[self.a_x, self.a_y], [self.speed_x, self.speed_y], [self.coord_x, self.coord_y]]) 
            else:
                tang_before_zero = (abs(self.speed_y)/(self.speed_x))
                self.alpha = math.atan(tang_before_zero)
                self.a_x = self.f1_x_zero(self.speed_x,self.speed_y,self.coord_x,self.coord_y,self.time,self.alpha)
                self.a_y = self.f2_y_zero(self.speed_x,self.speed_y,self.coord_x,self.coord_y,self.time,self.alpha)
                delta_vx = self.a_x * 0.0001
                self.speed_x = self.Data_fly[-1][1][0] + delta_vx
                delta_vy = self.a_y * 0.0001
                self.speed_y = self.Data_fly[-1][1][1] + delta_vy
                delta_x  =   self.Data_fly[-1][1][0]*0.0001 + (self.a_x*(d**2))/2
                self.coord_x = self.Data_fly[-1][-1][0] + delta_x
                delta_y =  self.Data_fly[-1][1][-1]*0.0001 + (self.a_y*(d**2))/2
                self.coord_y = self.Data_fly[-1][-1][-1] + delta_y
                self.Data_fly.append([[self.a_x, self.a_y], [self.speed_x, self.speed_y], [self.coord_x, self.coord_y]])
            self.big_data.append(math.sqrt(self.coord_x**2+self.coord_y**2)-200_000)

            if math.sqrt(self.coord_x**2 + self.coord_y**2)-200_000 <= 0:
                return self.Data_fly
        
        
            if self.Data_fly[-1][-2][0] <=0:
                #print(self.speed_x,self.speed_y)
                #print(self.Luna_25  - self.time*1.596)
                #print('THIS IS Y COORD')
                #print(math.sqrt(self.coord_x**2+self.coord_y**2)-200_000)
                #print("THIS PARAMETR")
                #print(f'mass = {self.Luna_25-self.time}')
                #print(self.Data_fly[-1])
                #print(f'{i/10_000} ОКОНЧАНИЕ ВРЕМЯ СПУСКА')
                return self.Data_fly
            
            
    
p = Landing_Force([[[0,0],[0,0],[0,0]]],300)
ms = p.simulating()
l = p.data()

f = open('temp.txt','w')
for i in l:
    f.write(f'{str(i)} ')


fuck = test.Landing_Force_1(200)
lst = fuck.simulating()
for i in lst:
    ms.append(i)
    
x,y,sp = [],[],[]
for i in range(len(ms)):
    x.append(ms[i][-1][0]/1000)
    y.append(ms[i][-1][1]/1000)
    sp.append(math.sqrt(ms[i][1][1]**2+ms[i][1][0]**2))

D = Timetable(data_x=x,data_y=y)
D.trajectory()
time = [i/10000 for i in range(len(sp))]

import matplotlib.pyplot as plt
f = open(r"end_data.txt").readlines()
f1 = []
for i in range(len(f)):
    if f[i]=='\n':
        pass
    else:
        f1.append(float(f[i][0:-1]))
t = [i/4 for i in range(len(f1))]
print(f1[0:100])
plt.plot(t,f1)
plt.plot(time,sp)

plt.legend()
plt.show()
