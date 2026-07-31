# SETUP — Full Deployment Test Instructions

> **Temporary section.** Operational verification of the Linux kiosk deployment after the last rounds of commits (`0a9c522`, `1d71186`, `1f8ad70`). There is no automated test suite in this repo; verification runs on a target Ubuntu/GNOME device.

## What changed recently

- `0a9c522` — rewrote `prepare-kiosk.sh` (setup + reset), restructured README
- `1d71186` — added `INSTRUCTOR-CHEATSHEET.md`
- `1f8ad70` — **hardening**: active GDM service verification (`verify_active_gdm`), sudo-preflight error message, post-install `grep -Fxq` assertions that GDM actually has `AutomaticLoginEnable=True` and `AutomaticLogin=<user>`, Super-lockdown wording. This commit is the one most worth exercising.

## Test environment

A fresh Ubuntu Desktop (GNOME + GDM) VM or one of the 12 workshop devices. Do not test on a production machine — `prepare-kiosk.sh` reconfigures GDM, autostart, and gsettings.

This guide was validated on a VM snapshot with: user `kiosk`, GDM3 active, `/etc/gdm3/custom.conf` present, no prior kiosk config (fresh), sudo requiring the `kiosk` password.

## Stage 1 — Pre-flight (on a clean device, as `kiosk`)

Confirm the prerequisites the new hardening checks for. If any fail, the script will now `die` instead of silently misconfiguring:

```bash
id -un                       # -> kiosk
sudo -v                      # accepts instructor password (NEW: preflight now dies with a clear message)
systemctl is-active display-manager.service                       # -> active
systemctl show --property=FragmentPath --value display-manager.service  # -> *gdm*.service
cat /etc/X11/default-display-manager 2>/dev/null                  # -> gdm or gdm3
ls -l /etc/gdm3/custom.conf /etc/gdm/custom.conf 2>/dev/null      # one must exist
```

Remove any stale reserved file:

```bash
rm -f ~/.config/autostart/skyline-kiosk.desktop
```

## Stage 2 — First-time setup (interactive, to validate the reboot prompt)

```bash
cd "2 - Kiosk Playbook/4 - Linux Kiosks/1 - Initial Escape Tactics"
chmod +x prepare-kiosk.sh
./prepare-kiosk.sh --user kiosk
```

Enter the `kiosk` password at the sudo prompt. Watch for `Configured GDM automatic login for 'kiosk'.` (the new `grep -Fxq` assertions die if the write failed). Answer `y` to reboot (this branch only runs when stdin is a TTY — worth confirming).

## Stage 3 — Booted-kiosk validation checklist

After reboot, fill in the cheatsheet table per device:

| Check | Expected |
|---|---|
| GDM auto-logs in as `kiosk` | yes |
| Kiosk opens full screen ~5s after login | yes |
| Super → Activities | blocked |
| `Alt+F2`, `Alt+F4`, `Alt+Tab` | blocked |
| `Ctrl+W/T/N/L`, `F11` | blocked |
| `Ctrl+Alt+Shift+O` | opens `gnome-terminal` |
| `command -v kiosk` | `/usr/local/bin/kiosk` |

Diagnostics from the cheatsheet:

```bash
command -v kiosk
ls -l ~/.config/autostart/skyline-kiosk.desktop
sudo cat "/var/lib/ctrl-esc-host-kiosk/users/$(id -u)/config"
sudo grep -E '^(AutomaticLoginEnable|AutomaticLogin)=' /etc/gdm3/custom.conf
gsettings get org.gnome.mutter overlay-key   # -> ''
```

## Stage 4 — mailto escape (the actual workshop exercise)

Follow `Protocol-Handler-Escape/README.md`: 6-digit ID → Assistance → Digital Support → Contact Support → Email link. Confirm Thunderbird launches (Firefox must delegate `mailto:` to the OS handler the script verified). Then:

Thunderbird → Troubleshooting → Open Directory → Nautilus → right-click → Open in Terminal.

This validates the exercise still works end-to-end.

## Stage 5 — Reset round-trip (most important to re-test)

From the shell you just spawned, and then again via the recovery shortcut (`Ctrl+Alt+Shift+O`):

```bash
# via recovery shortcut Ctrl+Alt+Shift+O
kiosk reset            # interactive, asks about reboot
```

Re-verify Stage 3 after reset. Then test the non-interactive modes the cheatsheet documents:

```bash
kiosk reset --reboot
kiosk reset --no-reboot
```

Confirm reset refuses setup options:

```bash
kiosk reset --level 1   # should die: "kiosk reset reuses the saved browser, user, and level."
```

## Stage 6 — Update path (simulates pulling these commits onto a deployed device)

On an already-configured device, pull and run from the repo:

```bash
./prepare-kiosk.sh reset --reboot
```

Confirm it preserves `/var/lib/ctrl-esc-host-kiosk/users/<uid>/autostart.original` and the saved config while refreshing `/usr/local/libexec/...` and the HTML.

## Stage 7 — Negative paths worth hitting once

```bash
sudo ./prepare-kiosk.sh                  # dies: "Do not run this script with sudo."
./prepare-kiosk.sh                       # again, on configured account -> "already configured"
kiosk reset --level 1                    # dies: reset reuses saved options
```

Point at a non-GDM display manager (e.g. lightdm) → `verify_active_gdm` dies: "The active display manager is '...', not GDM."

## Regression focus for `1f8ad70`

The highest-risk changes are the new GDM-variant detection (`verify_active_gdm` + `detect_gdm_configuration` ordering) and the two post-install `grep -Fxq` assertions. If you only have time for one device, run Stages 1, 2, 5, and 7 — they exercise the commit's hardening directly.

## Revert

Roll back to the VM snapshot when done.