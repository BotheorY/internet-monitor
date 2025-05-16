# Internet Monitor Installation Guide

## For End Users

To install Internet Monitor on your Windows system:

1. Download the installer file (`InternetMonitorSetup.exe`) from the `dist` folder of this repository
2. Double-click the installer file to start the installation process
3. Follow the on-screen instructions:
   - Select your preferred language for the installer
   - Choose the installation location (default is Program Files)
   - Decide whether to create a desktop shortcut
   - Complete the installation
4. After installation, you can launch Internet Monitor from:
   - The desktop shortcut (if you chose to create one)
   - The Start Menu under "Internet Monitor"

## For Developers

### Building the Installer

To create the installer package for distribution:

1. Make sure you have already built the executable using PyInstaller:
   - The `internetm.exe` file should be in the `dist` folder
   - All required files should be included in the PyInstaller build

2. Install [Inno Setup](https://jrsoftware.org/isdl.php) (version 5 or 6)

3. Build the installer using one of these methods:

   **Option 1: Using the batch file**
   - Run `build_installer.bat` by double-clicking it
   - The script will automatically locate Inno Setup and build the installer

   **Option 2: Using the PowerShell script**
   - Right-click `build_installer.ps1` and select "Run with PowerShell"
   - If you get a security warning, you may need to run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

   **Option 3: Using Inno Setup directly**
   - Open Inno Setup Compiler
   - Open the `setup.iss` script file from this project
   - Click on the "Compile" button in the toolbar (or press F9)

4. The installer will be created in the `installer` folder as `InternetMonitorSetup.exe`

### What's Included in the Installer

The installer packages the following components:

- The main executable (`internetm.exe`)
- All localization files from the `locales` folder (*.json files)
- Icon files from the `icon` folder
- Desktop and Start Menu shortcuts
- Uninstaller

### Customizing the Installer

If you need to customize the installer, edit the `setup.iss` file. You can modify:

- Application version
- Publisher information
- Installation directory
- Included files
- Installer languages
- Shortcut creation

Refer to the [Inno Setup Documentation](https://jrsoftware.org/ishelp/) for detailed information.