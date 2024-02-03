import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Joy
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import *


class gripper(Node):
    def __init__(self):
        super().__init__('gripper')
        self.previous = 0
        self.position = True
        self.subscription = self.create_subscription(Joy, 'joy', self.joy_callback, 10)
        self.logger = self.get_logger()

        try:
            self.gripper = DigitalOutput()
            self.gripper.openWaitForAttachment(1000)
            self.gripper.setChannel(0)
        except:
            self.logger.warn('cant lode the phidget')



    def joy_callback(self, joy_msg):
        button_status = joy_msg.buttons[0]
        if self.previous == 0 and button_status ==1:
            self.move()
        if button_status == 1:
            self.previous = 1
        if button_status == 0:
            self.previous = 0

        pass


    def move(self):
        try:
            self.position = self.gripper.getState()
            if self.position == True:
                self.gripper.setDutyCycle(0)
                
            else:
                self.gripper.setDutyCycle(1)
                
            self.logger.info(str(self.position))
        except:
            self.logger.warn('cant move the phidget')




def main(args=None):
    rclpy.init()

    gripper1 = gripper()
    rclpy.spin(gripper1)
    

    gripper1.destroy_node()
    rclpy.shutdown()
    gripper1.gripper.close()


if __name__ == '__main__':
    main()