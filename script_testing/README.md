In this folder you can find a script we elaborated for automatically testing our project. It only opens the webpages mentioned in targets.csv.<br>

Requirements:<br>
**-Install (with dpkg) the provided .deb**
**-Install (with pip) selenium, panda**
**-Install (with apt) softflowd**

How to use:<br>
**- sudo softflowd -v 5 -n <ip of the PC where the project is running>:2055 -i eth0 -d**
**- python3 test.py**

The project must be running at the specified IP in softflowd command
