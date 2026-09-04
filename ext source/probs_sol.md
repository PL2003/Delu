# BYPASSING BATTERY HEALTH 
bypass battery health checks and prevent your faulty power module from blocking arming, you must disable both the **Battery Pre-Arm Checks** and the **Battery Failsafes** in ArduPilot via QGroundControl.

> **Warning:** Disabling battery checks means ArduPilot cannot monitor your battery voltage or current in flight. The flight controller will not alert you or automatically Return-To-Launch (RTL) when the LiPo is low. Use a standalone LiPo voltage alarm / buzzer plugged directly into your battery balance lead.

---

### Step 1: Disable Battery Failsafes

1. Connect your flight controller to **QGroundControl**.
2. Go to **Vehicle Setup** (Gear Icon) $\rightarrow$ **Parameters**.
3. Search for **`BATT_FS_LOW_ACT`** (Low Battery Action).
* Change value to **`0`** (Disabled).


4. Search for **`BATT_FS_CRT_ACT`** (Critical Battery Action).
* Change value to **`0`** (Disabled).



---

### Step 2: Disable Battery Monitor Hardware Pin

Setting the battery monitor to `0` stops ArduPilot from reading inputs from the power module sensing pins:

1. In **Parameters**, search for **`BATT_MONITOR`**.
2. Change its value to **`0`** (Disabled).

---

### Step 3: Remove Battery Check from Pre-Arm Checklist

To ensure ArduPilot doesn't require battery voltage data during system boot checks:

1. Search for **`ARMING_CHECK`**.
2. If using the bitmask menu in QGroundControl, **uncheck "Battery"** (or subtract `2` from the numerical bitmask value).
3. If you want to keep all other safety checks active (GPS, Compass, RC, INS), setting **`ARMING_CHECK = 1`** alongside **`BATT_MONITOR = 0`** will automatically ignore battery checks while keeping other hardware checks intact.

---

### Step 4: Save and Reboot

1. Click **Save / Write** for all modified parameters.
2. Power cycle the flight controller (unplug and replug the battery/USB).

---

### Verification Checklist

| Parameter | Recommended Value | Purpose |
| --- | --- | --- |
| **`BATT_MONITOR`** | `0` | Disables analog ADC readings from power module |
| **`BATT_FS_LOW_ACT`** | `0` | Disables low voltage action trigger |
| **`BATT_FS_CRT_ACT`** | `0` | Disables critical voltage action trigger |
| **`ARMING_CHECK`** | Uncheck *Battery* | Removes voltage/current checks from pre-arm gate |

# ALTERNATIVES FOR BATTERY MONITOR

Depending on whether you want **standalone hardware alerts** on the drone or **voltage telemetry back to ArduPilot**, here are the best low-cost alternatives to replace a faulty flight controller power module.

---

### Option 1: Standalone LiPo Low Voltage Alarm (BX100 / "Buzzer Board")

A simple plug-and-play module that plugs directly into the LiPo battery's **balance lead**.

| Feature | Details |
| --- | --- |
| **Cost** | Extremely Low ($\sim \$1.50 - \$3.00$) |
| **Connection** | Plugs into the white 3S/4S balance plug of your battery |
| **FC Connection** | None (Operates completely independently) |

* **Pros:**
* **Ultra Low Cost:** Dirt cheap and available at almost every hobby shop.
* **Individual Cell Monitoring:** Measures every cell individually, not just total pack voltage.
* **Super Loud:** Dual 95dB buzzers that you can hear easily from 50–100 meters away in flight.
* **Adjustable Threshold:** Push-button lets you set trigger voltage from $2.7\text{V}$ to $3.8\text{V}$ per cell (default $3.3\text{V}$).


* **Cons:**
* **No Telemetry:** ArduPilot/QGroundControl will not see battery voltage on-screen.
* **Range Limited:** You must rely on hearing the audible beep while flying nearby.



---

### Option 2: Custom Resistor Voltage Divider (To FC Analog ADC)

If you still want **real-time voltage telemetry in QGroundControl** without paying for a new power module, build a simple 2-resistor voltage divider to send a scaled signal ($0–3.3\text{V}$) directly to an unused ADC pin on your flight controller.

| Component | Values (For 3S/4S LiPo) |
| --- | --- |
| **Resistor $R_1$** | $10\text{ k}\Omega$ |
| **Resistor $R_2$** | $1\text{ k}\Omega$ |
| **Output Pin** | Flight Controller Analog Voltage Pin (e.g., `VOLT_SENS` or `ADC` pin) |

$$\text{Output Voltage} = V_{\text{Battery}} \times \left( \frac{R_2}{R_1 + R_2} \right)$$

* **Pros:**
* **Near Zero Cost:** Costs pennies in basic resistors.
* **Direct QGC Telemetry:** Restores live battery voltage display and voice alerts in QGroundControl.


* **Cons:**
* **No Current Sensing:** Measures voltage only (no current/mAH consumption tracking).
* **Requires Soldering:** Needs basic soldering skills and careful insulation to avoid shorting battery power to the $3.3\text{V}$ ADC pin.



---

### Option 3: I2C Power Monitor Module (INA219 / INA228)

An external digital power monitoring breakout board connected via the **I2C bus** (SCL/SDA) on your flight controller.

| Feature | Details |
| --- | --- |
| **Cost** | Low ($\sim \$3.00 - \$8.00$) |
| **Interface** | I2C (SCL, SDA, $5\text{V}$, GND) |
| **ArduPilot Setting** | `BATT_MONITOR = 7` (SWR / INA219 / I2C Digital) |

* **Pros:**
* **Digital Accuracy:** Eliminates analog noise and doesn't require complex calibration.
* **Voltage & Current:** Measures both total voltage and current draw over I2C.


* **Cons:**
* **Current Limit (INA219):** Standard INA219 modules feature a $0.1\,\Omega$ shunt resistor limited to $\sim 3.2\text{A}$ continuous. For high-current drones ($>30\text{A}$), you must replace the shunt resistor or use a drone-specific I2C module (e.g., Matek INA228/I2C-INA-BM).



---

### Recommendation

1. **Easiest & Fastest Fix:** Get a **BX100 LiPo Buzzer Alarm**. Plug it into your balance port, set it to $3.5\text{V/cell}$, and fly safely without relying on QGroundControl.
2. **Best for QGroundControl Telemetry:** Build a **Resistor Voltage Divider** on a spare analog pin, set `BATT_MONITOR = 4`, and calibrate the divider multiplier in QGC.

# Fixing Tilting while lifting

When a drone lifts up unevenly or pulls to one side during takeoff, the flight controller is applying uneven power across the motors. This issue stems from one of four primary sources: software level calibration, transmitter stick centering, mechanical frame issues, or ground effect turbulence.

---

### Step 1: Accelerometer Calibration (Most Common)

If the flight controller's internal sensor (IMU/accelerometer) believes the drone is tilted when it is sitting flat, it will immediately try to "correct" its position by pushing hard to one side.

1. Place the drone on a **100% level surface** (use a bubble level or phone level app).
2. Connect to your ground control software (QGroundControl or Mission Planner).
3. Go to **Mandatory Hardware $\rightarrow$ Accelerometer Calibration**.
4. Run the level calibration procedure and restart the drone.

---

### Step 2: Radio Transmitter Stick Calibration

If your transmitter's pitch or roll stick centers at a value slightly off from $1500\,\mu\text{s}$ (e.g., $1530\,\mu\text{s}$), the drone interprets your neutral stick as a command to roll or pitch.

1. Go to **Radio Setup / Calibration** in QGroundControl.
2. Ensure your Roll and Pitch sticks rest **exactly at 1500** when centered.
3. Re-run stick calibration if the center points are off.
4. Verify sub-trims on your transmitter (FlySky) are centered at zero.

---

### Step 3: Physical & Mechanical Checks

* **Motor Mount Tilt:** Ensure all 4 arm mounts and motor bases are completely perpendicular to the frame. A single motor tilted by even $2^{\circ}$ or $3^{\circ}$ will generate side-thrust and pull the drone horizontally.
* **Center of Gravity (CoG):** Lift the drone by the center top plate with your fingers. If it sags heavily toward one arm, shift your main LiPo battery position to balance the weight evenly.
* **Propeller & Motor Condition:** Inspect all propellers for subtle bends or cracks. Verify that all four motors spin smoothly by hand with equal resistance.

---

### Step 4: Rule Out Ground Effect (Takeoff Technique)

When lifting off very slowly near the ground (under $1\text{ ft} / 30\text{ cm}$), the air bouncing off the floor creates chaotic turbulence known as **Ground Effect**.

* **Fix:** Do not creep up slowly off the floor. Give a clean, decisive throttle pop to raise the drone $2–3\text{ feet}$ ($1\text{ meter}$) into clean air immediately, then check if the drift persists in a hover.

---

### Step 5: Trim Fine-Tuning in ArduPilot

If the drone is physically balanced and calibrated but still drifts slightly in manual hover modes (Stabilize / AltHold):

* Connect to QGroundControl $\rightarrow$ **Parameters**.
* Adjust **`AHRS_TRIM_X`** (Roll) or **`AHRS_TRIM_Y`** (Pitch) in tiny increments ($\pm 0.005$ to $0.01$ radians) to counteract the steady drift.
