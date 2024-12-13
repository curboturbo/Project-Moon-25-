import math
import time
import krpc

# Соединяемся с KSP и задаём основные переменные для космического центра, ракеты и полёта
conn = krpc.connect(name='Flight Mission')
space_center = conn.space_center
vessel = space_center.active_vessel
flight = vessel.flight()

# Готовим переменные потоков данных (Чтобы дальше мгновенно доставать текущее значение из потока)
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
periapsis = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
srb_tank = vessel.parts.with_title('Топливный бак FL-C1000')[0].resources
srb_fuel = conn.add_stream(srb_tank.amount, 'LiquidFuel')
second_tank = vessel.parts.with_title('Топливный бак FL-TX1800')[0].resources
second_fuel = conn.add_stream(second_tank.amount, 'LiquidFuel')
third_tank = vessel.parts.with_title('Топливный бак FL-TX440')[0].resources
third_fuel = conn.add_stream(third_tank.amount, 'LiquidFuel')
sx = vessel.orbit.body.position(vessel.surface_reference_frame)[0]
sy = vessel.orbit.body.position(vessel.surface_reference_frame)[1]
sz = vessel.orbit.body.position(vessel.surface_reference_frame)[2]
# Откроем для записи текстовый файл, в который будем сгружать информацию о завершении важных шагов полёта
f = open("StepTiming.txt", "a")

# Подготовка к запуску
space_center.warp_to(60474.315)
target_altitude = 200000
vessel.control.sas = False
vessel.control.rcs = False
vessel.control.throttle = 1.0
# Обратный отсчёт...
f.write(f"ЗАПУСК: {ut()}\n")
print('3...')
time.sleep(1)
print('2...')
time.sleep(1)
print('1...')
time.sleep(1)
print('Запуск!')
TimeStart = float(ut())
TimeSecondStage = 0.0
TimeThirdStage = 0.0
# Первые четыре шага (Активация первой ступени)
vessel.control.activate_next_stage()
vessel.control.activate_next_stage()
vessel.control.activate_next_stage()
vessel.control.activate_next_stage()
vessel.auto_pilot.engage()
vessel.auto_pilot.target_pitch_and_heading(90, 90)

# Подготовка переменных для основного цикла взлёта
srbs_separated = False
first_separated = False
second_separated = False
third_separated = False
turn_angle = 0
ang1 = 59.0 / 93.4
ang2 = 17.0 / 64.54
ang3 = 5.0 / 39.0
prevTime = float(ut())
newTime = float(ut())
f.write(f"Масса ракеты на старте: {vessel.mass}\n")
# Основной цикл взлёта
while True:
    newTime = float(ut())
    if not srbs_separated:  # Совершаемые проверки и действия до отстыковки четырёх боковых блоков первой ступени
        if (newTime - prevTime) >= 1.0:
            # Каждую секунду увеличиваем угол взлёта
            prevTime = newTime
            turn_angle += ang1
            vessel.auto_pilot.target_pitch_and_heading(90 - turn_angle, 90)
        if float(srb_fuel()) < 0.1:
            # Когда топливо кончается, отстыковываемся
            srbs_separated = True
            vessel.control.activate_next_stage()
            print('Первая ступень полностью отсоединена')
            f.write(f"Высота отстыковки 1 ступени: {float(altitude())}\n")
            f.write(f"Масса ракеты после 1 отстыковки: {vessel.mass}\n")
            TimeSecondStage = float(ut())
    elif not second_separated:   # Совершаемые проверки и действия до отстыковки второй ступени
        if (newTime - prevTime) >= 1.0:
            # Каждую секунду увеличиваем угол взлёта
            prevTime = newTime
            turn_angle += ang2
            vessel.auto_pilot.target_pitch_and_heading(90 - turn_angle, 90)
        if float(second_fuel()) < 0.1:
            # Когда топливо кончается, отстыковываемся
            second_separated = True
            vessel.control.activate_next_stage()
            print('Вторая ступень полностью отсоединена')
            f.write(f"Высота отстыковки 2 ступени: {float(altitude())}\n")
            f.write(f"Масса ракеты после 2 отстыковки: {vessel.mass}\n")
            TimeThirdStage = float(ut())
    elif not third_separated:   # Совершаемые проверки и действия до снятия третьей ступени и обнажения Луны-25
        if (newTime - prevTime) >= 1.0:
            # Каждую секунду увеличиваем угол взлёта
            prevTime = newTime
            turn_angle += ang3
            vessel.auto_pilot.target_pitch_and_heading(90 - turn_angle, 90)
        if float(third_fuel()) < 0.1:
            # Когда топливо кончается, отстыковываемся
            third_separated = True
            print('Третья ступень отработала')
            f.write(f"Высота ОСТАНОВКИ ДВИЖКА 3 ступени: {float(altitude())}\n")
            f.write(f"Масса ракеты когда кончилось топливо 3 ступени: {space_center.active_vessel.mass}\n")
            TimeFregatOnly = float(ut())

    if third_separated:
        print('Приближаемся к целевому апоцентру')
        # Выходим из цикла взлёта
        break

vessel.control.throttle = 0.0
while apoapsis() < target_altitude:
    pass
print('Целевой апоцентр достигнут')
print('Ожидание выхода из атмосферы')
while float(altitude()) < 70500:
    # Ждём выхода из атмосферы, выводим в консоль текущую высоту для проверки
    print(float(altitude()))
    pass
# Далее полное избавление от Союза-2.1б
vessel.control.activate_next_stage()
f.write(f"Высота отстыковки 3 ступени: {vessel.flight().mean_altitude}\n")
f.write(f"Масса ракеты без 3 ступени (Фрегат + Луна-25): {space_center.active_vessel.mass}\n")
time.sleep(1)
# Игра теперь считает Луну-25 с разгонным блоком "Фрегат" отдельным космическим аппаратом,
# потому перенастраиваем переменные и потоки
vessel = space_center.active_vessel
flight = vessel.flight()
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
vessel.control.activate_next_stage()
vessel.auto_pilot.engage()
# Планирование коррекции орбиты (Через vis-viva equation, уравнение живой силы)
print('Планирование коррекции орбиты')
mu = vessel.orbit.body.gravitational_parameter
r = vessel.orbit.apoapsis
a1 = vessel.orbit.semi_major_axis
a2 = r
v1 = math.sqrt(mu*((2./r)-(1./a1)))
v2 = math.sqrt(mu*((2./r)-(1./a2)))
delta_v = v2 - v1
node = vessel.control.add_node(ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

# Рассчитываем время коррекции
F = vessel.available_thrust
Isp = vessel.specific_impulse * 9.82
m0 = vessel.mass
m1 = m0 / math.exp(delta_v/Isp)
flow_rate = F / Isp
burn_time = (m0 - m1) / flow_rate

# Ориентируем направление аппарата
print('Ориентация корабля для кругового сжигания')
vessel = conn.space_center.active_vessel
vessel.auto_pilot.reference_frame = node.reference_frame
vessel.auto_pilot.target_direction = (0, 1, 0)
vessel.auto_pilot.wait()

# Ожидаем манёвра по коррекции орбиты
print('Ожидание манёвра')
burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
lead_time = 5
space_center.warp_to(burn_ut - lead_time)

# Проведение манёвра
print('Готовность провести манёвр')
time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
while time_to_apoapsis() - (burn_time/2.) > 0:
    pass
print('Проводим манёвр')
vessel.control.throttle = 1.0
time.sleep(burn_time - 0.1)
print('Корректировка')
vessel.control.throttle = 0.05
remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)
vessel.control.throttle = 0.0
node.remove()
print('Вывод на орбиту закончен')

# Запись полезных данных по окончанию взлёта после корректировки орбиты
f.write(f"1 ступень: {round(TimeSecondStage - TimeStart, 3)}\n")
f.write(f"2 ступень: {round(TimeThirdStage - TimeStart, 3)}\n")
f.write(f"3 ступень: {round(TimeFregatOnly - TimeStart, 3)}\n")
f.write(f"Остался только фрегат с Луной-25\n")
vessel.control.antennas = True  # Развёртка антенн

# Расчёты для Гомановского перехода
destSemiMajor = space_center.bodies["Mun"].orbit.semi_major_axis
hohmannSemiMajor = destSemiMajor / 2
neededPhase = 2 * math.pi * (1 / (2 * (destSemiMajor ** 3 / hohmannSemiMajor ** 3) ** (1 / 2)))
optimalPhaseAngle = 180 - neededPhase * 180 / math.pi  # В градусах; Луна должна быть впереди аппарата

# Берём угол для перехода
phaseAngle = 1080
vessel.auto_pilot.engage()
vessel.auto_pilot.reference_frame = vessel.orbital_reference_frame
vessel.auto_pilot.target_direction = (0.0, 1.0, 0.0)  # Point pro-grade

angleDec = False  # Поскольку Луна должна быть впереди аппарата, следим за тем, чтобы угол не уменьшался
prevPhase = 0
while abs(phaseAngle - optimalPhaseAngle) > 1 or not angleDec:
    # С расчётами для Гомановского перехода ожидаем подходящего положения, чтобы начать переход
    bodyRadius = space_center.bodies["Mun"].orbit.radius
    vesselRadius = vessel.orbit.radius
    time.sleep(1)
    bodyPos = space_center.bodies["Mun"].orbit.position_at(space_center.ut, space_center.bodies["Mun"].reference_frame)
    vesselPos = vessel.orbit.position_at(space_center.ut, space_center.bodies["Mun"].reference_frame)
    bodyVesselDistance = ((bodyPos[0] - vesselPos[0]) ** 2 + (bodyPos[1] - vesselPos[1]) ** 2 + (
                bodyPos[2] - vesselPos[2]) ** 2) ** (1 / 2)
    try:
        phaseAngle = math.acos(
            (bodyRadius ** 2 + vesselRadius ** 2 - bodyVesselDistance ** 2) / (2 * bodyRadius * vesselRadius))
    except:
        print("Математическая ошибка в расчётах, пробуем дальше")
        continue  # Ошибка расчёта
    phaseAngle = phaseAngle * 180 / math.pi
    if prevPhase - phaseAngle > 0:
        angleDec = True
        if abs(phaseAngle - optimalPhaseAngle) > 20:
            space_center.rails_warp_factor = 2
        else:
            space_center.rails_warp_factor = 0
    else:
        angleDec = False
        space_center.rails_warp_factor = 4
    prevPhase = phaseAngle
    print("Угол:", phaseAngle)

# Используем vis-viva equation (уравнение живой силы) для расчёта дельты V для перехода с орбиты на орбиту
GM = vessel.orbit.body.gravitational_parameter  # Берём гравитационный параметр для Земли
r = vessel.orbit.radius
a = vessel.orbit.semi_major_axis
initialV = (GM * ((2/r) - (1/a)))**(1/2)
a = (space_center.bodies["Mun"].orbit.radius + vessel.orbit.radius) / 2
finalV = (GM * ((2/r) - (1/a)))**(1/2)
deltaV = 0.9215 * (finalV - initialV)
print("Проводим манёвр с дельтой V:", deltaV)
actualDeltaV = 0
vessel.control.throttle = 1.0
while (deltaV > actualDeltaV and apoapsis() > 100000 and periapsis() > 100000):  # Проводим манёвр
    time.sleep(0.15)
    r = vessel.orbit.radius
    a = vessel.orbit.semi_major_axis
    actualDeltaV = (GM * ((2/r) - (1/a)))**(1/2) - initialV
    print("Дельта V сейчас: ", actualDeltaV, " из необходимой ", deltaV)
vessel.control.throttle = 0
time.sleep(1)
# Когда мы разогнали Луну-25 на нужную Гомановскую траекторию для встречи с Луной,
# можно отбросить разгонный блок "Фрегат"
f.write(f"Отстыкован фрегат: {round(ut() - TimeStart, 3)}\n")
vessel.control.activate_next_stage()
time.sleep(2)
vessel.control.throttle = 0
vessel.auto_pilot.disengage()

print("Ожидаем встречи с Луной")
vessel = space_center.active_vessel
flight = vessel.flight()
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
periapsis = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
vessel.control.activate_next_stage()
time_to_warp = vessel.orbit.next_orbit.time_to_periapsis + vessel.orbit.time_to_soi_change
space_center.warp_to(space_center.ut + time_to_warp - 300)  # Ждём времени за 5 минут до встречи с Луной
vessel.control.antennas = True
vessel.auto_pilot.engage()
vessel.auto_pilot.reference_frame = vessel.surface_velocity_reference_frame
vessel.auto_pilot.target_direction = (0.0, -1.0, 0.0)  # Поворот для орбитирования Луны

vessel.auto_pilot.wait()  # Ждём поворота
time_to_warp = vessel.orbit.time_to_periapsis
space_center.warp_to(space_center.ut + time_to_warp - 30)  # Ждём времени за 30 секунд до перигея орбиты

vessel.auto_pilot.wait()
print("Включаем двигатель...")
# Нам понадобится поток для поверхностной скорости
flight = vessel.flight(vessel.orbit.body.reference_frame)
surfaceSpeed = conn.add_stream(getattr, flight, 'speed')
good = False
# Собираемся сужать орбиту с включённым двигателем, пока не получим нужную высоту
while surfaceSpeed() > 1.0:
    vessel.control.throttle = 1 - (0.95 / 1.01 ** surfaceSpeed())
    if (apoapsis() < 100000 and apoapsis() > 0.0) or (periapsis() < 100000 and periapsis() > 0.0):
        good = True
    error = (vessel.auto_pilot.pitch_error ** 2 + vessel.auto_pilot.heading_error ** 2) ** (1 / 2)
    if error > 3:
        vessel.control.throttle = 0
        while error > 1.2:
            error = (vessel.auto_pilot.pitch_error ** 2 + vessel.auto_pilot.heading_error ** 2) ** (1 / 2)
            print("Ошибка поворота/направления:", vessel.auto_pilot.error)
            time.sleep(0.25)
            if (apoapsis() < 100000 and apoapsis() > 0.0) or (periapsis() < 100000 and periapsis() > 0.0):
                good = True
                break
    if good:
        break
vessel.control.throttle = 0
flight = vessel.flight()
vessel.auto_pilot.engage()
vessel.auto_pilot.reference_frame = vessel.surface_velocity_reference_frame
vessel.auto_pilot.target_direction = (0.0, -1.0, 0.0)  # Снова поворачиваемся для сужения другой стороны орбиты

vessel.auto_pilot.wait()  # Ожидаем поворота
time_to_warp = vessel.orbit.time_to_periapsis
space_center.warp_to(space_center.ut + time_to_warp - 50)  # Ждём времени за 50 секунд до перигея
vessel.auto_pilot.target_direction = (0.0, -1.0, 0.0)
flight = vessel.flight(vessel.orbit.body.reference_frame)
good = False
delt = 4000
# Собираемся сужать орбиту с включённым двигателем, пока не получим нужную высоту (Снова)
while apoapsis() > 14000 and periapsis() > 14000 or not good:
    vessel.control.throttle = 0.15
    if apoapsis() < 14000 or periapsis() < 14000:
        good = True
    error = (vessel.auto_pilot.pitch_error ** 2 + vessel.auto_pilot.heading_error ** 2) ** (1 / 2)
    if error > 3:
        vessel.control.throttle = 0
        while error > 1.2:
            error = (vessel.auto_pilot.pitch_error ** 2 + vessel.auto_pilot.heading_error ** 2) ** (1 / 2)
            print("Direction error:", vessel.auto_pilot.error)
            time.sleep(0.25)
            if apoapsis() < 14000 or periapsis() < 14000:
                good = True
                break
    if good:
        break
vessel.control.throttle = 0
print("Готовы к посадке...")
if apoapsis() < periapsis():
    time_to_warp = vessel.orbit.time_to_apoapsis
else:
    time_to_warp = vessel.orbit.time_to_periapsis
space_center.warp_to(space_center.ut + time_to_warp - 10)
vessel.auto_pilot.wait()
print("Начинаем посадку...")
f.write(f"Орбита от уровня моря Луны (sea level): "
        f"{space_center.active_vessel.flight(vessel.orbit.body.reference_frame).mean_altitude}\n")
f.write(f"Орбита от поверхности под станцией (surface level): "
        f"{space_center.active_vessel.flight(vessel.orbit.body.reference_frame).surface_altitude}\n")
vessel = space_center.active_vessel
flight = vessel.flight(vessel.orbit.body.reference_frame)
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
periapsis = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
timestart = space_center.ut

print("Поворачиваемся для посадки")
vessel.auto_pilot.engage()
surfaceSpeed = conn.add_stream(getattr, flight, 'speed')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
vessel.auto_pilot.reference_frame = vessel.surface_velocity_reference_frame
vessel.auto_pilot.target_direction = (0.0, -1.0, 0.0)
vessel.auto_pilot.wait()
prevspeed = float(surfaceSpeed())
print("Включаем двигатель")
pred = 1.5
print("Время включения первой тяги:")
print(space_center.ut - timestart)
# Повернувшись горизонтально над поверхностью Луны, включаем двигатель на малую тягу и ждём, пока
# горизонтальная поверхностная скорость не станет минимальной
while flight.horizontal_speed > pred:
    vessel.auto_pilot.reference_frame = vessel.surface_velocity_reference_frame
    vessel.auto_pilot.target_direction = (0.0, -1.0, 0.0)
    vessel.control.throttle = 0.1235
print("Около нуля, поворачиваемся вертикально")
print(flight.surface_altitude)
vessel.auto_pilot.reference_frame = vessel.surface_velocity_reference_frame
# Для вертикальной посадки понадобится гибридная система координат
landing_reference_frame = space_center.ReferenceFrame.create_hybrid(
        position=vessel.orbit.body.reference_frame, rotation=vessel.surface_reference_frame)
flight = vessel.flight(landing_reference_frame)
print("Садимся")
vessel.control.legs = True
vessel.auto_pilot.reference_frame = landing_reference_frame
vessel.control.throttle = 0.0
wassaid = False
print(f"Высота вертикального падения sea~ {vessel.flight(vessel.orbit.body.reference_frame).mean_altitude}")
print(f"Высота вертикального падения surf~ {vessel.flight(vessel.orbit.body.reference_frame).surface_altitude}")
# Далее – цикл для мягкой посадки
while True:
    vessel.auto_pilot.target_pitch_and_heading(90, 90)
    if flight.vertical_speed < -42:  # Вертикально падаем, пока скорость не увеличится до крайней допустимой величины
        if not wassaid:
            # Включаем малую тягу, для уменьшения вертикальной скорости
            print("Время включения второй тяги:")
            print(space_center.ut - timestart)
            print(f"Высота вертикального падения ~ {vessel.flight(vessel.orbit.body.reference_frame).mean_altitude}")
            wassaid = True
        vessel.control.throttle = 0.0775
    if flight.surface_altitude < 5:
        vessel.control.throttle = 0.0
        break
print("Посадка завершена")
vessel.auto_pilot.disengage()
vessel.auto_pilot.sas = True
print()
f.write(f"Время посадки: {round(ut() - TimeStart, 3)}\n")
print()
f.close()
