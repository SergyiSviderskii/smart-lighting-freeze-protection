# Asynchronous ESPHome Lighting Control

This folder contains the ESPHome firmware configurations (`.yaml`) and the corresponding Home Assistant automation rules for hybrid smart switches.

## 🔌 Hardware Compatibility & Pinout
The provided configuration frameworks are field-tested on **Tuya TYWE3S (ESP8266)** Wi-Fi modules:
* `tywe3s.yaml` – Configured for **Single-gang switches WITH a neutral wire**.
* `tywe3s_1.yaml` – Configured for **Single-gang switches WITHOUT a neutral wire** (No-Neutral setups).

> 💡 **Note:** You can easily adapt these configurations to any other ESP8266 or ESP32 development boards (like NodeMCU, Wemos D1 Mini, or custom relays). Simply change the target board type and adjust the hardware GPIO pins in the `substitutions:` block to match your device. Refer to the photos in this repository for visual examples of the modules used.

## 🧠 Local Autonomy & Presence Sync
The sensors and automations shown in `automation_ha.yaml` are calibrated for a specific domestic environment.

The core architecture utilizes a template switch component inside ESPHome linked directly to the Home Assistant presence machine:
* **The `activation` Switch:** This switch dynamically syncs tracking states with Home Assistant to monitor whether or not someone is present in the area. 
* **Hardware-Level Fallback:** If the connection drops or the house goes into an empty state, the microcontroller executes immediate localized automation rules, overriding external commands and safely driving the power relays to avoid phantom energy drain.
