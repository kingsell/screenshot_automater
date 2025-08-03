# ScreenshotAutomater

Two small Tkinter tools:

1) **Kindle Capture** — select a screen region and repeatedly capture it, pressing Right Arrow between shots to advance Kindle pages.  
2) **PNGs → PDF** — pick a folder of PNGs, natural-sort by filename, and assemble into one PDF.

## Quick start (Windows)


python -m venv .venv && call .venv\Scripts\activate && pip install -U pyautogui mss pillow


Kindle Capture

python kindle_capture.py
Choose output folder.

Select Region.

Optionally set Start Delay (sec), Interval (sec), Base Filename, Start Page #.

Start to begin: it waits for the start delay, screenshots, presses Right Arrow, repeats. Stop to end.

PNGs → PDF
Install only Pillow if you want this tool alone:

pip install -U pillow
Run:

python pngs_to_pdf.py
Choose a folder with PNGs.

Choose output PDF path (or accept default).

Build PDF.

Notes
Tested on Windows. Requires Python 3.9+ recommended.

High DPI: the apps call SetProcessDPIAware() to reduce coordinate drift.

Thread safety: mss() is created and used inside the worker thread in kindle_capture.py.

Packaging (optional)

pip install -U pyinstaller
pyinstaller --noconfirm --name ScreenshotAutomater --windowed --onefile --collect-all mss kindle_captur