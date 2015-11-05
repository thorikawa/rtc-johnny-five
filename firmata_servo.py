#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file firmata_servo.py
 @brief rt component for firmata interface of servo motor
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

from pyfirmata import Arduino, util

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
firmata_servo_spec = ["implementation_id", "firmata_servo", 
		 "type_name",         "firmata_servo", 
		 "description",       "rt component for firmata interface of servo motor", 
		 "version",           "1.0.0", 
		 "vendor",            "Takahiro Horikawa", 
		 "category",          "Development", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.com_port", "/dev/tty.USB0",
		 "conf.__widget__.com_port", "text",
		 ""]
# </rtc-template>

##
# @class firmata_servo
# @brief rt component for firmata interface of servo motor
# 
# 
class firmata_servo(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_servo_data = RTC.TimedVector2D(RTC.Time(0,0),0)
		"""
		"""
		self._servo_dataIn = OpenRTM_aist.InPort("servo_data", self._d_servo_data)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  com_port
		 - DefaultValue: /dev/tty.USB0
		"""
		self._com_port = ['/dev/tty.USB0']
		
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("com_port", self._com_port, "/dev/tty.USB0")
		
		# Set InPort buffers
		self.addInPort("servo_data",self._servo_dataIn)
		
		# Set OutPort buffers
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onStartup(self, ec_id):
		print "onStartup Begin"
		pinNumber = [3, 5, 6, 7, 11]
		self.pin = [None, None, None, None, None]
		try:
			self.board = Arduino('/dev/tty.usbmodem1411')
			for i in range(5):
				self.board.servo_config(pinNumber[i], angle=90)
				# Caution: Don't use board.get_pin('d:*:s') as it calls servo_config method with angle=0, which damages your servo.
				self.pin[i] = self.board.digital[pinNumber[i]]
			print "onStartup End"
		except Exception as e:
			print "some errors %s" % str(e)
		self.pin[0].write(80)
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The activated action (Active state entry action)
	#	# former rtc_active_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	# 
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onActivated(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The deactivated action (Active state exit action)
	#	# former rtc_active_exit()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onDeactivated(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The execution action that is invoked periodically
	#	# former rtc_active_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onExecute(self, ec_id):
		if self._servo_dataIn.isNew():
			print "onExecute New"
			servoData = self._servo_dataIn.read()
			servoId = int(servoData.data.x)
			angle = int(servoData.data.y)
			print "%d %d" % (servoId, angle)
			if servoId < len(self.pin) and angle <= 180 and angle >= 0:
				self.pin[servoId].write(angle)
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onError(self, ec_id):
		print "error"
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def firmata_servoInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=firmata_servo_spec)
    manager.registerFactory(profile,
                            firmata_servo,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    firmata_servoInit(manager)

    # Create a component
    comp = manager.createComponent("firmata_servo")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

