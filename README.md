# SmartZoneGuard

## Description

SmartZoneGuard is a program for monitoring a user-selected area of the screen and alerting when a car, bus, truck, or any COCO object is detected using YOLOv8 models. The user selects the model (speed/accuracy), confidence level, device, and screen region via a modern GUI.

## Installation

1. Install Python 3.8–3.12 (recommended, as some packages may not support 3.13+).
2. Clone the repository or download the project.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Make sure the file `alert.wav` is located in `src/sounds/` (by default, it is already there). You can add your own `.wav` files to this folder.

## Usage

```bash
python main.py
```

Or use the provided `run_smartzoneguard.bat` file.

## Project Structure

- `main.py` — entry point
- `src/` — all source code and resources
  - `gui/` — GUI logic
  - `detection/` — detection and screen capture
  - `utils/` — utilities (sound)
  - `models/` — YOLOv8 model weights (downloaded automatically)
  - `sounds/` — sound files (all .wav files in this folder are included in the repo)

## Requirements

- Windows 10/11
- Python 3.8–3.12

## Notes

- YOLOv8 weights are downloaded automatically to `src/models/` on first run.
- Sound alerts use the standard `winsound` module (Windows only, .wav files).
- All user interface and messages are in English.
- All sound files in `src/sounds/` are included in the repository. You can add your own `.wav` files for custom alerts.

## Sound Settings

- The default alert sound is set in `src/config.json` (see the `alert_sound` parameter in `defaults`).
- You can add any `.wav` file to `src/sounds/` and set its name in the config to use it as the alert.

## How to use

1. Run the program.
2. Select the YOLO model, confidence level, device, and theme.
3. Click "Select region" and select the area of the screen to monitor.
4. Click "Start" to begin monitoring. An alert will sound when a selected object is detected in the selected area.
5. Click "Stop" to end monitoring.

## Supported Objects

- You can monitor any of the 80 COCO classes (see `src/config.json` for the full list in the `_help` section).
- Just add the desired class names to the `monitored_classes` array in the config.

---

If you have any questions or want to add new features, feel free to ask!
