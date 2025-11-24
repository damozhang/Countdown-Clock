# Countdown Clock

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-blue)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A minimalist, always-on-top desktop countdown timer that displays a highly visible countdown to a specific time on your screen.

Perfect for presentations, live streaming, broadcasts, meetings, or any scenario where you need a clear, distraction-free countdown timer.

## Download

### Windows
See [build_instructions.md](build_instructions.md) for instructions on building the Windows executable.

Alternatively, download pre-built `CountdownClock.exe` from the [Releases](https://github.com/damozhang/countdown-clock/releases) page (when available).

### macOS
Clone this repository and run with Python 3.12+:
```bash
git clone https://github.com/damozhang/countdown-clock.git
cd countdown-clock
uv run python desktop_clock.py
```

## Features

- **Large, Bold Display**: Highly visible countdown in `HH:MM:SS.mmm` format with 120pt font.
- **Silent Operation**: Visual alerts only - no sound notifications to interrupt your work.
- **Always on Top**: Floats above all other windows to ensure visibility.
- **Frameless Design**: Clean, modern interface with no window borders.
- **Visual Alerts**: Blinks red/white during the final 10 seconds.
- **Smart Persistence**: Remembers your window position and target time.
- **Flexible Input**: Supports both `HH:MM` and `HH:MM:SS` time formats.
- **Cross-Platform**: Works on both **Windows 10/11** and **macOS**.
- **Portable**: Windows standalone `.exe` requires no installation.

## Usage Guide

### Basic Controls
- **Move Window**: Click and drag anywhere on the window.
- **Set Target Time**: Click the **yellow time** at the bottom.
- **Exit**: Press **ESC** key.

### Setting the Timer
1. Click the yellow target time display at the bottom.
2. Enter your desired time in 24-hour format:
   - Example: `14:30` (2:30 PM)
   - Example: `14:30:45` (Precise to the second)
3. Click **Set** or press Enter.
4. The countdown will start automatically.

### Configuration
The application automatically saves your preferences to `~/.countdownclock_config.json`:
- Window Position (X, Y coordinates)
- Last Target Time

## Development

### Building from Source
See [build_instructions.md](build_instructions.md) for detailed instructions on building the Windows executable.

### Requirements
- Python 3.12 or higher
- `uv` package manager
- `tkinter` (usually included with Python)

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
