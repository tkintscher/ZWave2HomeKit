import logging
import os
from pydispatch import dispatcher
import signal
import sys
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('openzwave')


device_file = os.getenv("ZWAVE_DEVICE", "/dev/ttyACM0")
bridge_name = os.getenv("BRIDGE_NAME",  "Z-Wave Bridge")
bridge_mac  = os.getenv("MAC",          "AA:11:22:33:44:55")
bridge_pin  = os.getenv("PINCODE",      "123-45-678")
config_path = '/config'


from pyhap.accessory import Accessory, Bridge, Category
from pyhap.accessory_driver import AccessoryDriver
import pyhap.loader as loader

class Thermostat(Accessory):

    category = Category.THERMOSTAT

    def __init__(self, *args, **kwargs):
        self.zwave_node = kwargs.pop('node')
        
        super(Thermostat, self).__init__(*args, **kwargs)

        self.c_mode_char = self.get_service("Thermostat").get_characteristic("CurrentHeatingCoolingState")
        self.t_mode_char = self.get_service("Thermostat").get_characteristic("TargetHeatingCoolingState")
        self.c_temp_char = self.get_service("Thermostat").get_characteristic("CurrentTemperature")
        self.t_temp_char = self.get_service("Thermostat").get_characteristic("TargetTemperature")
        self.units_char  = self.get_service("Thermostat").get_characteristic("TemperatureDisplayUnits")

        self.c_mode_char.set_value(1)
        self.t_mode_char.set_value(1)
        self.units_char.set_value(0)
        
        self.t_mode_char.setter_callback = self.set_mode
        self.t_temp_char.setter_callback = self.set_target

    def _set_services(self):
        super(Thermostat, self)._set_services()
        self.add_service(loader.get_serv_loader().get("Thermostat"))

    def update_current(self, value):
        print("***** Updating current temperature to {:}".format(value))
        self.c_temp_char.set_value(value)
        self.t_temp_char.set_value(value, should_callback=False)

    def update_target(self, value):
        print("***** Updating target temperature to {:}".format(value))
        self.t_temp_char.set_value(value)

    def set_mode(self, value):
        print("***** Setting heating mode to {:}".format(value))

    def set_target(self, value):
        print("***** Setting target temperature to {:}".format(value))
        for v_id, val in self.zwave_node.get_thermostats().items():
            val.data = value


thermostats = {}


import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption


options = ZWaveOption(device,
                      #config_path=config_path,
                      user_path=config_path,
                      cmd_line="")

options.set_log_file("OZW_Log.txt")
options.set_append_log_file(False)
options.set_console_output(True)
options.set_save_log_level("Info")
options.set_logging(False)
options.lock()

def network_started(network):
    print("***** ZWave network started!")
    print("      Home ID: {:08x} with {:} nodes".format(network.home_id, network.nodes_count))
    dispatcher.connect(node_update,  ZWaveNetwork.SIGNAL_NODE)
    dispatcher.connect(value_update, ZWaveNetwork.SIGNAL_VALUE)

def network_failed(network):
    print("***** ZWave network failed!")
    sys.exit(1)

def network_ready(network):
    print("***** ZWave network ready!")
    print("      Controller: {:}".format(network.controller))
    print("      Nodes: {:}".format(network.nodes_count))

def node_update(network, node):
    print("***** Node update!")
    print("      Name: {:}".format(node))

def value_update(network, node, value):
    print("***** Value update!")
    print("      Node: {:}".format(node))
    print("      Value: {:}".format(value))
    global thermostats
    for val in node.get_thermostats():
        setpoint = node.get_thermostat_value(val)
        if node.node_id in thermostats.keys():
            thermostats[node.node_id].update_current(setpoint)
        else:
            print("!!!!! Could not find thermostat in list")


network = ZWaveNetwork(options, autostart=False)
dispatcher.connect(network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
dispatcher.connect(network_failed,  ZWaveNetwork.SIGNAL_NETWORK_FAILED)
dispatcher.connect(network_ready,   ZWaveNetwork.SIGNAL_NETWORK_READY)
network.start()

print("***** Waiting for ZWave network to start...")
while network.state < network.STATE_READY:
    sys.stdout.write(".")
    sys.stdout.flush()
    time.sleep(1.0)

print("***** ZWave network is ready!")


for node in network.nodes:
    name  = "Node{:d}".format(node)
    for val in network.nodes[node].get_thermostats():
        setpoint = network.nodes[node].get_thermostat_value(val)
        thermostat = Thermostat(name, node=network.nodes[node])
        thermostat.update_current(setpoint)
        thermostat.update_target(setpoint)
        thermostats[node] = thermostat


bridge = Bridge(display_name=bridge_name, mac=bridge_mac, pincode=bridge_pin)
for thermostat in thermostats.values():
    bridge.add_accessory(thermostat)
driver = AccessoryDriver(bridge, port=51826, persist_file=os.path.join(config_path, "accessory.state"))
signal.signal(signal.SIGINT,  driver.signal_handler)
signal.signal(signal.SIGTERM, driver.signal_handler)
driver.start()

