/*
  4WD Robot Car — ESP32 + L298N + Web Button Control (5-gear)
  + 2x Ultrasonic (HC-SR04) + 2x IR Sensor — Fog/Obstacle Alert Layer
  -------------------------------------------------------------
  - ESP32 creates its own WiFi Access Point.
  - Connect any phone/laptop to that WiFi, open the IP in a browser.
  - Tap Forward/Reverse/Left/Right buttons to drive; pick a gear (1-5)
    to set speed. Left/Right pivot-turn in place (one wheel forward,
    one wheel backward). Releasing all buttons stops the car.
  - Sensor readings (2x ultrasonic + 2x IR) are polled every 300ms and
    shown live on the same webpage, with a Safe/Caution/Danger banner.

  Wiring (L298N -> ESP32):
    ENA -> GPIO14   (left side speed / PWM)
    IN1 -> GPIO27   (left side direction)
    IN2 -> GPIO26   (left side direction)
    ENB -> GPIO32   (right side speed / PWM)
    IN3 -> GPIO25   (right side direction)
    IN4 -> GPIO33   (right side direction)
    GND -> GND      (shared ground with ESP32 - required)

  Wiring (Sensors -> ESP32):
    Ultrasonic 1: VCC->5V, GND->GND, Trig->GPIO5,  Echo->GPIO18
    Ultrasonic 2: VCC->5V, GND->GND, Trig->GPIO19, Echo->GPIO21
    IR 1:         VCC->5V/3.3V, GND->GND, OUT->GPIO34
    IR 2:         VCC->5V/3.3V, GND->GND, OUT->GPIO35

  No extra libraries needed - WiFi.h, WebServer.h and ArduinoJson-free
  manual JSON string building are used (keeps it dependency-light).
*/

#include <WiFi.h>
#include <WebServer.h>

// ---------- WiFi Access Point credentials ----------
const char* ssid     = "RobotCar_Shiv";
const char* password = "rasmalai";   // must be 8+ characters, or "" for open network

// ---------- Motor driver pins ----------
const int ENA = 14;   // left speed (PWM)
const int IN1 = 27;   // left direction
const int IN2 = 26;   // left direction
const int ENB = 32;   // right speed (PWM)
const int IN3 = 25;   // right direction
const int IN4 = 33;   // right direction

// ---------- Sensor pins ----------
#define US1_TRIG 5
#define US1_ECHO 18
#define US2_TRIG 19
#define US2_ECHO 21
#define IR1_PIN  34
#define IR2_PIN  35
#define BUZZER_PIN 4          // any free GPIO — buzzer +ve here, -ve to GND

const int DANGER_DISTANCE  = 20;   // cm - red alert
const int CAUTION_DISTANCE = 40;   // cm - yellow alert

// ---------- PWM config (ESP32 LEDC) ----------
const int pwmFreq       = 5000;
const int pwmResolution = 8;      // 8-bit -> duty 0-255
const int pwmChannelA   = 0;      // left  (only used on old core)
const int pwmChannelB   = 1;      // right (only used on old core)

#if defined(ESP_ARDUINO_VERSION_MAJOR) && ESP_ARDUINO_VERSION_MAJOR >= 3
  #define PWM_LEFT  ENA
  #define PWM_RIGHT ENB
  #define SETUP_PWM() do { ledcAttach(ENA, pwmFreq, pwmResolution); \
                            ledcAttach(ENB, pwmFreq, pwmResolution); } while (0)
#else
  #define PWM_LEFT  pwmChannelA
  #define PWM_RIGHT pwmChannelB
  #define SETUP_PWM() do { ledcSetup(pwmChannelA, pwmFreq, pwmResolution); \
                            ledcAttachPin(ENA, pwmChannelA); \
                            ledcSetup(pwmChannelB, pwmFreq, pwmResolution); \
                            ledcAttachPin(ENB, pwmChannelB); } while (0)
#endif

WebServer server(80);

// ---------- Sensor state (updated in loop(), read by /sensors handler) ----------
long  s_dist1 = -1, s_dist2 = -1;
bool  s_ir1 = false, s_ir2 = false;   // true = obstacle detected
String s_alertLevel = "safe";
unsigned long lastSensorRead = 0;
const unsigned long SENSOR_INTERVAL_MS = 300;

// ================= Motor functions =================
void setMotors(int speedLeft, int speedRight) {
  if (speedLeft >= 0) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
  } else {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
  }
  ledcWrite(PWM_LEFT, abs(speedLeft));

  if (speedRight >= 0) {
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
  } else {
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
  }
  ledcWrite(PWM_RIGHT, abs(speedRight));
}

void stopMotors() {
  ledcWrite(PWM_LEFT, 0);
  ledcWrite(PWM_RIGHT, 0);
}

// ================= Sensor functions =================
long readUltrasonicCM(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000); // 30ms timeout ~ 500cm
  if (duration == 0) return -1;                  // no echo / out of range

  return duration * 0.0343 / 2;                  // convert to cm
}

void updateSensors() {
  s_dist1 = readUltrasonicCM(US1_TRIG, US1_ECHO);
  s_dist2 = readUltrasonicCM(US2_TRIG, US2_ECHO);
  s_ir1   = (digitalRead(IR1_PIN) == HIGH);        // most IR modules: LOW = obstacle
  s_ir2   = (digitalRead(IR2_PIN) == HIGH);

  bool danger  = false;
  bool caution = false;

  if ((s_dist1 > 0 && s_dist1 < DANGER_DISTANCE) ||
      (s_dist2 > 0 && s_dist2 < DANGER_DISTANCE) ||
      s_ir1 || s_ir2) {
    danger = true;
  } else if ((s_dist1 > 0 && s_dist1 < CAUTION_DISTANCE) ||
             (s_dist2 > 0 && s_dist2 < CAUTION_DISTANCE)) {
    caution = true;
  }

  s_alertLevel = danger ? "danger" : (caution ? "caution" : "safe");

  // Buzzer: ON the moment ANY of the 4 sensors reports something close
  digitalWrite(BUZZER_PIN, danger ? HIGH : LOW);
}

// ---------- Web page (game-style button controls + sensor panel) ----------
const char htmlPage[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, viewport-fit=cover">
<title>Robot Car Control</title>
<style>
  * {
    box-sizing: border-box;
    -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none;
    -webkit-touch-callout: none;
    -webkit-tap-highlight-color: transparent;
  }
  html, body { margin:0; padding:0; width:100%; height:100%; overflow:hidden;
               background:#0a0a0a; color:#eee; font-family: sans-serif; }
  #status { position: absolute; top: 10px; left: 50%; transform: translateX(-50%);
            font-size: 13px; color: #888; z-index: 5; }
  #log { position: absolute; top: 34px; left: 50%; transform: translateX(-50%);
         font-size: 12px; color: #4caf50; z-index: 5; font-family: monospace; }

  #gears {
    position: absolute; top: 58px; left: 50%; transform: translateX(-50%);
    display: flex; gap: 8px; z-index: 5;
  }
  .gear {
    width: 32px; height: 32px; border-radius: 50%;
    background: rgba(255,255,255,0.12); border: 2px solid rgba(255,255,255,0.25);
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: bold; color: #eee;
    touch-action: manipulation;
  }
  .gear.active { background: rgba(255,152,0,0.75); border-color: #ff9800; }

  .pad {
    position: absolute;
    width: 90px; height: 90px; border-radius: 16px;
    background: rgba(255,255,255,0.12); border: 2px solid rgba(255,255,255,0.25);
    display: flex; align-items: center; justify-content: center;
    touch-action: none; transition: background 0.1s;
  }
  .pad:active, .pad.held { background: rgba(76,175,80,0.55); border-color: #4caf50; }
  .pad svg { width: 40px; height: 40px; fill: #eee; pointer-events: none; }

  #btnLeft    { left: 20px;  bottom: 90px; }
  #btnRight   { left: 120px; bottom: 90px; }
  #btnForward { right: 20px; bottom: 200px; }
  #btnReverse { right: 20px; bottom: 90px; }

  /* Sensor panel */
  #sensorPanel {
    position: absolute; top: 100px; left: 50%; transform: translateX(-50%);
    width: 240px; padding: 10px 14px; border-radius: 12px;
    background: rgba(255,255,255,0.08); border: 2px solid rgba(255,255,255,0.2);
    font-size: 12px; font-family: monospace; z-index: 5; text-align: left;
  }
  #sensorPanel .row { display:flex; justify-content: space-between; margin: 2px 0; }
  #alertBanner {
    position: absolute; top: 190px; left: 50%; transform: translateX(-50%);
    padding: 6px 16px; border-radius: 8px; font-weight: bold; font-size: 13px;
    z-index: 5; transition: background 0.2s;
  }
  .alert-safe    { background: rgba(76,175,80,0.85); color:#fff; }
  .alert-caution { background: rgba(255,193,7,0.9);  color:#000; }
  .alert-danger  { background: rgba(244,67,54,0.9);  color:#fff; }
</style>
</head>
<body>
<div id="status">Ready</div>
<div id="log">Gear: 3 | L: 0, R: 0</div>

<div id="gears">
  <div class="gear" data-gear="1">1</div>
  <div class="gear" data-gear="2">2</div>
  <div class="gear active" data-gear="3">3</div>
  <div class="gear" data-gear="4">4</div>
  <div class="gear" data-gear="5">5</div>
</div>

<div id="sensorPanel">
  <div class="row"><span>Ultrasonic 1</span><span id="u1">-- cm</span></div>
  <div class="row"><span>Ultrasonic 2</span><span id="u2">-- cm</span></div>
  <div class="row"><span>IR 1</span><span id="i1">--</span></div>
  <div class="row"><span>IR 2</span><span id="i2">--</span></div>
</div>
<div id="alertBanner" class="alert-safe">SAFE</div>

<div class="pad" id="btnLeft"><svg viewBox="0 0 24 24"><path d="M15 6l-6 6 6 6"/></svg></div>
<div class="pad" id="btnRight"><svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg></div>
<div class="pad" id="btnForward"><svg viewBox="0 0 24 24"><path d="M12 5l7 7h-4v7h-6v-7H5z"/></svg></div>
<div class="pad" id="btnReverse"><svg viewBox="0 0 24 24"><path d="M12 19l-7-7h4V5h6v7h4z"/></svg></div>

<script>
const statusEl = document.getElementById('status');
const logEl = document.getElementById('log');
const state = { left: false, right: false, forward: false, reverse: false, gear: 3 };

const GEAR_SPEEDS = [20, 40, 60, 80, 100];

function currentSpeed() {
  return GEAR_SPEEDS[state.gear - 1];
}

function clamp(v, lo, hi) {
  return Math.max(lo, Math.min(hi, v));
}

function computeAndSend() {
  const speed = currentSpeed();

  let throttle = 0;
  if (state.forward) throttle += speed;
  if (state.reverse) throttle -= speed;

  let turn = 0;
if (state.left)  turn += speed;
if (state.right) turn -= speed;

  const left  = clamp(throttle - turn, -100, 100);
  const right = clamp(throttle + turn, -100, 100);

  logEl.textContent = `Gear: ${state.gear} | L: ${left}, R: ${right}`;
  fetch(`/move?left=${left}&right=${right}`)
    .then(() => statusEl.textContent = 'Connected')
    .catch(() => statusEl.textContent = 'Connection lost');
}

let sendTimer = null;
function startSending() {
  if (sendTimer) return;
  computeAndSend();
  sendTimer = setInterval(computeAndSend, 100);
}
function stopSendingIfIdle() {
  if (!state.left && !state.right && !state.forward && !state.reverse) {
    clearInterval(sendTimer);
    sendTimer = null;
    computeAndSend();
  }
}

function bind(id, key) {
  const el = document.getElementById(id);
  const press = (e) => { e.preventDefault(); state[key] = true; el.classList.add('held'); startSending(); };
  const release = (e) => { e.preventDefault(); state[key] = false; el.classList.remove('held'); stopSendingIfIdle(); };
  el.addEventListener('pointerdown', press);
  el.addEventListener('pointerup', release);
  el.addEventListener('pointercancel', release);
  el.addEventListener('pointerleave', release);
}

bind('btnLeft', 'left');
bind('btnRight', 'right');
bind('btnForward', 'forward');
bind('btnReverse', 'reverse');

document.querySelectorAll('.gear').forEach(el => {
  el.addEventListener('pointerdown', (e) => {
    e.preventDefault();
    document.querySelectorAll('.gear').forEach(g => g.classList.remove('active'));
    el.classList.add('active');
    state.gear = parseInt(el.dataset.gear, 10);
    if (state.left || state.right || state.forward || state.reverse) {
      computeAndSend();
    } else {
      logEl.textContent = `Gear: ${state.gear} | L: 0, R: 0`;
    }
  });
});

document.addEventListener('contextmenu', (e) => e.preventDefault());
document.addEventListener('selectstart', (e) => e.preventDefault());
document.addEventListener('dragstart', (e) => e.preventDefault());

// ---------- Sensor polling ----------
const banner = document.getElementById('alertBanner');
function pollSensors() {
  fetch('/sensors')
    .then(r => r.json())
    .then(d => {
      document.getElementById('u1').textContent = d.dist1 > 0 ? d.dist1 + ' cm' : 'no echo';
      document.getElementById('u2').textContent = d.dist2 > 0 ? d.dist2 + ' cm' : 'no echo';
      document.getElementById('i1').textContent = d.ir1 ? 'Clear' : 'Obstacle';
      document.getElementById('i2').textContent = d.ir2 ? 'Clear' : 'Obstacle';

      banner.className = 'alert-' + d.alert;
      banner.textContent = d.alert.toUpperCase();
    })
    .catch(() => {});
}
setInterval(pollSensors, 300);
pollSensors();
</script>
</body>
</html>
)rawliteral";

void handleRoot() {
  server.send(200, "text/html", htmlPage);
}

void handleMove() {
  if (server.hasArg("left") && server.hasArg("right")) {
    int left  = server.arg("left").toInt();
    int right = server.arg("right").toInt();

    int leftPWM  = map(constrain(left,  -100, 100), -100, 100, -255, 255);
    int rightPWM = map(constrain(right, -100, 100), -100, 100, -255, 255);

    setMotors(leftPWM, rightPWM);
    server.send(200, "text/plain", "OK");
  } else {
    server.send(400, "text/plain", "Missing left/right params");
  }
}

void handleSensors() {
  // Manual JSON build - no extra library needed
  String json = "{";
  json += "\"dist1\":" + String(s_dist1) + ",";
  json += "\"dist2\":" + String(s_dist2) + ",";
  json += "\"ir1\":" + String(s_ir1 ? "true" : "false") + ",";
  json += "\"ir2\":" + String(s_ir2 ? "true" : "false") + ",";
  json += "\"alert\":\"" + s_alertLevel + "\"";
  json += "}";
  server.send(200, "application/json", json);
}

void handleNotFound() {
  server.send(404, "text/plain", "Not found");
}

void setup() {
  Serial.begin(115200);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  pinMode(US1_TRIG, OUTPUT);
  pinMode(US1_ECHO, INPUT);
  pinMode(US2_TRIG, OUTPUT);
  pinMode(US2_ECHO, INPUT);
  pinMode(IR1_PIN, INPUT);
  pinMode(IR2_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);

  SETUP_PWM();
  stopMotors();

  WiFi.softAP(ssid, password);
  Serial.print("Access Point started. Connect to WiFi: ");
  Serial.println(ssid);
  Serial.print("Then open in browser: http://");
  Serial.println(WiFi.softAPIP());

  server.on("/", handleRoot);
  server.on("/move", handleMove);
  server.on("/sensors", handleSensors);
  server.onNotFound(handleNotFound);
  server.begin();
}

void loop() {
  server.handleClient();

  // Non-blocking-ish periodic sensor read (doesn't block server.handleClient much)
  unsigned long now = millis();
  if (now - lastSensorRead >= SENSOR_INTERVAL_MS) {
    lastSensorRead = now;
    updateSensors();
  }
}
