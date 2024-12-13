import math
import time
import krpc

# ����������� � KSP � ����������� ������ ������, ��� � � ������� main
conn = krpc.connect(name='Charts2', address="127.0.0.1", rpc_port=50004, stream_port=50005)
vessel = conn.space_center.active_vessel
flight = vessel.flight()
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
staltitude = float(altitude())
Kerbin = vessel.orbit.body

initial_position = vessel.position(vessel.orbit.body.reference_frame)
initial_rotation = vessel.rotation(vessel.orbit.body.reference_frame)
initial_reference_frame = conn.space_center.ReferenceFrame.create_relative(
  vessel.orbit.body.reference_frame,
  position=initial_position,
  rotation=initial_rotation
)
special_delta = (0.0, Kerbin.position(initial_reference_frame)[1], 0.0)
initial_reference_frame = initial_reference_frame.create_relative(reference_frame=initial_reference_frame,
                                                                  position=special_delta)
pos = conn.add_stream(vessel.position, reference_frame=initial_reference_frame)

prevTime = float(ut())
newTime = float(ut())
# ������� ���� ��� ������
f = open("ascendCords.txt", "a")
f.writelines("")
# ��� ������
while vessel.control.throttle == 0.0:
    pass
print("������ ������")
while not conn.space_center.active_vessel.control.sas:
    newTime = float(ut())
    if (newTime - prevTime) >= 0.25:
        prevTime = newTime
        writing_pos = conn.space_center.active_vessel.position(initial_reference_frame)
        f.write(f"{round(writing_pos[2], 2)} {round(writing_pos[1], 2)} {round(writing_pos[0], 2)}\n")
        # ������ �������� ������� ���������� � ���� ������� ���������� ������������ ��������;
        # ���� ������ ������ ������������� ��� ������ ������ ������ � ������ �����, ��� ��� �� ������, � ��� �����
        # ������ ���������� �������� ��� ������
f.close()
