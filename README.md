# What is this
The purpose of this project is to get telemetrics from Rpanion together with the video stream.
The project includes a python script that puts the data together in a combined TCP stream.
Each UDP package from the video stream is combined with the telemetrics is combined into a single byte array.

Included is also a .NET project which will take the resulting data stream and convert it into one stream of telemetrics and one stream of video.


# Instructions
- Install Rpanion 0.8
- Modify the file /home/pi/Rpanion-server/python/rtsp-server.py - please see the file in the instructions folder
  On the rows that start with pipeline_str we have changed it to "config-interval=1" on rtph264pay so that
	! rtph264pay name=pay0 pt=96
	becomes
	! rtph264pay name=pay0 pt=96 config-interval=1	
- See the images provided in the instructions folder to see how we set up Rpanion


Created at HackAddThon August 2022 by Pajkastarna