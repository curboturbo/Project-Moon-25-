import math
import time
import krpc

# Соединяемся с KSP и настраиваем потоки данных, как и в скрипте main
conn = krpc.connect(name='Charts1', address="127.0.0.1", rpc_port=50002, stream_port=50003)
vessel = conn.space_center.active_vessel
flight = vessel.flight()
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
staltitude = float(altitude())
landing_reference_frame = conn.space_center.ReferenceFrame.create_hybrid(
        position=vessel.orbit.body.reference_frame, rotation=vessel.surface_reference_frame)
vel = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), 'speed')
prevTime = float(ut())
newTime = float(ut())
# Откроем файл для записи
f = open("ascendVelocity.txt", "a")
f.writelines("")
# Ждём старта
while vessel.control.throttle == 0.0:
    pass
print("Начали запись")
while not conn.space_center.active_vessel.control.sas:
    newTime = float(ut())
    if (newTime - prevTime) >= 0.25:
        prevTime = newTime
        f.write(f"{round(vessel.flight(vessel.orbit.body.reference_frame).speed, 3)}\n")
        # Каждую четверть секунды записываем в файл текущую скорость космического аппарата;
        # Этот скрипт иногда использовался для записи других данных в другие файлы, так как он удобен, а для смены
        # данных достаточно поменять две строки
f.close()
