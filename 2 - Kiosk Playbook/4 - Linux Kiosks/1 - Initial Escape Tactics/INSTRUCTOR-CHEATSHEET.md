# Linux Kiosk Instructor Cheatsheet

## Set Up a Kiosk

From this directory, run the setup as the logged-in `kiosk` user, **not** with `sudo`:

```bash
./prepare-kiosk.sh --level 2 --browser firefox --user kiosk --reboot
```

Enter the instructor-held `kiosk` password when prompted. For prerequisites and other options, see the [full setup guide](README.md).

## What Reboot Should Do

1. GDM automatically logs in as `kiosk`.
2. GNOME autostart runs `~/Public/start-kiosk.sh`.
3. The kiosk app opens full screen after about five seconds.

Confirm that `Ctrl+Alt+Shift+O` opens the instructor terminal and that common escape shortcuts such as `Super`, `Alt+Tab`, and `Ctrl+L` are blocked.

## Reset Between Students

If anything fails or the kiosk is changed:

1. Press `Ctrl+Alt+Shift+O`.
2. Run:

```bash
kiosk reset --reboot
```

The reset restores the original autostart baseline, kiosk files, GDM automatic login, GNOME lockdown, and instructor shortcut. It then reboots so GDM can log in and launch the kiosk app again.

Run only one reset at a time on each device. If a newly pulled repository version must be installed, run `./prepare-kiosk.sh reset --reboot` from this directory instead.

## Workshop Links

- [Linux kiosk playbook](../README.md)
- [Initial protocol-handler escape](Protocol-Handler-Escape/README.md)
- [Next steps: persistence and enumeration](<../2 - Next Steps/README.md>)
- [Internal discovery and recon](<../3 - Internal Discovery and Recon/README.md>)
- [Post-exploitation](<../4 - Post-Exploitation - Moving from Kiosk to Domain and-or Network/README.md>)
- [Defensive recommendations](<../../../5 - Defensive Recommendations/README.md>)
