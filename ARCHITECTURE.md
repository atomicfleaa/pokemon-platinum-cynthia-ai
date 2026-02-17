Pokémon Platinum Cynthia AI
System Architecture
1️⃣ High-Level System Overview

The project uses a vision-driven control architecture.

The emulator is treated as a black box.

There is:

No memory reading

No emulator internals access

No save-state manipulation for decision making

All intelligence is derived from pixels.

Core loop:

Emulator (GUI)
        ↓
Windows Desktop
        ↓
dxcam Capture
        ↓
Vision Processing (OpenCV)
        ↓
Decision Logic
        ↓
Key Injection (pyautogui)
        ↓
Emulator


This forms a closed loop.

2️⃣ System Components
Emulator Layer

DeSmuME 0.9.13 x64 GUI

Launched manually

Uses custom keyboard mapping

Renders pixels to Windows desktop

Role:

Pure execution environment

Capture Layer

Library:

dxcam

Function:

Captures full monitor frame

Crops emulator window region

Extracts top DS screen only

Output:

NumPy array (BGR image)

Design principle:

Vision must be OS-level and independent of emulator internals.

Vision Layer

Library:

OpenCV

NumPy

Responsibilities:

Crop regions of interest

Detect UI elements

Detect dialogue arrow

Detect state transitions

Vision currently detects:

Dialogue active state via bottom-right arrow

Future vision modules may detect:

HP bars

Battle menus

Player sprite movement

Collision

Map transitions

Design principle:

Detect stable UI anchors, not global brightness.

Control Layer

Library:

pyautogui

Function:

Inject key presses into focused emulator window

Key mapping strategy:

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

Design principle:

Use standard keyboard characters for reliable injection.

Decision Layer

Currently:

Rule-based conditional logic

Example:

if dialogue:
    press A
else:
    move up


Future:

Finite State Machine

Deterministic exploration logic

Possibly reinforcement learning policy

Design principle:

Separate perception from decision logic.

3️⃣ Data Flow

Each loop iteration:

Capture full frame

Crop emulator window

Crop top screen

Run dialogue detection

Decide action

Inject key

Sleep briefly

Timing considerations:

No infinite tight loops

Bounded frame processing

Adjustable delays

4️⃣ System Constraints

Windows OS

GUI emulator (not headless)

Pixel-based only

No memory reading

Emulator must remain focused

These constraints are intentional.

The project simulates how a real human sees and interacts.

5️⃣ Current Stability Status

Working:

Movement injection

Dialogue detection

Dialogue advancement

Continuous perception loop

Unimplemented:

Collision detection

Navigation logic

Battle automation

Gym progression logic

Full game completion strategy

6️⃣ Architectural Philosophy

This project prioritizes:

Modularity

Replaceable components

Clear separation of concerns

Debuggable subsystems

Deterministic baseline before ML

We are building:

A vision-based autonomous agent for Pokémon Platinum.

Not a memory-reading bot.

7️⃣ Future Expansion Paths

Possible upgrades:

Frame differencing for movement detection

Object detection models

CNN-based policy learning

Battle state classifier

Reward system for reinforcement learning

But only after deterministic systems are stable.