# -*- coding: utf-8 -*-
"""
PNG to PDF assembler with Tkinter UI.

Features:
- Choose a folder that contains PNG files.
- Natural filename sort (e.g., img2 before img10).
- Choose output PDF path.
- Converts images to RGB and applies EXIF orientation for correct rendering.
- Minimal dependencies: Pillow only.

Usage (Windows, cmd.exe):
  python pngs_to_pdf.py

Dependency install:
  pip install -U pillow
"""

import os
import re
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from PIL import Image, ImageOps


def natural_sort_key(s):
    """
    Split a string into a list of text and integer chunks for natural sort.
    Example: "page12.png" -> ["page", 12, ".png"]
    """
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def list_pngs_sorted(folder):
    files = []
    try:
        for name in os.listdir(folder):
            if name.lower().endswith(".png"):
                files.append(name)
    except Exception:
        return []
    files.sort(key=natural_sort_key)
    return files


def convert_for_pdf(img):
    """
    Ensure the image is in RGB for PDF and apply EXIF orientation.
    Handles RGBA and P mode with transparency by pasting onto white background.
    """
    img = ImageOps.exif_transpose(img)
    if img.mode == "RGB":
        return img
    if img.mode in ("L", "LA"):
        # grayscale; remove alpha if present and convert to RGB
        if img.mode == "LA":
            bg = Image.new("L", img.size, 255)
            img = Image.composite(img.split()[0], bg, img.split()[1])
        return img.convert("RGB")
    if img.mode in ("RGBA", "P"):
        # flatten transparency over white
        if img.mode == "P":
            img = img.convert("RGBA")
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(bg, img)
        return img.convert("RGB")
    # Fallback
    return img.convert("RGB")


class PngToPdfApp:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("PNG to PDF")
        self.master.geometry("560x260")
        self.master.resizable(False, False)

        self.folder_var = tk.StringVar(value=os.path.expanduser("~"))
        self.outfile_var = tk.StringVar(value="")
        self.count_var = tk.StringVar(value="No folder selected")
        self.status_var = tk.StringVar(value="")

        self._build_ui()
        self._refresh_count()

    def _build_ui(self):
        pad = 8
        root = ttk.Frame(self.master, padding=pad)
        root.pack(fill="both", expand=True)

        # Folder row
        row1 = ttk.Frame(root)
        row1.pack(fill="x", pady=(0, pad))
        ttk.Label(row1, text="PNG Folder:").pack(side="left")
        ent1 = ttk.Entry(row1, textvariable=self.folder_var)
        ent1.pack(side="left", fill="x", expand=True, padx=(pad, pad))
        ttk.Button(row1, text="Browse...", command=self.choose_folder).pack(side="left")

        # Count row
        row2 = ttk.Frame(root)
        row2.pack(fill="x", pady=(0, pad))
        ttk.Label(row2, text="Files found:").pack(side="left")
        ttk.Label(row2, textvariable=self.count_var).pack(side="left", padx=(pad, 0))

        # Output file row
        row3 = ttk.Frame(root)
        row3.pack(fill="x", pady=(0, pad))
        ttk.Label(row3, text="Output PDF:").pack(side="left")
        ent2 = ttk.Entry(row3, textvariable=self.outfile_var)
        ent2.pack(side="left", fill="x", expand=True, padx=(pad, pad))
        ttk.Button(row3, text="Choose...", command=self.choose_outfile).pack(side="left")

        # Buttons row
        row4 = ttk.Frame(root)
        row4.pack(fill="x", pady=(pad, 0))
        self.build_btn = ttk.Button(row4, text="Build PDF", command=self.build_pdf)
        self.build_btn.pack(side="left")
        ttk.Button(row4, text="Exit", command=self.master.destroy).pack(side="right")

        # Status
        row5 = ttk.Frame(root)
        row5.pack(fill="x", pady=(pad, 0))
        ttk.Label(row5, textvariable=self.status_var, foreground="#333333").pack(side="left")

        # Update output default when folder changes
        self.folder_var.trace_add("write", lambda *_: self._on_folder_changed())

    def choose_folder(self):
        initial = self.folder_var.get()
        if not os.path.isdir(initial):
            initial = os.path.expanduser("~")
        folder = filedialog.askdirectory(initialdir=initial, title="Choose a folder with PNG files")
        if folder:
            self.folder_var.set(folder)
            self._refresh_count()

    def choose_outfile(self):
        default_name = self._default_pdf_name(self.folder_var.get())
        initialdir = self.folder_var.get() if os.path.isdir(self.folder_var.get()) else os.path.expanduser("~")
        path = filedialog.asksaveasfilename(
            title="Save PDF as",
            defaultextension=".pdf",
            initialdir=initialdir,
            initialfile=default_name,
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if path:
            self.outfile_var.set(path)

    def _default_pdf_name(self, folder):
        if not folder or not os.path.isdir(folder):
            return "output.pdf"
        base = os.path.basename(os.path.normpath(folder))
        if not base:
            return "output.pdf"
        return base + ".pdf"

    def _on_folder_changed(self):
        # Set a sensible default output path when folder changes
        folder = self.folder_var.get()
        if os.path.isdir(folder):
            default_name = self._default_pdf_name(folder)
            self.outfile_var.set(os.path.join(folder, default_name))
        self._refresh_count()

    def _refresh_count(self):
        folder = self.folder_var.get()
        if not os.path.isdir(folder):
            self.count_var.set("No folder selected")
            return
        pngs = list_pngs_sorted(folder)
        self.count_var.set(f"{len(pngs)} PNG file(s)")

    def build_pdf(self):
        self.status_var.set("")
        folder = self.folder_var.get().strip()
        outpath = self.outfile_var.get().strip()

        if not os.path.isdir(folder):
            messagebox.showerror("Error", "Please choose a valid folder containing PNG files.")
            return

        png_names = list_pngs_sorted(folder)
        if not png_names:
            messagebox.showerror("Error", "No PNG files found in the selected folder.")
            return

        if not outpath:
            # choose default if empty
            outpath = os.path.join(folder, self._default_pdf_name(folder))
            self.outfile_var.set(outpath)

        # Ensure the output directory exists
        outdir = os.path.dirname(outpath)
        if outdir and not os.path.isdir(outdir):
            try:
                os.makedirs(outdir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot create output directory:\n{e}")
                return

        # Load and convert images
        images = []
        try:
            for name in png_names:
                p = os.path.join(folder, name)
                with Image.open(p) as im:
                    images.append(convert_for_pdf(im).copy())
        except Exception as e:
            messagebox.showerror("Error", f"Failed reading images:\n{e}")
            for im in images:
                try:
                    im.close()
                except Exception:
                    pass
            return

        if not images:
            messagebox.showerror("Error", "No images to write.")
            return

        # Write PDF
        try:
            first, rest = images[0], images[1:]
            # Use resolution=300 for a reasonable default; adjust if needed
            first.save(outpath, "PDF", resolution=300.0, save_all=True, append_images=rest)
            self.status_var.set(f"Saved PDF: {outpath}")
            try:
                # On Windows, open the PDF when done (optional). Comment out if unwanted.
                if sys.platform.startswith("win") and os.path.exists(outpath):
                    os.startfile(outpath)  # type: ignore[attr-defined]
            except Exception:
                pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed writing PDF:\n{e}")
        finally:
            # Close images
            for im in images:
                try:
                    im.close()
                except Exception:
                    pass


def main():
    # Improve DPI handling on Windows so the UI looks crisp
    try:
        import ctypes  # type: ignore
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

    root = tk.Tk()
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except Exception:
        pass
    app = PngToPdfApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
