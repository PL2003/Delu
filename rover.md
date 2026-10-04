# 🚗 Autonomous Rover — Jetson Orin Deployment & User Guide

Complete deployment, configuration, testing, and operation guide for running the **Obstacle Avoidance Prototype** on a **Jetson Orin + 4-Wheel Rover**.

---

## 1. System Overview

The rover uses the following architecture:

```text
┌──────────────────────────┐
│          PHONE           │
│                          │
│   Local Web Dashboard    │
│  START / STOP / STATUS   │
└────────────┬─────────────┘
             │ Wi-Fi
             ▼
┌──────────────────────────────────────────────────────────────┐
│                         JETSON ORIN                          │
│                                                              │
│                  main_robot_controller.py                    │
│                                                              │
│  ┌────────────┐        ┌──────────────┐    ┌─────────────────┐ │
│  │ RealSense  │───────►│    ArUco     │    │   YOLO-World    │ │
│  │ RGB+Depth  │        │  Detection   │    │ Object Detection│ │
│  └────────────┘        └──────────────┘    └─────────────────┘ │
│        │                      │                     │        │
│        └──────────────────────┴─────────────────────┘        │
│                               │                              │
│                               ▼                              │
│                    Obstacle / Navigation                     │
│                        Decision Logic                        │
│                               │                              │
│                               ▼                              │
│                           USB Serial                         │
└───────────────────────────────┬──────────────────────────────┘
                                │ 115200 baud
                                ▼
                       ┌─────────────────┐
                       │      ESP32      │
                       │ Motor Controller│
                       └────────┬────────┘
                                │ Motor Driver
                        ┌───────┴───────┐
                        ▼               ▼
                   Left Motors     Right Motors

2. Hardware Requirements
 * Main Computer:
   * Jetson Orin
   * Ubuntu/Linux compatible with your JetPack installation
   * Wi-Fi connection
 * Sensors:
   * Intel RealSense camera (RGB + Depth capability)
 * Motor Control:
   * ESP32
   * Motor driver
   * 4-wheel chassis
   * DC motors
   * Suitable battery/power system
 * Navigation Marker:
   * Printed ArUco marker
   * Default marker: Dictionary DICT_4X4_50, ID 0
 * Optional Remote Control:
   * Smartphone on the same local network as Jetson Orin
3. Software Architecture
The original repository structure remains intact. Additional files can be added beside the original project.
Recommended structure:
~/rover/
│
├── main_robot_controller.py
├── esp32_motor_controller.ino
├── generate_aruco_marker.py
├── test_webcam_detection.py
├── requirements.txt
│
├── rover_web_server.py
├── models/
└── venv/

File Purposes
| File / Folder | Description |
|---|---|
| main_robot_controller.py | Main autonomous rover controller |
| esp32_motor_controller.ino | ESP32 motor-control firmware |
| generate_aruco_marker.py | Generates the navigation ArUco marker |
| test_webcam_detection.py | Camera/detection testing utility |
| requirements.txt | Python dependencies |
| rover_web_server.py | Optional local web interface for START/STOP/status control |
| models/ | Optional local AI model files |
| venv/ | Python virtual environment |
4. Clone the Repository
Open a terminal on the Jetson Orin and execute:
cd ~
git clone [https://github.com/n4b1lAh/obstacle-avoidance-prototype.git](https://github.com/n4b1lAh/obstacle-avoidance-prototype.git) rover
cd ~/rover
ls

Expected files include:
 * main_robot_controller.py
 * esp32_motor_controller.ino
 * generate_aruco_marker.py
 * test_webcam_detection.py
 * requirements.txt
5. Check Jetson Orin
Verify system specifications and JetPack release:
# Check JetPack
cat /etc/nv_tegra_release

# Check architecture (Expected: aarch64)
uname -m

# Check Python version
python3 --version

# Check Jetson GPU status (Press Ctrl+C to exit)
sudo tegrastats

6. Install Basic System Packages
Update system dependencies and install required build tools:
sudo apt update
sudo apt install -y \
  git \
  python3-pip \
  python3-venv \
  python3-dev \
  build-essential \
  cmake \
  libopencv-dev \
  v4l-utils

7. Create Python Virtual Environment
Set up and activate a dedicated virtual environment:
cd ~/rover
python3 -m venv venv
source venv/bin/activate

Your prompt should now display (venv) jetson@orin:~/rover$. Upgrade core Python build tools:
pip install --upgrade pip setuptools wheel

8. Install Python Dependencies
Install the repository requirements:
pip install -r requirements.txt

Required packages include numpy, opencv-python, opencv-contrib-python, pyrealsense2, ultralytics, and pyserial.
Important — Jetson PyTorch Setup
Do not blindly install a generic desktop PyTorch build. Jetson Orin uses an NVIDIA JetPack/CUDA environment, so PyTorch must match your specific JetPack release.
Verify installation and CUDA availability:
python3 -c "import torch; print(torch.__version__)"
python3 -c "import torch; print(torch.cuda.is_available())"

Expected output: True. If PyTorch is missing or returns False, install the Jetson-compatible PyTorch build for your exact JetPack version before running YOLO.
9. RealSense Installation
 * Connect the Intel RealSense camera to a USB 3.x port.
 * Verify USB recognition and Python bindings:
# Check USB connection
lsusb

# Check Python library binding
python3 -c "import pyrealsense2 as rs; print('RealSense OK')"

# Check video devices
ls /dev/video*

10. ESP32 Connection
 * Connect the ESP32 to the Jetson via USB.
 * Verify device creation:
ls /dev/ttyUSB*
ls /dev/ttyACM*

Typical result: /dev/ttyUSB0 or /dev/ttyACM0. Check system messages using:
dmesg | tail -30

11. Give Serial-Port Permission
Grant the current user access to the serial interface:
sudo usermod -aG dialout $USER

Log out and log back in, then verify membership:
groups

dialout must be listed in the group output.
12. ESP32 Firmware
 * Open esp32_motor_controller.ino using the Arduino IDE or CLI tool.
 * Flash the code to the ESP32.
 * Operating parameters:
   * Baud rate: 115200
   * Control commands: F (Forward), L (Left), R (Right), S (Stop), SPIN (Rotate)
13. ESP32 Safety Watchdog
The ESP32 firmware includes a command timeout/watchdog mechanism. If communication from the Jetson ceases for longer than the configured timeout window, the ESP32 automatically halts motor activity. Always confirm watchdog functionality prior to untethered autonomous testing.
14. Test ESP32 Before Autonomous Operation
 * Lift the rover off the ground so wheels rotate freely.
 * Confirm the complete communication path:
   
 * Perform manual signal generation tests before placing the vehicle on the ground.
15. ArUco Marker Configuration
The vision system uses standard target markers. Default target parameters:
 * Dictionary: DICT_4X4_50
 * Target ID: 0
Non-matching examples (will be ignored by default): DICT_4X4_50 ID 1, DICT_5X5_50 ID 0, DICT_6X6_250 ID 0.
16. Generate the ArUco Marker
Generate and print the navigation target:
cd ~/rover
source venv/bin/activate
python3 generate_aruco_marker.py

Target Placement Standards:
 * High contrast, non-reflective flat surface
 * Sufficient physical size with clear black border
 * Mounted vertically relative to camera field of view
17. Camera Test
Run optical diagnostics prior to autonomous execution:
python3 test_webcam_detection.py

Verify camera stream stability, target recognition, and frame rates.
18. Main Autonomous Controller
Run the main execution loop directly:
cd ~/rover
source venv/bin/activate
python3 main_robot_controller.py

Core Processing Pipeline
RealSense RGB ──► ArUco & YOLO Detection ──┐
                                            ├──► Obstacle Decision ──► Serial Commands ──► ESP32 ──► Motors
RealSense Depth ───────────────────────────┘

19. Navigation Logic
The controller operates on a reactive hierarchy:
┌──────────────────────────┐
│      Target Reached?     │
└────────────┬─────────────┘
             │
     ┌───────┴───────┐
    YES              NO
     │               │
     ▼               ▼
  [ SPIN ]  ┌──────────────────┐
            │ Center Obstructed│
            └────────┬─────────┘
                     │
             ┌───────┴───────┐
            YES              NO
             │               │
             ▼               ▼
     [ Safer Path ]    [ Target Chase ]
             │               │
             └───────┬───────┘
                     │
                     ▼
                  [ DRIVE ]

20. Important Current Limitations
The controller performs reactive spatial navigation. It does not feature:
 * SLAM map building / Global path planning
 * GPS positioning / Odometry integration
 * IMU sensor fusion / Velocity PID controllers
 * Spatial obstacle persistence memory
21. First Autonomous Test
Follow this sequential validation workflow:
 * Camera Test: Run python3 test_webcam_detection.py
 * ArUco Test: Validate recognition of DICT_4X4_50 / ID 0
 * Object Detection: Ensure YOLO CUDA acceleration is active
 * Serial Connection: Verify Jetson \leftrightarrow ESP32 link
 * Wheel Spin Test: Lift wheels; execute manual F, L, R, S, SPIN commands
 * Floor Clearance Test: Clear a wide area; ensure emergency power cutoff accessibility
 * Target Navigation Test: Place target in line-of-sight and execute python3 main_robot_controller.py
22. Stop the Controller
To gracefully terminate execution:
 * Issue a terminal interrupt via Ctrl+C.
 * Ensure the cleanup routines execute:
   * ESP32 receives explicit S (Stop) signal
   * Camera feed and OpenCV handles release cleanly
23. Optional Phone Web Dashboard
The web dashboard functions as a supervisor without modifying core logic.
Phone (Browser) ──► Wi-Fi ──► Jetson Orin (rover_web_server.py) ──► main_robot_controller.py

24. Install the Web Server
Place rover_web_server.py in the root repository folder:
~/rover/
├── main_robot_controller.py
├── rover_web_server.py
├── esp32_motor_controller.ino
├── generate_aruco_marker.py
├── test_webcam_detection.py
└── requirements.txt

25. Start the Web Server
Execute the server inside the virtual environment:
cd ~/rover
source venv/bin/activate
python3 rover_web_server.py

26. Find Jetson IP Address
Obtain local network credentials:
hostname -I

Example response: 192.168.1.120
27. Connect From Phone
 * Connect smartphone to the same local Wi-Fi subnet as the Jetson Orin.
 * Open a web browser and navigate to:
   http://<JETSON_IP>:8080 (e.g., http://192.168.1.120:8080).
28. Web Dashboard Operation
Interface Layout:
┌─────────────────────────────┐
│        ROVER CONTROL        │
├─────────────────────────────┤
│ Status: STOPPED             │
│                             │
│  [ START ]    [ STOP ]      │
│                             │
│ Controller: OFF             │
│ Live Log Feed:              │
│ --------------------------- │
│ > System initialized...     │
└─────────────────────────────┘

29. Important Telemetry Limitation
An external process cannot inspect internal Python state variables unless explicitly printed to stdout or exported through an IPC mechanism (IPC/Sockets). Information like FPS, Depth matrix values, and YOLO bounding boxes must be written to standard stdout streams to display on external web dashboards.
30. Recommended Zero-Modification Approach
Capture subprocess standard output streams without changing target base modules:
main_robot_controller.py ──(stdout)──► rover_web_server.py ──► Phone Dashboard

Provides non-invasive runtime logging, status tracking, process execution, and graceful shutdown monitoring.
31. Safe STOP Procedure
Standard termination pipeline:
If the process fails to terminate within timeout bounds, fallback strategies issue SIGTERM followed by SIGKILL.
32. LAN Security
 * Do not expose port 8080 directly to public routing tables.
 * Operate within trusted local networks, isolated access points, or encrypted VPN tunnels (e.g., Tailscale, WireGuard).
33. Automatic Startup — Optional
System boot sequence when using systemd services:
> Safety Warning: Do not configure autonomous driving logic to automatically start executing motor commands on system boot.
> 
34. Recommended systemd Services
Maintain separate service definitions to keep web serving decoupled from vehicle execution:
systemd
 └── rover-web.service
      └── launches: rover_web_server.py
           └── manually triggers: main_robot_controller.py

35. Useful Commands
# Activate environment
cd ~/rover && source venv/bin/activate

# Execute core controller
python3 main_robot_controller.py

# Execute web supervisor
python3 rover_web_server.py

# Diagnostic checks
hostname -I                                                      # IP Address
ls /dev/ttyUSB* /dev/ttyACM*                                     # Serial Interfaces
lsusb                                                            # USB Devices
ls /dev/video*                                                   # Video Devices
sudo tegrastats                                                  # System Resource Utilization

# Environment validation
python3 -c "import torch; print(torch.cuda.is_available())"      # PyTorch CUDA
python3 -c "import cv2; print(cv2.__version__)"                  # OpenCV
python3 -c "import pyrealsense2 as rs; print('RealSense OK')"    # RealSense SDK
python3 -c "from ultralytics import YOLO; print('YOLO OK')"      # Ultralytics Framework

36. Troubleshooting
 * Jetson cannot see ESP32: Check ls /dev/ttyUSB* and dmesg | tail -30. Verify cable supports data transmission, not just power delivery.
 * Permission denied on serial port: Ensure user belongs to the dialout group (sudo usermod -aG dialout $USER). Re-log required.
 * RealSense not detected: Verify USB connection status using lsusb. Ensure attachment to a USB 3.x port.
 * CUDA available returns False: Validate JetPack compatibility and reinstall PyTorch built for NVIDIA L4T environments.
 * YOLO execution sluggish: Run sudo tegrastats to observe GPU allocation. High latency usually indicates fallback to CPU execution or severe thermal throttling.
 * ArUco marker ignored: Verify marker uses dictionary DICT_4X4_50 and ID 0. Ensure minimal glare and adequate lighting.
 * Vehicle oscillates during approach: Reactive systems suffer jitter near decision boundaries. Fine-tune camera placement or adjust sector threshold parameters.
37. Pre-Deployment Checklist
 * [ ] Jetson Orin boots cleanly
 * [ ] JetPack version verified
 * [ ] Python environment configured
 * [ ] Requirements installed
 * [ ] CUDA hardware acceleration verified in PyTorch
 * [ ] Intel RealSense camera operational
 * [ ] ESP32 recognized on serial bus
 * [ ] dialout group permissions set
 * [ ] ESP32 firmware uploaded
 * [ ] Safety watchdog tested
 * [ ] Correct ArUco marker printed (DICT_4X4_50 / ID 0)
 * [ ] Camera and YOLO inference tested
 * [ ] Elevated wheel spin tests completed
 * [ ] Physical emergency stop confirmed operational
 * [ ] Floor test area cleared
 * [ ] Web server functional (if deployed)
38. Recommended Operating Procedure
1. Power ON vehicle & Jetson Orin
   └─► 2. Verify hardware interfaces (RealSense / ESP32)
        └─► 3. Launch Web Server or Terminal Session
             └─► 4. Establish smartphone client connection
                  └─► 5. Position ArUco target
                       └─► 6. Issue START command
                            └─► 7. Monitor performance
                                 └─► 8. Issue STOP command
                                      └─► 9. Power down

39. Emergency Procedure
In case of abnormal physical behavior:
 * PRIMARY: Actuate the physical battery/power cutoff switch immediately.
 * SECONDARY: Issue terminal interjection (Ctrl+C) or tap STOP on the web dashboard.
 * Perform diagnostics on motor drivers and serial logs prior to restarting.
40. Final System
PHONE (Wi-Fi Dashboard)
        │
        ▼
   JETSON ORIN
 ┌──────────────────────────────────────┐
 │  rover_web_server.py                 │
 │     └─► main_robot_controller.py     │
 │            ├─► RealSense RGB/Depth   │
 │            ├─► Vision (ArUco/YOLO)   │
 │            └─► Navigation Logic      │
 └──────────────────┬───────────────────┘
                    │ Serial 115200
                    ▼
                  ESP32 ──► Motor Driver ──► 4-Wheel Rover

41. Important Design Principle
Keep core driving routines modular:
This structure ensures physical debugging capability directly on the robot even if network connectivity or web serving breaks down.
42. Quick Start
# Start Web Server Workflow
cd ~/rover
source venv/bin/activate
python3 rover_web_server.py

# Open browser at http://<JETSON_IP>:8080 and click START

# Direct Command Line Workflow (Without Web Interface)
cd ~/rover
source venv/bin/activate
python3 main_robot_controller.py

Project Metadata Summary:
 * Repository: obstacle-avoidance-prototype
 * Target Hardware: Jetson Orin & ESP32 Motor Controller
 * Default Target Marker: DICT_4X4_50 (ID: 0)
 * Baud Rate: 115200
 * Default Web Server Port: 8080

