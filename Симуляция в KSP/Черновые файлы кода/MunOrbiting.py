import math
import time
import krpc

conn = krpc.connect(name='Flight Mission')
space_center = conn.space_center
vessel = space_center.active_vessel
flight = vessel.flight()
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
periapsis = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
vessel.control.activate_next_stage()
time_to_warp = vessel.orbit.next_orbit.time_to_periapsis + vessel.orbit.time_to_soi_change
space_center.warp_to(space_center.ut + time_to_warp - 300)  # 5 minutes before periapsis of mun encounter

#v essel.control.rcs = True
vessel.control.antennas = True
vessel.auto_pilot.engage()
vessel.auto_pilot.reference_frame = vessel.surface_velocity_reference_frame
vessel.auto_pilot.target_direction = (0.0, -1.0, 0.0)  # Point retro-grade surface

vessel.auto_pilot.wait()  # Wait until pointing retro-grade
time_to_warp = vessel.orbit.time_to_periapsis
space_center.warp_to(space_center.ut + time_to_warp - 30)  # 30 seconds from periapsis

vessel.auto_pilot.wait()
print("Fire engine...")
print(apoapsis())
print(periapsis())
# Stream surface velocity
flight = vessel.flight(vessel.orbit.body.reference_frame)
surfaceSpeed = conn.add_stream(getattr, flight, 'speed')
good = False
while surfaceSpeed() > 1.0:
    vessel.control.throttle = 1 - (0.95 / 1.01 ** surfaceSpeed())
    if (apoapsis() < 100000 and apoapsis() > 0.0) or (periapsis() < 100000 and periapsis() > 0.0):
        good = True
    error = (vessel.auto_pilot.pitch_error ** 2 + vessel.auto_pilot.heading_error ** 2) ** (1 / 2)
    if error > 3:
        vessel.control.throttle = 0
        while error > 1.2:
            error = (vessel.auto_pilot.pitch_error ** 2 + vessel.auto_pilot.heading_error ** 2) ** (1 / 2)
            print("Direction error:", vessel.auto_pilot.error)
            time.sleep(0.25)
            if (apoapsis() < 100000 and apoapsis() > 0.0) or (periapsis() < 100000 and periapsis() > 0.0):
                good = True
                break
    if good:
        break
vessel.control.throttle = 0
print(apoapsis())
print(periapsis())
flight = vessel.flight()
vessel.auto_pilot.engage()
vessel.auto_pilot.reference_frame = vessel.surface_velocity_reference_frame
vessel.auto_pilot.target_direction = (0.0, -1.0, 0.0)  # Point retro-grade surface

vessel.auto_pilot.wait()  # Wait until pointing retro-grade
print("WHAT THE 1")
time_to_warp = vessel.orbit.time_to_periapsis
space_center.warp_to(space_center.ut + time_to_warp - 50)  # 30 seconds from periapsis
vessel.auto_pilot.target_direction = (0.0, -1.0, 0.0)
flight = vessel.flight(vessel.orbit.body.reference_frame)
good = False
print("WHAT THE 2")
delt = 4000
while apoapsis() > 14000 and periapsis() > 14000 or not good:
    vessel.control.throttle = 0.15
    if apoapsis() < 14000 or periapsis() < 14000:
        good = True
    #print(f"{apoapsis()} - {periapsis()} = {apoapsis() - periapsis()}")
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
print("Prepared for landing...")
if apoapsis() < periapsis():
    time_to_warp = vessel.orbit.time_to_apoapsis
else:
    time_to_warp = vessel.orbit.time_to_periapsis
space_center.warp_to(space_center.ut + time_to_warp - 10)
vessel.auto_pilot.engage()
#vessel.auto_pilot.target_direction = (1.0, -1.0, 1.0)
vessel.auto_pilot.reference_frame = vessel.surface_velocity_reference_frame
vessel.auto_pilot.target_pitch_and_heading(90.0, 0)
vessel.auto_pilot.wait()
print("Landing...")

print()
