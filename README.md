# TMA Lab - Netflow Classifier

This is a Netflow Classifier that can classify web applications using flow-level data. It can be run in two modes, a live capturing of Netflow packets from an exporter or with a CSV file. First the Python Netflow module needs to be instaled with **pip install netflow**. Then the **main.py** script can be run. If being run with a CSV file, the usage is as follows <br>

**python3 main.py <file_name> <max_seconds_between_flow> <ip_addressess_of_PCs>** <br>
  
Otherwise, first a Netflow exporter needs to be run using **sudo softflowd -i eth0 -n 127.0.0.1:2055 -d** while the usage is: <br>
  
**python3 main.py <max_seconds_between_flow> <ip_addressess_of_PCs>**
  
Where in both cases: <br>
  
**<ip_addresses_of_PCs> can be an IP format or a list of addresses separated by space eg. 10.0.2.X or 10.0.2.15 10.0.2.16**
