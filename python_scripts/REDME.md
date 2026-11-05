# Python Reset Script for Entity State Overrides

This folder contains `set_state.py`, a crucial backend utility that allows Home Assistant to surgically force state resets on unresponsive or frozen Zigbee/ESPHome entities.

## 🚀 Installation & Path Setup

1. **Create the Directory:** Ensure you have a dedicated scripts folder inside your Home Assistant core configuration directory.
2. **Deploy the File:** Copy `set_state.py` into the following exact path:
   ```text
   /config/python_scripts/set_state.py
   ```
   *(Note: Depending on your installation type, the root path might map to `/homeassistant/python_scripts/set_state.py`)*

## 🛠️ Home Assistant Configuration

To enable Python script execution in your environment, open your primary configuration file located at `/config/configuration.yaml` (or `/homeassistant/configuration.yaml`) and append the following single-line integration key:

```yaml
python_script:
```

3. **Restart:** Save the file and restart Home Assistant to apply the changes. The new action `python_script.set_state` will automatically become available in your automations developer tools.
