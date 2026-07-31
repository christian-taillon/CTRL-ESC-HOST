This directory contains the Linux kiosk setup and the initial escape workshop resources.

## Resources

- `prepare-kiosk.sh`: One-time GNOME kiosk installer and workshop reset utility.
- `airline_kiosk.html`: SkyLine Premium full-screen kiosk demo.
- `INSTRUCTOR-CHEATSHEET.md`: Deployment, validation, recovery, and between-student reset commands.
- `Protocol-Handler-Escape/`: Protocol-handler breakout walkthrough.

## First-Time Setup

Run the installer as the desktop user that will become the kiosk account. Do not run the entire script with `sudo`; it requests elevated access only for packages, GDM, `/usr/local` installation, and the root-protected reset state under `/var/lib`.

```bash
chmod +x prepare-kiosk.sh
./prepare-kiosk.sh --level 2
```

Defaults:

- Browser: Firefox
- Lockdown: Level 2
- Autologin account: Current user
- Reboot: Ask after successful setup

For unattended deployment to the 12 workshop devices:

```bash
./prepare-kiosk.sh --level 2 --browser firefox --user kiosk --reboot
```

Use `--no-reboot` to finish configuration without rebooting. Google Chrome must already be installed if selected; Firefox and Chromium are installed through `apt-get` when missing.

## Lockdown Levels

### Level 1

```bash
./prepare-kiosk.sh --level 1
```

Level 1 disables the ordinary GNOME Activities and Super-key paths:

- Standalone Super key
- GNOME Activities Overview and application view shortcuts
- GNOME hot corners
- Super-based application, window, workspace, and media-key bindings

### Level 2

```bash
./prepare-kiosk.sh --level 2
```

Level 2 includes Level 1 and blocks common kiosk escape navigation:

- `Alt+F2`, `Alt+F4`, `Alt+Tab`, reverse window switching, and window cycling
- Standard terminal, logout, show-desktop, window movement, and workspace shortcuts
- `Ctrl+W`, `Ctrl+Shift+W`, `Ctrl+T`, `Ctrl+Shift+T`, `Ctrl+N`, and `Ctrl+Shift+N`
- `Ctrl+L`, `F11`, `F12`, and common Chromium developer-tools shortcuts

The script uses normal GNOME `gsettings` and custom media-key bindings. It does not install a GNOME Shell extension or modify the top bar. The browser's full-screen kiosk mode covers the desktop UI.

## Instructor Recovery

Both levels reserve this instructor shortcut:

```text
Ctrl+Alt+Shift+O
```

It opens `gnome-terminal`. From that terminal, restore the workshop kiosk with:

```bash
kiosk reset
```

The shortcut is an operational recovery path, not a security boundary. A participant who obtains a shell can inspect GNOME settings or the setup source.

## Autostart Backup and Reset

The first setup captures `~/.config/autostart` before adding the kiosk launcher. The authoritative workshop baseline and saved setup configuration are protected by a root-owned mode `0700` state directory so a participant shell cannot replace them:

```text
/var/lib/ctrl-esc-host-kiosk/users/<uid>/autostart.original
```

`kiosk reset` performs the following actions:

1. Removes the current participant-modified `~/.config/autostart` directory.
2. Restores the exact first-run baseline.
3. Adds the managed `skyline-kiosk.desktop` entry back on top of the baseline.
4. Refreshes the installed kiosk HTML and browser wrapper.
5. Reapplies GDM autologin, the saved lockdown level, and the instructor shortcut.
6. Asks whether to reboot.

Use either reboot mode when scripting a reset:

```bash
kiosk reset --reboot
kiosk reset --no-reboot
```

Reset first builds a complete replacement in a sibling staging directory. It only swaps that directory into place after the baseline and managed launcher have been prepared successfully. The baseline is never replaced by reset. Therefore the resulting autostart directory is the original pre-kiosk content plus the managed `skyline-kiosk.desktop` required to start the kiosk after login.

## Installed Files

First-time setup installs:

```text
/usr/local/bin/kiosk
/usr/local/libexec/ctrl-esc-host-kiosk/prepare-kiosk.sh
/usr/local/share/ctrl-esc-host-kiosk/airline_kiosk.html
~/Public/airline_kiosk.html
~/Public/start-kiosk.sh
~/.config/autostart/skyline-kiosk.desktop
```

The installed `kiosk` command does not depend on the repository remaining on the device.

## Automatic Login

The installer supports both common GDM configuration paths:

```text
/etc/gdm3/custom.conf
/etc/gdm/custom.conf
```

It creates a one-time sibling backup ending in `.ctrl-esc-host-original`, preserves unrelated configuration, and configures the selected user under `[daemon]`.

## Scope

The lockdown targets common GNOME and browser navigation used to escape a full-screen workshop kiosk. It does not disable Linux virtual-terminal switching such as `Ctrl+Alt+F3`, firmware keys, or physical access recovery.
