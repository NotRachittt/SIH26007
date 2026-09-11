# THIS IS MAIN 01 PY


import requests
import time
import threading
from collections import Counter

import av
import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import VideoProcessorBase, webrtc_streamer
from ultralytics import YOLO
from streamlit_autorefresh import st_autorefresh


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="FOG//VISION",
    page_icon="🌫️",
    layout="wide"
)

ESP32_URL = "http://192.168.4.1/sensors"

# Refresh dashboard telemetry without rebuilding the video frame.
st_autorefresh(interval=500, key="sensor_refresh")


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Syne:wght@700;800&display=swap');

.stApp {
background:
radial-gradient(circle at 50% -10%, rgba(139,92,246,.11), transparent 34%),
radial-gradient(circle at 100% 55%, rgba(56,189,248,.055), transparent 28%),
#070a0f;
color: #eef2f7;
}

.stApp::before {
content: "";
position: fixed;
inset: 0;
pointer-events: none;
background: repeating-linear-gradient(
180deg,
rgba(255,255,255,.012) 0px,
rgba(255,255,255,.012) 1px,
transparent 1px,
transparent 5px
);
opacity: .22;
z-index: 0;
}

[data-testid="stSidebar"] {
background: #0b0f16;
border-right: 2px solid #242b38;
}

.block-container {
padding-top: 1.0rem;
padding-bottom: 1rem;
max-width: 1500px;
}

.hero {
background: #101620;
border: 2px solid #303847;
border-left: 7px solid #8b5cf6;
box-shadow: 7px 7px 0 #020306;
padding: 20px 26px;
margin-bottom: 16px;
position: relative;
}

.hero h1 {
font-family: 'Syne', sans-serif;
font-size: 42px;
font-weight: 800;
letter-spacing: -2px;
margin: 0;
}

.hero p {
color: #8995aa;
margin: 5px 0 0;
font-size: 12px;
}

.live-pill {
position: absolute;
right: 22px;
top: 22px;
font-size: 11px;
font-weight: 700;
letter-spacing: 1px;
color: #86efac;
}

.section {
font-family: 'Syne', sans-serif;
font-size: 18px;
font-weight: 800;
margin: 7px 0 9px;
}

.card {
background: #101620;
border: 2px solid #303847;
box-shadow: 5px 5px 0 #020306;
padding: 14px;
margin-bottom: 12px;
}

.card.good { border-left: 5px solid #22c55e; }
.card.warn { border-left: 5px solid #f59e0b; }
.card.bad { border-left: 5px solid #ef4444; }

.label {
color: #8490a5;
font-size: 9px;
font-weight: 700;
letter-spacing: 1.2px;
text-transform: uppercase;
}

.value {
font-family: 'Syne', sans-serif;
font-size: 25px;
font-weight: 800;
margin-top: 5px;
}

.muted {
color: #8490a5;
font-size: 11px;
}

.stButton > button {
background: #111722;
color: #f5f7fa;
border: 2px solid #303847;
box-shadow: 4px 4px 0 #020306;
font-weight: 700;
}

.stButton > button:hover {
border-color: #8b5cf6;
color: #fff;
}

footer {
visibility: hidden;
}

/* =======================================================
   NATIVE STREAMLIT TOP HEADER
   ======================================================= */
header[data-testid="stHeader"] {
background: rgba(7,10,15,.96) !important;
border-bottom: 1px solid #273142 !important;
box-shadow: 0 4px 18px rgba(0,0,0,.28) !important;
height: 64px !important;
}

header[data-testid="stHeader"]::before {
content: "SIH PROJECT";
position: absolute;
left: 74px;
top: 23px;
font-family: 'Space Grotesk', sans-serif;
font-size: 10px;
font-weight: 800;
letter-spacing: 2px;
color: #cbd5e1;
}

header[data-testid="stHeader"]::after {
content: "SIH26007";
position: absolute;
left: 50%;
top: 18px;
transform: translateX(-50%);
font-family: 'Syne', sans-serif;
font-size: 16px;
font-weight: 800;
letter-spacing: 1.8px;
color: #a78bfa;
text-shadow: 0 0 16px rgba(167,139,250,.25);
}

header[data-testid="stHeader"] [data-testid="stAppDeployButton"] {
display: none !important;
}

header[data-testid="stHeader"] [data-testid="stToolbar"] {
background: transparent !important;
}

/* The third header label is injected into the header toolbar. */
header[data-testid="stHeader"] [data-testid="stToolbar"]::after {
content: "BRAINBYTE08";
position: absolute;
right: 70px;
top: 23px;
font-family: 'Space Grotesk', sans-serif;
font-size: 9px;
font-weight: 800;
letter-spacing: 1.7px;
color: #7dd3fc;
}

/* Keep the native sidebar control usable above the custom header labels. */
header[data-testid="stHeader"] button {
z-index: 20;
}

@media (max-width: 700px) {
header[data-testid="stHeader"]::before { left: 54px; font-size: 8px; }
header[data-testid="stHeader"]::after { font-size: 13px; }
header[data-testid="stHeader"] [data-testid="stToolbar"]::after { right: 42px; font-size: 7px; }
}


/* =======================================================
PERCEPTION DISPLAY
======================================================= */

.perception-wrap {
position: relative;
overflow: hidden;
background: #080c12;
border: 2px solid #303847;
box-shadow: 7px 7px 0 #020306;
min-height: 520px;
height: 520px;
margin-bottom: 17px;
}

.perception-title {
position: absolute;
top: 14px;
left: 18px;
z-index: 20;
font-family: 'Syne', sans-serif;
font-weight: 800;
font-size: 14px;
letter-spacing: 1px;
}

.perception-state {
position: absolute;
top: 14px;
right: 18px;
z-index: 20;
font-size: 10px;
letter-spacing: 1px;
color: #7dd3fc;
font-weight: 700;
}

.road {
position: absolute;
left: 50%;
top: 0;
transform: translateX(-50%);
width: 58%;
min-width: 390px;
height: 100%;
overflow: hidden;
background:
linear-gradient(90deg,
rgba(255,255,255,.025) 0%,
rgba(255,255,255,.045) 49.5%,
rgba(255,255,255,.045) 50.5%,
rgba(255,255,255,.025) 100%);
clip-path: polygon(27% 0%, 73% 0%, 96% 100%, 4% 100%);
}

.road::before,
.road::after {
content: "";
position: absolute;
top: -160px;
width: 4px;
height: calc(100% + 320px);
background: repeating-linear-gradient(
to bottom,
rgba(139,92,246,.72) 0px,
rgba(139,92,246,.72) 34px,
transparent 34px,
transparent 68px
);
animation: roadFlow 1.15s linear infinite;
}

.road::before { left: 31%; }
.road::after { right: 31%; }

.road-center {
position: absolute;
top: -180px;
left: 50%;
width: 3px;
height: calc(100% + 360px);
transform: translateX(-50%);
background: repeating-linear-gradient(
to bottom,
rgba(255,255,255,.30) 0px,
rgba(255,255,255,.30) 35px,
transparent 35px,
transparent 78px
);
animation: roadFlow .9s linear infinite;
}

@keyframes roadFlow {
from { transform: translateY(0); }
to { transform: translateY(78px); }
}

.road-center {
animation: centerFlow .9s linear infinite;
}

@keyframes centerFlow {
from { top: -180px; }
to { top: -102px; }
}

.distance-line {
position: absolute;
left: 14%;
right: 14%;
height: 1px;
border-top: 1px dashed rgba(148,163,184,.20);
}

.distance-line span {
position: absolute;
left: 2px;
top: -8px;
color: #64748b;
font-size: 8px;
}

.d10 { top: 17%; }
.d25 { top: 34%; }
.d50 { top: 57%; }
.d75 { top: 76%; }

.sensor-cone {
position: absolute;
top: 0;
width: 44%;
height: 78%;
opacity: .18;
pointer-events: none;
}

.cone-left {
left: 4%;
background: linear-gradient(145deg, rgba(56,189,248,.5), transparent 65%);
clip-path: polygon(0 0, 100% 0, 72% 100%, 0 100%);
}

.cone-right {
right: 4%;
background: linear-gradient(215deg, rgba(56,189,248,.5), transparent 65%);
clip-path: polygon(0 0, 100% 0, 100% 100%, 28% 100%);
}

.sensor-tag {
position: absolute;
top: 72px;
z-index: 10;
padding: 5px 8px;
background: rgba(7,10,15,.85);
border: 1px solid #334155;
font-size: 9px;
font-weight: 700;
color: #94a3b8;
}

.sensor-tag.left { left: 18px; }
.sensor-tag.right { right: 18px; }

.vehicle {
position: absolute;
z-index: 15;
left: 50%;
bottom: 48px;
transform: translateX(-50%);
width: 76px;
height: 132px;
filter: drop-shadow(0 14px 15px rgba(0,0,0,.65));
}

.vehicle-body {
position: absolute;
left: 9px;
right: 9px;
top: 4px;
bottom: 4px;
border-radius: 24px 24px 15px 15px;
background: linear-gradient(105deg,#4b5563 0%,#e5e7eb 20%,#ffffff 48%,#9ca3af 78%,#374151 100%);
box-shadow: inset 5px 0 8px rgba(255,255,255,.45), inset -6px 0 10px rgba(0,0,0,.35), 0 0 24px rgba(139,92,246,.25);
transform: perspective(260px) rotateX(7deg);
}

.vehicle-roof {
position: absolute;
left: 17px;
right: 17px;
top: 29px;
height: 66px;
border-radius: 17px 17px 12px 12px;
background: linear-gradient(110deg,#0f172a,#334155 38%,#0b1220 75%,#020617);
box-shadow: inset 2px 2px 5px rgba(255,255,255,.22), inset -3px -5px 8px rgba(0,0,0,.65);
}

.vehicle-windshield {
position: absolute;
left: 20px;
right: 20px;
top: 36px;
height: 30px;
clip-path: polygon(12% 0,88% 0,100% 100%,0 100%);
background: linear-gradient(110deg,#475569,#0f172a 45%,#64748b 100%);
opacity:.92;
}

.vehicle-rear-glass {
position: absolute;
left: 21px;
right: 21px;
top: 70px;
height: 21px;
clip-path: polygon(0 0,100% 0,88% 100%,12% 100%);
background: linear-gradient(110deg,#1e293b,#020617 55%,#475569);
}

.vehicle-light {
position: absolute;
top: 9px;
width: 17px;
height: 7px;
border-radius: 8px 8px 3px 3px;
background:#f8fafc;
box-shadow:0 0 9px rgba(255,255,255,.9);
}
.vehicle-light.left{left:16px}.vehicle-light.right{right:16px}

.vehicle-taillight {
position: absolute;
bottom: 10px;
width: 19px;
height: 7px;
border-radius:3px 3px 8px 8px;
background:#ef4444;
box-shadow:0 0 8px rgba(239,68,68,.75);
}
.vehicle-taillight.left{left:15px}.vehicle-taillight.right{right:15px}

.vehicle-wheel {
position:absolute;
width:9px;
height:28px;
border-radius:5px;
background:#020617;
box-shadow:0 2px 4px rgba(0,0,0,.7);
}
.vehicle-wheel.left{left:4px;top:36px}.vehicle-wheel.right{right:4px;top:36px}
.vehicle-wheel.left2{left:4px;bottom:27px}.vehicle-wheel.right2{right:4px;bottom:27px}

.vehicle-glow {
position:absolute;
left:50%;
bottom:-3px;
width:105px;
height:28px;
transform:translateX(-50%);
background:radial-gradient(ellipse,rgba(139,92,246,.42),transparent 70%);
z-index:-1;
}

.vehicle-label {
position: absolute;
bottom: 24px;
left: 50%;
transform: translateX(-50%);
color: #94a3b8;
font-size: 8px;
letter-spacing: 1.5px;
font-weight: 700;
white-space: nowrap;
}

.target-3d { position:relative; width:30px; height:30px; transform:perspective(100px) rotateX(55deg) rotateZ(-1deg); }
.target-body { position:absolute; left:4px; right:4px; bottom:2px; height:18px; background:linear-gradient(90deg,#713f12,#f59e0b 45%,#78350f); border:1px solid #fbbf24; box-shadow:0 5px 7px rgba(0,0,0,.5); }
.target-top { position:absolute; left:6px; right:6px; top:3px; height:11px; background:linear-gradient(135deg,#fde68a,#f59e0b 55%,#92400e); transform:skewX(-18deg); border:1px solid #fbbf24; z-index:2; }
.obstacle.danger .target-body { background:linear-gradient(90deg,#7f1d1d,#ef4444 45%,#450a0a); border-color:#fca5a5; }
.obstacle.danger .target-top { background:linear-gradient(135deg,#fecaca,#ef4444 55%,#7f1d1d); border-color:#fca5a5; }

.obstacle {
position: absolute;
z-index: 14;
transform: translate(-50%, -50%);
width: 48px;
height: 48px;
border: 2px solid #f59e0b;
background: rgba(245,158,11,.10);
box-shadow: 0 0 18px rgba(245,158,11,.25);
display: flex;
align-items: center;
justify-content: center;
font-size: 23px;
transition: left .35s ease, top .35s ease, border-color .25s ease,
box-shadow .25s ease, background .25s ease;
}

.obstacle.danger {
border-color: #ef4444;
background: rgba(239,68,68,.18);
box-shadow: 0 0 24px rgba(239,68,68,.45);
animation: obstaclePulse .7s ease-in-out infinite alternate;
}

.obstacle.caution {
border-color: #f59e0b;
}

.obstacle.clear {
opacity: 0;
}

@keyframes obstaclePulse {
from { box-shadow: 0 0 10px rgba(239,68,68,.20); }
to { box-shadow: 0 0 28px rgba(239,68,68,.60); }
}

.obstacle-info {
position: absolute;
top: 100%;
margin-top: 5px;
white-space: nowrap;
background: rgba(7,10,15,.90);
border: 1px solid #334155;
padding: 4px 7px;
font-size: 8px;
color: #cbd5e1;
}

.range-label {
position: absolute;
z-index: 9;
color: #64748b;
font-size: 8px;
letter-spacing: 1px;
}

.left-range { left: 18%; top: 46%; }
.right-range { right: 18%; top: 46%; }

.edge-alert {
position: absolute;
z-index: 30;
top: 0;
bottom: 0;
width: 10%;
pointer-events: none;
opacity: 0;
transition: opacity .25s ease;
}

.edge-alert.left {
left: 0;
background: linear-gradient(90deg, rgba(239,68,68,.22), transparent);
}

.edge-alert.right {
right: 0;
background: linear-gradient(270deg, rgba(239,68,68,.22), transparent);
}

.edge-alert.active {
opacity: 1;
animation: edgePulse 1.1s ease-in-out infinite;
}

@keyframes edgePulse {
0%, 100% { opacity: .45; }
50% { opacity: .95; }
}

.front-alert {
position: absolute;
z-index: 31;
left: 50%;
bottom: 12px;
transform: translateX(-50%);
padding: 7px 13px;
background: rgba(7,10,15,.92);
border: 1px solid #334155;
font-size: 9px;
font-weight: 800;
letter-spacing: 1.2px;
}

.front-alert.danger {
border-color: #ef4444;
color: #fca5a5;
}

.front-alert.caution {
border-color: #f59e0b;
color: #fcd34d;
}

.front-alert.safe {
border-color: #22c55e;
color: #86efac;
}


/* =======================================================
TELEMETRY
======================================================= */

.telemetry {
display: grid;
grid-template-columns: repeat(7, 1fr);
gap: 8px;
margin-bottom: 16px;
}

.telemetry-box {
background: #101620;
border: 1px solid #303847;
padding: 10px 11px;
min-height: 66px;
}

.telemetry-value {
font-family: 'Syne', sans-serif;
font-size: 19px;
font-weight: 800;
margin-top: 4px;
}

.telemetry-sub {
color: #64748b;
font-size: 9px;
margin-top: 2px;
}


/* =======================================================
EVENT LOG
======================================================= */

.log-panel {
background: #0a0f16;
border: 2px solid #303847;
box-shadow: 5px 5px 0 #020306;
height: 270px;
overflow-y: auto;
padding: 9px;
}

.log-row {
display: grid;
grid-template-columns: 68px 62px 1fr;
gap: 7px;
padding: 6px 4px;
border-bottom: 1px solid #1b2330;
font-family: monospace;
font-size: 9px;
}

.log-time { color: #64748b; }
.log-type { font-weight: 800; }
.log-info { color: #cbd5e1; }

.log-good { color: #4ade80; }
.log-warn { color: #fbbf24; }
.log-danger { color: #f87171; }
.log-info-type { color: #60a5fa; }


/* =======================================================
RESPONSIVE
======================================================= */

@media (max-width: 900px) {
.telemetry {
grid-template-columns: repeat(4, 1fr);
}

.road {
width: 75%;
}
}


/* =======================================================
   UPGRADED HMI / NAV / STATUS SYSTEM
======================================================= */

.top-nav {
position: relative;
z-index: 50;
display: grid;
grid-template-columns: 1fr auto 1fr;
align-items: center;
min-height: 46px;
padding: 0 15px;
margin-bottom: 12px;
background: rgba(10,14,21,.94);
border: 1px solid #303847;
box-shadow: 4px 4px 0 #020306;
font-size: 10px;
font-weight: 800;
letter-spacing: 1.8px;
text-transform: uppercase;
}

.top-nav .nav-left { justify-self: start; color: #cbd5e1; }
.top-nav .nav-center { justify-self: center; color: #a78bfa; font-family: 'Syne', sans-serif; font-size: 13px; }
.top-nav .nav-right { justify-self: end; color: #7dd3fc; }

.nav-dot {
display: inline-block;
width: 6px;
height: 6px;
border-radius: 50%;
margin-right: 7px;
background: #22c55e;
box-shadow: 0 0 10px rgba(34,197,94,.85);
animation: navPulse 1.3s ease-in-out infinite;
}

@keyframes navPulse { 0%,100% { opacity:.45; } 50% { opacity:1; } }

.system-strip {
display: grid;
grid-template-columns: repeat(4, 1fr);
gap: 8px;
margin: -4px 0 16px;
}

.system-chip {
background: rgba(11,16,24,.82);
border: 1px solid #293241;
padding: 7px 10px;
font-size: 9px;
letter-spacing: 1px;
font-weight: 800;
color: #94a3b8;
}

.system-chip strong { color: #e2e8f0; }
.system-chip.live strong { color: #86efac; }
.system-chip.ai strong { color: #c4b5fd; }
.system-chip.link strong { color: #7dd3fc; }
.system-chip.safe strong { color: #fcd34d; }

.hero {
background:
linear-gradient(120deg, rgba(16,22,32,.98), rgba(13,18,27,.96));
border-top: 1px solid #414b5e;
}

.hero::after {
content: "";
position: absolute;
right: 0;
bottom: 0;
width: 190px;
height: 2px;
background: linear-gradient(90deg, transparent, #8b5cf6);
box-shadow: 0 0 14px rgba(139,92,246,.6);
}

.hero h1 { text-shadow: 0 0 28px rgba(139,92,246,.18); }

.perception-wrap {
background:
radial-gradient(circle at 50% 42%, rgba(139,92,246,.055), transparent 35%),
linear-gradient(180deg, #080c12 0%, #090d14 100%);
}

.perception-wrap::before {
content: "";
position: absolute;
inset: 0;
z-index: 4;
pointer-events: none;
background:
linear-gradient(90deg, transparent 49.8%, rgba(125,211,252,.045) 50%, transparent 50.2%),
linear-gradient(0deg, transparent 49.8%, rgba(125,211,252,.035) 50%, transparent 50.2%);
background-size: 100% 100%, 100% 100%;
}

.perception-wrap::after {
content: "";
position: absolute;
left: 10%;
right: 10%;
top: 18%;
height: 1px;
z-index: 5;
background: linear-gradient(90deg, transparent, rgba(125,211,252,.35), transparent);
box-shadow: 0 0 18px rgba(125,211,252,.18);
animation: scanSweep 3.2s linear infinite;
pointer-events: none;
}

@keyframes scanSweep {
0% { top: 17%; opacity: 0; }
12% { opacity: .7; }
82% { opacity: .7; }
100% { top: 84%; opacity: 0; }
}

.perception-meta {
position: absolute;
z-index: 22;
left: 18px;
bottom: 17px;
font-family: monospace;
font-size: 8px;
letter-spacing: 1px;
color: #64748b;
}

.telemetry-box {
position: relative;
overflow: hidden;
transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease;
}
.telemetry-box:hover {
transform: translateY(-2px);
border-color: #475569;
box-shadow: 0 7px 18px rgba(0,0,0,.24);
}
.telemetry-box::after {
content: "";
position: absolute;
left: 0;
bottom: 0;
width: 100%;
height: 2px;
background: linear-gradient(90deg, transparent, rgba(139,92,246,.65), transparent);
opacity: .55;
}

.log-panel {
scrollbar-width: thin;
scrollbar-color: #334155 transparent;
}

.footer-shell {
margin-top: 26px;
padding: 18px 4px 4px;
border-top: 1px solid #273142;
text-align: center;
}
.footer-brand {
font-family: 'Syne', sans-serif;
font-size: 15px;
font-weight: 800;
letter-spacing: 1px;
}
.footer-sub {
margin-top: 4px;
font-size: 9px;
letter-spacing: 1.3px;
color: #64748b;
text-transform: uppercase;
}
.footer-repo {
display: inline-block;
text-decoration: none;
margin-top: 12px;
padding: 8px 15px;
border: 1px solid #3b4658;
background: #0d131d;
color: #c4b5fd;
font-size: 9px;
font-weight: 800;
letter-spacing: 1.3px;
text-transform: uppercase;
}
.footer-copy {
margin-top: 11px;
font-size: 8px;
color: #475569;
letter-spacing: 1px;
}

@media (max-width: 900px) {
.top-nav { grid-template-columns: 1fr 1fr; }
.top-nav .nav-center { justify-self: end; }
.top-nav .nav-right { display: none; }
.system-strip { grid-template-columns: repeat(2,1fr); }
}

</style>""", unsafe_allow_html=True)


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">
<div class="live-pill">● LIVE SYSTEM</div>
<h1>FOG//VISION</h1>
<p>AI PERCEPTION • ROBOT SENSOR FUSION • FOG / VISIBILITY • V2V SAFETY</p>
</div>

<div class="system-strip">
<div class="system-chip live"><strong>● ESP32</strong> &nbsp; SENSOR LINK</div>
<div class="system-chip ai"><strong>◈ YOLO</strong> &nbsp; VISION ENGINE</div>
<div class="system-chip link"><strong>◉ V2V</strong> &nbsp; SAFETY MODULE</div>
<div class="system-chip safe"><strong>▣ HUD</strong> &nbsp; PERCEPTION ACTIVE</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# MODEL
# =========================================================

@st.cache_resource
def get_model():
    return YOLO("yolo11n.pt")


# =========================================================
# ESP32
# =========================================================

def get_esp32_sensors():
    try:
        r = requests.get(ESP32_URL, timeout=0.2)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass

    return {
        "dist1": -1,
        "dist2": -1,
        "ir1": False,
        "ir2": False,
        "alert": "offline"
    }


# =========================================================
# VISIBILITY
# =========================================================

def analyze_visibility(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    contrast = float(np.std(gray))

    sharpness = float(
        cv2.Laplacian(gray, cv2.CV_64F).var()
    )

    contrast_score = np.clip(
        (contrast - 10.0) / 65.0,
        0.0,
        1.0
    )

    sharpness_score = np.clip(
        np.log1p(sharpness) / 9.0,
        0.0,
        1.0
    )

    score = float(
        np.clip(
            (
                0.55 * contrast_score
                + 0.45 * sharpness_score
            ) * 100,
            0,
            100
        )
    )

    if score >= 70:
        condition = "CLEAR"
    elif score >= 45:
        condition = "LIGHT FOG"
    elif score >= 25:
        condition = "DENSE FOG"
    else:
        condition = "SEVERE FOG"

    return score, condition


# =========================================================
# VIDEO PROCESSOR
# =========================================================

class FogVisionProcessor(VideoProcessorBase):

    def __init__(self):
        self.model = get_model()
        self.confidence = 0.35
        self.frame_no = 0
        self.last_detections = []
        self.last_visibility = 0.0
        self.last_condition = "ANALYZING"
        self.fps = 0.0
        self._last_time = time.perf_counter()
        self._lock = threading.Lock()

    def recv(self, frame):

        image = frame.to_ndarray(format="bgr24")
        self.frame_no += 1

        h, w = image.shape[:2]

        if w > 960:
            scale = 960.0 / w
            image = cv2.resize(
                image,
                (int(w * scale), int(h * scale)),
                interpolation=cv2.INTER_AREA
            )

        visibility, condition = analyze_visibility(image)

        if self.frame_no % 3 == 0:
            try:
                results = self.model.predict(
                    image,
                    conf=self.confidence,
                    imgsz=512,
                    verbose=False
                )

                result = results[0]
                detections = []

                if result.boxes is not None:
                    for box in result.boxes:
                        cls_id = int(box.cls[0])
                        conf = float(box.conf[0])

                        x1, y1, x2, y2 = map(
                            int,
                            box.xyxy[0].tolist()
                        )

                        detections.append(
                            (
                                str(result.names[cls_id]),
                                conf,
                                x1,
                                y1,
                                x2,
                                y2
                            )
                        )

                with self._lock:
                    self.last_detections = detections

            except Exception:
                pass

        with self._lock:
            detections = list(self.last_detections)
            self.last_visibility = visibility
            self.last_condition = condition

        now = time.perf_counter()
        instant = 1.0 / max(
            now - self._last_time,
            0.001
        )

        self.fps = (
            instant
            if self.fps == 0
            else 0.85 * self.fps + 0.15 * instant
        )

        self._last_time = now

        for (
            name,
            conf,
            x1,
            y1,
            x2,
            y2
        ) in detections:

            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                (139, 92, 246),
                2
            )

            label = f"{name} {conf:.0%}"
            ty = max(24, y1 - 7)

            cv2.rectangle(
                image,
                (x1, ty - 22),
                (
                    x1 + max(115, len(label) * 9),
                    ty + 3
                ),
                (7, 10, 15),
                -1
            )

            cv2.putText(
                image,
                label,
                (x1 + 5, ty),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.52,
                (245, 245, 245),
                2,
                cv2.LINE_AA
            )

        cv2.rectangle(
            image,
            (0, 0),
            (image.shape[1], 46),
            (7, 10, 15),
            -1
        )

        cv2.putText(
            image,
            f"FOG//VISION | FPS {self.fps:04.1f} | OBJECTS {len(detections):02d}",
            (14, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.62,
            (242, 245, 250),
            2,
            cv2.LINE_AA
        )

        y1 = image.shape[0] - 86

        cv2.rectangle(
            image,
            (14, y1),
            (365, image.shape[0] - 14),
            (7, 10, 15),
            -1
        )

        cv2.putText(
            image,
            f"VISIBILITY INDEX {visibility:04.0f}/100",
            (28, y1 + 27),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.56,
            (242, 245, 250),
            2,
            cv2.LINE_AA
        )

        cv2.putText(
            image,
            condition,
            (28, y1 + 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.62,
            (139, 92, 246),
            2,
            cv2.LINE_AA
        )

        return av.VideoFrame.from_ndarray(
            image,
            format="bgr24"
        )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## SYSTEM")

    st.markdown("### CAMERA SOURCE")

    st.caption(
        "Press START and choose Camo / Realme / webcam in the browser."
    )

    st.markdown("### AI MODEL")

    st.code("yolo11n.pt")

    confidence = st.slider(
        "Detection confidence",
        0.10,
        0.90,
        0.35,
        0.05
    )

    st.divider()

    st.markdown("### PERCEPTION")

    st.markdown(
        "📡 ULTRASONIC RANGE\n\n"
        "↓\n\n"
        "🔴 PROXIMITY ZONE\n\n"
        "↓\n\n"
        "🚗 VEHICLE SAFETY"
    )

    st.divider()

    st.caption(
        "The animated perception display is driven by live ESP32 sensor values."
    )


# =========================================================
# SENSOR DATA
# =========================================================

sensor_data = get_esp32_sensors()

# Physical mounting is opposite to dashboard sides.
# dist2 is the physical LEFT sensor; dist1 is the physical RIGHT sensor.
us_left = float(sensor_data.get("dist2", -1))
us_right = float(sensor_data.get("dist1", -1))
# Current IR modules are active-LOW:
# LOW = obstacle detected, HIGH = clear.
# The ESP32 currently exposes the raw logical reading, so invert it here.
ir_left = not bool(sensor_data.get("ir1", False))
ir_right = not bool(sensor_data.get("ir2", False))
alert = str(sensor_data.get("alert", "offline")).lower()


# =========================================================
# SENSOR HELPERS
# =========================================================

def valid_distance(value):
    return value > 0


def distance_state(distance):
    if distance <= 0:
        return "offline"
    if distance < 30:
        return "danger"
    if distance < 60:
        return "caution"
    return "clear"


def obstacle_top(distance):
    """
    Map distance to a vertical perception position.
    Nearer obstacle = lower on screen, closer to vehicle.
    10 cm -> ~80%
    150+ cm -> ~12%
    """
    if distance <= 0:
        return 0

    d = min(max(distance, 10), 150)

    ratio = (150 - d) / 140

    return 14 + ratio * 68


def obstacle_class(distance, ir):
    if ir or (distance > 0 and distance < 30):
        return "danger"

    if distance > 0 and distance < 60:
        return "caution"

    if distance > 0:
        return "clear"

    return "clear"


left_state = distance_state(us_left)
right_state = distance_state(us_right)

left_danger = (
    ir_left
    or (us_left > 0 and us_left < 30)
)

right_danger = (
    ir_right
    or (us_right > 0 and us_right < 30)
)

left_caution = (
    not left_danger
    and us_left > 0
    and us_left < 60
)

right_caution = (
    not right_danger
    and us_right > 0
    and us_right < 60
)

front_danger = left_danger and right_danger

if front_danger:
    display_alert = "DANGER"
    alert_class = "danger"
elif left_danger or right_danger:
    display_alert = "SIDE DANGER"
    alert_class = "danger"
elif left_caution or right_caution or alert == "caution":
    display_alert = "CAUTION"
    alert_class = "caution"
elif alert == "offline":
    display_alert = "SENSOR OFFLINE"
    alert_class = "caution"
else:
    display_alert = "SAFE"
    alert_class = "safe"


# =========================================================
# EVENT LOG
# =========================================================

if "event_log" not in st.session_state:
    st.session_state.event_log = []

if "last_sensor_state" not in st.session_state:
    st.session_state.last_sensor_state = None

def add_log(kind, message):
    now = time.strftime("%H:%M:%S")

    st.session_state.event_log.insert(
        0,
        {
            "time": now,
            "kind": kind,
            "message": message
        }
    )

    st.session_state.event_log = (
        st.session_state.event_log[:30]
    )


sensor_state = (
    left_danger,
    right_danger,
    left_caution,
    right_caution,
    ir_left,
    ir_right,
    alert
)

if st.session_state.last_sensor_state is None:
    add_log("INFO", "ESP32 sensor telemetry connected")

elif sensor_state != st.session_state.last_sensor_state:

    if front_danger:
        add_log(
            "DANGER",
            "Front obstruction detected on both sensor zones"
        )
    elif left_danger:
        add_log(
            "DANGER",
            f"Left-side proximity critical • {us_left:.0f} cm"
        )
    elif right_danger:
        add_log(
            "DANGER",
            f"Right-side proximity critical • {us_right:.0f} cm"
        )
    elif left_caution:
        add_log(
            "WARN",
            f"Left obstacle approaching • {us_left:.0f} cm"
        )
    elif right_caution:
        add_log(
            "WARN",
            f"Right obstacle approaching • {us_right:.0f} cm"
        )
    elif ir_left:
        add_log(
            "WARN",
            "Left IR detected near-field obstacle"
        )
    elif ir_right:
        add_log(
            "WARN",
            "Right IR detected near-field obstacle"
        )
    else:
        add_log(
            "INFO",
            "Obstacle condition changed / cleared"
        )

st.session_state.last_sensor_state = sensor_state


# =========================================================
# PERCEPTION DISPLAY
# =========================================================

left_top = obstacle_top(us_left)
right_top = obstacle_top(us_right)

left_cls = obstacle_class(us_left, ir_left)
right_cls = obstacle_class(us_right, ir_right)

left_text = (
    f"{us_left:.0f} cm"
    if us_left > 0
    else "--"
)

right_text = (
    f"{us_right:.0f} cm"
    if us_right > 0
    else "--"
)

left_style = (
    f"left:30%; top:{left_top:.1f}%;"
    if us_left > 0
    else "left:30%; top:15%;"
)

right_style = (
    f"left:70%; top:{right_top:.1f}%;"
    if us_right > 0
    else "left:70%; top:15%;"
)

left_obstacle_opacity = "1" if us_left > 0 else "0"
right_obstacle_opacity = "1" if us_right > 0 else "0"

st.markdown(
f"""
<div class="section">◈ LIVE ROBOT PERCEPTION</div>

<div class="perception-wrap">

<div class="perception-title">
FORWARD SENSOR FIELD
</div>

<div class="perception-state">
{display_alert}
</div>

<div class="edge-alert left {'active' if left_danger else ''}"></div>
<div class="edge-alert right {'active' if right_danger else ''}"></div>

<div class="road">

<div class="road-center"></div>

<div class="distance-line d10"><span>100 CM</span></div>
<div class="distance-line d25"><span>75 CM</span></div>
<div class="distance-line d50"><span>50 CM</span></div>
<div class="distance-line d75"><span>25 CM</span></div>

<div class="sensor-cone cone-left"></div>
<div class="sensor-cone cone-right"></div>

<div
class="obstacle {left_cls}"
style="{left_style} opacity:{left_obstacle_opacity};"
>
<div class="target-3d"><div class="target-top"></div><div class="target-body"></div></div>
<div class="obstacle-info">
US-L • {left_text}
</div>
</div>

<div
class="obstacle {right_cls}"
style="{right_style} opacity:{right_obstacle_opacity};"
>
<div class="target-3d"><div class="target-top"></div><div class="target-body"></div></div>
<div class="obstacle-info">
US-R • {right_text}
</div>
</div>

<div class="vehicle">
<div class="vehicle-body">
<div class="vehicle-light left"></div><div class="vehicle-light right"></div>
<div class="vehicle-roof"></div>
<div class="vehicle-windshield"></div>
<div class="vehicle-rear-glass"></div>
<div class="vehicle-taillight left"></div><div class="vehicle-taillight right"></div>
</div>
<div class="vehicle-wheel left"></div><div class="vehicle-wheel right"></div>
<div class="vehicle-wheel left2"></div><div class="vehicle-wheel right2"></div>
<div class="vehicle-glow"></div>
</div>

<div class="vehicle-label">
YOUR VEHICLE
</div>

</div>

<div class="sensor-tag left">
US-L • {left_text}
</div>

<div class="sensor-tag right">
US-R • {right_text}
</div>

<div class="range-label left-range">
LONG RANGE
</div>

<div class="range-label right-range">
LONG RANGE
</div>

<div class="front-alert {alert_class}">
{'⚠ FRONT DANGER' if front_danger else
'◀ LEFT DANGER' if left_danger else
'RIGHT DANGER ▶' if right_danger else
'⚠ CAUTION' if alert_class == 'caution' else
'● PERCEPTION CLEAR'}
</div>

<div class="perception-meta">
LIVE FUSION // ULTRASONIC + IR // 10–150 CM MODELLED RANGE
</div>

</div>""",
unsafe_allow_html=True
)


# =========================================================
# TELEMETRY
# =========================================================

visibility_value = 0.0
condition_value = "ANALYZING"
object_count = 0
camera_fps = 0.0

# =========================================================
# CAMERA + LOG
# =========================================================

left, right = st.columns(
    [1.55, 1],
    gap="large"
)


# =========================================================
# CAMERA
# =========================================================

with left:

    st.markdown(
        '<div class="section">📹 LIVE CAMERA + YOLO</div>',
        unsafe_allow_html=True
    )

    ctx = webrtc_streamer(
        key="fog-vision",
        video_processor_factory=FogVisionProcessor,
        media_stream_constraints={
            "video": True,
            "audio": False
        },
        async_processing=True,
    )

    if ctx.video_processor:

        p = ctx.video_processor

        visibility_value = p.last_visibility
        condition_value = p.last_condition
        object_count = len(p.last_detections)
        camera_fps = p.fps

        # Add only meaningful new YOLO detections to the log.
        if (
            p.last_detections
            and st.session_state.get("last_object_count") != object_count
        ):
            counts = Counter(
                d[0]
                for d in p.last_detections
            )

            object_summary = ", ".join(
                f"{k} x{v}"
                for k, v in counts.items()
            )

            add_log(
                "DETECT",
                f"YOLO objects • {object_summary}"
            )

        st.session_state.last_object_count = object_count

    else:

        st.markdown(
"""
<div class="card">
<div class="label">CAMERA STATUS</div>
<div class="value">STANDBY</div>
<div class="muted">Press START and allow camera access.</div>
</div>""",
            unsafe_allow_html=True
        )


# =========================================================
# EVENT LOG
# =========================================================

with right:

    st.markdown(
        '<div class="section">◉ EVENT LOG</div>',
        unsafe_allow_html=True
    )

    rows = []

    for event in st.session_state.event_log:

        kind = event["kind"]

        if kind == "DANGER":
            kind_class = "log-danger"
        elif kind == "WARN":
            kind_class = "log-warn"
        elif kind == "DETECT":
            kind_class = "log-good"
        else:
            kind_class = "log-info-type"

        rows.append(
            f"""
<div class="log-row">
<div class="log-time">{event["time"]}</div>
<div class="log-type {kind_class}">{kind}</div>
<div class="log-info">{event["message"]}</div>
</div>
"""
        )

    if not rows:
        rows.append(
            """
<div class="log-row">
<div class="log-time">--:--:--</div>
<div class="log-type log-info-type">INFO</div>
<div class="log-info">Waiting for events...</div>
</div>
"""
        )

    st.markdown(
        '<div class="log-panel">' +
        "".join(rows) +
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# TELEMETRY BAR
# =========================================================

st.markdown(
    '<div class="section">▣ LIVE TELEMETRY</div>',
    unsafe_allow_html=True
)

sensor_link = (
    "CONNECTED"
    if alert != "offline"
    else "OFFLINE"
)

visibility_text = (
    f"{visibility_value:.0f}/100"
    if ctx.video_processor
    else "--"
)

fog_text = (
    condition_value
    if ctx.video_processor
    else "--"
)

fps_text = (
    f"{camera_fps:.1f}"
    if ctx.video_processor
    else "--"
)

st.markdown(
f"""
<div class="telemetry">

<div class="telemetry-box">
<div class="label">US-L</div>
<div class="telemetry-value">{left_text}</div>
<div class="telemetry-sub">LEFT RANGE</div>
</div>

<div class="telemetry-box">
<div class="label">US-R</div>
<div class="telemetry-value">{right_text}</div>
<div class="telemetry-sub">RIGHT RANGE</div>
</div>

<div class="telemetry-box">
<div class="label">IR-L</div>
<div class="telemetry-value">{'OBSTACLE' if ir_left else 'CLEAR'}</div>
<div class="telemetry-sub">NEAR FIELD</div>
</div>

<div class="telemetry-box">
<div class="label">IR-R</div>
<div class="telemetry-value">{'OBSTACLE' if ir_right else 'CLEAR'}</div>
<div class="telemetry-sub">NEAR FIELD</div>
</div>

<div class="telemetry-box">
<div class="label">VISIBILITY</div>
<div class="telemetry-value">{visibility_text}</div>
<div class="telemetry-sub">{fog_text}</div>
</div>

<div class="telemetry-box">
<div class="label">YOLO</div>
<div class="telemetry-value">{object_count:02d}</div>
<div class="telemetry-sub">OBJECTS • {fps_text} FPS</div>
</div>

<div class="telemetry-box">
<div class="label">SAFETY</div>
<div class="telemetry-value">{display_alert}</div>
<div class="telemetry-sub">ESP32 {sensor_link}</div>
</div>

</div>""",
unsafe_allow_html=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer-shell">
<div class="footer-brand">FOG//VISION</div>
<div class="footer-sub">SIH26007 • BRAINBYTE08 • SMART INDIA HACKATHON 2026</div>
<a class="footer-repo" href="https://github.com/NotRachittt/SIH26007" target="_blank" rel="noopener noreferrer">⌘ &nbsp; GITHUB REPOSITORY &nbsp; • &nbsp; SIH26007</a>
<div class="footer-copy">© 2026 BRAINBYTE08 • AI PERCEPTION + SENSOR FUSION + V2V SAFETY</div>
</div>
""", unsafe_allow_html=True)
