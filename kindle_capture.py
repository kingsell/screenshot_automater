# -*- coding: utf-8 -*-
"""
Kindle region screenshot automation:
- Choose output folder in the UI.
- Click "Select Region" to draw a capture rectangle.
- Click "Start" to begin: waits 5 seconds so you can click back into Kindle,
  then repeats: screenshot region, press Right Arrow to advance.
- Click "Stop" to halt the loop.

Tested on Windows. Requires: pyautogui, mss, pillow.
"""

import os
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Dependencies
import pyautogui
from PIL import Image
import mss

# Improve coordinate accuracy on Windows with display scaling
try:
    import ctypes  # type: ignore
    ctypes.windll.user32.SetProcessDPIAware()
except Exception:
    pass


class KindleCaptureApp:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("Kindle Region Capture")
        self.master.geometry("420x280")
        self.master.resizable(False, False)

        # State
        self.output_dir = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Pictures"))
        self.interval_sec = tk.DoubleVar(value=1.0)  # delay between cycles
        self.start_delay_sec = tk.DoubleVar(value=5.0)  # initial delay before first capture
        self.page_counter = tk.IntVar(value=1)
        self.base_filename = tk.StringVar(value="capture")
        self.region = None  # (left, top, width, height)
        self.running = False
        self.stop_event = threading.Event()

        # UI
        self._build_ui()

    def _build_ui(self):
        pad = 8
        frm = ttk.Frame(self.master, padding=pad)
        frm.pack(fill="both", expand=True)

        # Output folder
        row0 = ttk.Frame(frm)
        row0.pack(fill="x", pady=(0, pad))
        ttk.Label(row0, text="Output Folder:").pack(side="left")
        ent = ttk.Entry(row0, textvariable=self.output_dir)
        ent.pack(side="left", fill="x", expand=True, padx=(pad, pad))
        ttk.Button(row0, text="Browse...", command=self.choose_folder).pack(side="left")

        # Base filename and start page
        row1 = ttk.Frame(frm)
        row1.pack(fill="x", pady=(0, pad))
        ttk.Label(row1, text="Base Filename:").pack(side="left")
        ttk.Entry(row1, textvariable=self.base_filename, width=16).pack(side="left", padx=(pad, 0))
        ttk.Label(row1, text="Start Page #:").pack(side="left", padx=(pad, 0))
        ttk.Spinbox(row1, from_=1, to=999999, textvariable=self.page_counter, width=8).pack(side="left", padx=(pad, 0))

        # Interval and initial delay
        row2 = ttk.Frame(frm)
        row2.pack(fill="x", pady=(0, pad))
        ttk.Label(row2, text="Interval (sec):").pack(side="left")
        ttk.Spinbox(row2, from_=0.1, to=10.0, increment=0.1, textvariable=self.interval_sec, width=8).pack(side="left", padx=(pad, 0))
        ttk.Label(row2, text="Start Delay (sec):").pack(side="left", padx=(pad, 0))
        ttk.Spinbox(row2, from_=0.0, to=30.0, increment=0.5, textvariable=self.start_delay_sec, width=8).pack(side="left", padx=(pad, 0))

        # Region status
        row3 = ttk.Frame(frm)
        row3.pack(fill="x", pady=(0, pad))
        self.region_label = ttk.Label(row3, text="Region: not selected")
        self.region_label.pack(side="left")

        # Buttons
        row4 = ttk.Frame(frm)
        row4.pack(fill="x", pady=(pad, 0))
        ttk.Button(row4, text="Select Region", command=self.select_region).pack(side="left")
        self.start_btn = ttk.Button(row4, text="Start", command=self.start, state="disabled")
        self.start_btn.pack(side="left", padx=(pad, 0))
        self.stop_btn = ttk.Button(row4, text="Stop", command=self.stop, state="disabled")
        self.stop_btn.pack(side="left", padx=(pad, 0))
        ttk.Button(row4, text="Exit", command=self.on_exit).pack(side="right")

        # Enable/disable Start based on folder and region
        self.master.after(200, self._refresh_start_state)

    def _refresh_start_state(self):
        ok_folder = os.path.isdir(self.output_dir.get())
        ok_region = self.region is not None
        self.start_btn.configure(state="normal" if (ok_folder and ok_region and not self.running) else "disabled")
        self.stop_btn.configure(state="normal" if self.running else "disabled")
        self.master.after(200, self._refresh_start_state)

    def choose_folder(self):
        d = filedialog.askdirectory(initialdir=self.output_dir.get(), title="Choose output folder")
        if d:
            self.output_dir.set(d)

    def select_region(self):
        # Fullscreen transparent overlay to drag a rectangle
        overlay = tk.Toplevel(self.master)
        overlay.attributes("-fullscreen", True)
        overlay.attributes("-topmost", True)
        try:
            overlay.attributes("-alpha", 0.3)
        except Exception:
            pass
        overlay.config(bg="black")
        overlay.title("Drag to select region. Press Esc to cancel.")

        canvas = tk.Canvas(overlay, cursor="cross", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        start = {"x": 0, "y": 0}
        rect = {"id": None}

        def on_key(evt):
            if evt.keysym == "Escape":
                overlay.destroy()

        def on_press(evt):
            start["x"], start["y"] = evt.x, evt.y
            if rect["id"] is not None:
                canvas.delete(rect["id"])
            rect["id"] = canvas.create_rectangle(start["x"], start["y"], evt.x, evt.y, outline="red", width=2)

        def on_drag(evt):
            if rect["id"] is not None:
                canvas.coords(rect["id"], start["x"], start["y"], evt.x, evt.y)

        def on_release(evt):
            x0, y0 = start["x"], start["y"]
            x1, y1 = evt.x, evt.y
            left = min(x0, x1)
            top = min(y0, y1)
            width = abs(x1 - x0)
            height = abs(y1 - y0)
            if width < 4 or height < 4:
                messagebox.showwarning("Selection too small", "Please select a larger region.")
                overlay.destroy()
                return
            self.region = (left, top, width, height)
            self.region_label.config(text=f"Region: left={left}, top={top}, w={width}, h={height}")
            overlay.destroy()

        overlay.bind("<Escape>", on_key)
        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)

    def start(self):
        if not os.path.isdir(self.output_dir.get()):
            messagebox.showerror("Invalid folder", "Please choose a valid output folder.")
            return
        if self.region is None:
            messagebox.showerror("No region", "Please select a region first.")
            return
        self.stop_event.clear()
        t = threading.Thread(target=self._run_loop, daemon=True)
        t.start()

    def stop(self):
        self.stop_event.set()

    def _run_loop(self):
        # Create and use mss INSIDE this worker thread. Also avoid touching Tk from this thread.
        try:
            self._set_buttons_running(True)

            # Snapshot configuration once at start
            left, top, width, height = self.region
            bbox = {"left": int(left), "top": int(top), "width": int(width), "height": int(height)}
            outdir = self.output_dir.get()
            base = self.base_filename.get().strip() or "capture"
            page_num = int(self.page_counter.get())
            interval = max(0.05, float(self.interval_sec.get()))
            start_delay = max(0.0, float(self.start_delay_sec.get()))

            # Initial delay so you can focus the Kindle app
            if start_delay > 0:
                # Optional: show a non-blocking info box in the main thread
                self.master.after(0, lambda d=start_delay: self._show_transient_info(f"Starting in {d:.1f} seconds..."))
                time.sleep(start_delay)

            # Do the work
            with mss.mss() as sct:
                while not self.stop_event.is_set():
                    # Capture
                    img = self._grab_region(bbox, sct)

                    # Save
                    fname = f"{base}_{page_num:04d}.png"
                    fpath = os.path.join(outdir, fname)
                    img.save(fpath)

                    # Advance Kindle page
                    pyautogui.press("right")

                    # Increment page counter (reflect in UI via main thread)
                    page_num += 1
                    self.master.after(0, lambda v=page_num: self.page_counter.set(v))

                    # Wait
                    time.sleep(interval)

        except Exception as e:
            # Show the error from the main thread
            self.master.after(0, lambda: messagebox.showerror("Error", f"Run loop error:\n{e}"))
        finally:
            self._set_buttons_running(False)

    def _grab_region(self, bbox, sct):
        shot = sct.grab(bbox)
        img = Image.frombytes("RGB", shot.size, shot.rgb)
        return img

    def _set_buttons_running(self, is_running: bool):
        def apply():
            self.running = is_running
            self.start_btn.configure(state="disabled" if is_running else "normal")
            self.stop_btn.configure(state="normal" if is_running else "disabled")
        self.master.after(0, apply)

    def _show_transient_info(self, text):
        # Small transient label at the bottom of the window
        try:
            if hasattr(self, "_info_label") and self._info_label.winfo_exists():
                self._info_label.config(text=text)
            else:
                self._info_label = ttk.Label(self.master, text=text, foreground="#333333")
                self._info_label.pack(side="bottom", pady=4)
            # Remove after a short while
            self.master.after(2500, self._clear_transient_info)
        except Exception:
            pass

    def _clear_transient_info(self):
        try:
            if hasattr(self, "_info_label") and self._info_label.winfo_exists():
                self._info_label.destroy()
        except Exception:
            pass

    def on_exit(self):
        if self.running:
            if not messagebox.askyesno("Quit", "Capture is running. Stop and exit?"):
                return
            self.stop_event.set()
            time.sleep(0.2)
        self.master.destroy()


def main():
    # Small pause so actions have slight delay
    pyautogui.PAUSE = 0.05

    root = tk.Tk()
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except Exception:
        pass
    app = KindleCaptureApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
