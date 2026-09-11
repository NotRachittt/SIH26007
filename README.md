# 🌫️ FOG//VISION
### AI-Powered Perception & Sensor-Fusion System for Mining Haul-Road Safety
**SIH26007 · BRAINBYTE08 · Smart India Hackathon 2026**

FOG//VISION is a real-time safety and perception prototype for mining haul-road environments. It combines computer vision, YOLO-based object detection, fog/visibility analysis, ESP32 vehicle sensors, real-time perception, warning mechanisms, V2V distance management, and data logging into one safety-oriented ecosystem.

---

## 🚧 The Problem
Mining haul roads can experience rapidly changing visibility and vehicle conditions. Fog, obstacles, blind spots, and multiple vehicles operating in close proximity can reduce reaction time and increase safety risk.

FOG//VISION provides an additional real-time perception and warning layer using both vision and physical vehicle sensors.

## 💡 The Solution
The system combines two major information sources:

- 👁️ **Computer Vision** — camera-based object/vehicle detection and visibility analysis
- 📡 **Vehicle Sensors** — ESP32-connected ultrasonic and IR sensors for proximity awareness
- 🧠 **Perception Layer** — converts these inputs into an intuitive operator-facing safety view
- 🚨 **Warning Layer** — represents SAFE / CAUTION / DANGER conditions through visual and hardware alerts
- 📊 **Logging Layer** — records system events and data for later analysis

**Core pipeline:** `SENSE → PERCEIVE → FUSE → EVALUATE → WARN → LOG`

---

## 🏗️ System Architecture
```
MINING HAUL ROAD
        │
   ┌────┴────┐
   │         │
   ▼         ▼
📷 CAMERA  📡 VEHICLE SENSORS
   │             │
OpenCV+YOLO   Ultrasonic/IR
Visibility     Detection
   │             │
   └──────┬──────┘
          ▼
  🧠 PERCEPTION LAYER
          │
          ▼
 SENSOR/VISION FUSION
          │
          ▼
  SAFE / CAUTION / DANGER
          │
   ┌──────┼──────┐
   ▼      ▼      ▼
🚨 ALERT 🖥️ HUD 📊 LOG
```

---

## 🚗 Vehicle 01 — Primary Perception Vehicle
The main perception platform. Integrates:
- ESP32, ultrasonic + IR sensing, buzzer warning, motor control
- Camera perception, YOLO object/vehicle detection, fog/visibility analysis
- Real-time dashboard, sensor telemetry, safety-state visualization, warning mechanisms

The dashboard represents the ultrasonic sensors as a forward sensing corridor, with left/right zones and distance-driven obstacle visualization.

## 🚙 Vehicle 02 — V2V Platform
Extends the prototype toward vehicle-to-vehicle safety. Includes:
- Sensor integration, hardware implementation, ESP32-based vehicle control
- Local vehicle-control website
- Distance monitoring & V2V distance-management logic

The two-vehicle architecture explores safer separation between vehicles operating on the same road.

---

## 📡 Sensor System

**Ultrasonic Sensors** — short-range distance info for:
- Obstacle proximity
- Left/right sensing
- Forward safety-zone monitoring
- Distance-based warning states

```
         FORWARD ROAD
              │
    ┌─────────┴─────────┐
LEFT ZONE           RIGHT ZONE
    📡                   📡
    └─────────┬─────────┘
              🚗 VEHICLE
```

**IR Sensors** — additional near-field obstacle layer, acting as a local confirmation layer when an obstacle enters close proximity.

## 🧠 Computer Vision
Pipeline uses OpenCV, NumPy, Ultralytics YOLO, and real-time video processing to detect visible objects/vehicles, exposed through the perception dashboard.

**Sensor vs Vision**
- Ultrasonic → "Something is approximately this far away."
- Vision → "A visible object/vehicle appears in the camera view."

FOG//VISION presents both sources together without pretending a proximity sensor itself identifies an object.

## 🌫️ Fog & Visibility Perception
Fog is treated as an environmental perception problem. The dashboard provides a visibility-oriented HUD representing changing visual conditions and camera-perception reliability, incorporating video quality, scene visibility, fog-related degradation, detection availability, and visibility status.

## 🎯 Real-Time Perception HUD
Designed as an automotive/HMI-style operator interface rather than a simple sensor debug screen:
- 🚗 3D-style vehicle visualization · 🛣️ Forward road corridor
- 📡 Left/right ultrasonic zones · 🎯 Obstacle markers · 📏 Distance visualization
- 🔴 Direction-specific danger indicators · 🟡 CAUTION · 🟢 SAFE
- 📹 Live camera perception · 🌫️ Fog/visibility status
- 📊 Sensor telemetry · 📝 Event log · ⚡ Performance info

Obstacle animation is driven by actual measured distance, so decreasing distance is represented as an approaching obstacle.

## 🚨 Warning Mechanism
```
SENSOR / AI INPUT → SAFETY EVALUATION → SAFE / CAUTION / DANGER
                                          │        │        │
                                       NORMAL   WARNING  CRITICAL
                                       STATE     STATE    ALERT
```
Represented through dashboard state changes, direction-specific alerts, obstacle proximity indicators, front warning indicators, buzzer/hardware alerts, and event logging.

## 📏 V2V Distance Management
Explores vehicle-to-vehicle proximity management: relative proximity, safe separation, distance monitoring, warning conditions, and local vehicle control — a foundation for future multi-vehicle mining safety systems.

## 🎮 ESP32 Vehicle Control
Handles the vehicle-side implementation — motor control, sensor acquisition/processing, vehicle communication, local control. A local ESP32 web interface allows vehicle movement commands through a browser.
```
Browser → Wi-Fi → ESP32 → L298N Motor Driver → Left/Right Motors
                        → Ultrasonic Sensors
                        → IR Sensors
                        → Buzzer
```

## 📶 Communication Architecture
```
PHONE CAMERA → CAMO STUDIO → LAPTOP → OpenCV/YOLO
                                    → ESP32 SENSOR API → VEHICLE
```
The ESP32 exposes sensor info through a local HTTP endpoint; the laptop dashboard retrieves readings and combines them with the camera perception pipeline.

## 🖥️ Dashboard
Live camera feed · AI object detection · Fog/visibility HUD · 3D vehicle visualization · Ultrasonic perception corridor · IR near-field layer · Safety state · Sensor telemetry · Event log · Connectivity status · FPS/performance info · Real-time warnings — designed around operator perception and rapid decision-making.

## 📊 Data & Logging
Structured handling of sensor readings, event records, warning states, detection information, test records, and system logs — a foundation for analysing prototype behaviour and future field-test data.

## 🧪 Prototype & Scaling
The current prototype proves the architecture and perception logic. Some bench-testing thresholds are prototype values, not final mining-derived safety values. A scaled system would need:
- Speed-dependent thresholds, braking-distance-derived warning zones
- Sensor ranges suited to mining haul-road dimensions, terrain/environment baselines
- Industrial-grade, ruggedized hardware, calibration, reliable communications
- Vehicle-scale testing, formal safety engineering and validation

Architecture stays: `SENSE → PERCEIVE → FUSE → EVALUATE → WARN → LOG`

---

## 🔧 Hardware
**Vehicle Electronics:** ESP32, L298N motor driver, DC motors, ultrasonic sensors, IR sensors, buzzer, battery/power system, robot vehicle chassis
**Vision:** Camera, laptop/processing system, phone camera via Camo Studio (prototype testing)

## 💻 Software Stack
| Technology | Purpose |
|---|---|
| Python | Perception & dashboard backend |
| Streamlit | Real-time web dashboard |
| streamlit-webrtc | Live camera/video |
| OpenCV | Image/video processing |
| NumPy | Numerical processing |
| Ultralytics YOLO | AI object detection |
| ESP32 / Arduino | Vehicle control & sensing |
| HTTP / Wi-Fi | ESP32 ↔ Dashboard |
| HTML / CSS / JavaScript | Dashboard UI |
| Camo Studio | Phone-camera integration |

## 🔄 End-to-End Data Flow
```
CAMERA → FOG/VISIBILITY ANALYSIS ─┐
       → YOLO OBJECT DETECTION ───┴→ VISUAL PERCEPTION
ESP32  → ULTRASONIC ─┐
       → IR ──────────┴→ SENSOR FUSION
VISUAL PERCEPTION + SENSOR FUSION → SAFETY EVALUATION
                                   → SAFE / CAUTION / DANGER
                                   → DASHBOARD HUD → EVENT LOG
```

## 🚀 Future Scope
Mining-grade LiDAR · Long-range radar · RTK-GPS · Digital haul-road mapping · Dedicated V2V/V2X communication · Advanced sensor fusion · Dedicated fog-density estimation · Moving-vehicle tracking · Automatic emergency braking integration · Fleet-level monitoring · Cloud analytics · Historical safety analytics · Industrial security · Ruggedized hardware · Large-scale field validation

## ⚠️ Prototype Disclaimer
FOG//VISION is a prototype/research implementation. It is not a replacement for certified mining safety systems or operator judgement. Real-world deployment would require industrial hardware, site-specific calibration, redundancy, safety validation, environmental testing, regulatory compliance, and integration with existing mine safety infrastructure.

---

## 👥 BRAINBYTE08 — Team Contributions

| Member | Role | Contributions |
|---|---|---|
| **Rachit Shrirame** 👑 | Team Lead · Vehicle-01 & Perception Systems | Led the project architecture and integration. Developed the Vehicle-01 sensor system, designed the complete FOG//VISION dashboard, introduced the real-time perception layer, integrated live sensor readings with the dashboard, implemented camera-based vehicle/object detection, safety-state visualization, warning mechanisms, and the overall web interface. |
| **Shivam Chavhan** | Vehicle-02 · Hardware & V2V Systems | Developed Vehicle-02 sensor integration, handled hardware connections and physical implementation, worked on ESP32-based vehicle control, designed the local ESP32 vehicle-control interface, and developed the Vehicle-to-Vehicle (V2V) distance management system. |
| **Rakesh Chaudhary** | Data & Logging Systems | Handled data records, database management, event/log handling, sensor data organization, and system data tracking, supporting analysis and maintaining structured records generated during testing. |
| **Satvik Pole** | Initial Dashboard & UI Foundation | Created the initial website/dashboard skeleton before sensor integration, establishing the basic structure and UI foundation later expanded into the complete real-time monitoring interface. |
| **Manashree Chandak** | System Design · Physical Integration & Research | Contributed to the physical outlook and presentation of the system, helped shape the overall physical implementation, worked on information gathering and problem-domain research, and supported documentation, presentation, and system-level organization. |
| **Moksha Zambad** | Research · Testing & Documentation | Contributed to problem research, requirement gathering, system testing, documentation, validation of the prototype, and presentation preparation, helping connect the technical implementation with the project's intended mining-safety use case. |

---

## 🧠 BRAINBYTE08
### WE DON'T JUST DETECT. WE PERCEIVE.

```
┌─────────────────────────────┐
│            SENSE            │
│ Sensors + Camera + Vehicle  │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│          PERCEIVE           │
│ AI + Visibility + Detection │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│            FUSE             │
│ Vision + Sensors + V2V      │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│          EVALUATE           │
│   SAFE / CAUTION / DANGER   │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│            WARN             │
│     Visual + Hardware       │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│            LOG               │
│      Events + Records       │
└─────────────────────────────┘
```

## 🏁 FOG//VISION
**See Further. React Earlier. Operate Safer.**
*SIH26007 · BRAINBYTE08 · Smart India Hackathon 2026*

Built as a collaborative prototype exploring how AI perception + vehicle sensors + real-time visualization + V2V awareness can contribute to safer mining haul-road operations.

**Project Status:** Prototype / Research & Development
