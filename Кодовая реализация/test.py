import math
from moon_graph import Timetable

class Landing_Force_1():
    def __init__(self,time):
        """Инициализация данных"""
        self.alpha = (90 * math.pi / 180) 
        self.flight_time = time
        G = 6.67430e-11  
        self.cnt = 0
        M_moon = 9.7599066*10**20 
        R_moon = 200_000
        height = 5_000  
        r_orbit = R_moon + height
        self.F_1 = 0
        self.Luna_25 = 2654
        self.g = 1.63    
        self.hundredth = 0.0001
        """Отработка прошлого файла landing.py"""
        self.Data_fly  =[ [[-0.4750354600589308, 1.5614750081824915], [-1.4063341700017474e-05, -31.678416484659657], [59944.68997998155, 196762.352515318]]]
        self.speed_x = self.Data_fly[-1][1][0]
        self.speed_y = self.Data_fly[-1][1][1]
        self.coord_x = self.Data_fly[-1][-1][0]
        self.coord_y = self.Data_fly[-1][-1][1] 
        self.file = open("my_coords.txt",'w')
        self.big_data = []



    def fuel_consumption(self,t):
        return (self.Luna_25  - t*0.274)

    def correct_gy(self,x,y):
        mod_g = math.sqrt(x**2 + y**2)
        sin_phi = y/mod_g
        return sin_phi
    
    def correct_gx(self,x,y):
        mod_g = math.sqrt((x)**2 + (y)**2)
        cos_phi = x/mod_g
        return cos_phi

    def f2_y(self,vx,vy,x,y,t,alpha):
        """Проекция сил на y"""
        return (self.F_1*self.correct_gy(x,y)/self.fuel_consumption(t))    - self.correct_gy(x,y)*self.g
    
    
    def f1_x(self,vx,vy,x,y,t,alpha):
        """Проекция сил на X"""
        return (self.F_1*self.correct_gx(x,y)/self.fuel_consumption(t)) - self.correct_gx(x,y)*self.g
    
    def simulating(self):
        d = 0.0001
        check = 0
        """Математическое моделирование"""
        for i in range(1,int(self.flight_time / self.hundredth)):
            self.time = i/10000
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
            self.big_data.append(math.sqrt(self.coord_x**2+self.coord_y**2)-200_000)
         
            if math.sqrt(self.speed_y**2+self.speed_x**2) > 49 and self.cnt == 0:
                self.F_1 = 4650 + 1022
                self.cnt = 1
                

            if math.sqrt((self.coord_x**2+self.coord_y**2))-200_000 - 3050  < 0:
                print(math.sqrt((self.coord_x**2+self.coord_y**2)) - 200_000)
                for i in self.big_data:
                    self.file.write(f'{str(i)} ')
                self.file.close()
                return self.Data_fly
        return self.Data_fly
            
"""Отрисовка графиков и прочее"""
p = Landing_Force_1(300)
ms = p.simulating()
x,y,sp = [],[],[]
for i in range(len(ms)):
    x.append(ms[i][-1][0]/1000)
    y.append(ms[i][-1][1]/1000)
    sp.append(ms[i][1][1])
    cur = math.sqrt(ms[i][1][1]**2+ms[i][1][0]**2)
    sp.append(cur)
print(cur)
D = Timetable(data_x=x,data_y=y)
D.trajectory()
#time = [i/10000 for i in range(len(sp))]
#print(sp[-1])
#import matplotlib.pyplot as plt
#plt.plot(time,sp)
#plt.show()
#
###f = open(r"Moon_25_speed.txt").readlines()
###f1 = []
###for i in range(len(f)):
##    if f[i]=='\n':
##        pass
##    else:
##        f1.append(float(f[i][0:-1]))
##t = [i/4 for i in range(len(f1))]
##print(f1[0:100])
##plt.plot(t,f1)
##plt.show()
