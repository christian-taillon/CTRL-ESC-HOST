This directory contains the Linux kiosk setup and the initial escape workshop resources.

## Resources

- `prepare-kiosk.sh`: One-time GNOME kiosk installer and workshop reset utility.
- `airline_kiosk.html`: SkyLine Premium full-screen kiosk demo.
- `INSTRUCTOR-CHEATSHEET.md`: Deployment, validation, recovery, and between-student reset commands.
- `Protocol-Handler-Escape/`: Protocol-handler breakout walkthrough.

## First-Time Setup

Run the installer as the desktop user that will become the kiosk account. The account must be an Ubuntu administrator authorized to use `sudo`; keep its password available to instructors and do not disclose it to participants. Do not make the account UID 0 or run the entire script with `sudo`. The script requests elevated access only for packages, GDM, `/usr/local` installation, and the root-protected reset state under `/var/lib`. Run repository-based setup or update only from an administrator-reviewed checkout because approval installs that script and HTML into root-owned locations.

On a fresh Ubuntu installation, the simplest arrangement is to create `kiosk` as the initial administrator account. To authorize an existing account, run the following from another administrator account, then sign out and back in:

```bash
sudo usermod -aG sudo kiosk
sudo passwd kiosk
```

Confirm authorization before setup:

```bash
sudo -v
```

```bash
chmod +x prepare-kiosk.sh
./prepare-kiosk.sh --level 2
```

Defaults:

- Browser: Firefox
- Lockdown: Level 2
- Autologin account: Current user
- Reboot: Ask after successful setup when stdin is an interactive terminal; otherwise skip reboot

For unattended deployment to the 12 workshop devices:

```bash
./prepare-kiosk.sh --level 2 --browser firefox --user kiosk --reboot
```

Use `--no-reboot` to finish configuration without rebooting. Google Chrome must already be installed if selected; Firefox and Chromium are installed through `apt-get` when missing.

Firefox is resolved from the system `PATH`. On current Ubuntu Desktop installations this normally selects `/snap/bin/firefox`; the installer no longer silently prefers a separate Firefox under `~/.local/opt`. Refresh the Firefox Snap before workshop deployment and validate the email-link workflow on each image.

## Lockdown Levels

### Level 1

```bash
./prepare-kiosk.sh --level 1
```

Level 1 disables the ordinary Activities and Super-key paths provided by core GNOME schemas:

- Standalone Super key
- GNOME Activities Overview and application view shortcuts
- GNOME hot corners
- Super-based application, window, workspace, and media-key bindings in core GNOME schemas

GNOME Shell extensions can define shortcuts in their own schemas. The script does not disable extension-specific bindings such as Ubuntu Dock or third-party tiling-extension shortcuts; verify or configure those separately on the workshop image.

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

The installer installs Thunderbird when it is absent, selects an installed Thunderbird desktop entry as the OS `mailto:` handler, and verifies that association with `xdg-mime`. The selected browser still decides whether to delegate a `mailto:` link to the OS, so verify the email-link workflow in the deployed browser profile.

## Instructor Recovery

Both levels reserve this instructor shortcut:

```text
Ctrl+Alt+Shift+O
```

It opens `gnome-terminal`. From that terminal, restore the workshop kiosk with:

```bash
kiosk reset
```

The installer also adds `alias kiosk='/usr/local/bin/kiosk'` to `~/.bashrc`. New Bash terminals load it automatically. In a terminal that was already open during setup, run `source ~/.bashrc`; the global `/usr/local/bin/kiosk` command remains available even without the alias.

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
6. Asks whether to reboot when run from an interactive terminal. Without an interactive terminal it skips reboot unless `--reboot` is supplied.

Use either reboot mode when scripting a reset:

```bash
kiosk reset --reboot
kiosk reset --no-reboot
```

`kiosk reset` validates sudo authorization before making changes. Unless a sudo credential is already cached, the instructor enters the `kiosk` account password and then chooses whether to reboot. Run only one reset at a time on each device; separate devices can be reset simultaneously.

Use `kiosk reset` when the instructor should be asked before rebooting. Use `kiosk reset --reboot` only when an immediate reboot after a successful reset is intended.

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

It first verifies that the active systemd display-manager service and Debian display-manager selection, when present, identify GDM. It then creates a one-time sibling backup ending in `.ctrl-esc-host-original`, preserves unrelated configuration, configures the selected user under `[daemon]`, and verifies the installed values.

## Scope

The lockdown targets common core GNOME and browser navigation used to escape a full-screen workshop kiosk. It does not manage GNOME Shell extension shortcuts or disable Linux virtual-terminal switching such as `Ctrl+Alt+F3`, firmware keys, or physical access recovery.
