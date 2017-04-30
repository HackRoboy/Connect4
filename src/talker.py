#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

from std_msgs.msg import Int8MultiArray


def talker():

    pub = rospy.Publisher('new_action', Int8MultiArray, queue_size=10)

    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(0.2) # publish every 1/rate seconds
    while not rospy.is_shutdown():

        new_action = Int8MultiArray()
        new_action.layout.dim = []

        new_action.data=[1,1,2,3]
        # 1st cell: 0 -> cv; 1 -> talk; 2 -> logic
        # 2nd cell: 1 -> player; 2 -> Roboy
        # 3rd cell: row-coordinate
        # 4th cell: column-coordinate

        pub.publish(new_action)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
