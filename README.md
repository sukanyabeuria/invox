# 🪄 Invisibility Cloak — Real-Time Computer Vision Project

A real-time invisibility effect built with Python and OpenCV, inspired by the classic "Harry Potter cloak" trick. Wear a solid-colored cloth in front of your webcam and the app makes it — and anything else that color — appear to vanish, replaced by the background behind you.

The effect works entirely through classical computer vision: color-space conversion, masking, and image compositing. No deep learning models are involved in the current version.

---

## 📌 Table of Contents 

- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [Project Objective](#-project-objective)
- [How the Project Works](#-how-the-project-works)
- [AI Pipeline](#-ai-pipeline)
- [Key Features](#-key-features)
- [Computer Vision](#-computer-vision)
- [Natural Language Processing](#-natural-language-processing)
- [Invisibility Technique](#-invisibility-technique)
- [System Architecture](#-system-architecture)
- [Project Workflow](#-project-workflow)
- [Example Commands](#-example-commands)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Running the Project](#-running-the-project)
- [Example](#-example)
- [Challenges](#-challenges)
- [Future Improvements](#-future-improvements)
- [Applications](#-applications)
- [Limitations](#-limitations)
- [Conclusion](#-conclusion)

---

## 🔍 Project Overview

This project uses a laptop or computer webcam to create a real-time "invisibility" illusion.

1. The app captures a still image of the empty background.
2. You step into frame wearing a solid-colored cloth (calibrated for red by default).
3. Every video frame is converted to the HSV color space and scanned for that color.
4. Wherever the color is found, the app swaps those pixels with the matching pixels from the captured background.
5. Everywhere else, the live camera feed is shown normally.

The result: the cloak (and anything else that shade of red) appears to disappear, revealing the background behind it.

---

## ❗ Problem Statement

A believable "invisibility" effect needs to:

- Tell the cloak apart from skin tones, clothing, and the rest of the scene in real time.
- Keep working as lighting shifts slightly and the person moves.
- Run smoothly on ordinary consumer hardware with no GPU required.
- Be simple enough to calibrate for different cloak colors or lighting setups without touching the core code.

This project solves that with classic, lightweight color-segmentation techniques rather than a heavyweight detection model — trading some flexibility for speed and simplicity.

---

## 🎯 Project Objective

The goal is a small, real-time computer vision application that can:

1. Capture a clean background frame from the webcam.
2. Continuously capture live video.
3. Detect a target color range (the cloak) in each frame.
4. Build a mask isolating that color.
5. Composite the background over the masked region and the live frame everywhere else.
6. Display the result in a live window, with a hotkey to re-capture the background on the fly.

A companion calibration tool (`calibrate.py`) lets you interactively find the right HSV range for your specific cloak and lighting before running the main effect.

---

## ⚙️ How the Project Works

The system has two scripts that work together:

**`calibrate.py`** — opens the webcam alongside a window of HSV sliders (trackbars). You adjust the sliders until the "Mask" preview clearly isolates your cloak from everything else, then press `q` to print the resulting `lower`/`upper` HSV values to the terminal.

**`main.py`** — runs the actual effect:

1. Opens the webcam and waits briefly for it to warm up.
2. Captures ~60 frames to build a stable background image (you need to step out of frame for this).
3. On each subsequent frame, converts the image to HSV and builds a mask using pre-set red HSV ranges.
4. Cleans up the mask with morphological opening/closing and dilation to remove noise.
5. Combines the background (where the mask is active) with the live frame (everywhere else).
6. Displays the composited output in a live window.

---

## 🤖 AI Pipeline

This section is labeled "AI Pipeline" for consistency with the project's terminology, but the current implementation is classical computer vision (color-space thresholding), not a trained model. The processing pipeline looks like this:

```text
              WEBCAM
                │
                ▼
     Capture Background Frame
                │
                ▼
        Live Video Frame
                │
                ▼
     Convert Frame to HSV
                │
                ▼
   Threshold for Cloak Color
        (red, two ranges)
                │
                ▼
      Clean Mask (Morphology)
                │
                ▼
   Composite: Background + Live Frame
                │
                ▼
           LIVE OUTPUT
```

---

## ✨ Key Features

**1. Real-Time Webcam Processing**
Runs directly on your live camera feed — no image upload needed.

**2. Color-Based Detection**
Uses HSV thresholding across two ranges to reliably catch red, which wraps around the hue circle.

**3. Noise Cleanup**
Morphological opening, closing, and dilation remove small holes and speckles from the raw color mask for a cleaner edge around the cloak.

**4. On-the-Fly Background Recapture**
Press `b` while the app is running to re-capture the background without restarting — useful if lighting or your position changes.

**5. Interactive Calibration Tool**
`calibrate.py` provides live HSV sliders so you can tune the detection range for a different cloak color or lighting condition, rather than hardcoding values.

---

## 🧠 Computer Vision

The computer vision pipeline in `main.py` has these stages:

**Step 1 — Frame Capture**
OpenCV reads frames from the webcam via `cv2.VideoCapture`.

**Step 2 — Background Capture**
The first ~60 frames (captured while you're out of shot) are used to build a reference background image, mirrored to match the live feed.

**Step 3 — Color Masking**
Each live frame is converted to HSV, and two `cv2.inRange` masks are combined to capture the full red hue range (which spans both ends of the hue circle: roughly 0–10 and 160–179).

**Step 4 — Mask Cleanup**
`cv2.morphologyEx` (open, then close) and `cv2.dilate` smooth the mask, removing small noisy regions and filling small gaps.

**Step 5 — Compositing**
`cv2.bitwise_and` extracts the background where the mask is active and the live frame elsewhere; `cv2.addWeighted` merges the two into the final output.

---

## 🗣️ Natural Language Processing

Natural language command input is **not yet implemented** in this project. Currently, the app is controlled with simple keyboard shortcuts (`q` to quit, `b` to recapture the background) rather than typed or spoken commands like "make my face invisible."

Adding an NLP layer that lets a user type or say what to hide, and mapping that to an object-detection target, is listed as a planned direction — see [Future Improvements](#-future-improvements).

---

## 🪄 Invisibility Technique

The invisibility effect is a visual illusion created through image compositing — not physical invisibility.

**Current technique — Chroma-key style color substitution:**
The system detects a specific color range (the cloak) and replaces those pixels with a previously captured background image. This is the same principle behind green-screen compositing, applied per-frame in real time.

This approach works best when:

- The camera is stationary.
- The background stays relatively static.
- The cloak color is distinct from everything else in the scene (skin, clothing, furniture).

Other reconstruction techniques (previous-frame estimation, OpenCV inpainting, AI-based inpainting) are possible extensions — see [Future Improvements](#-future-improvements).

---

## 🏗️ System Architecture

```text
┌───────────────────────────────┐
│           WEBCAM               │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│   BACKGROUND CAPTURE (once)    │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        LIVE FRAME (loop)       │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      HSV COLOR CONVERSION      │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      RED COLOR MASKING         │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│    MORPHOLOGICAL CLEANUP       │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│  COMPOSITE BACKGROUND + FRAME  │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│         LIVE DISPLAY           │
└───────────────────────────────┘
```

---

## 🔄 Project Workflow

1. Run `calibrate.py` (optional) to find the right HSV range for your cloak and lighting.
2. Update the HSV values in `main.py` if they differ from the defaults.
3. Run `main.py`.
4. Step out of frame for a couple of seconds while the background is captured.
5. Step back in wearing the colored cloak.
6. The cloak area is replaced with the captured background in real time.
7. Press `b` at any time to re-capture the background.
8. Press `q` to quit.

---

## 💬 Example Commands

The project is controlled with keyboard shortcuts while the live window is focused:

| Key | Action |
|---|---|
| `q` | Quit the application |
| `b` | Re-capture the background |

(In `calibrate.py`, the six trackbars set the HSV `min`/`max` bounds live, and `q` prints the final `lower`/`upper` arrays to the terminal.)

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| OpenCV (`cv2`) | Webcam capture, color conversion, masking, display |
| NumPy | Array operations for masks and image data |

---

## 📁 Project Structure

```text
invox/
│
├── README.md
├── .gitignore
│
└── invisible_cloak_project/
    ├── main.py         # Runs the real-time invisibility effect
    ├── calibrate.py    # Interactive HSV calibration tool
    ├── README.md
    └── .gitignore
```

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/sukanyabeuria/invox.git
cd invox/invisible_cloak_project
```

Create and activate a virtual environment (recommended):

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

Install the required libraries:

```bash
pip install opencv-python numpy
```

---

## ▶️ Running the Project

**1. (Optional) Calibrate your cloak color**

```bash
python calibrate.py
```

Adjust the HSV sliders until only the cloak shows up white in the "Mask" window, then press `q` and note the printed `lower`/`upper` values.

**2. Run the invisibility effect**

```bash
python main.py
```

Step out of frame while the background is captured (a couple of seconds), then step back in wearing the cloak.

- Press `b` to re-capture the background at any time.
- Press `q` to quit.

---

## 📊 Example

**Input:** A person wearing a red cloth steps in front of the camera.

**Processing:**

- HSV conversion isolates the red hue range.
- The red region is masked and cleaned up.
- That region is replaced with the pre-captured background.

**Output:** The red cloth appears to vanish, revealing the background behind the person, while the rest of the scene (face, arms, surroundings) stays visible normally.

---

## 🚧 Challenges

**1. Color Ambiguity**
Any other red object or clothing in frame will also be masked out, since detection is purely color-based.

**2. Lighting Sensitivity**
Changes in lighting can shift how a color appears in HSV space, requiring re-calibration.

**3. Mask Noise**
Raw color masks often contain small holes and speckles, which is why morphological cleanup is needed before compositing.

**4. Background Stability**
The illusion only holds up if the captured background still matches the current camera view — camera movement or background changes require a re-capture.

---

## 🔮 Future Improvements

These are potential directions for extending the project beyond the current color-based approach:

- **Natural Language Commands** — let the user type or speak what to hide (e.g. "hide my face"), parsed by an NLP module into an action + target.
- **Object Detection & Segmentation** — replace fixed color thresholding with a detection/segmentation model (e.g. YOLO + a segmentation head) so any recognizable object, not just a specific color, can be hidden.
- **AI-Based Background Inpainting** — use a generative inpainting model instead of a static captured background, so the effect works even with a moving camera or changing scene.
- **Web Interface** — wrap the effect in a Streamlit (or similar) app for easier setup and sharing, instead of a local OpenCV window.
- **Voice Control** — add speech recognition ahead of the NLP layer.
- **Multi-Object / Multi-Color Support** — hide more than one color or object at once.

---

## 🌍 Applications

While primarily an educational computer vision demo, the underlying technique has practical uses:

- **Content creation** — special-effects style shots for videos.
- **Computer vision education** — a hands-on introduction to color spaces, masking, and image compositing.
- **Prototype for chroma-key tools** — a lightweight, camera-only alternative to a physical green screen.

---

## ⚠️ Limitations

- This creates a *visual* illusion, not physical invisibility.
- Any object matching the target color range will also be hidden, whether intended or not.
- Requires a relatively stable camera position and background.
- Sensitive to lighting changes, shadows, and background complexity.
- Skin tones or other objects with similar hue/saturation to the cloak can trigger false masking.

---

## 🏁 Conclusion

This project recreates the classic "invisibility cloak" effect using nothing but OpenCV and basic color-space image processing: capture a background, detect a target color in HSV space, clean up the resulting mask, and composite the background back in over that region in real time.

It's a compact, dependency-light demonstration of how far simple, classical computer vision techniques can go — and a solid base to build on if extended toward object detection, segmentation, or natural-language control in the future.

---

## 👩‍💻 Authors

- Sukanya Beuria
- Anima Sau
- Ishika Sheet
- Manisa Sau

## ⭐ Project Status

**Status:** 🚧 In Development

Future versions will improve:

- Detection accuracy
- Segmentation
- Background reconstruction
- NLP capabilities
- Real-time performance
- Voice control
- Multi-object invisibility
