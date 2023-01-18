# TMA Lab - Netflow Classifier

This is a Netflow Classifier that can classify web applications using flow-level data. It can be run in two modes, a live capturing of Netflow packets from an exporter or with a CSV file.<br>

The dependencies of the project can be installed with:<br>
**pip install netflow gensim==4.1.2 elasticsearch python-dateutil**

Then the **main.py** script can be run. If being run with a CSV file, the usage is as follows <br>

**python3 main.py <file_name> <max_seconds_between_flow> <ip_addressess_of_PCs>** <br>
  
You can find a CSV example in netflowcollector/merged.csv. The PC address in that case would be 10.0.2.15. Note also that you will have to comment line 321 of the main.py and discomment line 320.<br>

Otherwise, first a Netflow exporter needs to be run using **sudo softflowd -i eth0 -n <ip of the PC running main.py>:2055 -d** while the usage is: <br>
  
**python3 main.py <max_seconds_between_flow> <ip_addressess_of_PCs>**
  
Where in both cases: <br>
  
**<ip_addresses_of_PCs> can be an IP format or a list of addresses separated by space eg. 10.0.2.X or 10.0.2.15 10.0.2.16**
