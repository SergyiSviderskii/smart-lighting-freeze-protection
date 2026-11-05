# Wireless Zigbee Lighting Automation

This folder contains the monolithic Home Assistant automation configurations for managing lighting via Zigbee devices.

## ⚙️ Core Architecture & Helpers
All auxiliary logic components are handled directly within the Home Assistant core backend:
* **Timers:** Used for precisely tracking light duration state machines.
* **Input Booleans:** Utilized as logical flip-flops to manage operational states.
* **Python Scripts:** Used to forcefully clear unresponsive or frozen entities.

## ⚠️ Important Note on External Dependencies
The sensors provided in these examples are tailored to a specific real-world domestic environment. 

This automation relies on a custom external boundary component:
`input_boolean.vspomogatelnyi_avtomatizatsii_voshli_vyshli_v_zonu_upravleniia_elektrichestvom`

* **Customization:** If you are deploying this configuration in your own smart home, you can easily create a local "virtual" version of this helper entity to match your ecosystem.
* **Support:** If you need assistance understanding the dual-loop architecture of this external component, feel free to open an issue or reach out—I will gladly explain how I set it up!
