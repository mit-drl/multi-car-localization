#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped


class InitialPoseNode(object):

    def __init__(self):
        self.num_cars = rospy.get_param("/num_cars", 3)
        self.pubs = list()
        for i in xrange(self.num_cars):
            topic = "/initial_pose_car{}".format(i)
            self.pubs.append(rospy.Publisher(
                topic, PoseWithCovarianceStamped, queue_size=1))

        self.count = 0
        self.rate = rospy.Rate(30)

        self.sub = rospy.Subscriber(
            "/initialpose",
            PoseWithCovarianceStamped,
            self.initial_pose_cb, queue_size=1)

    def initial_pose_cb(self, pwc):
        rospy.loginfo("Publishing initpose to car{}".format(self.count % 3))
        for i in xrange(50):
            self.pubs[self.count % 3].publish(pwc)
            self.rate.sleep()
        self.count += 1


if __name__ == "__main__":
    rospy.init_node("initial_pose_node", anonymous=False)
    initial_pose_node = InitialPoseNode()
    rospy.spin()
