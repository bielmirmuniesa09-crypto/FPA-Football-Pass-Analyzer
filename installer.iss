#define MyAppName "FPA - Football Pass Analyzer"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Biel Mir Muniesa"
#define MyAppExeName "FPA.exe"

[Setup]
AppId={{3D4552A8-5BF4-4D65-85D8-B181DA3AC51F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\FPA Football Pass Analyzer
DefaultGroupName=FPA Football Pass Analyzer
DisableProgramGroupPage=yes
OutputDir=installer-output
OutputBaseFilename=FPA-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "catalan"; MessagesFile: "compiler:Languages\Catalan.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear una drecera a l'escriptori"; GroupDescription: "Dreceres addicionals:"

[Files]
Source: "dist\FPA\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\FPA - Football Pass Analyzer"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\FPA - Football Pass Analyzer"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Obrir FPA"; Flags: nowait postinstall skipifsilent
