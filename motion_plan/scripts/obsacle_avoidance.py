#! /usr/bin/env python



import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
pub = None

def clbk_laser(msg):
    regions = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:719]), 10),
    }

    take_action(regions)

def take_action(regions):
    msg = Twist()
    linear_x = 0
    angular_z = 0

    state_description = ''

    if regions['front'] < 1:
        state_description='obstacle'
        if max(regions['right'],regions['fright'],regions['fleft'],regions['front'],regions['left'])==regions['right']:
            linear_x=0
            angular_z=3
        elif max(regions['right'],regions['fright'],regions['fleft'],regions['front'],regions['left'])==regions['left']:
            linear_x=0
            angular_z=-3
        elif max(regions['right'],regions['fright'],regions['fleft'],regions['front'],regions['left'])==regions['fleft']:
            linear_x=0
            angular_z=-1.5
        elif max(regions['right'],regions['fright'],regions['fleft'],regions['front'],regions['left'])==regions['fright']:
            linear_x=0
            angular_z=1.5
        elif max(regions['right'],regions['fright'],regions['fleft'],regions['front'],regions['left'])==regions['front']:
            linear_x=0.6
            angular_z=0
        else:
            linear_x=-0.6
            angular_z=0

    else:
        state_description = 'no obstacle'
        linear_x=0.6
        rospy.loginfo(regions)

    rospy.loginfo(state_description)
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pub.publish(msg)

def main():
    global pub

    rospy.init_node('reading_laser')

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    sub = rospy.Subscriber('/m2wr/laser/scan', LaserScan, clbk_laser)
    rospy.spin()

if __name__ == '__main__':
    main()
