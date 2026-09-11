


🌫️ FOG//VISION
AI-Powered Perception & Sensor-Fusion System for Mining Haul-Road Safety
SIH26007 · BRAINBYTE08 · Smart India Hackathon 2026

FOG//VISION is a real-time safety and perception prototype for mining haul-road environments. It combines computer vision, YOLO-based object detection, fog/visibility analysis, ESP32 vehicle sensors, real-time perception, warning mechanisms, V2V distance management, and data logging into one safety-oriented ecosystem.

🚧 The Problem
Mining haul roads can experience rapidly changing visibility and vehicle conditions. Fog, obstacles, blind spots, and multiple vehicles operating in close proximity can reduce reaction time and increase safety risk.

FOG//VISION provides an additional real-time perception and warning layer using both vision and physical vehicle sensors.

💡 The Solution
The system combines two major information sources:

👁️ Computer Vision — camera-based object/vehicle detection and visibility analysis.

📡 Vehicle Sensors — ESP32-connected ultrasonic and IR sensors for proximity awareness.

🧠 Perception Layer — converts these inputs into an intuitive operator-facing safety view.

🚨 Warning Layer — represents SAFE / CAUTION / DANGER conditions through visual and hardware alerts.

📊 Logging Layer — records system events and data for later analysis.

Core pipeline
SENSE → PERCEIVE → FUSE → EVALUATE → WARN → LOG
🏗️ System Architecture
                    MINING HAUL ROAD
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
        📷 CAMERA                    📡 VEHICLE
             │                       SENSORS
             ▼                           │
       OpenCV + YOLO                     │
       Visibility                       │
       Detection                         │
             │                           │
             └─────────────┬─────────────┘
                           ▼
                  🧠 PERCEPTION LAYER
                           │
                           ▼
                   SENSOR / VISION
                      INTEGRATION
                           │
                           ▼
                    SAFE / CAUTION
                       / DANGER
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
           🚨 ALERT      🖥️ HUD       📊 LOG
🚗 Vehicle 01 — Primary Perception Vehicle
Vehicle 01 is the main perception platform.

It integrates:

ESP32

Ultrasonic proximity sensing

IR obstacle sensing

Buzzer warning

Motor control

Camera perception

YOLO object/vehicle detection

Fog/visibility analysis

Real-time dashboard

Sensor telemetry

Safety-state visualization

Warning mechanisms

The dashboard represents the ultrasonic sensors as a forward sensing corridor, with left/right zones and distance-driven obstacle visualization.

🚙 Vehicle 02 — V2V Platform
Vehicle 02 extends the prototype toward vehicle-to-vehicle safety.

It includes:

Sensor integration

Hardware implementation

ESP32-based vehicle control

Local vehicle-control website

Distance monitoring

V2V distance-management logic

The two-vehicle architecture allows the prototype to explore safer separation between vehicles operating on the same road.

📡 Sensor System
Ultrasonic Sensors
Ultrasonic sensors provide short-range distance information.

They are used for:

Obstacle proximity

Left/right sensing

Forward safety-zone monitoring

Distance-based warning states

             FORWARD ROAD
                  │
        ┌─────────┴─────────┐
        │                   │
    LEFT ZONE           RIGHT ZONE
        │                   │
       📡                   📡
        │                   │
        └─────────┬─────────┘
                  │
                 🚗
               VEHICLE
IR Sensors
IR sensors provide an additional near-field obstacle layer and can act as a local confirmation layer when an obstacle enters close proximity.

🧠 Computer Vision
The vision pipeline uses:

OpenCV

NumPy

Ultralytics YOLO

Real-time video processing

The camera pipeline detects visible objects/vehicles and exposes those detections through the perception dashboard.

Sensor vs Vision
An ultrasonic sensor can tell the system:

Something is approximately this far away.

Computer vision can tell the system:

A visible object/vehicle appears in the camera view.

FOG//VISION presents both information sources together without pretending that a proximity sensor itself identifies an object.

🌫️ Fog & Visibility Perception
Fog is treated as an environmental perception problem.

The dashboard provides a visibility-oriented HUD representing changing visual conditions and the reliability of camera-based perception.

The system can incorporate:

Video quality

Scene visibility

Fog-related visual degradation

Detection availability

Visibility status

🎯 Real-Time Perception HUD
The FOG//VISION dashboard is designed as an automotive/HMI-style operator interface rather than a simple sensor debug screen.

It includes:

🚗 3D-style vehicle visualization

🛣️ Forward road corridor

📡 Left/right ultrasonic sensing zones

🎯 Obstacle markers

📏 Distance visualization

🔴 Direction-specific danger indicators

🟡 CAUTION state

🟢 SAFE state

📹 Live camera perception

🌫️ Fog/visibility status

📊 Sensor telemetry

📝 Event log

⚡ Performance information

Obstacle animation is driven by actual measured distance so that decreasing distance is represented as an approaching obstacle.

🚨 Warning Mechanism
              SENSOR / AI INPUT
                      │
                      ▼
              SAFETY EVALUATION
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
        SAFE       CAUTION      DANGER
          │           │           │
          ▼           ▼           ▼
       NORMAL       WARNING     CRITICAL
       STATE         STATE       ALERT
Warnings can be represented through:

Dashboard state changes

Direction-specific visual alerts

Obstacle proximity indicators

Front warning indicators

Buzzer/hardware alerts

Event logging

📏 V2V Distance Management
The V2V subsystem explores vehicle-to-vehicle proximity management.

The concept focuses on:

Relative vehicle proximity

Safe separation

Distance monitoring

Warning conditions

Local vehicle control

This creates a foundation for future multi-vehicle mining safety systems.

🎮 ESP32 Vehicle Control
ESP32 handles the vehicle-side implementation:

Motor control

Sensor acquisition

Sensor processing

Vehicle communication

Local control

A local ESP32 web interface allows vehicle movement commands through a browser.

Browser
   │
 Wi-Fi
   ▼
 ESP32
   │
   ├── L298N Motor Driver
   │       ├── Left Motors
   │       └── Right Motors
   │
   ├── Ultrasonic Sensors
   ├── IR Sensors
   └── Buzzer
📶 Communication Architecture
PHONE CAMERA
     │
     ▼
CAMO STUDIO
     │
     ▼
LAPTOP
     │
     ├──────────────► OpenCV / YOLO
     │
     └──────────────► ESP32 SENSOR API
                              │
                              ▼
                           VEHICLE
The ESP32 exposes sensor information through a local HTTP endpoint. The laptop dashboard retrieves the readings and combines them with the camera perception pipeline.

🖥️ Dashboard
The web dashboard provides:

Live camera feed

AI object detection

Fog/visibility HUD

3D vehicle visualization

Ultrasonic perception corridor

IR near-field layer

Safety state

Sensor telemetry

Event log

Connectivity status

FPS/performance information

Real-time warnings

The interface is intentionally designed around operator perception and rapid decision-making.

📊 Data & Logging
The project includes structured handling of:

Sensor readings

Event records

Warning states

Detection information

Test records

System logs

This provides a foundation for analysing prototype behaviour and future field-test data.

🧪 Prototype & Scaling
The current prototype proves the architecture and perception logic.

Some thresholds used during bench testing are prototype values rather than final mining-derived safety values.

A scaled system would require:

Speed-dependent thresholds

Braking-distance-derived warning zones

Sensor ranges suitable for mining haul-road dimensions

Terrain/environment baselines

Industrial-grade sensors

Ruggedized hardware

Calibration

Reliable communications

Vehicle-scale testing

Formal safety engineering and validation

The architecture itself remains:

SENSE → PERCEIVE → FUSE → EVALUATE → WARN → LOG
🔧 Hardware
Vehicle Electronics
ESP32

L298N motor driver

DC motors

Ultrasonic sensors

IR sensors

Buzzer

Battery/power system

Robot vehicle chassis

Vision
Camera

Laptop/processing system

Phone camera through Camo Studio during prototype testing

💻 Software Stack
Technology	Purpose
Python	Perception & dashboard backend
Streamlit	Real-time web dashboard
streamlit-webrtc	Live camera/video
OpenCV	Image/video processing
NumPy	Numerical processing
Ultralytics YOLO	AI object detection
ESP32 / Arduino	Vehicle control & sensing
HTTP / Wi-Fi	ESP32 ↔ Dashboard
HTML / CSS / JavaScript	Dashboard UI
Camo Studio	Phone-camera integration
🔄 End-to-End Data Flow
CAMERA
  │
  ├────────► FOG / VISIBILITY ANALYSIS
  │
  └────────► YOLO OBJECT DETECTION
                     │
                     ▼
               VISUAL PERCEPTION
                     │
ESP32 ──► ULTRASONIC ─┤
      └─► IR ─────────┤
                     ▼
                SENSOR FUSION
                     │
                     ▼
              SAFETY EVALUATION
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
        SAFE       CAUTION     DANGER
          │          │          │
          └──────────┼──────────┘
                     ▼
                DASHBOARD HUD
                     │
                     ▼
                 EVENT LOG
🚀 Future Scope
Potential extensions include:

Mining-grade LiDAR

Long-range radar

RTK-GPS

Digital haul-road mapping

Dedicated V2V/V2X communication

Advanced sensor fusion

Dedicated fog-density estimation

Moving-vehicle tracking

Automatic emergency braking integration

Fleet-level monitoring

Cloud analytics

Historical safety analytics

Industrial security

Ruggedized hardware

Large-scale field validation

⚠️ Prototype Disclaimer
FOG//VISION is a prototype/research implementation. It is not a replacement for certified mining safety systems or operator judgement.

Real-world deployment would require industrial hardware, site-specific calibration, redundancy, safety validation, environmental testing, regulatory compliance, and integration with existing mine safety infrastructure.

👥 BRAINBYTE08
The Team Behind FOG//VISION
👑 Rachit Shrirame
Team Lead · Vehicle-01 & Perception Systems

Led overall system architecture and integration

Developed Vehicle-01 sensor integration

Designed the complete FOG//VISION dashboard

Introduced the real-time perception layer

Integrated live sensor readings

Implemented camera-based vehicle/object detection

Developed warning and safety-state mechanisms

Worked across the overall web interface

🚗 Shivam Chavhan
Vehicle-02 · Hardware & V2V Systems

Developed Vehicle-02 sensor integration

Handled hardware connections

Implemented vehicle-side hardware

Worked on ESP32 vehicle control

Designed the local ESP32 vehicle-control website

Developed the V2V distance-management system

📊 Rakesh Chaudhary
Data & Logging Systems

Handled system data records

Worked on database management

Managed event and system logs

Organized sensor and test records

Supported data tracking and analysis

🖥️ Satvik Pole
Initial Dashboard & UI Foundation

Created the initial website/dashboard skeleton

Established the basic UI before sensor integration

Provided the foundation for the later real-time dashboard

Contributed to the early interface structure

🏗️ Manashree Chandak
Physical Design · Research & Information

Contributed to the physical outlook of the prototype

Worked on physical presentation and system appearance

Gathered problem-domain information

Supported research and requirement understanding

Contributed to documentation and presentation

🧪 Moksha Zambad
Research · Testing & Documentation

Contributed to problem-domain research

Assisted with requirement gathering

Supported prototype testing and validation

Worked on documentation and presentation

Helped organize project information and implementation details

🧠 BRAINBYTE08
                 WE DON'T JUST DETECT.
                     WE PERCEIVE.

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
        │     SAFE / CAUTION /        │
        │          DANGER             │
        └──────────────┬──────────────┘
                       ▼
        ┌─────────────────────────────┐
        │            WARN             │
        │     Visual + Hardware       │
        └──────────────┬──────────────┘
                       ▼
        ┌─────────────────────────────┐
        │            LOG              │
        │      Events + Records       │
        └─────────────────────────────┘
🏁 FOG//VISION
See Further. React Earlier. Operate Safer.
SIH26007 · BRAINBYTE08 · Smart India Hackathon 2026

Built as a collaborative prototype exploring how AI perception + vehicle sensors + real-time visualization + V2V awareness can contribute to safer mining haul-road operations.

Project Status: Prototype / Research & Development
