#!/usr/bin/env python

import math
import rospy
from sensor_msgs.msg import Range
from std_msgs.msg import Header
from geometry_msgs.msg import PoseStamped
from multi_car_msgs.msg import CarMeasurement
from multi_car_msgs.msg import CarState
from multi_car_msgs.msg import UWBRange
import random
import copy

class FakeUWB(object):

    def __init__(self):
        self.rate = rospy.Rate(rospy.get_param("~frequency", 20))
        self.Ncars = rospy.get_param("/num_cars", 3)

        self.ranges = {}
        self.rng = UWBRange()
        self.rng.header = Header()

        self.sigma = rospy.get_param("/uwb_sigma")

        self.position = None

        self.positions = [None]*self.Ncars

        self.range_pub = rospy.Publisher('/ranges', UWBRange, queue_size=1)
        self.range_sub = rospy.Subscriber('/range_position', CarState, self.range_sub_cb)
        self.inner_rate = rospy.Rate(50)

    def range_sub_cb(self, cs):
        frame_id = cs.header.frame_id
        ID = cs.car_id
        self.positions[ID] = (cs.state[0], cs.state[1])

    def publish_range(self):
        pos_good = True
        for pos in self.positions:
            if pos is None:
                pos_good = False

        if pos_good:
            for j, pos1 in enumerate(self.positions):
                for k, pos2 in enumerate(self.positions):
                    if k > j:
                        x = pos2[0]
                        y = pos2[1]
                        dist = math.sqrt((pos1[0] - x)**2 + (pos1[1] - y)**2)
                        rng = UWBRange()
                        rng.header = Header()
                        rng.header.stamp = rospy.Time.now()
                        rng.header.frame_id = "car" + str(j)
                        rng.to_id = j
                        rng.from_id = k
                        rng.distance = max(0.0, dist + random.gauss(0.0, self.sigma))
                        self.range_pub.publish(rng)
                        self.inner_rate.sleep()

                        rng.to_id = k
                        rng.from_id = j
                        rng.distance = max(0.0, dist + random.gauss(0.0, self.sigma))
                        self.range_pub.publish(rng)
                        self.inner_rate.sleep()

    def run(self):
        while not rospy.is_shutdown():
            self.publish_range()


if __name__ == "__main__":
    rospy.init_node("uwb", anonymous=False)
    uwb = FakeUWB()
    uwb.run()
    #rospy.spin()
