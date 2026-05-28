# Install Apps Outside C Drive

Use this checklist when a desktop app defaults to `C:` but you want the main
program files on another drive.

## Checklist

1. Prefer the installer option for a custom installation path.
2. If the installer has no path option, check whether the app has a portable zip.
3. Put portable apps under a stable folder such as `F:\Apps\AppName`.
4. Keep launch scripts and shortcuts outside temporary download folders.
5. Do not move user profile data blindly. Many apps still keep settings under
   `%APPDATA%` or `%LOCALAPPDATA%`.
6. After installation, verify:
   - desktop shortcut target
   - start menu shortcut target
   - app launch
   - update behavior
   - uninstall or rollback path

## Shortcut Repair Pattern

Use a small launcher script when the real executable path needs extra setup,
environment variables, or patch injection. Keep the launcher readable and avoid
hard-coding secrets.
