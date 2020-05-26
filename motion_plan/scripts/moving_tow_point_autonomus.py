#! /usr/bin/env python
import rospy
import math
import cv2
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import LaserScan, Image
from geometry_msgs.msg import Twist
pub = None
bridge = CvBridge()
flag=1
regions={}
angular_z=0
backSub = cv2.createBackgroundSubtractorMOG2()
def image_callback(msg):
    global c

    #print("Received an image!")
    try:
        # Convert your ROS Image message to OpenCV2
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")

    except CvBridgeError, e:
        print(e)
    else:

        # Save your OpenCV2 image as a jpeg
        if cv2_img is None:
            exit()
        fgMask = backSub.apply(cv2_img)


        cv2.rectangle(cv2_img, (10, 2), (100,20), (255,255,255), -1)


        cv2.imshow('Frame', cv2_img)
        cv2.imshow('FG Mask', fgMask)
        keyboard = cv2.waitKey(30)
def clbk_laser(msg):
    global regions

    regions = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:150]), 10),
        'front':  min(min(msg.ranges[150:550]), 10),
        'fleft':  min(min(msg.ranges[550:575]), 10),
        'left':   min(min(msg.ranges[576:719]), 10),
    }

def clbk_dis(msg):
    x=msg.pose.pose.position.x
    y=msg.pose.pose.position.y
    z_orenitation=msg.pose.pose.orientation.z
    move_to_x=7
    move_to_y=7
    b=math.sqrt((move_to_x-x)**2+(move_to_y-y)**2)
    a=((move_to_y-y)/(move_to_x-x))
    #print('intan:',a)
    angle=math.atan(a)
    #print('pre:',angle)
    take_action(angle,z_orenitation,b)

def take_action(angle,z_orenitation,b):
    msg = Twist()
    linear_x = 0
    global angular_z
    global flag
    state_description = ''
    print(regions['front'])
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
        if z_orenitation==angle/math.pi:
            angular_z=0
        elif z_orenitation>angle/math.pi:
            angular_z=(angle-z_orenitation)
        else:
            angular_z=-(angle-z_orenitation)
    print("angle:",angular_z)
    print("linear:",linear_x)
    print(state_description)
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pub.publish(msg)

def main():
    global pub

    rospy.init_node('reading_laser')

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    image_topic = "/rrbot/camera1/image_raw"
    rospy.Subscriber(image_topic, Image, image_callback)
    sub = rospy.Subscriber('/odom', Odometry, clbk_dis)
    sub1 = rospy.Subscriber('/m2wr/laser/scan', LaserScan, clbk_laser)
    rospy.spin()

if __name__ == '__main__':
    main()
