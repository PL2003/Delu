Below is an updated USER_GUIDE.md you can copy directly into the repository. It keeps the original project architecture intact and treats the phone web server as an optional independent addition.

# 🚗 Autonomous Rover — Jetson Orin Deployment & User Guide

Complete deployment, configuration, testing, and operation guide for running the
**Obstacle Avoidance Prototype** on a **Jetson Orin + 4-Wheel Rover**.

---

## 1. System Overview

The rover uses the following architecture:

```text
                         ┌──────────────────────────┐
                         │        PHONE             │
                         │                          │
                         │ Local Web Dashboard      │
                         │ START / STOP / STATUS    │
                         └────────────┬─────────────┘
                                      │ Wi-Fi
                                      ▼
┌──────────────────────────────────────────────────────────────┐
│                       JETSON ORIN                            │
│                                                              │
│  main_robot_controller.py                                    │
│                                                              │
│  ┌────────────┐    ┌──────────────┐    ┌─────────────────┐ │
│  │ RealSense  │───►│ ArUco        │    │ YOLO-World      │ │
│  │ RGB+Depth  │    │ Detection    │    │ Object Detection│ │
│  └────────────┘    └──────────────┘    └─────────────────┘ │
│          │                  │                    │            │
│          └──────────────────┴────────────────────┘            │
│                             │                                 │
│                    Obstacle / Navigation                      │
│                       Decision Logic                           │
│                             │                                 │
│                             ▼                                 │
│                       USB Serial                              │
└─────────────────────────────┬────────────────────────────────┘
                              │
                         115200 baud
                              │
                              ▼
                     ┌─────────────────┐
                     │      ESP32      │
                     │ Motor Controller│
                     └────────┬────────┘
                              │
                         Motor Driver
                              │
                  ┌───────────┴───────────┐
                  ▼                       ▼
             Left Motors             Right Motors


---

2. Hardware Requirements

Main Computer

Jetson Orin

Ubuntu/Linux compatible with your JetPack installation

Wi-Fi connection


Sensors

Intel RealSense camera

RGB + Depth capability


Motor Control

ESP32

Motor driver

4-wheel chassis

DC motors

Suitable battery/power system


Navigation Marker

Printed ArUco marker

Default marker:

Dictionary: DICT_4X4_50

ID: 0



Optional Remote Control

Smartphone

Same local network as Jetson Orin



---

3. Software Architecture

The original repository should remain unchanged.

Additional files can be added beside the original project.

Recommended final structure:

~/rover/
│
├── main_robot_controller.py
├── esp32_motor_controller.ino
├── generate_aruco_marker.py
├── test_webcam_detection.py
├── requirements.txt
│
├── rover_web_server.py
│
├── models/
│
└── venv/

File purposes

main_robot_controller.py
    Main autonomous rover controller.

esp32_motor_controller.ino
    ESP32 motor-control firmware.

generate_aruco_marker.py
    Generates the navigation ArUco marker.

test_webcam_detection.py
    Camera/detection testing utility.

requirements.txt
    Python dependencies.

rover_web_server.py
    Optional local web interface for START/STOP/status control.

models/
    Optional local AI model files.

venv/
    Python virtual environment.


---

4. Clone the Repository

Open a terminal on the Jetson Orin.

cd ~

Clone the project:

git clone https://github.com/n4b1lAh/obstacle-avoidance-prototype.git rover

Enter the project:

cd ~/rover

Check the files:

ls

Expected files include:

main_robot_controller.py
esp32_motor_controller.ino
generate_aruco_marker.py
test_webcam_detection.py
requirements.txt


---

5. Check Jetson Orin

Check JetPack:

cat /etc/nv_tegra_release

Check architecture:

uname -m

Expected:

aarch64

Check Python:

python3 --version

Check Jetson GPU status:

sudo tegrastats

Press:

Ctrl+C

to exit tegrastats.


---

6. Install Basic System Packages

Update the system:

sudo apt update

Install required utilities:

sudo apt install -y \
    git \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    cmake \
    libopencv-dev \
    v4l-utils


---

7. Create Python Virtual Environment

From the project directory:

cd ~/rover

Create the environment:

python3 -m venv venv

Activate it:

source venv/bin/activate

Your terminal should now look similar to:

(venv) jetson@orin:~/rover$

Upgrade pip:

pip install --upgrade pip setuptools wheel


---

8. Install Python Dependencies

Install the repository requirements:

pip install -r requirements.txt

The project requires packages such as:

numpy
opencv-python
opencv-contrib-python
pyrealsense2
ultralytics
pyserial

Important — Jetson PyTorch

Do not blindly install a generic desktop PyTorch build.

Jetson Orin uses an NVIDIA JetPack/CUDA environment, so PyTorch should be compatible with the installed JetPack version.

Check:

python3 -c "import torch; print(torch.__version__)"

Check CUDA:

python3 -c "import torch; print(torch.cuda.is_available())"

Expected:

True

If PyTorch is missing or CUDA returns False, install the Jetson-compatible PyTorch version for your exact JetPack release before running YOLO.


---

9. RealSense Installation

Connect the Intel RealSense camera to a USB 3.x port.

Check USB:

lsusb

The RealSense device should appear.

Check the Python package:

python3 -c "import pyrealsense2 as rs; print('RealSense OK')"

Expected:

RealSense OK

Check video devices:

ls /dev/video*


---

10. ESP32 Connection

Connect the ESP32 to the Jetson through USB.

Check:

ls /dev/ttyUSB*

Also check:

ls /dev/ttyACM*

Typical result:

/dev/ttyUSB0

or:

/dev/ttyACM0

Check recent USB messages:

dmesg | tail -30


---

11. Give Serial-Port Permission

If the user cannot access the ESP32 serial port:

sudo usermod -aG dialout $USER

Log out and log back in.

Then check:

groups

dialout should appear.


---

12. ESP32 Firmware

Open:

esp32_motor_controller.ino

Upload it to the ESP32.

The Jetson ↔ ESP32 serial communication uses:

Baud rate: 115200

The controller sends commands such as:

F
L
R
S
SPIN

The ESP32 controls the motor driver based on these commands.


---

13. ESP32 Safety Watchdog

The ESP32 firmware contains a command timeout/watchdog mechanism.

If communication from the Jetson stops for approximately the configured timeout period, the ESP32 should stop the motors.

This is an important safety feature.

Always verify the watchdog before autonomous testing.


---

14. Test ESP32 Before Autonomous Operation

Do not place the rover on the floor initially.

Lift the rover so the wheels can rotate freely.

Start the controller only after confirming:

Jetson
   ↓
USB Serial
   ↓
ESP32
   ↓
Motor Driver
   ↓
Motors

is correctly connected.


---

15. ArUco Marker Configuration

The current project does NOT accept every possible ArUco marker.

The default configuration is:

Dictionary:
DICT_4X4_50

Target ID:
0

Therefore the navigation marker must be:

DICT_4X4_50
ID 0

Examples that do NOT match the default configuration:

DICT_4X4_50 / ID 1
DICT_5X5_50 / ID 0
DICT_6X6_250 / ID 0
DICT_7X7_1000 / ID 0

unless the controller is modified accordingly.


---

16. Generate the ArUco Marker

Run:

cd ~/rover
source venv/bin/activate

python3 generate_aruco_marker.py

Generate/print the required marker.

Recommended:

High contrast

Flat surface

No reflections

Sufficient physical size

Clear black border

Mounted vertically



---

17. Camera Test

Before autonomous operation, test the camera.

Run:

python3 test_webcam_detection.py

Confirm that:

Camera opens correctly

Image is stable

Detection works

Jetson can access the camera



---

18. Main Autonomous Controller

Before using the web server, run the original controller directly.

cd ~/rover
source venv/bin/activate

python3 main_robot_controller.py

The basic processing pipeline is:

RealSense RGB
      │
      ├──► ArUco Detection
      │
      └──► YOLO Object Detection

RealSense Depth
      │
      ▼
Obstacle Detection
      │
      ▼
Navigation Decision
      │
      ▼
F / L / R / S / SPIN
      │
      ▼
ESP32
      │
      ▼
Motors


---

19. Navigation Logic

The current controller is a reactive navigation system.

The general decision hierarchy is:

┌───────────────┐
                    │ Target reached│
                    └───────┬───────┘
                            │
                           YES
                            ▼
                           SPIN

                            │
                           NO
                            ▼
                  ┌──────────────────┐
                  │ Center obstructed?│
                  └────────┬─────────┘
                           │
                    YES ───┴─── NO
                     │            │
                     ▼            ▼
             Choose safer     Chase ArUco
                direction       target
                     │            │
                     └─────┬──────┘
                           ▼
                         DRIVE

If the target is lost, the controller can stop depending on its current logic.


---

20. Important Current Limitations

The current repository is a reactive rover controller.

It does not provide a complete:

SLAM system
Global map
Path planner
GPS navigation
Wheel odometry
IMU fusion
Velocity PID controller
Obstacle memory

The system primarily uses:

RGB
Depth
ArUco
YOLO
Reactive obstacle avoidance


---

21. First Autonomous Test

Perform testing in this order.

Test 1 — Camera

Verify RealSense.

python3 test_webcam_detection.py


---

Test 2 — ArUco

Place:

DICT_4X4_50 / ID 0

in front of the camera.

Verify that the marker is detected.


---

Test 3 — Object Detection

Verify YOLO detection.

Make sure CUDA is available:

python3 -c "import torch; print(torch.cuda.is_available())"


---

Test 4 — Serial

Verify Jetson → ESP32 communication.


---

Test 5 — Motors

Lift the rover.

Verify:

F → Forward
L → Left
R → Right
S → Stop
SPIN → Rotation


---

Test 6 — Low-Speed Floor Test

Place the rover on the floor.

Use a large open area.

Keep a physical emergency stop available.


---

Test 7 — Autonomous Navigation

Place the ArUco target ahead of the rover.

Start the controller:

python3 main_robot_controller.py

Observe:

Target detection
Depth
Obstacle avoidance
Motor commands
Target approach


---

22. Stop the Controller

Normally press:

Ctrl+C

The controller should stop and execute its cleanup procedure.

Confirm that:

Motors → STOP
Camera → Released
OpenCV windows → Closed


---

23. Optional Phone Web Dashboard

The web dashboard is an additional independent component.

It should NOT replace:

main_robot_controller.py

Architecture:

Phone
  │
  │ Wi-Fi
  ▼
Jetson Orin
  │
  ▼
rover_web_server.py
  │
  ├── START
  ├── STOP
  ├── STATUS
  └── LOG / TELEMETRY
       │
       ▼
main_robot_controller.py


---

24. Install the Web Server

Place:

rover_web_server.py

inside:

~/rover/

The final structure becomes:

~/rover/
│
├── main_robot_controller.py
├── esp32_motor_controller.ino
├── generate_aruco_marker.py
├── test_webcam_detection.py
├── requirements.txt
├── rover_web_server.py
│
├── models/
└── venv/


---

25. Start the Web Server

Activate the environment:

cd ~/rover
source venv/bin/activate

Start:

python3 rover_web_server.py


---

26. Find Jetson IP Address

Run:

hostname -I

Example:

192.168.1.120


---

27. Connect From Phone

Connect the phone to the same Wi-Fi/LAN as the Jetson.

Open a browser:

http://192.168.1.120:8080

Replace:

192.168.1.120

with the actual Jetson IP.


---

28. Web Dashboard Operation

The dashboard should provide controls such as:

┌─────────────────────────────┐
│       ROVER CONTROL         │
├─────────────────────────────┤
│                             │
│ Status: STOPPED             │
│                             │
│ [ START ]    [ STOP ]       │
│                             │
│ Controller: OFF             │
│ PID: ---                    │
│                             │
│ Detection: ---              │
│ Next Step: ---              │
│                             │
│ Live Log                    │
│ -------------------------   │
│                             │
└─────────────────────────────┘


---

29. Important Telemetry Limitation

If the original:

main_robot_controller.py

does not print a particular internal value, an external web server cannot directly know that Python variable without modifying/instrumenting the controller.

For example:

ArUco ID
ArUco distance
Left depth
Center depth
Right depth
YOLO detections
Navigation decision
FPS

can only be displayed externally if:

1. The controller already prints them, or


2. A telemetry interface is added, or


3. A separate wrapper parses the controller output.



The web server should not pretend to have access to internal variables that the original process does not expose.


---

30. Recommended Zero-Modification Approach

To keep the repository architecture unchanged:

main_robot_controller.py
        │
        │ stdout
        ▼
rover_web_server.py
        │
        ▼
Phone Dashboard

The web server can capture and display controller output.

This allows:

START
STOP
PROCESS STATUS
PID
RUNTIME
LOG
AVAILABLE TELEMETRY

without modifying the original controller.


---

31. Safe STOP Procedure

The web server should preferably stop the controller gracefully.

Recommended sequence:

Phone STOP
     │
     ▼
Send SIGINT
     │
     ▼
main_robot_controller.py
     │
     ▼
cleanup()
     │
     ▼
Send STOP to ESP32
     │
     ▼
Motors stop

If the process does not stop:

SIGTERM
     ↓
KILL fallback

should be used only as a final fallback.


---

32. LAN Security

The web server controls a physical rover.

Therefore:

Do not expose port 8080 directly to the public Internet.

Recommended:

Phone
  │
  │ Trusted Wi-Fi
  ▼
Jetson

Avoid:

Internet
   │
   ▼
Jetson:8080

For a permanent deployment, add authentication or use a secure VPN/SSH tunnel.


---

33. Automatic Startup — Optional

After the entire system has been tested manually, the web server can be configured as a systemd service.

Desired boot sequence:

Jetson boots
     │
     ▼
Network available
     │
     ▼
rover_web_server.py starts
     │
     ▼
Phone opens dashboard
     │
     ▼
START
     │
     ▼
main_robot_controller.py

Do NOT enable automatic autonomous motor movement at boot.

The rover should remain stopped until explicitly started.


---

34. Recommended systemd Services

Recommended final arrangement:

systemd
   │
   └── rover-web.service
            │
            ▼
      rover_web_server.py
            │
            └── START/STOP
                    │
                    ▼
          main_robot_controller.py

The controller itself should not automatically drive the rover after Jetson boot.


---

35. Useful Commands

Activate environment

cd ~/rover
source venv/bin/activate

Run controller

python3 main_robot_controller.py

Run web server

python3 rover_web_server.py

Check Jetson IP

hostname -I

Check serial ports

ls /dev/ttyUSB*
ls /dev/ttyACM*

Check USB devices

lsusb

Check camera devices

ls /dev/video*

Check Jetson status

sudo tegrastats

Check Python

python3 --version

Check CUDA

python3 -c "import torch; print(torch.cuda.is_available())"

Check OpenCV

python3 -c "import cv2; print(cv2.__version__)"

Check RealSense

python3 -c "import pyrealsense2 as rs; print('RealSense OK')"

Check Ultralytics

python3 -c "from ultralytics import YOLO; print('Ultralytics OK')"


---

36. Troubleshooting

Jetson cannot see ESP32

Check:

ls /dev/ttyUSB*
ls /dev/ttyACM*

Then:

dmesg | tail -30

Check USB cable.

Some USB cables are power-only.


---

Permission denied on serial

Run:

sudo usermod -aG dialout $USER

Log out and log back in.


---

RealSense not detected

Check:

lsusb

Try another USB 3.x port.

Check:

python3 -c "import pyrealsense2 as rs; print('OK')"


---

CUDA is False

Run:

python3 -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"

Check:

cat /etc/nv_tegra_release

Install a PyTorch build compatible with the installed JetPack version.

Do not randomly downgrade/upgrade CUDA libraries.


---

YOLO is very slow

Check:

sudo tegrastats

Look at:

GPU
CPU
RAM
Temperature
Power

Possible causes:

Wrong PyTorch build

CPU inference instead of GPU

High image resolution

Large YOLO model

Thermal throttling

Insufficient power



---

ArUco marker not detected

Confirm:

Dictionary = DICT_4X4_50
ID = 0

Also check:

Good lighting

Marker is flat

Marker is not blurred

Entire marker is visible

Adequate camera distance

Correct print quality



---

Rover keeps stopping

Check:

ArUco detection
Depth detection
ESP32 serial connection
ESP32 watchdog
Motor driver
Battery

Check controller logs.


---

Rover turns/oscillates

The current navigation algorithm is reactive.

Possible causes:

Target near image center boundary

Depth measurements changing rapidly

Three-sector depth representation

Target detection jitter

No velocity PID

No obstacle memory

No odometry


This is a limitation of the current architecture rather than necessarily a hardware failure.


---

37. Pre-Deployment Checklist

Before operating the rover:

[ ] Jetson Orin boots correctly
[ ] JetPack verified
[ ] Python installed
[ ] Virtual environment created
[ ] Dependencies installed
[ ] Jetson CUDA verified
[ ] PyTorch CUDA verified
[ ] RealSense detected
[ ] ESP32 detected
[ ] Serial permissions configured
[ ] ESP32 firmware uploaded
[ ] Motor driver tested
[ ] ESP32 watchdog tested
[ ] ArUco marker generated
[ ] DICT_4X4_50 confirmed
[ ] ArUco ID 0 confirmed
[ ] YOLO tested
[ ] Main controller tested
[ ] Motors tested with wheels lifted
[ ] Emergency stop available
[ ] Low-speed floor test completed
[ ] Web server tested
[ ] Phone can connect
[ ] START tested
[ ] STOP tested


---

38. Recommended Operating Procedure

Every normal operation should follow:

1. Power ON rover
       ↓
2. Power ON Jetson Orin
       ↓
3. Wait for Linux/network
       ↓
4. Verify ESP32
       ↓
5. Verify RealSense
       ↓
6. Start web server
       ↓
7. Connect phone
       ↓
8. Confirm rover is physically safe
       ↓
9. Place ArUco target
       ↓
10. Press START
       ↓
11. Monitor dashboard
       ↓
12. Press STOP when required
       ↓
13. Verify motors stopped
       ↓
14. Power down rover


---

39. Emergency Procedure

If the rover behaves unexpectedly:

First priority

Use the physical power/emergency switch.

POWER OFF

Do not depend only on the web interface.

Then

Stop the controller:

Ctrl+C

or use the web dashboard:

STOP

Check:

ESP32
Motor driver
Battery
Serial connection
Camera
Navigation detection

before restarting.


---

40. Final System

The intended final system is:

PHONE
                           │
                        Wi-Fi
                           │
                           ▼
                 ┌──────────────────┐
                 │     Jetson Orin  │
                 │                  │
                 │ Web Server       │
                 │ START / STOP     │
                 │ STATUS / LOG     │
                 └────────┬─────────┘
                          │
                          ▼
              main_robot_controller.py
                          │
             ┌────────────┼────────────┐
             │            │            │
             ▼            ▼            ▼
        RealSense       ArUco        YOLO
        RGB + Depth     Target       Objects
             │            │            │
             └────────────┼────────────┘
                          ▼
                  Navigation Logic
                          │
                          ▼
                   Serial 115200
                          │
                          ▼
                       ESP32
                          │
                     Motor Driver
                          │
                          ▼
                    4-Wheel Rover


---

41. Important Design Principle

The deployment should preserve the original repository:

main_robot_controller.py

as the core autonomous controller.

The web interface is an external supervisory layer:

Phone
  ↓
Web Server
  ↓
Controller
  ↓
ESP32
  ↓
Motors

This makes the system easier to debug, update, and recover if the web interface fails.

The rover's physical safety should never depend solely on the phone, Wi-Fi, or web server.


---

42. Quick Start

After everything has been installed and tested:

cd ~/rover
source venv/bin/activate
python3 rover_web_server.py

Find the Jetson IP:

hostname -I

Open from the phone:

http://JETSON_IP:8080

Then:

START
  ↓
Autonomous rover begins
  ↓
Monitor status/log
  ↓
STOP

For direct operation without the web server:

cd ~/rover
source venv/bin/activate
python3 main_robot_controller.py


---

END

Project: https://github.com/n4b1lAh/obstacle-avoidance-prototype

Platform: Jetson Orin

Vehicle: 4-Wheel Autonomous Rover

Default ArUco: DICT_4X4_50 / ID 0

ESP32 Serial: 115200 baud

Web Dashboard: Port 8080