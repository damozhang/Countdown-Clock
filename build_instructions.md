# How to Build Windows Executable (.exe)

Since `pyinstaller` does not support cross-compilation (building a Windows .exe from macOS), you must perform these steps on a **Windows** machine.

## Step 1: Install Python

### Version Requirement
- **Python 3.12 or higher** is required

### Installation Methods

#### Method 1: Official Website (Recommended)
1. Visit https://www.python.org/downloads/
2. Download **Python 3.12** or newer for Windows
3. Run the installer
4. ⚠️ **IMPORTANT**: Check the box "Add Python to PATH" at the bottom
5. Click "Install Now"
6. After installation, open Command Prompt (CMD) and verify:
   ```cmd
   python --version
   ```
   Should display `Python 3.12.x` or higher

#### Method 2: Microsoft Store (Easier)
1. Open Microsoft Store
2. Search for "Python 3.12" or "Python 3.13"
3. Click Install
4. Environment variables are configured automatically

### Install uv (Package Manager)
After installing Python, install `uv`:
```cmd
pip install uv
```

Verify installation:
```cmd
uv --version
```

## Step 2: Build the Executable

### Prerequisites
### Prerequisites
- Python 3.12+ installed (see Step 1 above)
- `uv` package manager installed (see Step 1 above)
- Project files copied to your Windows machine

### Build Steps

1.  **Copy the project** to your Windows machine.
2.  Open a terminal (PowerShell or CMD) in the project folder.
3.  **Install dependencies**:
    ```powershell
    uv sync
    ```
4.  **Build the executable**:
    Run the following command to generate a single-file executable:
    ```powershell
    uv run pyinstaller --noconsole --onefile --name "CountdownClock" desktop_clock.py
    ```

## Output
- The generated `.exe` file will be located in the `dist` folder:
  `dist\CountdownClock.exe`
- This is a **standalone executable** that can be:
  - Placed anywhere on your computer
  - Copied to other Windows machines
  - Run without installing Python
  - Distributed via USB drive or network

## Notes
- `--noconsole`: Hides the terminal window when the app runs.
- `--onefile`: Packages everything into a single `.exe` file.
- `--name "CountdownClock"`: Names the output file.
