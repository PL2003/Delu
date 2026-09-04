# 🚁 Mission Planner Beginner User Manual

> **A complete, step-by-step guide for absolute beginners using ArduPilot's Mission Planner Ground Control Station**

---

## 📑 Table of Contents

1. [Introduction](#1-introduction)
2. [Installation & Connection](#2-installation--connection)
3. [Initial Setup Walkthrough](#3-initial-setup-walkthrough)
4. [Flight Data Screen](#4-flight-data-screen)
5. [Flight Plan Screen](#5-flight-plan-screen)
6. [All Flight Modes Explained](#6-all-flight-modes-explained)
7. [MAVLink Commands & Actions](#7-mavlink-commands--actions)
8. [Step-by-Step First Flight Procedure](#8-step-by-step-first-flight-procedure)
9. [Troubleshooting & Tips](#9-troubleshooting--tips)
10. [Glossary](#10-glossary)

---

## 1. Introduction

### What Is Mission Planner?

**Mission Planner (MP)** is a free, open-source **Ground Control Station (GCS)** software created by Michael Oborne. It is the most widely used and feature-rich GCS for the **ArduPilot** autopilot ecosystem. Think of it as the "mission control center" on your laptop — it lets you talk to, configure, monitor, and command your drone (or other vehicle) before, during, and after flight.

### What Can You Do With It?

- ✅ Flash firmware onto your flight controller (e.g., Pixhawk)
- ✅ Calibrate sensors, radio, and ESCs
- ✅ Plan autonomous missions with waypoints on a map
- ✅ Monitor real-time telemetry (battery, GPS, altitude, speed)
- ✅ Download and analyze flight logs
- ✅ Run simulations (SITL) without real hardware
- ✅ Configure flight modes, failsafes, and safety settings

### Supported Vehicles

Mission Planner works with **all ArduPilot vehicle types**:

| Vehicle | Description |
|---------|-------------|
| 🚁 **Copter** | Multirotors (quad, hex, octo), traditional helicopters |
| ✈️ **Plane** | Fixed-wing aircraft, flying wings, VTOL (QuadPlanes) |
| 🚗 **Rover** | Ground vehicles, boats, sailboats, balance bots |
| 🤿 **Sub** | Underwater ROVs |
| 🎈 **Blimp** | Airships |
| 📡 **AntennaTracker** | Ground-based antenna tracking systems |

> **Note:** Mission Planner runs natively on **Windows**. It can run on macOS and Linux using **Mono**, but Windows is strongly recommended for best compatibility.

---

## 2. Installation & Connection

### 2.1 Download & Install

1. Visit the official download page: `https://ardupilot.org/planner/docs/mission-planner-installation.html`
2. Download the latest stable installer (`MissionPlanner-x.x.x.msi`).
3. Run the installer and follow the prompts.
4. If Windows warns about an unsigned driver, click **"Install anyway"** — this is normal for the USB drivers.
5. Launch Mission Planner from your Start Menu or Desktop.

### 2.2 Connect to Your Flight Controller

You can connect in two ways:

#### 🔌 USB Connection (Wired)

1. **Remove propellers** ⚠️ (safety first!).
2. Connect your flight controller (e.g., Pixhawk) to your PC using a **USB cable**.
3. In Mission Planner, look at the **top-right corner**.
4. Click the **COM Port** dropdown and select the port that appears (e.g., `COM3` or `COM4`).
5. Set the **Baud Rate** to `115200`.
6. Click the **Connect** button.
7. Wait for the progress bar to fill. You should hear a "connected" tone.

#### 📡 Telemetry Connection (Wireless)

1. Plug your **ground telemetry module** into your PC via USB.
2. Power on your vehicle (battery connected).
3. Select the COM port for the telemetry module.
4. Set Baud Rate to `57600` (standard for most telemetry radios).
5. Click **Connect**.

> **💡 Tip:** If the COM port doesn't appear, you may need to install **CP210x** or **FTDI drivers** for your telemetry radio.

---

## 3. Initial Setup Walkthrough

> ⚠️ **CRITICAL SAFETY WARNING**
> **REMOVE ALL PROPELLERS** before performing any setup or calibration. Motors can spin unexpectedly and cause serious injury.

The **Initial Setup** tab (top menu) contains everything you need to prepare your vehicle for flight. Follow these steps in order.

### 3.1 Install Firmware

1. Go to **SETUP → Install Firmware**.
2. **Disconnect** Mission Planner from the autopilot (click the **Disconnect** button).
3. Select your vehicle type from the icons:
   - 🚁 Copter
   - ✈️ Plane
   - 🚗 Rover
   - 🤿 Sub
4. Click the icon. Mission Planner will download and flash the latest stable firmware.
5. Wait for the "Upload Complete" message. The board will reboot automatically.

> **Note:** If your board has no firmware at all, you may need to use a different method first. See ArduPilot's "Loading Firmware" docs for details.

### 3.2 Frame Type / Configuration

1. Go to **SETUP → Mandatory Hardware → Frame Type** (Copter only).
2. Select your frame configuration:
   - **X** (most common for quads)
   - **+** (plus configuration)
   - **H** (H-frame)
   - **V** (V-tail)
   - Or select a specific frame from the dropdown.
3. Click **Save**.

### 3.3 Accelerometer Calibration

1. Go to **SETUP → Mandatory Hardware → Accel Calibration**.
2. Click **Calibrate Accel**.
3. Follow the on-screen prompts to hold your vehicle in each position:
   - Level
   - Left side down
   - Right side down
   - Nose down
   - Nose up
   - Upside down
   - (Some boards also require "Back" position)
4. Click **Done** when finished.

> **💡 Tip:** Place the vehicle on a flat, stable surface for the "Level" step. Even a slight tilt will affect flight performance.

### 3.4 Compass Calibration

1. Go to **SETUP → Mandatory Hardware → Compass**.
2. Ensure your compass is enabled. Most flight controllers have an internal compass; external GPS/compass modules are preferred.
3. Click **Start** under **Onboard Mag Calibration**.
4. You will hear a single tone, then short beeps once per second.
5. **Rotate the vehicle slowly** so that each side (front, back, left, right, top, bottom) points toward the ground for a few seconds each.
6. Do at least **6 full rotations**, pointing a different side down each time.
7. When complete, you'll hear **three rising tones**.
8. A window will prompt you to **reboot the autopilot**. Do so.

> ⚠️ **WARNING:** Do NOT calibrate near computers, metal desks, phones, or power supplies. These cause magnetic interference and bad calibration.

> **💡 Tip:** If calibration fails repeatedly, try moving outdoors away from metal objects, or lower the "Fitness" setting to "Relaxed."

### 3.5 Radio Control (RC) Calibration

1. Go to **SETUP → Mandatory Hardware → Radio Calibration**.
2. Turn on your **RC transmitter**.
3. Ensure **battery is disconnected** and **propellers are removed**.
4. Click the green **Calibrate Radio** button.
5. Move **all sticks, switches, and knobs** to their full limits.
6. Red lines will appear showing the min/max values.
7. Click **Click when Done**.
8. When prompted, **center all sticks** and move **throttle to zero**.
9. Click **OK**.
10. Verify the summary shows values around **1100 (min)** and **1900 (max)**.

**Standard Channel Mapping (Mode 2 transmitter):**

| Channel | Control | Stick |
|---------|---------|-------|
| Ch 1 | Roll | Right stick, left/right |
| Ch 2 | Pitch | Right stick, up/down |
| Ch 3 | Throttle | Left stick, up/down |
| Ch 4 | Yaw | Left stick, left/right |
| Ch 5 | Flight Mode | 3-position switch |
| Ch 6 | Tuning | Knob (Copter) |
| Ch 7-12 | Auxiliary functions | Switches |

### 3.6 ESC Calibration (Copter Only)

> ⚠️ **WARNING:** Propellers MUST be removed. Motors will spin during this process.

1. Go to **SETUP → Mandatory Hardware → ESC Calibration**.
2. Click **Start**.
3. Unplug and re-plug the **battery**.
4. Wait for the ESCs to beep. All ESCs should emit the same tones.
5. When complete, move the throttle stick to verify all motors start and stop at the same time.
6. Unplug the battery to exit test mode.

> **Note:** If using **DShot** ESCs, this step is not required. DShot ESCs are configured in ArduPilot parameters instead.

### 3.7 Servo Output Configuration

1. Go to **SETUP → Mandatory Hardware → Servo Output**.
2. Verify each output is assigned to the correct function:
   - Motor 1, Motor 2, etc. (for multirotors)
   - Aileron, Elevator, Throttle, Rudder (for planes)
3. Default values are loaded with firmware, but double-check them.

### 3.8 Flight Modes Setup

1. Go to **SETUP → Mandatory Hardware → Flight Modes**.
2. Use your transmitter's **3-position switch** (Channel 5 by default on Copter).
3. Assign a flight mode to each switch position.
4. **Recommended beginner setup for Copter:**

| Switch Position | Flight Mode | Why |
|-----------------|-------------|-----|
| Low | **Stabilize** | Manual control with self-leveling |
| Middle | **Alt Hold** | Holds altitude automatically |
| High | **Loiter** | Holds position and altitude (GPS required) |

5. Click **Save Modes**.

> **💡 Tip:** Always keep **Stabilize** or **Alt Hold** on one position. These are your "safe" manual modes if GPS fails.

### 3.9 Failsafe Configuration

Failsafes protect your vehicle if something goes wrong.

1. Go to **SETUP → Mandatory Hardware → Failsafe** (or find it under your vehicle's docs).
2. Configure these critical failsafes:

**Radio Failsafe (FS_THR_ENABLE):**
- Set to `Enabled Always RTL` or `Enabled Continue with Mission in Auto Mode`
- This triggers if the RC transmitter signal is lost.

**Battery Failsafe (BATT_FS_LOW_ACT):**
- Set to `RTL` or `Land`
- Triggers when battery voltage drops below safe levels.

**GCS Failsafe (FS_GCS_ENABLE):**
- Set to `Enabled Always RTL`
- Triggers if Mission Planner loses connection to the vehicle.

> ⚠️ **WARNING:** Test failsafes in a simulator or at very low altitude before relying on them.

### 3.10 Battery Monitor Setup

1. Go to **SETUP → Optional Hardware → Battery Monitor**.
2. Select your battery monitor type (e.g., `Analog Voltage and Current` for most Pixhawk boards).
3. Enter the correct **Voltage Divider** and **Amps Per Volt** values for your hardware.
4. Set **Low Voltage** and **Critical Voltage** thresholds.
5. Click **Write** to save.

> **💡 Tip:** Common values for Pixhawk 2.4.8: Voltage Divider ≈ `10.1`, Amps Per Volt ≈ `17.0`. Check your specific hardware documentation.

### 3.11 GPS Configuration

1. Go to **SETUP → Optional Hardware → GPS Inject** (or check GPS status in the Flight Data screen).
2. Ensure your GPS module is connected to the correct UART port.
3. In the **CONFIG → Full Parameter List**, verify:
   - `GPS_TYPE` = `1` (Auto) or your specific GPS type
   - `GPS_SBAS_MODE` = `2` (EGNOS/WAAS/MSAS if available in your region)
4. Wait for a **3D Fix** (shown in the HUD) before flying.

---

## 4. Flight Data Screen

The **Flight Data** screen is your "virtual cockpit." Click the **FLIGHT DATA** tab at the top to open it.

### 4.1 Heads-Up Display (HUD)

The **HUD** is the artificial horizon in the center. It shows:

| Element | What It Shows |
|---------|---------------|
| Artificial Horizon | Pitch and roll attitude |
| Compass Heading | Direction the vehicle is facing (0° = North) |
| Altitude | Height above home (meters) |
| Airspeed / Ground Speed | How fast the vehicle is moving |
| Battery Voltage | Current battery level |
| GPS Status | Number of satellites and fix type |
| Flight Mode | Current active mode |
| Arm Status | Armed or Disarmed |

### 4.2 Telemetry Data

On the left side, you'll see real-time data:
- **Dist to WP:** Distance to next waypoint
- **WP Dist:** Same as above
- **Alt:** Current altitude
- **GS:** Ground speed
- **AS:** Airspeed (planes)
- **Nav Pitch / Roll:** Target attitude
- **Sonar Range:** Rangefinder distance (if equipped)

### 4.3 Map

The map shows:
- Your vehicle's current position (colored icon)
- Home position ("H" marker)
- Waypoints (if a mission is loaded)
- Flight path trace (breadcrumb trail)

**Map Controls:**
- Left-click and drag to pan
- Scroll wheel to zoom
- Right-click for options (Measure Distance, Set Home Here, etc.)

### 4.4 Actions Tab

The **Actions** tab (bottom-left) lets you send commands:

| Button | Function |
|--------|----------|
| **Arm / Disarm** | Enable or disable motors |
| **Takeoff** | Command an automatic takeoff (Copter) |
| **Land** | Command immediate landing |
| **RTL** | Trigger Return to Launch |
| **Loiter** | Hold current position |
| **Auto** | Start executing the loaded mission |
| **Guided** | Enter Guided mode (click on map to send vehicle there) |

> **💡 Tip:** You can also right-click on the map and select **"Fly to Here"** to send the vehicle to a specific point in Guided mode.

### 4.5 Messages Tab

Shows text messages from the autopilot:
- Pre-arm checks
- Errors and warnings
- Mode changes
- GPS status updates

**Common messages:**
- `PreArm: Need 3D Fix` — Wait for GPS before arming
- `PreArm: Compass not calibrated` — Calibrate compass first
- `EKF variance` — Position estimation is uncertain; do not fly

### 4.6 Status Tab

Displays raw parameter values in real time. Useful for debugging.

### 4.7 Gauges Tab

Shows analog-style gauges for:
- Battery voltage
- Current draw
- RPM (if equipped)
- Servo positions

### 4.8 Logs Tab

- **Download Logs:** Retrieve DataFlash logs from the autopilot's SD card
- **Review Logs:** Open `.bin` files to analyze past flights
- **Create KML + GPX:** Export flight paths for Google Earth

---

## 5. Flight Plan Screen

The **Flight Plan** screen is where you create autonomous missions. Click the **FLIGHT PLAN** tab.

### 5.1 Basic Waypoint Mission

1. Find your area on the map (zoom and pan).
2. **Right-click** on the map where you want a waypoint.
3. Select **"Add Waypoint"** or simply **left-click** on the map.
4. A new waypoint appears in the list on the right.
5. Set the **Default Alt** (e.g., `50` meters).
6. Choose altitude type:
   - **Relative:** Height above home position (recommended for beginners)
   - **Absolute:** Height above sea level (ASL)
   - **Terrain:** Height above ground (requires terrain data)
7. Add more waypoints by clicking on the map.
8. Click **Write** to upload the mission to the autopilot.
9. Click **Read** to download the mission from the autopilot.

**Waypoint List Columns:**

| Column | Description |
|--------|-------------|
| # | Waypoint number |
| Command | Action at this point (WAYPOINT, TAKEOFF, LAND, etc.) |
| Lat | Latitude |
| Long | Longitude |
| Alt | Altitude |
| Delay | Wait time at waypoint (seconds) |

### 5.2 Survey / Grid Missions

For mapping and photography, Mission Planner can auto-generate "lawnmower" patterns.

1. **Right-click** on the map.
2. Select **Draw Polygon → Add Polygon Point**.
3. Click multiple points to outline the area you want to survey.
4. Close the polygon by clicking the first point again.
5. **Right-click** inside the polygon.
6. Select **Auto WP → Survey (Grid)**.
7. A dialog opens. Set:
   - **Altitude:** Flying height
   - **Camera:** Select your camera model (or skip)
   - **Overlap:** Front and side overlap percentage (e.g., 75%)
   - **Spacing:** Distance between flight lines
8. Click **Accept**. Mission Planner generates the grid waypoints automatically.
9. Click **Write** to upload.

> **💡 Tip:** Check **"Verify Height"** to automatically adjust waypoint altitudes based on terrain elevation. This prevents crashing into hills!

### 5.3 Rally Points

Rally points are alternative "safe landing" locations.

1. In the **FLIGHT PLAN** screen, select **Rally** from the dropdown (top-right of map).
2. **Right-click** on the map and select **"Add Rally Point"**.
3. Rally points are used if RTL is triggered far from home — the vehicle goes to the nearest rally point instead.
4. Click **Write** to save.

> **Note:** Rally points are primarily used by **Plane**. Copter typically returns directly to home.

### 5.4 Geofence

A geofence creates a virtual boundary. If the vehicle crosses it, a failsafe action triggers (usually RTL or Land).

**For Copter / Rover:**
1. In **FLIGHT PLAN**, select **Fence** from the dropdown.
2. Click the **Draw Polygon** icon (top-left of map).
3. Click points to draw a boundary.
4. Select **"Fence Inclusion"** (stay inside) or **"Fence Exclusion"** (stay outside).
5. You can also add a **Circular Fence** by left-clicking and setting a radius.
6. Click **Write** to upload.

**For Plane:**
1. Draw a polygon on the map.
2. **Right-click** and select **Geo-Fence → Upload**.
3. Set a **Return Location** inside the fence.

**Configure Fence Behavior:**
1. Go to **CONFIG → GeoFence**.
2. Set **Type:**
   - `1` = Altitude only
   - `2` = Circle only
   - `3` = Polygon only
   - `4` = Altitude + Circle
   - `7` = All types
3. Set **Action:** `1` (Report only) or `0` (RTL or Land).

> ⚠️ **WARNING:** Always test geofences at low altitude first. A misconfigured fence can cause unexpected RTL behavior.

### 5.5 Advanced Mission Commands

Mission Planner supports many command types. Click the **Command** dropdown in any waypoint row:

| Command | Purpose |
|---------|---------|
| **WAYPOINT** | Fly to this location |
| **TAKEOFF** | Climb to altitude (first command for Copter missions) |
| **LAND** | Descend and land at this location |
| **RTL** | Return to launch position |
| **LOITER_TIME** | Circle a point for X seconds |
| **LOITER_TURNS** | Circle a point for X turns |
| **DO_JUMP** | Jump to another waypoint (for loops) |
| **DO_SET_SERVO** | Move a servo to a specific PWM value |
| **DO_DIGICAM_CONTROL** | Trigger camera shutter |
| **DO_SET_ROI** | Point camera at a Region of Interest |

---

## 6. All Flight Modes Explained

Flight modes determine how your vehicle behaves. You switch between them using your transmitter or Mission Planner.

### 🚁 Copter Flight Modes

| Mode | Abbreviation | What It Does | GPS Needed? | Beginner Safe? |
|------|-------------|--------------|-------------|----------------|
| **Stabilize** | STABILIZE | Self-levels roll and pitch. Pilot controls throttle manually. | No | ✅ Yes |
| **Altitude Hold** | ALT_HOLD | Self-levels + holds altitude automatically. Pilot controls direction. | No | ✅ Yes |
| **Loiter** | LOITER | Holds position AND altitude using GPS. Stays in one spot. | Yes | ✅ Yes |
| **Position Hold** | POSHOLD | Like Loiter, but more manual control feel. Drifts when sticks moved. | Yes | ✅ Yes |
| **Return to Launch** | RTL | Flies back to takeoff point and lands automatically. | Yes | ✅ Yes |
| **Auto** | AUTO | Follows the uploaded mission waypoints automatically. | Yes | ⚠️ Experienced |
| **Land** | LAND | Descends straight down and disarms. | Optional | ✅ Yes |
| **Guided** | GUIDED | Goes to a point commanded by the GCS (click on map). | Yes | ⚠️ Experienced |
| **Circle** | CIRCLE | Circles a point in front of the vehicle. | Yes | ⚠️ Experienced |
| **Sport** | SPORT | Altitude hold + rate control on roll/pitch. More agile than Alt Hold. | No | ❌ No |
| **Acro** | ACRO | No self-leveling. Rate control only. For acrobatics. | No | ❌ No |
| **Drift** | DRIFT | Like Stabilize but yaw coordinates with roll (plane-like feel). | Yes | ⚠️ Experienced |
| **Flip** | FLIP | Automated flip maneuver. | No | ❌ No |
| **Brake** | BRAKE | Stops immediately and holds position. | Yes | ✅ Yes |
| **Smart RTL** | SMART_RTL | Returns by retracing its flight path (not direct line). | Yes | ✅ Yes |
| **AutoTune** | AUTOTUNE | Automatically tunes PID values while flying. | Yes | ⚠️ Experienced |
| **Throw** | THROW | Arms when thrown into the air. | Yes | ❌ No |
| **FlowHold** | FLOWHOLD | Holds position using optical flow (no GPS). | Optical Flow | ⚠️ Experienced |
| **Follow** | FOLLOW | Follows another vehicle. | Yes | ⚠️ Experienced |
| **ZigZag** | ZIGZAG | Automated back-and-forth pattern for spraying. | Yes | ⚠️ Experienced |
| **System ID** | SYSID | Used for system identification (advanced). | Yes | ❌ No |

### ✈️ Plane Flight Modes

| Mode | What It Does | GPS Needed? |
|------|-------------|-------------|
| **MANUAL** | Full manual control. No stabilization. | No |
| **STABILIZE** | Self-leveling on stick release. Manual throttle. | No |
| **FBWA** (Fly By Wire A) | Roll and pitch follow stick input up to set limits. | No |
| **FBWB** (Fly By Wire B) | Like FBWA but with automatic altitude and speed control. | Yes |
| **CRUISE** | Like FBWB but tracks ground course automatically. | Yes |
| **ACRO** | Rate control, no attitude limits. | No |
| **TRAINING** | Manual control up to roll/pitch limits. | No |
| **AUTO** | Follows mission waypoints. | Yes |
| **LOITER** | Circles the point where mode was switched. | Yes |
| **CIRCLE** | Gently turns in a circle. | No |
| **RTL** | Returns to home and circles. | Yes |
| **TAKEOFF** | Automatic takeoff to set altitude. | Yes |
| **LAND** | Automatic landing sequence. | Yes |
| **GUIDED** | Flies to GCS-commanded point. | Yes |
| **AUTOTUNE** | Learns attitude tuning while flying. | Yes |
| **THERMAL** | Searches for thermal lift (gliders). | Yes |
| **AUTOLAND** | Fixed-wing autoland sequence. | Yes |
| **QSTABILIZE / QHOVER / QLOITER** | VTOL modes (quadplane hover modes). | Varies |

### 🚗 Rover Flight Modes

| Mode | What It Does |
|------|-------------|
| **MANUAL** | Full manual control. |
| **ACRO** | Rate-controlled turns. |
| **STEERING** | Steering with speed control. |
| **HOLD** | Stops and holds position. |
| **LOITER** | Holds position (boats). |
| **AUTO** | Follows waypoints. |
| **RTL** | Returns to start point. |
| **GUIDED** | Goes to GCS-commanded point. |
| **SMART_RTL** | Retraces path home. |
| **FOLLOW** | Follows another vehicle. |

---

## 7. MAVLink Commands & Actions

**MAVLink** is the communication protocol between Mission Planner and your flight controller. Here are the most common commands you can send.

### 7.1 Navigation Commands (NAV_*)

| Command | Description | Parameters |
|---------|-------------|------------|
| **NAV_TAKEOFF** | Take off to specified altitude | Altitude |
| **NAV_WAYPOINT** | Fly to location | Lat, Lon, Alt, Delay |
| **NAV_LAND** | Land at location | Lat, Lon |
| **NAV_RTL** | Return to launch | — |
| **NAV_LOITER_TIME** | Loiter for X seconds | Time, Radius |
| **NAV_LOITER_TURNS** | Loiter for X turns | Turns, Radius, Direction |
| **NAV_SPLINE_WAYPOINT** | Smooth curved path to waypoint | Lat, Lon, Alt |
| **NAV_DELAY** | Wait until specific time | Hour, Min, Sec |

### 7.2 DO Commands (Actions)

| Command | Description |
|---------|-------------|
| **DO_JUMP** | Jump to another waypoint (for repeating missions) |
| **DO_CHANGE_SPEED** | Change target speed |
| **DO_SET_HOME** | Set a new home location |
| **DO_SET_SERVO** | Set a servo to a specific PWM value |
| **DO_SET_RELAY** | Turn a relay on/off |
| **DO_REPEAT_SERVO** | Cycle a servo repeatedly |
| **DO_DIGICAM_CONTROL** | Trigger camera shutter |
| **DO_SET_CAM_TRIGG_DIST** | Trigger camera every X meters |
| **DO_SET_ROI** | Point gimbal/camera at a location |
| **DO_MOUNT_CONTROL** | Control camera mount angles |
| **DO_PARACHUTE** | Deploy parachute |
| **DO_GRIPPER** | Operate cargo gripper |
| **DO_WINCH** | Control winch |
| **DO_AUX_FUNCTION** | Trigger an auxiliary function |

### 7.3 Condition Commands

| Command | Description |
|---------|-------------|
| **CONDITION_DELAY** | Wait for X seconds before next command |
| **CONDITION_DISTANCE** | Wait until within X meters of waypoint |
| **CONDITION_YAW** | Point nose to specific heading |
| **CONDITION_CHANGE_ALT** | Change altitude at specified rate |

### 7.4 Quick-Reference: Common Actions in Mission Planner

| Action | How to Send | When to Use |
|--------|-------------|-------------|
| **Arm** | Actions tab → Arm/Disarm | Before takeoff |
| **Disarm** | Actions tab → Arm/Disarm | After landing |
| **Takeoff** | Actions tab → Takeoff | Start autonomous flight |
| **Land Now** | Actions tab → Land | Emergency landing at current position |
| **RTL** | Actions tab → RTL | Return home immediately |
| **Loiter** | Actions tab → Loiter | Hold position right now |
| **Auto** | Actions tab → Auto | Start uploaded mission |
| **Guided → Point** | Right-click map → "Fly to Here" | Send vehicle to specific point |
| **Guided → Altitude** | Actions tab → Set Alt | Change altitude in Guided mode |

---

## 8. Step-by-Step First Flight Procedure

### ✅ Pre-Flight Checklist

**Before leaving for the field:**
- [ ] Firmware flashed and configured
- [ ] All calibrations completed (Accel, Compass, Radio, ESC)
- [ ] Flight modes assigned on transmitter
- [ ] Failsafes configured and tested
- [ ] Battery monitor calibrated
- [ ] Propellers installed (correct CW/CCW direction)
- [ ] Battery fully charged
- [ ] SD card inserted in flight controller (for logging)
- [ ] Mission Planner installed on laptop
- [ ] Telemetry radio charged/paired

**At the field:**
- [ ] Survey area for obstacles, people, and restricted airspace
- [ ] Check weather (wind < 15 km/h for beginners)
- [ ] Set home position (power on vehicle at takeoff spot)
- [ ] Wait for GPS 3D Fix (at least 8 satellites)
- [ ] Verify flight mode switch works (check HUD display)
- [ ] Test radio range (walk away with transmitter)
- [ ] Verify battery voltage in HUD

### 🚀 Arming and Takeoff

1. **Place the vehicle on flat, level ground.**
2. **Power on the transmitter first** (always TX before vehicle).
3. **Connect the battery** to the vehicle.
4. Wait for the flight controller to boot up (LEDs stop flashing).
5. In Mission Planner, verify:
   - GPS: 3D Fix (green icon)
   - Battery voltage is normal
   - No red error messages in the Messages tab
6. **Switch to Stabilize or Alt Hold mode** on your transmitter.
7. **Arm the motors:**
   - **Copter:** Hold throttle stick **down and right** for 2 seconds.
   - Or use Mission Planner: **Actions → Arm/Disarm**.
8. If pre-arm checks pass, the motors will beep and the HUD shows **"Armed"**.

> ⚠️ **WARNING:** If arming fails, check the Messages tab. Common reasons: no GPS fix, compass error, throttle not at zero, or safety switch not pressed.

### 🛫 Manual Takeoff (Copter)

1. Ensure you are in **Stabilize** or **Alt Hold** mode.
2. Slowly raise the **throttle stick**.
3. The vehicle will lift off. Keep movements gentle.
4. Hover at **2-3 meters** to verify stability.
5. Test roll, pitch, and yaw response.

### 📤 Upload and Execute a Mission

1. In Mission Planner, go to **FLIGHT PLAN**.
2. Create a simple mission:
   - Waypoint 1: **TAKEOFF** to 20m
   - Waypoint 2: **WAYPOINT** 50m North
   - Waypoint 3: **WAYPOINT** 50m East
   - Waypoint 4: **RTL**
3. Click **Write** to upload to the autopilot.
4. Click **Read** to verify it uploaded correctly.
5. Arm the vehicle.
6. Switch your transmitter to **AUTO** mode.
7. The vehicle will:
   - Take off to 20m
   - Fly to each waypoint
   - Return to launch
   - Land automatically

> **💡 Tip:** For your first mission, keep the total distance under 100m and altitude under 30m.

### 🏠 Using RTL (Return to Launch)

1. At any time, switch your transmitter to **RTL** mode.
2. The vehicle will:
   - Climb to **RTL_ALT** (default 15m) if below that altitude
   - Fly directly to the home position
   - Descend and land automatically
3. In Mission Planner, you can also click **Actions → RTL**.

> ⚠️ **WARNING:** RTL flies in a straight line. Make sure there are no obstacles (trees, buildings) between the vehicle and home.

### 🛬 Landing

**Automatic Landing (Copter):**
1. Switch to **LAND** mode.
2. The vehicle descends straight down.
3. It will automatically disarm when it detects landing.

**Manual Landing:**
1. In **Alt Hold** or **Loiter**, slowly lower the throttle stick.
2. The vehicle descends.
3. When it touches down, hold throttle at minimum for 2 seconds to disarm.

> **💡 Tip:** In **Stabilize** mode, you must manually control throttle all the way to landing. This is harder for beginners — use Alt Hold or Land mode instead.

### 🔒 Post-Flight

1. Disarm the motors.
2. Disconnect the battery.
3. Turn off the transmitter.
4. In Mission Planner, go to **FLIGHT DATA → Logs**.
5. Click **Download Logs** to save your flight data.
6. Review the mission track on the map.

---

## 9. Troubleshooting & Tips

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| **"PreArm: Need 3D Fix"** | GPS not ready | Wait longer; move to open area; check GPS wiring |
| **"PreArm: Compass not calibrated"** | Bad/missing compass cal | Redo compass calibration away from metal |
| **"PreArm: Compass variance"** | Magnetic interference | Move away from metal objects; disable internal compass if external available |
| **"PreArm: Radio failsafe"** | Throttle too high or no RC signal | Lower throttle stick; check transmitter binding |
| **"PreArm: Hardware safety switch"** | Safety switch not pressed | Press and hold the safety button on the GPS module |
| **"EKF variance" / "Bad Velocity"** | Poor position estimation | Do not fly! Check GPS and compass; reboot flight controller |
| **"Bad LiDAR Health"** | Rangefinder issue | Check wiring; disable if not equipped |
| **Motors won't arm** | Multiple possible causes | Check all PreArm messages; verify throttle at zero; check arming checks parameter |
| **Vehicle drifts in Loiter** | GPS drift or compass issue | Recalibrate compass; wait for better GPS fix; check for magnetic interference |
| **Vehicle flips on takeoff** | Wrong motor order or prop direction | Check motor numbering and rotation; verify prop CW/CCW placement |
| **"No heartbeat" / disconnects** | Bad USB cable or telemetry link | Try a different USB cable; reduce telemetry radio distance; check baud rate |
| **Mission won't upload** | Wrong vehicle type or no connection | Verify connection; check firmware matches vehicle type |

### Safety Notes

> ⚠️ **ALWAYS remove propellers during setup and calibration.**

> ⚠️ **NEVER fly without a GPS 3D Fix** unless you are an expert in manual modes.

> ⚠️ **Test failsafes in a simulator or at very low altitude first.**

> ⚠️ **Keep RTL altitude higher than any obstacles** in your flight area.

> ⚠️ **Maintain visual line of sight** at all times.

> ⚠️ **Have a spotter** for your first flights.

> ⚠️ **Check local regulations** before flying. Many areas require registration or have no-fly zones.

### Pro Tips

- **Prefetch maps:** Before going to the field, go to **FLIGHT PLAN → Map Tools → Prefetch**. Hold Alt and draw a box to download map imagery for offline use.
- **Use a checklist:** Print the pre-flight checklist and use it every time.
- **Start in Stabilize/Alt Hold:** Master manual flight before using Auto mode.
- **Log everything:** Always download logs after flying. They are invaluable for diagnosing issues.
- **Simulate first:** Use Mission Planner's built-in simulator (**Ctrl+F** → Simulation) to practice missions without risk.
- **Parameter backups:** Before making major changes, go to **CONFIG → Full Parameter List → Save to File**.
- **Update regularly:** Check for Mission Planner updates to get the latest features and bug fixes.

---

## 10. Glossary

| Abbreviation | Full Name | Meaning |
|-------------|-----------|---------|
| **AHRS** | Attitude Heading Reference System | The system that tracks orientation |
| **APM** | ArduPilot Mega | Legacy name for ArduPilot hardware/software |
| **ArduPilot** | — | The open-source autopilot firmware |
| **ASL** | Above Sea Level | Altitude measured from sea level |
| **Auto** | Automatic Mode | Vehicle follows uploaded mission |
| **BATT** | Battery | Power source monitoring |
| **BEC** | Battery Eliminator Circuit | Voltage regulator for servos/RC |
| **BIN** | Binary | Flight log file format |
| **BMP** | Barometer | Pressure sensor for altitude |
| **CCW** | Counter-Clockwise | Propeller/motor rotation direction |
| **COM Port** | Communication Port | Serial port on your PC |
| **CW** | Clockwise | Propeller/motor rotation direction |
| **DFU** | Device Firmware Update | Mode for flashing bootloader |
| **DO_*** | Do Command | Action commands in missions |
| **DShot** | Digital Shot | Digital ESC protocol |
| **EKF** | Extended Kalman Filter | Algorithm that fuses sensor data for position estimation |
| **ESC** | Electronic Speed Controller | Controls motor speed |
| **FBW** | Fly By Wire | Assisted flight mode (Plane) |
| **FC** | Flight Controller | The autopilot board (e.g., Pixhawk) |
| **FFT** | Fast Fourier Transform | Used for vibration analysis |
| **Firmware** | — | Software running on the flight controller |
| **FLTMODE** | Flight Mode | Operating mode of the vehicle |
| **FS** | Failsafe | Safety system for lost signal/low battery |
| **GCS** | Ground Control Station | Software like Mission Planner |
| **GeoFence** | Geographic Fence | Virtual boundary for the vehicle |
| **GPS** | Global Positioning System | Satellite navigation |
| **GPX** | GPS Exchange Format | File format for GPS tracks |
| **GUI** | Graphical User Interface | The visual interface of software |
| **HDOP** | Horizontal Dilution of Precision | GPS accuracy indicator (lower is better) |
| **HUD** | Heads-Up Display | The artificial horizon display |
| **IMU** | Inertial Measurement Unit | Accelerometer + gyroscope sensor |
| **KML** | Keyhole Markup Language | Google Earth file format |
| **LED** | Light Emitting Diode | Status lights on the flight controller |
| **Loiter** | — | Hold position and altitude |
| **MAV** | Micro Air Vehicle | Term for small drones/UAVs |
| **MAVLink** | Micro Air Vehicle Link | Communication protocol |
| **MP** | Mission Planner | This software |
| **MSL** | Mean Sea Level | Same as ASL |
| **NAV_*** | Navigation Command | Movement commands in missions |
| **OSD** | On-Screen Display | Telemetry overlay on video |
| **PID** | Proportional-Integral-Derivative | Control loop tuning parameters |
| **Pixhawk** | — | Popular flight controller hardware |
| **PWM** | Pulse Width Modulation | Signal type for servos/ESCs |
| **RC** | Radio Control | Transmitter and receiver |
| **ROI** | Region of Interest | Point for camera to focus on |
| **RTL** | Return to Launch | Fly back to takeoff point |
| **SITL** | Software In The Loop | Simulator running on PC |
| **SLCAN** | Serial Line CAN | Protocol for CAN bus devices |
| **Telemetry** | — | Wireless data link between vehicle and GCS |
| **TX** | Transmitter | Radio controller |
| **UART** | Universal Asynchronous Receiver/Transmitter | Serial communication port |
| **UAV** | Unmanned Aerial Vehicle | Drone |
| **UAVCAN** / **DroneCAN** | — | CAN bus protocol for UAV peripherals |
| **VTOL** | Vertical Take-Off and Landing | Aircraft that hovers and flies forward |
| **WP** | Waypoint | A point in a mission |
| **WPradius** | Waypoint Radius | Distance to consider a waypoint "reached" |
| **YAW** | — | Rotation around the vertical axis (left/right turn) |

---

## 📋 Quick-Reference Tables

### Flight Mode Quick Reference (Copter)

| Mode | Self-Level | Alt Hold | Pos Hold | GPS | Use Case |
|------|-----------|----------|----------|-----|----------|
| Stabilize | ✅ | ❌ | ❌ | ❌ | Learning manual flight |
| Alt Hold | ✅ | ✅ | ❌ | ❌ | First hovers |
| Loiter | ✅ | ✅ | ✅ | ✅ | Safe hovering, photography |
| PosHold | ✅ | ✅ | Partial | ✅ | Manual feel with position hold |
| RTL | ✅ | ✅ | ✅ | ✅ | Emergency return |
| Auto | ✅ | ✅ | ✅ | ✅ | Autonomous missions |
| Land | ✅ | ✅ | N/A | Optional | Automatic landing |
| Guided | ✅ | ✅ | ✅ | ✅ | GCS-directed flight |

### MAVLink Command Quick Reference

| Command Type | Examples | Purpose |
|-------------|----------|---------|
| **NAV** | WAYPOINT, TAKEOFF, LAND, RTL, LOITER | Movement and navigation |
| **DO** | SET_SERVO, DIGICAM_CONTROL, SET_ROI, JUMP | Actions and triggers |
| **CONDITION** | DELAY, DISTANCE, YAW | Timing and sequencing |

---

> **🎓 Congratulations!** You now have the knowledge to install, configure, and fly with Mission Planner. Remember: **safety first, simulate often, and fly within your limits.**
>
> For more detailed information, visit the official ArduPilot documentation: https://ardupilot.org
>
> **Happy flying! 🚁**

---

*This manual was generated for educational purposes. Always refer to the latest official ArduPilot and Mission Planner documentation for the most current procedures and safety information.*
