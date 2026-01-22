; Inno Setup Script for Zoom Auto Scheduler
; Generated for version 0.1.2

#define MyAppName "Zoom Auto Scheduler"
#define MyAppVersion "0.1.2"
#define MyAppPublisher "ZoomAuto"
#define MyAppURL "https://github.com/tronghv77/zoom-auto"
#define MyAppExeName "ZoomAuto.exe"
#define SourceDir "dist"

[Setup]
AppId={{DE7F7E1A-2B3C-4D5E-8F9A-1B2C3D4E5F6A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\ZoomAuto
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=
OutputDir=dist
OutputBaseFilename=ZoomAuto-Setup-{#MyAppVersion}
Compression=zip
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ChangesAssociations=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1
Name: "startupmenu"; Description: "Chạy tự động khi khởi động máy"; GroupDescription: "Khởi động"; Flags: unchecked

[Files]
Source: "{#SourceDir}\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceDir}\app.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\app.ico"
Name: "{group}\Dỡ cài đặt {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\app.ico"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon; IconFilename: "{app}\app.ico"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Chạy {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Registry]
; Startup task for "Run on startup" option
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueName: "ZoomAuto"; ValueType: string; ValueData: "{app}\{#MyAppExeName}"; Flags: uninsdeletevalue; Tasks: startupmenu

[InstallDelete]
Type: filesandordirs; Name: "{app}\*"

[UninstallDelete]
Type: filesandordirs; Name: "{localappdata}\ZoomAuto"
