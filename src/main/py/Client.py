from pymavlink import mavutil
import json


the_connection = mavutil.mavlink_connection(':5555')

print('running...')

init_time = the_connection.recv_match(type='ATTITUDE',blocking=True).time_boot_ms
while True:
    try:
        the_connection.wait_heartbeat()

        attitude = the_connection.recv_match(type='ATTITUDE', blocking=True)
        speed = the_connection.recv_match(type='VFR_HUD', blocking=True).airspeed
        servo5 = the_connection.recv_match(type='SERVO_OUTPUT_RAW', blocking=True).servo6_raw
        servo6 = the_connection.recv_match(type='SERVO_OUTPUT_RAW', blocking=True).servo6_raw
        time = the_connection.recv_match(type="SYSTEM_TIME", blocking=True)

        thisdict = {
            "servo_5" : servo5,
            "servo_6" : servo6,
            "airspeed" : speed,
            "attitude" : {
                "roll": attitude.roll,
                "pitch":attitude.pitch,
                "yaw":attitude.yaw,
                "rollspeed":attitude.rollspeed,
                "pitchspeed":attitude.pitchspeed,
                "yawspeed":attitude.yawspeed

            }
        }

        data_loaded = json.dumps(thisdict)

        print(data_loaded)
        #print(thisdict)

        #print(attitude)
        #print("servo 5: " + str(servo5))
        #print("servo 6: " + str(servo6))
        #print("airspeed: " + str(speed))
        #print("time: " + str(attitude.time_boot_ms - init_time  ))
    except KeyboardInterrupt:
        print('abort')
        break