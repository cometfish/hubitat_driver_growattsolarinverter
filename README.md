# Hubitat Driver for Growatt Solar Inverter

This driver allows you to read data from a Growatt Solar Inverter from Hubitat. Requires a Raspberry Pi with Bluetooth and a web server, and a self-powered Bluetooth Serial adapter connected to the inverter's serial port.

## Set up bluetooth to connect to your Growatt inverter

Connect your bluetooth receiver (if required - some have built-in bluetooth).

Login to your Raspberry Pi and type the following:
```
sudo apt install bluetooth bluez
sudo bluetoothctl
> agent on
> default-agent
> scan on
```
Hold down Pair on your Bluetooth serial adapter
The device should appear in the list with Mac address
`> pair xx:xx:xx:xx:xx:xx`
Enter PIN if prompted. (If you don't get the prompt, but get Authentication failure, you didn't turn the agent on earlier)
Once connected successfully:
```
> trust xx:xx:xx:xx:xx:xx
> exit
```
Now set up serial port profile:
`sudo nano /etc/systemd/system/dbus-org.bluez.service`
Locate the line which says:
`ExecStart=/usr/lib/bluetooth/bluetoothd`
and add `-C` at the end, to run in compatibility mode for rfcomm. Then on the line immediately after, add
`ExecStartPost=/usr/bin/sdptool add SP`
which will add the bluetooth connection into sdp.
Save and exit nano.
Reboot the Pi to apply the changes.
Then:
`sudo sdptool browse local`
Find your newly added BlueZ serial port in the list, note the channel number eg. 1
Bind the device to the serial port `rfcomm1` using BT MAC address and SDP channel number:
`sudo rfcomm bind /dev/rfcomm1 xx:xx:xx:xx:xx:xx 1`

Add above line to `/etc/rc.local` file to bind to bluetooth at boot

## Grant bluetooth access to web server

To grant Apache user (`www-data`) access to the bluetooth connection:
Find out the group that the bluetooth connection belongs to:
`cd /dev`
`ls -l`, and find the group of `rfcomm1`
Then add the Apache user to that group:
`sudo usermod -a -G dialout www-data`

## Install drivers

1. Make sure your Raspberry Pi has a fixed IP address
2. Add `growatt.cgi` to your Raspberry Pi's web server script folder, eg. `/usr/lib/cgi-bin`
3. Add `growatt.groovy` to your Hubitat as a new Driver (under `Drivers Code`)
4. Add a new device for the inverter to your Hubitat, set device Type to your User driver of 'Growatt Solar Inverter'
5. Configure the Hubitat bulb device with:
    1. the script address (your Raspberry Pi IP address plus the script path, eg. `http://192.168.0.2/cgi-bin/growatt.cgi`)

## References
Bluetooth setup for Raspberry Pi: [https://www.teachmemicro.com/setting-raspberry-pi-zero-bluetooth/](https://www.teachmemicro.com/setting-raspberry-pi-zero-bluetooth/)
Growatt Inverter serial interface: [https://snafu.priv.at/mystuff/growatt-proto.pdf](https://snafu.priv.at/mystuff/growatt-proto.pdf)