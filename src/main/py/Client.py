import queue
from pymavlink import mavutil
import json
import socket
import threading
import time
from threading import Thread

#Telemetry socket
the_connection = mavutil.mavlink_connection(':8279')

#Video socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(("",5400))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.0.2.115', 12788))  # The address of the TCP server listening

buffer = queue.Queue()

keepRunning = True


def sendTCP(msgVid,msgTelemetry):

    buffVid = msgVid
    teleLen = len(json.dumps(msgTelemetry))
    buffTele = [teleLen]
    buffVid = msgVid
    buffTele = json.dumps(msgTelemetry)



    s.send((teleLen + len(buffVid)).to_bytes(4, 'big'))
    s.send((len(buffVid)).to_bytes(4, 'big'))
    s.send(buffVid)
    s.send(buffTele)
    leftToGFill = 4096 - len((teleLen + len(buffVid)).to_bytes(4, 'big')) + len((len(buffVid)).to_bytes(4, 'big')) + len(buffVid) + len(buffTele)


    xx = range(0, leftToGFill)
    for v in xx:
        s.send('1')


#To run locally set up a new UDP Output in Rpanion
#With <your ip>:<free port> eg. 5555
def telemetryStream():

    while True:

        if not keepRunning:
            break


        the_connection.wait_heartbeat()

        #Telemetry
        attitude = the_connection.recv_match(type='ATTITUDE', blocking=True)
        speed = the_connection.recv_match(type='VFR_HUD', blocking=True).airspeed
        servo5 = the_connection.recv_match(type='SERVO_OUTPUT_RAW', blocking=True).servo6_raw
        servo6 = the_connection.recv_match(type='SERVO_OUTPUT_RAW', blocking=True).servo6_raw
        time = the_connection.recv_match(type="SYSTEM_TIME", blocking=True)

        localdict = {
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

        buffer.put(localdict)


        #telemetry_data = json.dumps(thisdict)
        #print(data_loaded)

def updateDict(thisdict):

    if not buffer.empty():
        thisdict = buffer.get()
        return thisdict

    return thisdict



def videoStream(thisdict):

    thisdict = updateDict(thisdict)

    #Video
    data, addr = sock.recvfrom(4096)
    print("Telemetry: %s" % thisdict)
    print("received message: %s" % data)
    return thisdict



def mainloop():

    print('running...')
    stop_video_thread = False
    stop_telemetry_thread = False
    thisdict = {}
    counter = 500

    while True:
        try:
            counter = counter - 1
            thisdict = videoStream(thisdict)
            #telemetryStream()
            if counter < 1:
                break

        except KeyboardInterrupt:
            print('abort')
            break




# producer task
def producer(queue):
    print('Producer: Running')
    telemetryStream()

def consumer(queue):
    print('consumer: Running')
    mainloop()

# create a producer thread
producer_thread = threading.Thread(target=producer, args=(buffer,))
# start the producer thread
producer_thread.start()

# create a consumer thread
consumer_thread = threading.Thread(target=consumer, args=(buffer,))
# start the consumer thread
consumer_thread.start()
#init_time = the_connection.recv_match(type='ATTITUDE',blocking=True).time_boot_ms



consumer_thread.join()
keepRunning = False

producer_thread.join()

s.close()


#print(thisdict)

#print(attitude)
#print("servo 5: " + str(servo5))
#print("servo 6: " + str(servo6))
#print("airspeed: " + str(speed))
#print("time: " + str(attitude.time_boot_ms - init_time  ))
