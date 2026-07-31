# Linux Kiosk Instructor Cheatsheet

## Start the Kiosk

Plug in the device and turn it on. No setup is needed.

## What Reboot Should Do

1. GDM automatically logs in as `kiosk`.
2. GNOME autostart runs `~/Public/start-kiosk.sh`.
3. The kiosk app opens full screen after about five seconds.

If the kiosk does not appear, wait briefly, then use the recovery steps below.

For Firefox 147 or newer, manually verify that `Ctrl+W`, `Ctrl+Shift+W`, and `Ctrl+Q` do nothing. Then confirm that available controls or links can still open and use multiple tabs and popup windows, and that the kiosk Email link still launches the configured Thunderbird application.

## Reset Between Students

If the kiosk is broken, changed, or does not start correctly:

1. Press `Ctrl+Alt+Shift+O`.
2. Run:

```bash
kiosk reset --reboot
```

The reset restores the original kiosk files and autostart configuration, reapplies GDM automatic login and lockdown, and reboots. After reboot, GDM should automatically log in and launch the kiosk app.

Run only one reset at a time on each device. If the recovery shortcut does not work, contact the technical lead rather than changing system files.

## Switch Browser

`kiosk reset` always reuses the browser saved during first-time setup. To redeploy with a different browser, remove the saved kiosk configuration and run first-time setup with the new browser. Install the new browser first if it is not already present.

```bash
kiosk remove
./prepare-kiosk.sh --level 2 --browser chrome --user kiosk --reboot
```

`kiosk remove` clears the saved configuration and the managed autostart entry. GDM autologin and GNOME lockdown remain until the next setup overwrites them.

## Workshop Links

- [Linux kiosk playbook](../README.md)
- [Initial protocol-handler escape](Protocol-Handler-Escape/README.md)
- [Next steps: persistence and enumeration](<../2 - Next Steps/README.md>)
- [Internal discovery and recon](<../3 - Internal Discovery and Recon/README.md>)
- [Post-exploitation](<../4 - Post-Exploitation - Moving from Kiosk to Domain and-or Network/README.md>)
- [Defensive recommendations](<../../../5 - Defensive Recommendations/README.md>)
