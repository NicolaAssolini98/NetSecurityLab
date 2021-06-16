import easymodbus.modbusClient

plc1 = easymodbus.modbusClient.ModbusClient("157.27.95.62", 502)
plc1.connect()


# plc1.close()

