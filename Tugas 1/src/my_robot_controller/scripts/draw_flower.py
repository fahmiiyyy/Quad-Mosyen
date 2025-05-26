#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
import math
import random

def set_pen(r, g, b, width, off):
    rospy.wait_for_service('/turtle1/set_pen')
    try:
        pen_service = rospy.ServiceProxy('/turtle1/set_pen', SetPen)
        pen_service(r, g, b, width, off)
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s" % e)

def move_turtle(pub, linear, angular, duration):
    vel = Twist()
    vel.linear.x = linear
    vel.angular.z = angular
    rate = rospy.Rate(20)
    t0 = rospy.Time.now().to_sec()

    while not rospy.is_shutdown():
        t1 = rospy.Time.now().to_sec()
        if t1 - t0 > duration:
            break
        pub.publish(vel)
        rate.sleep()

if __name__ == '__main__':
    rospy.init_node("draw_color_spiral")
    pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
    rospy.sleep(1)

    rospy.loginfo("Drawing colorful spiral star...")

    base_linear = 0.5
    base_angular = 2.5
    step = 0.2

    for i in range(36):
        # Pilih warna acak
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        set_pen(r, g, b, 3, 0)  # ganti warna dengan ketebalan 3

        linear = base_linear + i * step
        angular = base_angular
        duration = 1.5 + i * 0.05

        move_turtle(pub, linear, angular, duration)

    rospy.loginfo("Done drawing colorful spiral star.")
