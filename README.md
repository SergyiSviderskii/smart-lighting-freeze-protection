# smart-lighting-freeze-protection
Advanced Home Assistant lighting ecosystem (Zigbee &amp; ESPHome) with a unique 3-layer protective mechanism against motion sensor hardware freezes.

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

## ☀️ Solar Elevation Modeling

Both setups feature an automated template calculating seasonal solar alignment. Instead of hardcoding static offsets, a dynamic template models sun angles mathematically:
*   **Winter Mode:** Offsets higher (~ +8.0°), turning on lights earlier during dark winter days.
*   **Summer Mode:** Offsets lower (~ +3.0°), adapting to late sunsets.

The automation uses safe floating-point filters (`| float(5.5)`) to continuously contrast actual telemetry against these changing targets.

---

## 🚀 Setup & Calibration

1.  **Secrets Configuration:** Populate the provided `secrets.yaml` framework with your specific Wi-Fi routing paths and access tokens.
2.  **Deploy Python Script:** Place `set_state.py` into your Home Assistant `/python_scripts/` directory.
3.  **Calibrate the Counter:** Create a local `counter` entity in Home Assistant for the target room. Start testing with a low empirical threshold (e.g., `above: 5` cycles) to observe real-time lockup recovery before setting it to your final production value.

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

**With this radio-safe native ZHA action:**
```yaml
- action: zha.set_zigbee_cluster_attribute
  data:
    ieee: "00:12:4b:00:xx:xx:xx:xx" # Replace with your sensor's IEEE address (found in ZHA device info)
    endpoint_id: 1
    cluster_id: 1280              # IAS Zone Cluster
    cluster_type: in
    attribute: 2                  # ZoneStatus
    value: 0                      # Force reset state to "Clear / No Motion"
```
This forces the ZHA engine itself to safely record the state change, aligning packet bookkeeping and keeping budget hardware online.



## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



