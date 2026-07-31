# Linux Kiosk Instructor Cheatsheet

Use this guide to deploy, validate, recover, and reset the CTRL+ESC+HOST workshop kiosks.

## Recommended Configuration

- Desktop: GNOME with GDM
- Kiosk account: `kiosk`
- Browser: Firefox
- Lockdown: Level 2
- Instructor recovery shortcut: `Ctrl+Alt+Shift+O`
- Workshop reset command: `kiosk reset`

Level 2 disables the ordinary Activities/Super paths, common GNOME navigation, standard terminal shortcuts, and common browser escape shortcuts. It leaves the instructor recovery shortcut available.

## Before First Setup

Complete these checks before running the installer on each device:

1. Log into the GNOME desktop as the account that will become the kiosk account.
2. Confirm the account name with `id -un`.
3. Confirm `~/.config/autostart` contains the baseline that should be restored between students.
4. Remove or rename any pre-existing `~/.config/autostart/skyline-kiosk.desktop` file.
5. Confirm the repository contains both `prepare-kiosk.sh` and `airline_kiosk.html` in the same directory.

The first run captures the autostart baseline once. Reset never replaces that baseline, so make sure the device is clean before initial setup.

## Deploy One Device

Run as the logged-in kiosk user, not with `sudo`:

```bash
chmod +x prepare-kiosk.sh
./prepare-kiosk.sh --level 2 --browser firefox --user kiosk
```

The installer requests `sudo` only when required. At the end, choose whether to reboot.

To configure and reboot without the final prompt:

```bash
./prepare-kiosk.sh --level 2 --browser firefox --user kiosk --reboot
```

To configure without rebooting:

```bash
./prepare-kiosk.sh --level 2 --browser firefox --user kiosk --no-reboot
```

## Deploy the 12 Devices

Use the same command on every device:

```bash
./prepare-kiosk.sh --level 2 --browser firefox --user kiosk --reboot
```

Record successful validation for each device before the workshop:

| Check | Device Result |
|---|---|
| GDM automatically logs in as `kiosk` | |
| Kiosk opens full screen after approximately five seconds | |
| Super does not open Activities | |
| `Alt+F2`, `Alt+F4`, and `Alt+Tab` are blocked | |
| `Ctrl+W`, `Ctrl+T`, `Ctrl+N`, `Ctrl+L`, and `F11` are blocked | |
| `Ctrl+Alt+Shift+O` opens `gnome-terminal` | |
| `command -v kiosk` returns `/usr/local/bin/kiosk` | |
| Email link opens the expected Thunderbird workflow | |

## Lockdown Level Reference

### Level 1

```bash
./prepare-kiosk.sh --level 1
```

Use Level 1 when only Activities, hot corners, and Super-based GNOME navigation need to be disabled.

### Level 2

```bash
./prepare-kiosk.sh --level 2
```

Use Level 2 for the workshop. It includes Level 1 and blocks common GNOME and browser shortcuts that would make the exercise trivial.

The selected level is saved during first setup. `kiosk reset` always reapplies that saved level.

## Reset Between Students

From the full-screen kiosk:

1. Press `Ctrl+Alt+Shift+O`.
2. Wait for `gnome-terminal` to open.
3. Run the reset command.

Reset and ask before rebooting:

```bash
kiosk reset
```

Reset and reboot automatically:

```bash
kiosk reset --reboot
```

Reset without rebooting:

```bash
kiosk reset --no-reboot
```

For normal workshop turnover, use `kiosk reset --reboot`. It performs the following operations:

1. Loads the browser, user, and lockdown level saved during first setup.
2. Stages the original pre-workshop autostart directory.
3. Removes participant-created autostart persistence from the active configuration.
4. Recreates `skyline-kiosk.desktop` on top of the baseline.
5. Refreshes the kiosk HTML and launch wrapper.
6. Reapplies Thunderbird handling, GDM autologin, GNOME lockdown, and instructor recovery.
7. Reboots into the full-screen kiosk.

## Emergency Recovery

If the kiosk application is broken but GNOME is still responding:

```text
Ctrl+Alt+Shift+O
```

Then run:

```bash
kiosk reset --reboot
```

If the recovery shortcut is unavailable, virtual-terminal switching is outside the GNOME lockdown scope. On the workshop image, an instructor can try:

```text
Ctrl+Alt+F3
```

Log in with the appropriate administrative credentials, return to the active kiosk account when required, and run `kiosk reset --reboot`. The reset needs the kiosk user's active GNOME session and its D-Bus session to reapply GNOME settings reliably.

## Update an Existing Kiosk

After pulling a newer repository version, run the repository copy with the `reset` action:

```bash
./prepare-kiosk.sh reset --reboot
```

This retains the original baseline and saved deployment choices while updating the installed script and HTML under `/usr/local`.

Do not run first-time setup again on an already configured account. It intentionally stops with:

```text
This account is already configured. Use 'kiosk reset' instead.
```

## Important Paths

Installed runtime:

```text
/usr/local/bin/kiosk
/usr/local/libexec/ctrl-esc-host-kiosk/prepare-kiosk.sh
/usr/local/share/ctrl-esc-host-kiosk/airline_kiosk.html
```

Active user files:

```text
~/Public/airline_kiosk.html
~/Public/start-kiosk.sh
~/.config/autostart/skyline-kiosk.desktop
```

Root-protected reset state:

```text
/var/lib/ctrl-esc-host-kiosk/users/<uid>/config
/var/lib/ctrl-esc-host-kiosk/users/<uid>/autostart.original
/var/lib/ctrl-esc-host-kiosk/users/<uid>/autostart.status
/var/lib/ctrl-esc-host-kiosk/users/<uid>/custom-keybindings.original
```

GDM configuration and first-run backup:

```text
/etc/gdm3/custom.conf
/etc/gdm3/custom.conf.ctrl-esc-host-original
```

Some systems use `/etc/gdm/custom.conf` instead.

## Quick Diagnostics

Confirm the installed command:

```bash
command -v kiosk
```

Confirm the active kiosk autostart entry:

```bash
ls -l ~/.config/autostart/skyline-kiosk.desktop
```

Confirm the saved deployment configuration:

```bash
sudo cat "/var/lib/ctrl-esc-host-kiosk/users/$(id -u)/config"
```

Confirm the GDM autologin values:

```bash
sudo grep -E '^(AutomaticLoginEnable|AutomaticLogin)=' /etc/gdm3/custom.conf
```

Confirm the Activities overlay key is disabled:

```bash
gsettings get org.gnome.mutter overlay-key
```

Expected value:

```text
''
```

## Common Failures

### Script Was Run with sudo

Run it again as the logged-in kiosk user:

```bash
./prepare-kiosk.sh --level 2 --browser firefox --user kiosk
```

The script invokes `sudo` internally when needed.

### Account Is Already Configured

Use:

```bash
kiosk reset --reboot
```

### No Completed Setup Was Found

Run first-time setup from the repository. `kiosk reset` only works after setup successfully saves the deployment configuration.

### GDM Configuration Was Not Found

Confirm the device uses GNOME with GDM and has either:

```text
/etc/gdm3/custom.conf
/etc/gdm/custom.conf
```

### Existing Custom Shortcut Conflict

The installer refuses to overwrite an existing shortcut that conflicts with Super lockdown, Level 2, or `Ctrl+Alt+Shift+O`. Remove or reassign the conflicting shortcut, then rerun setup.

### Reserved Autostart Filename Exists

Before first setup, remove or rename:

```text
~/.config/autostart/skyline-kiosk.desktop
```

Do not manually delete `/var/lib/ctrl-esc-host-kiosk` during routine workshop reset. That directory contains the authoritative first-run baseline.
