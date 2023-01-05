# tma-lab
To use the colector follow the next steps:
  - pip install netflow
  - sudo apt-get install softflowd
  - sudo softflowd -i eth0 -n 127.0.0.1:2055 -d
  - python colector.py
