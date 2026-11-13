# smart-lighting-freeze-protection
Advanced Home Assistant lighting ecosystem (Zigbee & ESPHome) with a unique 3-layer protective mechanism against motion sensor hardware freezes.

# Smart Lighting with Motion Sensor Freeze Protection (Zigbee & ESPHome)

Welcome to the advanced, field-tested domestic lighting ecosystem managed by Home Assistant. This repository contains complete automation scripts and hardware configurations that solve one of the most frustrating smart home issues: **hardware freeze states in battery-powered or wireless motion sensors (stuck in 'on' state)**.

---

## 📂 Repository Structure

The project is divided into dedicated ecosystems based on your deployment needs:

*   **`lighting_Zigbee/`**
    *   Contains pure Home Assistant monolithic automation configurations.
    *   Designed for wireless Zigbee motion sensors and door contact sensors (ZHA/Zigbee2MQTT) operating in places like kitchens or basements.
*   **`lighting_ESPHome/`**
    *   Contains asynchronous ESP8266/ESP32 configuration files (`.yaml`) alongside corresponding Home Assistant control scripts.
    *   Designed for hybrid deployments (e.g., bathrooms) where multiple presence zones (Main PIR, Shower, Toilet) offload physical timing loops directly to microcontrollers.
*   **`python_scripts/`**
    *   Houses `set_state.py`, a small but crucial script used by Home Assistant to surgically force state resets on unresponsive entities via the backend.

---

## 🧠 The 3-Layer Empirical Freeze Protection

Instead of relying on external timers, this project introduces a nested, single-flow `if-then-else` structure integrated directly into the lighting loop. It monitors sensor behavior empirically based on "life signatures":

1.  **Natural Reset:** When a user leaves the area and the sensor naturally transitions from `on` to `off`, the failure cycle counter instantly wipes to `0`.
2.  **Activity-Driven Reset:** If a secondary zone trips (e.g., a door opens or an auxiliary shower sensor detects motion) while the main sensor is active, the system detects a human presence signature, identifies the sensor as healthy, and resets empirical doubt.
3.  **Surgical Reset (Forced Python Override):** In conditions of total silence where all auxiliary sensors are quiet, if the main sensor holds an `on` state for `X` consecutive finished lighting cycles, the automation diagnoses a hardware freeze. It calls `python_script.set_state` to forcefully push an `off` state, successfully re-animating the device.

---

## 🔧 Hardware Insights & Zigbee PIR Revisions

While the 3-layer algorithm handles any stock sensor out of the box, hardware modifications can drastically improve sensor response times and allow tighter counter calibration:

### 1. Resistor-Timed Revision (`TS0202` / `_TZ3000_lf56vpxj`)
*   **Hardware Mod:** Follow the guide by [Victor (pvvx) — TS0202_TZ3000](https://github.io). Removing the timing resistor reduces the "blind time" and switches the sensor to **short 4–5 second pulses**.
*   **Automation Calibration:** With this fast reset behavior, you can tighten the freeze protection counter threshold to just **2 cycles** (triggering the forced reset on the **3rd cycle**).

### 2. Multi-Variant MOSFET Revisions (`TS0202` / `_TZ3000_o4mkahkc` & similar)
*   **Hardware Mod:** These boards use unmarked MOSFET cascades to control hold time (`Pin 6` / `ONTIME`) and sensitivity (`Pin 1` / `SENS`) of the 6-pin digital PIR element.
*   **What Was Done:** On my two board variants, I removed the high-value pull-up resistors feeding these cascades and tied the corresponding PIR inputs directly to **GND (ground)** so they never float. Everything is clearly visible on the photos below (click any image to zoom in):
<img width="3024" height="4032" alt="IMG_2143" src="https://github.com/user-attachments/assets/d957a977-dd11-41a0-bf60-4fddabc42863" />
<img width="4032" height="3024" alt="IMG_2142" src="https://github.com/user-attachments/assets/3b8af3cf-e511-420b-a29c-2c8da5774e92" />




---

## ☀️ Solar Elevation Modeling

Both setups feature an automated template calculating seasonal solar alignment. Instead of hardcoding static offsets, a dynamic template models sun angles mathematically:
*   **Winter Mode:** Offsets higher (~ +8.0°), turning on lights earlier during dark winter days.
*   **Summer Mode:** Offsets lower (~ +3.0°), adapting to late sunsets.

The automation uses safe floating-point filters (`| float(5.5)`) to continuously contrast actual telemetry against these changing targets.

---

## 🚀 Setup & Calibration

1.  **Secrets Configuration:** Populate the provided `secrets.yaml` framework with your specific Wi-Fi routing paths and access tokens.
2.  **Deploy Python Script:** Place `set_state.py` into your Home Assistant `/python_scripts/` directory.
3.  **Calibrate the Counter:** Create a local `counter` entity in Home Assistant for the target room:
    *   For **stock unmodded sensors** (30s–90s hold time), start with a conservative threshold (e.g., `above: 5` cycles) to observe real-time lockup recovery.
    *   For **hardware-modded short-pulse sensors** (4–5s hold time), you can safely tighten the threshold to `2` (resetting on the 3rd cycle).

### 💡 Important Update for ZHA (Zigbee Home Automation) Users

If you are using the modern native **ZHA** integration and notice that your Zigbee motion sensors occasionally enter a "deep sleep/coma" state after a forced Python `set_state` override, it is highly recommended to replace the virtual backend state rewrite with a native Zigbee cluster command. 

Recent Home Assistant core updates handle radio packet sequencing strictly, and bypassing the ZHA stack can break token synchronization. To fix this, swap the `python_script.set_state` block in your automation for a direct IAS Zone cluster attributes overwrite.

**Replace this block:**
```yaml
- action: python_script.set_state
  data:
    entity_id: binary_sensor.YOUR_MOTION_SENSOR
    state: "off"
```

This forces the ZHA engine itself to safely record the state change, aligning packet bookkeeping and keeping budget hardware online.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
