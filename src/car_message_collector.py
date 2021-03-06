#!/usr/bin/env python

import rospy

from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from multi_car_msgs.msg import UWBRange
from multi_car_msgs.msg import CanopyCollector
from vesc_msgs.msg import VescStateStamped
from std_msgs.msg import Float64
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import OccupancyGrid
from tf2_msgs.msg import TFMessage
from multi_car_msgs.msg import CarControl

class Collector(object):

    def __init__(self):
        self.rate = rospy.Rate(rospy.get_param("~frequency", 60))
        self.car_id = rospy.get_param("~name", "bad car name")

        self.canopy_msg = CanopyCollector()

        # self.imu_sub       = rospy.Subscriber("/imu/data", Imu, self.imu_cb)
        # self.odom_sub      = rospy.Subscriber("/odom", Odometry, self.odom_cb)
        # self.core_sub      = rospy.Subscriber("/sensors/core", VescStateStamped, self.core_cb)
        # self.servo_sub     = rospy.Subscriber("/sensors/servo_position_command", Float64, self.servo_cb)
        self.range_sub     = rospy.Subscriber("/ranges", UWBRange, self.range_cb)
        self.lidar_sub     = rospy.Subscriber("/control", CarControl, self.control_cb)

        self.canopy_pub    = rospy.Publisher("/canopy_msg", CanopyCollector, queue_size=1)

    def imu_cb(self, data):
        data.header.frame_id = self.car_id + "/" + data.header.frame_id
    	self.canopy_msg.imu = data

    def odom_cb(self, data):
        data.header.frame_id = self.car_id + "/" + data.header.frame_id
    	self.canopy_msg.odom = data

    def range_cb(self, data):
        data.header.frame_id = self.car_id + "/" + data.header.frame_id
    	self.canopy_msg.ranges = data

    def core_cb(self, data):
        data.header.frame_id = self.car_id + "/" + data.header.frame_id
    	self.canopy_msg.core = data

    def servo_cb(self, data):
    	self.canopy_msg.servo = data

    def control_cb(self, data):
        data.header.frame_id = self.car_id + "/" + data.header.frame_id
    	self.canopy_msg.control = data

    def run(self):
        while not rospy.is_shutdown():
            self.canopy_pub.publish(self.canopy_msg)
            self.canopy_msg = CanopyCollector()
            self.rate.sleep()

if __name__ == "__main__":
    rospy.init_node("collector", anonymous=False)
    collector = Collector()
    collector.run()
