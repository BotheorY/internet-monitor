; Inno Setup Script for Internet Monitor
; This script creates a Windows installer for the Internet Monitor application

#define MyAppName "Internet Monitor"
#define MyAppVersion "1.1.0"
#define MyAppPublisher "Internet Monitor"
#define MyAppExeName "internetm.exe"

[Setup]
; Basic application information
AppId={{A8F9D3B7-F2A1-4E8C-9B3D-C7E3A5F9D8E6}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; Compression settings
Compression=lzma
SolidCompression=yes
; Setup visual appearance
WizardStyle=modern

; Output directory for the installer
OutputDir=installer
OutputBaseFilename=InternetMonitorSetup

; Installer requires admin privileges to install to Program Files
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; Main executable
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; Icon files
Source: "icon\internet-monitor.ico"; DestDir: "{app}\icon"; Flags: ignoreversion
Source: "icon\internet-monitor.png"; DestDir: "{app}\icon"; Flags: ignoreversion
Source: "icon\internet-monitor_64x64.png"; DestDir: "{app}\icon"; Flags: ignoreversion
; Localization files - include all JSON files from the locales directory
Source: "locales\*.json"; DestDir: "{app}\locales"; Flags: ignoreversion

[Icons]
; Create program group shortcuts
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon\internet-monitor.ico"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
; Create desktop shortcut if selected
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon\internet-monitor.ico"; Tasks: desktopicon

[Run]
; Option to run the application after installation is complete
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent