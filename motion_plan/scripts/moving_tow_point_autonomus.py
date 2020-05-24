#! /usr/bin/env python
import rospy
import math
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
pub = None
regions={}
def clbk_laser(msg):
    global regions
    regions = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:146]), 10),
        'front':  min(min(msg.ranges[146:574]), 10),
        'fleft':  min(min(msg.ranges[574:575]), 10),
        'left':   min(min(msg.ranges[576:719]), 10),
    }

def clbk_dis(msg):
    x=msg.pose.pose.position.x
    y=msg.pose.pose.position.y
    z_orenitation=msg.pose.pose.orientation.z
    move_to_x=8
    move_to_y=9
    b=math.sqrt((move_to_x-x)**2+(move_to_y-y)**2)
    a=((move_to_y-y)/(move_to_x-x))
    angle=math.atan(a)
    print(angle)
    take_action(angle,z_orenitation,b)

def take_action(angle,z_orenitation,b):
    msg = Twist()
    linear_x = 0
    angular_z = 0

    state_description = ''

    if regions['front'] < 1:
        state_description='obstacle'
        if max(regions['right'],regions['fright'],regions['fleft'],regions['front'],regions['left'])==regions['right']:
            linear_x=0.5
            angular_z=3
        elif max(regions['right'],regions['fright'],regions['fleft'],regions['front'],regions['left'])==regions['left']:
            linear_x=0.5
            angular_z=-3
        elif max(regions['right'],regions['fright'],regions['fleft'],regions['front'],regions['left'])==regions['fleft']:
            linear_x=0.5
            angular_z=-3
        elif max(regions['right'],regions['fright'],regions['fleft'],regions['front'],regions['left'])==regions['fright']:
            linear_x=0.5
            angular_z=3
        elif max(regions['right'],regions['fright'],regions['fleft'],regions['front'],regions['left'])==regions['front']:
            linear_x=0.5
            angular_z=0
        else:
            linear_x=-0.6
            angular_z=0

    else:
        state_description = 'no obstacle'
    if state_description == 'no obstacle':
        linear_x = (b)/25
        print(b)
        if round(b,1)== 0.0:
            linear_x = 0

        angular_z=-(angle-z_orenitation)
    print(angular_z)
    print(linear_x)
    print(state_description)
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pub.publish(msg)

def main():
    global pub

    rospy.init_node('reading_laser')

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    sub = rospy.Subscriber('/odom', Odometry, clbk_dis)
    sub1 = rospy.Subscriber('/m2wr/laser/scan', LaserScan, clbk_laser)
    rospy.spin()

if __name__ == '__main__':
    main()
