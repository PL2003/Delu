# Pixhawk 2.4.8 Flight Board User Manual

> **Scope:** This manual covers the common Pixhawk 2.4.8 / Pixhawk 1 connector layout when used with ArduPilot Copter. Many Pixhawk 2.4.8 boards are clones, so connector labels, sensors, pinouts and power circuits may differ. Always verify the board silkscreen and manufacturer schematic before applying power.

> **Safety warning:** Remove all propellers before wiring, firmware installation, calibration, motor testing or troubleshooting. Never connect flight-battery voltage directly to a Pixhawk power input unless the board documentation explicitly allows it.

***

## 1. Board Overview

Pixhawk is a real-time flight controller that:

- Reads gyroscope and accelerometer data.
- Estimates attitude, altitude and position.
- Uses GPS and compass data for navigation.
- Receives pilot commands from a radio receiver.
- Controls motors, ESCs, servos and accessories.
- Records flight data to a microSD card.
- Communicates with a ground-control station through USB or telemetry.

<img width="600" height="507" alt="PixhawkLabled" src="https://github.com/user-attachments/assets/c6150d60-b01f-408b-9a66-5a07fa28fd93" />

<img width="1377" height="1837" alt="Pixhawk-Inforgraphic2" src="https://github.com/user-attachments/assets/fc354b68-da8d-4200-9521-c22478822804" />

The original Pixhawk design includes a 32-bit processor, redundant power inputs, multiple UART ports, PPM/S.Bus/DSM receiver inputs, I2C, SPI, CAN, ADC inputs, USB and up to 14 PWM outputs. [ardupilot](https://ardupilot.org/copter/docs/common-pixhawk-overview.html)

***

## 2. Port Functions and Connections

### 2.1 Main Port Table

| Port or Feature | Function | Connection Guide |
|---|---|---|
| `POWER` | Supplies regulated power and receives voltage/current measurements. | Connect a compatible power module. Do not connect the main battery directly to this port. |
| `MAIN OUT 1–8` | Primary motor and servo outputs. | Connect ESC signal wires to the numbered outputs according to the selected ArduPilot frame. |
| `AUX OUT 1–6` | Additional PWM outputs or configurable GPIO. | Use for gimbals, landing gear, camera triggers, relays or additional motors. |
| `RC IN` / `PPM-SUM` | PPM receiver input. | Connect receiver signal, power and ground. |
| `SBUS` | Futaba S.Bus receiver input. | Connect the receiver using the correct signal direction and configure the receiver protocol. |
| `DSM` | Spektrum DSM2/DSMX satellite receiver input. | Connect signal, ground and the specified 3.3 V supply. |
| `TELEM1` / `TELEM2` | Serial telemetry ports. | Use for telemetry radios, companion computers or other serial devices. |
| `GPS` | GPS serial port and, on the original layout, CAN2 signals. | Connect a compatible GPS module. Mount the GPS/compass away from high-current wires. |
| `SERIAL 4/5` | Two additional UART connections. | Use only after confirming the exact cable pinout. |
| `I2C` | External compass and compatible I2C peripherals. | Connect `SCL`, `SDA`, power and ground. |
| `CAN1` / `CAN2` | DroneCAN peripheral connections. | Connect CAN devices using `CAN_H`, `CAN_L`, power and ground. |
| `SPI` | High-speed peripheral bus. | Intended mainly for advanced hardware integration. |
| `ADC 3.3V` | Analog sensor inputs up to approximately 3.3 V. | Used for supported analog sensors, RSSI or rangefinders. |
| `ADC 6.6V` | Analog input with a higher voltage range. | Commonly used for analog airspeed sensors. Verify scaling before use. |
| `SWITCH` | Hardware safety switch. | Connect the Pixhawk safety button. |
| `BUZZER` | Audible status, arming and fault indications. | Connect a compatible buzzer. |
| `microSD` | Dataflash flight-log storage. | Insert the card with power removed. |
| `Micro USB` | Firmware, setup and ground-station communication. | Use a data-capable USB cable. USB is not the normal flight power source. |

Pixhawk wiring documentation identifies the safety switch and buzzer as important components for normal Pixhawk operation. [ardupilot](https://ardupilot.org/copter/docs/common-pixhawk-wiring-and-quick-start.html)

***

### 2.2 Common Serial Port Pinout

The usual original Pixhawk serial-port assignment is:

| Pin | Signal |
|---:|---|
| 1 | `+5 V` |
| 2 | `TX` |
| 3 | `RX` |
| 4 | `CTS` |
| 5 | `RTS` |
| 6 | `GND` |

Connect serial devices using crossed data lines:

```text
Pixhawk TX  → Device RX
Pixhawk RX  → Device TX
Pixhawk GND → Device GND
```

The serial signal logic is typically 3.3 V even though the port may provide a 5 V supply. Do not apply 5 V logic to signal pins unless the board documentation explicitly supports it.

***

### 2.3 GPS Port

A common original Pixhawk GPS connector uses:

| Pin | Signal |
|---:|---|
| 1 | `+5 V` |
| 2 | GPS `TX` |
| 3 | GPS `RX` |
| 4 | CAN2 `TX` |
| 5 | CAN2 `RX` |
| 6 | `GND` |

The GPS/compass module should be:

- Mounted with its arrow facing forward.
- Positioned away from motors, ESCs and battery cables.
- Kept clear of large metal parts and electromagnetic interference.
- Connected with the correct cable orientation.

***

### 2.4 I2C Port

The I2C port is commonly used for an external compass.

| Signal | Function |
|---|---|
| `+5 V` | Peripheral supply |
| `SCL` | I2C clock |
| `SDA` | I2C data |
| `GND` | Ground |

Use only compatible 3.3 V I2C devices. Do not connect an unknown 5 V sensor directly to the data lines.

***

### 2.5 CAN Port

A typical CAN connector contains:

| Signal | Function |
|---|---|
| `+5 V` | Peripheral supply |
| `CAN_H` | CAN high |
| `CAN_L` | CAN low |
| `GND` | Ground |

For DroneCAN devices:

1. Connect `CAN_H` to `CAN_H`.
2. Connect `CAN_L` to `CAN_L`.
3. Use the correct bus termination.
4. Configure the CAN protocol in ArduPilot.
5. Confirm that the peripheral is detected before flight.

***

### 2.6 PWM Outputs

#### Main Outputs

`MAIN OUT 1–8` are normally used for:

- Motors.
- ESCs.
- Primary servos.
- Conventional aircraft control surfaces.

The correct motor number and rotation direction depend on the selected frame type. Always use the motor-order diagram provided by ArduPilot rather than assuming that the outputs follow a simple clockwise sequence.

#### Auxiliary Outputs

`AUX OUT 1–6` can be assigned to:

- Camera triggers.
- Landing gear.
- Gimbals.
- Servos.
- Relays.
- Lights.
- Additional motors.
- GPIO functions.

The servo rail may require a separate BEC or power supply. Check the current rating before connecting multiple servos.

***

## 3. Wiring Procedure

Follow this sequence:

1. Remove all propellers.
2. Mount the Pixhawk near the vehicle’s center of gravity.
3. Align the board arrow with the vehicle’s forward direction.
4. Connect the compatible power module to `POWER`.
5. Connect ESC signal wires to `MAIN OUT`.
6. Connect the GPS and external compass.
7. Connect the receiver to `RC IN`, `SBUS` or `DSM`.
8. Connect the buzzer and safety switch.
9. Connect telemetry equipment if required.
10. Inspect polarity, connector orientation and ground connections.
11. Power the board through USB for the first configuration.
12. Use a current-limited battery supply for the first battery-powered test.

> **Important:** Do not power the servo rail from multiple BECs unless the power architecture has been checked. Different Pixhawk 2.4.8 clones may use different power arrangements.

***

## 4. First-Time Setup

Use Mission Planner for an ArduPilot-oriented installation.

### 4.1 Firmware and Frame Setup

1. Connect Pixhawk to the computer using USB.
2. Open Mission Planner.
3. Install the correct ArduPilot Copter firmware.
4. Select the exact frame type.
5. Set the board orientation if it is not mounted arrow-forward.
6. Reboot when requested.

### 4.2 Required Calibration

Perform the following calibrations:

- Accelerometer calibration.
- Compass calibration.
- Radio calibration.
- ESC calibration, if required by the ESC system.
- Power-monitor calibration.
- Optional airspeed or rangefinder calibration.

Compass calibration should be performed away from steel structures, speakers, batteries and high-current wiring. ArduPilot provides a dedicated compass-calibration procedure for this process. [ardupilot](https://ardupilot.org/copter/docs/common-compass-calibration-in-mission-planner.html)

### 4.3 Radio Configuration

Verify that:

- Throttle is identified correctly.
- Roll, pitch and yaw move in the correct direction.
- Flight-mode switches select the intended modes.
- Failsafe activates correctly.
- The receiver remains powered during normal operation.

If the transmitter uses a non-standard channel arrangement, configure the appropriate `RCMAP` parameters. [ardupilot](https://ardupilot.org/copter/docs/common-rcmap.html)

### 4.4 Motor Test

Perform motor testing only with the propellers removed.

Check:

- Correct motor number.
- Correct motor rotation direction.
- Correct ESC response.
- Secure motor and ESC wiring.
- No unexpected motor movement during arming.

### 4.5 Safety Switch

The safety switch prevents motors and servos from becoming active during setup. Press the switch only when:

- Propellers are removed during testing.
- The aircraft is clear of people.
- The vehicle is ready for controlled operation.

ArduPilot documents the safety switch as a mechanism for enabling or disabling motor and servo outputs. [ardupilot](https://ardupilot.org/copter/docs/common-safety-switch-pixhawk.html)

***

## 5. Vibration Measurement

Pixhawk accelerometers are sensitive to mechanical vibration. Accelerometer data is combined with barometer and GPS information to estimate vehicle position, so excessive vibration can affect altitude hold, position hold, RTL, Guided and Auto modes. [ardupilot](https://ardupilot.org/copter/docs/common-measuring-vibration.html)

### 5.1 Vibration Indicators

| Indicator | Meaning |
|---|---|
| `VibeX` | Vibration on the X axis |
| `VibeY` | Vibration on the Y axis |
| `VibeZ` | Vibration on the Z axis |
| `Clip0`, `Clip1`, `Clip2` | Accelerometer clipping counters |

### 5.2 General Interpretation

| Vibration Level | Interpretation |
|---:|---|
| Below `30 m/s²` | Generally acceptable |
| Above `30 m/s²` | May cause flight problems |
| Above `60 m/s²` | Very likely to cause position or altitude-hold problems |
| Accelerometer clipping | Should ideally remain at zero |

Check vibration in Mission Planner by selecting **Vibe** on the HUD or by reviewing the Dataflash log after flight. [ardupilot](https://ardupilot.org/copter/docs/common-measuring-vibration.html)

### 5.3 Vibration Troubleshooting

If vibration is excessive:

- Replace damaged or unbalanced propellers.
- Check motor shafts for bending.
- Inspect motor bearings.
- Tighten loose frame and arm fasteners.
- Check for cracked arms or plates.
- Inspect payloads and landing gear.
- Ensure cables do not touch the flight controller.
- Ensure cables do not pull on the flight controller.
- Check that the flight-controller mount is secure.
- Use suitable vibration isolation without allowing the board to bounce or twist.
- Repeat the same flight test and compare the logs.

Do not attempt to solve severe mechanical vibration by changing estimator parameters first. Correct the mechanical source before changing software settings.

***

## 6. Troubleshooting

| Problem | Recommended Checks |
|---|---|
| Pixhawk does not power on | Check power-module polarity, battery voltage, connector seating and 5 V output. |
| Pixhawk resets during flight | Check power-supply stability, loose connectors, BEC capacity and damaged wiring. |
| USB works but battery power does not | Check the power module, `POWER` connector and voltage-sensing configuration. |
| GPS is not detected | Check cable orientation, GPS power, serial settings, firmware configuration and sky visibility. |
| Compass is inconsistent | Move away from magnetic materials and high-current wires; use an external compass and recalibrate. |
| Receiver is not detected | Check receiver protocol, signal port, receiver power, binding and failsafe settings. |
| Motors spin in the wrong order | Recheck the frame type and motor-order diagram. |
| Pre-arm safety error appears | Press the safety button only when the vehicle is safe, or repair the switch and wiring. |
| Position hold is poor | Check GPS quality, compass setup, vibration levels, clipping and EKF status. |
| Altitude hold oscillates | Inspect vibration, propellers, frame rigidity, barometer protection and power stability. |
| One vibration axis is high | Inspect the flight-controller mount, cable tension and directional frame contact. |

ArduPilot’s pre-arm checks should be resolved rather than bypassed casually because they identify conditions that may make flight unsafe. [ardupilot](https://ardupilot.org/copter/docs/common-prearm-safety-checks.html)

***

## 7. Pre-Flight Checklist

### Mechanical

- [ ] Propellers are correctly installed and undamaged.
- [ ] Motors rotate freely.
- [ ] Motor shafts and bearings are in good condition.
- [ ] Arms and frame screws are tight.
- [ ] Flight controller is securely mounted.
- [ ] Cables cannot contact propellers or moving parts.
- [ ] Battery and payload are securely fastened.

### Electrical

- [ ] Battery polarity is correct.
- [ ] Power module is connected correctly.
- [ ] ESC signal wires are connected to the correct outputs.
- [ ] GPS and compass cables are secure.
- [ ] Receiver is powered and bound.
- [ ] Telemetry link is working if required.
- [ ] No exposed conductors or short circuits are present.

### Software

- [ ] Correct firmware and frame are selected.
- [ ] Accelerometer calibration is complete.
- [ ] Compass calibration is complete.
- [ ] Radio calibration is complete.
- [ ] Flight modes are correctly assigned.
- [ ] Battery monitor is correctly calibrated.
- [ ] Failsafe settings have been checked.
- [ ] GPS home position is established when required.
- [ ] Dataflash logging is working.
- [ ] Pre-arm checks pass.

***

## 8. Reference Pinout Summary

> These assignments represent the original Pixhawk layout. Verify every pin against the specific Pixhawk 2.4.8 board before connection.

| Port | Typical Assignment |
|---|---|
| `TELEM1 / TELEM2` | `+5 V`, `TX`, `RX`, `CTS`, `RTS`, `GND` |
| `GPS` | `+5 V`, GPS `TX`, GPS `RX`, CAN2 `TX`, CAN2 `RX`, `GND` |
| `SERIAL 4/5` | `+5 V`, `TX4`, `RX4`, `TX5`, `RX5`, `GND` |
| `I2C` | `+5 V`, `SCL`, `SDA`, `GND` |
| `CAN` | `+5 V`, `CAN_H`, `CAN_L`, `GND` |
| `POWER` | `+5 V`, `+5 V`, current sensing, voltage sensing |
| `ADC 3.3V` | 3.3 V analog input connections |
| `ADC 6.6V` | 6.6 V maximum analog input |
| `SPI` | `+5 V`, `SCK`, `MISO`, `MOSI`, chip-select, GPIO, `GND` |
| `SWITCH` | Safety LED and safety-switch signals |
| `DSM` | Receiver signal, ground and 3.3 V |

***

## 9. Important Notes

- Pixhawk 2.4.8 is not a single guaranteed hardware standard; clones can differ.
- Confirm power-rail voltage and current limits before connecting peripherals.
- Do not connect 5 V logic to 3.3 V signal pins.
- Do not connect the main battery directly to the flight controller.
- Always remove propellers during setup and testing.
- Keep the GPS/compass away from magnetic interference.
- Investigate vibration using flight logs rather than relying only on visual inspection.
- Keep a backup of stable parameters before making major configuration changes.

### Reference Documentation

- [ArduPilot Pixhawk Overview](https://ardupilot.org/copter/docs/common-pixhawk-overview.html) [ardupilot](https://ardupilot.org/copter/docs/common-pixhawk-overview.html)
- [ArduPilot Pixhawk Wiring Quick Start](https://ardupilot.org/copter/docs/common-pixhawk-wiring-and-quick-start.html) [ardupilot](https://ardupilot.org/copter/docs/common-pixhawk-wiring-and-quick-start.html)
- [ArduPilot Measuring Vibration](https://ardupilot.org/copter/docs/common-measuring-vibration.html) [ardupilot](https://ardupilot.org/copter/docs/common-measuring-vibration.html)
- [ArduPilot Compass Calibration](https://ardupilot.org/copter/docs/common-compass-calibration-in-mission-planner.html) [ardupilot](https://ardupilot.org/copter/docs/common-compass-calibration-in-mission-planner.html)
- [ArduPilot Pre-Arm Safety Checks](https://ardupilot.org/copter/docs/common-prearm-safety-checks.html) [ardupilot](https://ardupilot.org/copter/docs/common-prearm-safety-checks.html)
- [ArduPilot Safety Switch](https://ardupilot.org/copter/docs/common-safety-switch-pixhawk.html) [ardupilot](https://ardupilot.org/copter/docs/common-safety-switch-pixhawk.html)


