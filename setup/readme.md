# 🤖 Delivery Bot: ROS 2 Humble & Pi Cam Setup

## 1. System Preparation

Ensure you are using **Ubuntu 22.04 LTS (64-bit)**.

```bash
# Update System
sudo apt update && sudo apt upgrade -y

# Install essential build tools
sudo apt install -y python3-colcon-common-extensions python3-rosdep python3-argcomplete curl

```

## 2. Install ROS 2 Humble (Binary)

*No source build required. This takes 5 minutes instead of 10 hours.*

```bash
# Add ROS 2 GPG Key
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add Repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS 2 Base (Optimized for Pi)
sudo apt update
sudo apt install -y ros-humble-ros-base

# Source environment automatically
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

```

## 3. Raspberry Pi Camera Hardware Setup

Newer Ubuntu versions use the `libcamera` stack. To use the stable `v4l2` driver requested:

```bash
# Edit Boot Config
sudo nano /boot/firmware/config.txt

# Add/Ensure these lines are present at the bottom:
camera_auto_detect=1
start_x=1
disable_camera_led=1

# Reboot to apply changes
sudo reboot

```

## 4. Install & Run Camera Driver (V4L2)

We use the hardware-optimized `v4l2_camera` node.

```bash
# Install the driver package
sudo apt install -y ros-humble-v4l2-camera ros-humble-image-transport-plugins

# Run the Camera Node
ros2 run v4l2_camera v4l2_camera_node --ros-args -p image_size:=[640,480]

```

*To view images, run `ros2 run rqt_image_view rqt_image_view` on your **Laptop** (connected to the same Wi-Fi).*

## 5. Micro-ROS Setup (For ESP32/Arduino)

This bridges your Pi 4 to the motor controllers.

```bash
# Install Micro-ROS Agent via Docker (Easiest Method)
sudo apt install docker.io -y
sudo usermod -aG docker $USER
# Restart terminal after this

# Run the Agent
docker run -it --rm -v /dev:/dev --privileged --net=host microros/micro-ros-agent:humble serial --dev /dev/ttyUSB0

```

## 6. Development Workspace

Create your workspace for custom delivery logic.

```bash
mkdir -p ~/dev_ws/src
cd ~/dev_ws
colcon build

# Add workspace to bashrc
echo "source ~/dev_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc

```

---

## 🛠 Useful Commands for the Bot

| Task | Command |
| --- | --- |
| **Check Topics** | `ros2 topic list` |
| **See Camera Output** | `ros2 topic echo /image_raw` (Text only) |
| **Change Resolution** | `ros2 param set /v4l2_camera image_size [1280,720]` |
| **Check GPS (if conn)** | `ros2 run nmea_navsat_driver nmea_topic_serial_reader` |

---
