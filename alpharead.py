import yaml
import platform
from struct import *
from pyModbusTCP.client import ModbusClient
from os import system

# load registerlist from yaml file
with open('registers_new.yaml', 'r') as f:
    #data = list(yaml.load_all(f, Loader=SafeLoader))[0]
    data = yaml.safe_load(f)

mb_host = data['config']['modbus_host']
mb_port = data['config']['modbus_port']
mb_unitid = data['config']['modbus_unitid']
mb_timeout = data['config']['modbus_timeout']
 
# clear terminal screen
if platform.system() == "Darwin" or platform.system == 'Linux':
  system('clear') # Unix style
else:
  system('cls')   # Windows



# open modbus connection to inverter or proxy (if using e.g. EVCC.io)
mb_client = ModbusClient(host = mb_host, port = mb_port, unit_id = mb_unitid, auto_open=True, auto_close=False)

for register in data['registers']:
  #print (register)
  print (register["description"])
  print (f'Register address: {format(register["register_address"],"#06x")}' + f' size {register["register_size"]}')

  mb_return = mb_client.read_holding_registers(reg_addr=register["register_address"], reg_nb=register["register_size"])
  
  # test to do it more convenient 
  payload = b"".join(pack("!H", x) for x in mb_return)
  
  def decode_data(payload, type):
    match register['type']:
      case "uint":  # 2 x 16bit word
        return (unpack("!I", payload)[0])
      case "int": # 2 x 16bit word
        return (unpack("!i", payload)[0])
      case "ushort": # 1 x 16bit word
        return (unpack("!H", payload)[0])
      case "short": # 1 x 16bit word
        return (unpack("!h", payload)[0])
  
  print(f'{format(decode_data(payload,register["type"]) * register["scale"],".2f") + " " + register["unit"]}')

  print()
mb_client.close()