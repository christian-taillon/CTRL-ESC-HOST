# Linux Kiosk Instructor Cheatsheet

## Start the Kiosk

Plug in the device and turn it on. No setup is needed.

## What Reboot Should Do

1. GDM automatically logs in as `kiosk`.
2. GNOME autostart runs `~/Public/start-kiosk.sh`.
3. The kiosk app opens full screen after about five seconds.

If the kiosk does not appear, wait briefly, then use the recovery steps below.

## Reset Between Students

If the kiosk is broken, changed, or does not start correctly:

1. Press `Ctrl+Alt+Shift+O`.
2. Run:

```bash
kiosk reset --reboot
```

The reset restores the original kiosk files and autostart configuration, reapplies GDM automatic login and lockdown, and reboots. After reboot, GDM should automatically log in and launch the kiosk app.

Run only one reset at a time on each device. If the recovery shortcut does not work, contact the technical lead rather than changing system files.

## Workshop Links

- [Linux kiosk playbook](../README.md)
- [Initial protocol-handler escape](Protocol-Handler-Escape/README.md)
- [Next steps: persistence and enumeration](<../2 - Next Steps/README.md>)
- [Internal discovery and recon](<../3 - Internal Discovery and Recon/README.md>)
- [Post-exploitation](<../4 - Post-Exploitation - Moving from Kiosk to Domain and-or Network/README.md>)
- [Defensive recommendations](<../../../5 - Defensive Recommendations/README.md>)
