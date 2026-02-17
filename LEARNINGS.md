Pokémon Platinum Cynthia AI
Engineering Learnings Log
1️⃣ Headless Emulator ≠ Visual Emulator
Problem

Using py-desmume (headless build) produced blank screenshots.

Root Cause

The Python binding runs the core emulator without a renderer.
There is no framebuffer exposed to Python.

Internal screenshot calls return empty frames by design.

Resolution

Switched to:

DeSmuME 0.9.13 x64 GUI (manually launched)

OS-level screen capture using dxcam

Key Insight:

If you want pixels, you must capture the window that renders them.

2️⃣ OS-Level Capture is Stable on Windows

Using dxcam (DirectX Desktop Duplication API):

Captures full monitor reliably

Works at high FPS

Low latency

Stable in Windows 10/11

Architecture decision:

Emulator GUI → Windows Desktop → dxcam → NumPy → OpenCV


This separates:

Rendering

Vision

Control logic

Good design principle:

Keep vision independent from emulator internals.

3️⃣ Window Activation is Dangerous

Using:

window.activate()


Caused Windows focus errors:

PyGetWindowException: Error code 0


Modern Windows blocks background apps from stealing focus.

Resolution

Removed window activation entirely.
Require user to focus emulator before running script.

Lesson:

Avoid OS-level window manipulation when unnecessary.

4️⃣ Key Mapping Matters

Original mapping used arrow keys.

Problem:
Synthetic arrow injection was unreliable and conflicted with OS behavior.

Resolution

Remapped controls in DeSmuME:

Movement:

W → Up

A → Left

S → Down

D → Right

DS Buttons:

K → A

J → B

H → Y

U → X

Now all injected keys are standard character keys.

Lesson:

Use simple keyboard keys for automation stability

5️⃣ Dialogue Detection Strategy Evolution
❌ Attempt 1: Mean Brightness

Used average brightness of bottom region.

Failed because:

Dialogue includes white + purple + dark text

Mean brightness unstable

❌ Attempt 2: Purple Border HSV Detection

Too sensitive to scaling and color shifts.

Unreliable.

✅ Final Solution: UI Symbol Detection

Detected the small white triangle in bottom-right of dialogue box.

Implementation:

Crop bottom-right region

Count pixels > threshold

Detect ratio of bright pixels

Why it works:

High contrast

Consistent position

Unique to dialogue

Minimal false positives

Key Insight:

Detect stable UI elements, not global brightness.

6️⃣ Perception → Decision → Action Loop

System now successfully performs:

Capture frame

Crop emulator region

Extract top screen

Detect dialogue via arrow

Press DS A (mapped to K)

Otherwise move upward

This confirms a working closed loop:

Observe → Decide → Act


This is the first true autonomous behavior milestone.

7️⃣ Debugging Methodology Used

Instead of guessing, we:

Printed brightness values

Printed detection ratios

Printed key injection events

Removed silent failuresEliminated OS focus issues

Isolated failing layers

Systematically isolated:

Vision

Control

Window management

Key injection

Lesson:

Always instrument the failing subsystem.

8️⃣ Architecture Status

Current stack:

Emulator: DeSmuME GUI

Capture: dxcam

Vision: OpenCV

Input: pyautogui

Window detection: pygetwindow

State loop: Python

Design principles followed:

No infinite loops without delay

Separate vision from control

No emulator memory reading

Fully pixel-based perception

🧠 Current Capability

The agent can:

Walk

Trigger NPC interaction

Detect dialogue UI

Advance dialogue automatically

This marks the completion of:

Stage 3 – OS-Level Vision Integration

🚀 Next Stage

Build structured behavior:

State machine

Collision detection

Exploration logic

Deterministic navigation

Eventually: battle automation

Core Engineering Insight So Far

Vision-based automation is only as good as the UI anchors you choose.

The dialogue triangle became the first reliable anchor.

Future anchors will include:

HP bars

Battle menus

Gym badges

Doorways

Player sprite position





