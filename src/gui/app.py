import customtkinter as ctk
from tkinter import messagebox
from src.gui.region_selector import select_region
from src.detection.detector import Detector
from src.detection.screen_capture import ScreenCapture
from src.utils.sound import play_alert
import threading
import time
import os
import json

# Folder for models
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

MODEL_OPTIONS = [
    ("YOLOv8n (fast, low accuracy)", os.path.join(MODEL_DIR, "yolov8n.pt")),
    ("YOLOv8s (balanced)", os.path.join(MODEL_DIR, "yolov8s.pt")),
    ("YOLOv8m (medium)", os.path.join(MODEL_DIR, "yolov8m.pt")),
    ("YOLOv8l (accurate)", os.path.join(MODEL_DIR, "yolov8l.pt")),
    ("YOLOv8x (maximum accuracy)", os.path.join(MODEL_DIR, "yolov8x.pt")),
]

CONF_OPTIONS = [
    ("Minimal (0.2)", 0.2),
    ("Medium (0.4)", 0.4),
    ("High (0.6)", 0.6),
    ("Maximum (0.8)", 0.8),
]

DEVICE_OPTIONS = [
    ("CPU", "cpu"),
    ("GPU", "cuda"),
]

# Load defaults from config.json (array style)
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config.json"))
def get_default(name, fallback):
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
        for item in config.get("defaults", []):
            if item.get("name") == name:
                return item.get("value", fallback)
    except Exception:
        pass
    return fallback

DEFAULT_MODEL = get_default("model", MODEL_OPTIONS[0][0])
DEFAULT_CONFIDENCE = get_default("confidence", CONF_OPTIONS[1][0])
DEFAULT_DEVICE = get_default("device", DEVICE_OPTIONS[0][0])
DEFAULT_MONITORED_CLASSES = get_default("monitored_classes", ["car", "bus", "truck"])

ctk.set_appearance_mode(get_default("theme", "light"))  # Можно сменить на 'dark' для тёмной темы
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SmartZoneGuard")
        self.geometry("440x580")
        self.resizable(False, False)
        # self.iconbitmap('')  # Можно добавить .ico файл, если есть

        self.model_var = ctk.StringVar(value=DEFAULT_MODEL)
        self.conf_var = ctk.StringVar(value=DEFAULT_CONFIDENCE)
        self.device_var = ctk.StringVar(value=DEFAULT_DEVICE)
        self.region = None
        self.monitoring = False
        self.monitor_thread = None

        self.create_widgets()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        frame = ctk.CTkFrame(self, corner_radius=16)
        frame.grid(row=0, column=0, padx=32, pady=32, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(frame, text="SmartZoneGuard", font=("Segoe UI", 28, "bold"))
        title.grid(row=0, column=0, pady=(10, 30), sticky="n")

        # Model
        model_label = ctk.CTkLabel(frame, text="Model:", font=("Segoe UI", 16))
        model_label.grid(row=1, column=0, sticky="w", pady=(0, 4))
        self.model_combo = ctk.CTkOptionMenu(frame, variable=self.model_var, values=[m[0] for m in MODEL_OPTIONS], font=("Segoe UI", 15), width=320, height=36)
        self.model_combo.grid(row=2, column=0, pady=(0, 18))

        # Confidence
        conf_label = ctk.CTkLabel(frame, text="Confidence:", font=("Segoe UI", 16))
        conf_label.grid(row=3, column=0, sticky="w", pady=(0, 4))
        self.conf_combo = ctk.CTkOptionMenu(frame, variable=self.conf_var, values=[c[0] for c in CONF_OPTIONS], font=("Segoe UI", 15), width=320, height=36)
        self.conf_combo.grid(row=4, column=0, pady=(0, 18))

        # Device
        device_label = ctk.CTkLabel(frame, text="Device:", font=("Segoe UI", 16))
        device_label.grid(row=5, column=0, sticky="w", pady=(0, 4))
        self.device_combo = ctk.CTkOptionMenu(frame, variable=self.device_var, values=[d[0] for d in DEVICE_OPTIONS], font=("Segoe UI", 15), width=320, height=36)
        self.device_combo.grid(row=6, column=0, pady=(0, 18))

        # Region
        self.region_label = ctk.CTkLabel(frame, text="Region not selected", font=("Segoe UI", 14), text_color="#888888")
        self.region_label.grid(row=7, column=0, pady=(0, 24))

        # Select region button
        self.select_btn = ctk.CTkButton(frame, text="Select region", command=self.on_select_region, font=("Segoe UI", 15), height=40)
        self.select_btn.grid(row=8, column=0, pady=(0, 24), sticky="ew")

        # Start/Stop buttons
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.grid(row=9, column=0, pady=(0, 0), sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        self.start_btn = ctk.CTkButton(btn_frame, text="Start", command=self.on_start, font=("Segoe UI", 15, "bold"), fg_color="#2563eb", hover_color="#1d4ed8", height=40)
        self.start_btn.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.stop_btn = ctk.CTkButton(
            btn_frame,
            text="Stop",
            command=self.on_stop,
            state="disabled",
            font=("Segoe UI", 15),
            fg_color="#ef4444",        # Red
            hover_color="#b91c1c",     # Dark red on hover
            text_color="#fff",
            height=40
        )
        self.stop_btn.grid(row=0, column=1, padx=(8, 0), sticky="ew")

    def on_select_region(self):
        self.region = select_region()
        if self.region:
            self.region_label.configure(text=f"Region: {self.region}", text_color="#222222")
        else:
            self.region_label.configure(text="Region not selected", text_color="#888888")

    def on_start(self):
        if not self.region:
            messagebox.showerror("Error", "Please select a region first!")
            return
        model_idx = [m[0] for m in MODEL_OPTIONS].index(self.model_var.get())
        conf_idx = [c[0] for c in CONF_OPTIONS].index(self.conf_var.get())
        device_idx = [d[0] for d in DEVICE_OPTIONS].index(self.device_var.get())
        model_path = MODEL_OPTIONS[model_idx][1]
        conf = CONF_OPTIONS[conf_idx][1]
        device = DEVICE_OPTIONS[device_idx][1]
        self.detector = Detector(model_path, conf, device, monitored_classes=DEFAULT_MONITORED_CLASSES)
        self.monitoring = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()

    def on_stop(self):
        self.monitoring = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")

    def monitor_loop(self):
        capture = ScreenCapture(self.region)
        while self.monitoring:
            img = capture.grab()
            found = self.detector.detect(img)
            if found:
                play_alert()
                time.sleep(0.5)
            time.sleep(0.5)

def run_app():
    app = App()
    app.mainloop() 