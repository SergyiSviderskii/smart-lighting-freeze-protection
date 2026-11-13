## 🔧 Hardware Insights & Zigbee PIR Revisions

While the 3-layer algorithm handles any stock sensor out of the box, hardware modifications can drastically improve sensor response times and allow tighter counter calibration:

### 1. Resistor-Timed Revision (`TS0202` / `_TZ3000_lf56vpxj`)
*   **Hardware Mod:** Follow the guide by [Victor (pvvx) — TS0202_TZ3000](https://pvvx.github.io/TS0202_TZ3000/). Removing the timing resistor reduces the "blind time" and switches the sensor to **short 4–5 second pulses**.
*   **Automation Calibration:** With this fast reset behavior, you can tighten the freeze protection counter threshold to just **2 cycles** (triggering the forced reset on the **3rd cycle**).

### 2. Multi-Variant MOSFET Revisions (`TS0202` / `_TZ3000_o4mkahkc` & similar)
*   **Hardware Mod:** These boards use unmarked MOSFET cascades to control hold time (`Pin 6` / `ONTIME`) and sensitivity (`Pin 1` / `SENS`) of the 6-pin digital PIR element.
*   **What Was Done:** Since the exact SMD resistor markings were unreadable, I removed the high-value pull-up resistors feeding these cascades and tied the corresponding PIR inputs directly to **GND (ground)** so they never float. Everything is clearly visible on the photos below (click any image to zoom in):

<img width="3024" height="4032" alt="IMG_2143" src="https://github.com/user-attachments/assets/d957a977-dd11-41a0-bf60-4fddabc42863" />

*Board Variant 1 (`TY_ZIGBEE_PIR_V1` / `ZTU` module): High-value pull-up resistors removed and PIR inputs tied to GND.*

<img width="4032" height="3024" alt="IMG_2142" src="https://github.com/user-attachments/assets/3b8af3cf-e511-420b-a29c-2c8da5774e92" />

*Board Variant 2 (`IHSENO V9` / `ZTU` module): Same modification — pull-up resistors removed and corresponding PIR inputs tied directly to GND.*
