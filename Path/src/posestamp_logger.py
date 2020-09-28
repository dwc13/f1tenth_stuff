#!/usr/bin/env python

import rospy
import atexit
from os.path import expanduser
from time import gmtime, strftime

from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion,
from nav_msgs.msg import Odometry
from std_msgs.msg import Header

home = expanduser('~/Desktop/f1tenth_stuff/Path_logs')
file = open(strftime(home+'/p-%Y-%m-%d-%H-%M-%S',gmtime())+'.csv', 'w')

def save_posestamp(data):
    hdr = Header(stamp=rospy.Time.now(), frame_id='base_link')
    
    posestamp = PoseStamp(header=hdr, pose=Pose(position=Point(
                       data.twist.twist.linear.x, 
                       data.twist.twist.linear.y, 
                       data.twist.twist.linear.z),
                                                orientation=Quaternion(
                       data.pose.pose.orientation.x, 
                       data.pose.pose.orientation.y, 
                       data.pose.pose.orientation.z, 
                       data.pose.pose.orientation.w)
                                               )
                         )
  
    file.write('%f\n' % (posestamp)

def shutdown():
    file.close()
    print('Logger Closed')
 
def listener():
    rospy.init_node('posestamp_logger', anonymous=True)
    rospy.Subscriber('vesc/odom', Odometry, save_posestamp)
    rospy.spin()

if __name__ == '__main__':
    atexit.register(shutdown)
    print('Saving waypoints...')
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
