# dynamixel-controller

dynamixel-controller is a Python library designed from the ground up to work with any Dynamixel motor on the market with few to no modifications.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dynamixel-controller.

```bash
pip install dynamixel-controller
```

## Usage
#### Import:
```python
from dynio import *
```

#### Port handling:
```python
dxl_io = dxl.DynamixelIO('portname') # your port for U2D2 or other serial device
```

#### Pre-made motor declarations:
```python
ax_12 = dxl_io.new_ax12_1(1)     # AX-12 protocol 1 with ID 1
mx_2 = dxl_io.new_mx_2(1)        # MX series protocol 2 with ID 1
mx_12_1 = dxl_io.new_mx12_1(1)   # MX-12 protocol 1 with ID 1
mx_28_1 = dxl_io.new_mx28_1(1)   # MX-28 protocol 1 with ID 1
mx_64_1 = dxl_io.new_mx64_1(1)   # MX-64 protocol 1 with ID 1
mx_106_1 = dxl_io.new_mx106_1(1) # MX-106 protocol 1 with ID 1
```

#### Custom motor declarations:
These are made by creating a JSON file with the control table in it. 
See [this](https://github.com/UGA-BSAIL/dynamixel-controller/blob/master/example.json) as an example.
```python
custom_motor = dxl_io.new_motor(ID, JSON FILE, PROTOCOL, min_position=MIN_POSITION, max_position=MAX_POSITION)
```
If you are using a Protocol 2 motor set to run on Protocol 1
```python
custom_motor = dxl_io.new_motor(ID, JSON FILE, protocol=1, 
                                protocol_control_table=2, min_position=MIN_POSITION, max_position=MAX_POSITION)
```

#### Motor Control:
The most prevalent functions are pre-implemented as methods for the motor objects. 
These include:
```python
motor.torque_enable()
motor.torque_disable()
motor.set_acceleration(acceleration)
motor.set_velocity_mode()
motor.set_velocity(velocity)
motor.set_position_mode()
motor.set_position(position)
motor.set_angle(angle) 
motor.set_extended_position_mode()
motor.set_position(position)
position = motor.get_position()
angle = motor.get_angle()
current = motor.get_current()
```
All other values can be easily read from or written to using their [control table](http://emanual.robotis.com/) name. Example:
```python
motor.write_control_table("LED", 1) # Turns the LED on
speed = motor.read_control_table("Present_Speed") # Returns present velocity
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Especially encouraged is new control tables to be published as part of the package.

## License
[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)