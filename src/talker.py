#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

from std_msgs.msg import Int8MultiArray


def talker():

    pub = rospy.Publisher('game_state', Int8MultiArray, queue_size=10)
    pub2 = rospy.Publisher('life_sign', String, queue_size=10)

    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(0.2) # publish every 1/rate seconds
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)
        pub2.publish(hello_str)

        game_state = Int8MultiArray()
        game_state.layout.dim = []

        game_state.data=[0,1,2,1,2,0,2,1,0]

        pub.publish(game_state)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
