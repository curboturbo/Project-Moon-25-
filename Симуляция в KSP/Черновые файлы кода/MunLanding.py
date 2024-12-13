import math
import time
import krpc

conn = krpc.connect(name='Flight Mission')
space_center = conn.space_center
vessel = space_center.active_vessel
flight = vessel.flight(vessel.orbit.body.reference_frame)
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
periapsis = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')

timestart = space_center.ut
print("Turning shenanigans")


def true_height():
    mun = conn.space_center.bodies['Mun']
    v = conn.space_center.active_vessel
    f = mun.reference_frame
    return math.sqrt(v.position(f)[0]**2 + v.position(f)[1]**2 + v.position(f)[2]**2) - mun.equatorial_radius

print(true_height())
vessel.auto_pilot.engage()
surfaceSpeed = conn.add_stream(getattr, flight, 'speed')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
vessel.auto_pilot.reference_frame = vessel.surface_velocity_reference_frame
vessel.auto_pilot.target_direction = (0.0, -1.0, 0.0)
vessel.auto_pilot.wait()
prevspeed = float(surfaceSpeed())
print("Burning to limit of zero speed")
pred = 1.5
print(true_height())
print("Время включения первой тяги:")
print(space_center.ut - timestart)
print(f"Высота включения первой тяги ~ {true_height()}")
print(f"Скорость для системы координат от центра Луны: {vessel.flight(vessel.orbit.body.reference_frame).speed}")
print(f"Скорость вертикальная: {vessel.flight(vessel.orbit.body.reference_frame).vertical_speed}")
print(f"Скорость горизонтальная: {vessel.flight(vessel.orbit.body.reference_frame).horizontal_speed}")
while flight.horizontal_speed > pred:
    vessel.auto_pilot.reference_frame = vessel.surface_velocity_reference_frame
    vessel.auto_pilot.target_direction = (0.0, -1.0, 0.0)
    vessel.control.throttle = 0.1235
print("Near zero, turning vertically")
print(flight.surface_altitude)
vessel.auto_pilot.reference_frame = vessel.surface_velocity_reference_frame
landing_reference_frame = space_center.ReferenceFrame.create_hybrid(
        position=vessel.orbit.body.reference_frame, rotation=vessel.surface_reference_frame)
flight = vessel.flight(landing_reference_frame)
print("Landing")
vessel.control.legs = True
vessel.auto_pilot.reference_frame = landing_reference_frame
vessel.control.throttle = 0.0
wassaid = False
# 2.889 t
print(f"Высота вертикального падения ~ {true_height()}")
while True:
    #print(flight.surface_altitude)
    vessel.auto_pilot.target_pitch_and_heading(90, 90)
    if flight.vertical_speed < -46:
        if not wassaid:
            print("Время включения второй тяги:")
            print(space_center.ut - timestart)
            print(f"Высота вертикального падения ~ {true_height()}")
            wassaid = True
        vessel.control.throttle = 0.0775
        #print(vessel.control.throttle)
    if flight.surface_altitude < 5:
        vessel.control.throttle = 0.0
        break
print("End!")
vessel.auto_pilot.disengage()
vessel.auto_pilot.sas = True
print()