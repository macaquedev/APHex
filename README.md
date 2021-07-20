# APHex
Code for my Raspberry Pi-powered 3-DOF hexapod robot.

This is the code for a Hexapod robot I made. I used a lot of inverse kinematics equations which run in C and have Python bindings attached so they can be called from the main I/O code, which is written in Python.

To set this code up, please run the following commands in the Raspberry Pi terminal after cloning the repository.

```bash
sudo apt update
sudo apt upgrade
sudo apt install pigpio python-pigpio python3-pigpio
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cd ik
python setup.py install
cd ..
python3 APHex_with_Joystick.py
```
