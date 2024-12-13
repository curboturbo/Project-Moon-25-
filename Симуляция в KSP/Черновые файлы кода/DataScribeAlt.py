import math
import time
import krpc
# import main

conn = krpc.connect(name='Charts1', address="127.0.0.1", rpc_port=50002, stream_port=50003)
vessel = conn.space_center.active_vessel
flight = vessel.flight()
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
staltitude = float(altitude())
# Set up streams for telemetry
landing_reference_frame = conn.space_center.ReferenceFrame.create_hybrid(
        position=vessel.orbit.body.reference_frame, rotation=vessel.surface_reference_frame)
vel = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), 'speed')
prevTime = float(ut())
newTime = float(ut())
f = open("ascendCords.txt", "a")


def twr():
    return (conn.space_center.active_vessel.thrust / conn.space_center.active_vessel.mass) / conn.space_center.active_vessel.orbit.body.surface_gravity
print(f"Ratio 1 stup: {vessel.parts.with_tag('sus')[0].engine.propellant_ratios}")
f.writelines("")
while vessel.control.throttle == 0.0:
    pass
print("go")
while not conn.space_center.active_vessel.control.sas:
    newTime = float(ut())
    #ОНО ПО ИДЕЕ ЗАВИСИТ ОТ ИГРОВОГО ВРЕМЕНИ, ПЕРЕМОТКА НЕ ДОЛЖНА ВЛИЯТЬ
    if (newTime - prevTime) >= 0.25:
        prevTime = newTime
        print(f"Ratio 1 stup: {vessel.parts.with_tag('amogus')[0].engine.propellant_ratios}")
        print(f"Ratio 2 stup: {vessel.parts.with_tag('hahogus')[0].engine.propellant_ratios}")
        print(f"Ratio 3 stup: {vessel.parts.with_tag('memogus')[0].engine.propellant_ratios}")

f.close()
