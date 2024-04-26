# ap-monitor
A tool to monitor access points (or any other host), which disables the port on a TP-Link Easy Smart Switch when connection is lost. This can be handy if you have a host (such as an access point) in a physically unsecure location, and you don't want people to be able to unplug the access point and access your LAN (and any VLANs) without authenticating with a WiFi network first.

This should work on any TL-SG1[0]xx[P/D]E switch, and I've got it working on the following models:
- TL-SG1016PE
- TL-SG1024DE
- TL-SG116E

A big thanks to [vmakeev](https://github.com/vmakeev) and his [hass_tplink_easy_smart](https://github.com/vmakeev/hass_tplink_easy_smart) project. The TP-Link API interface he wrote for a Home Assistant component works perfectly standalone, and is used to disable the ports on the switches in this project.
