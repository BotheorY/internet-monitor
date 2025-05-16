# Internet Monitor Installer Guide

This guide explains how to create a Windows installer for the Internet Monitor application that includes the executable and all localization files.

## Prerequisites

1. [Inno Setup](https://jrsoftware.org/isdl.php) - Download and install the latest version
2. Make sure you have already built the executable using PyInstaller (the `internetm.exe` file should be in the `dist` folder)

## Creating the Installer

1. Open Inno Setup Compiler
2. Open the `setup.iss` script file from this project
3. Click on the "Compile" button in the toolbar (or press F9)
4. The installer will be created in the `installer` folder (the folder will be created automatically)

## What's Included in the Installer

The installer packages the following components:

- The main executable (`internetm.exe`)
- All localization files from the `locales` folder
- Icon files from the `icon` folder
- Desktop and Start Menu shortcuts
- Uninstaller

## Installer Features

- Multi-language support for the installer itself (English, French, German, Italian, Spanish)
- Option to create a desktop shortcut
- Option to launch the application after installation
- Proper installation in Program Files with appropriate permissions

## Customizing the Installer

You can modify the `setup.iss` file to customize various aspects of the installer:

- Change the application version
- Add additional files
- Modify installation directory
- Change installer appearance
- Add registry entries
- Add custom installation steps

Refer to the [Inno Setup Documentation](https://jrsoftware.org/ishelp/) for more details on customizing the installer.