#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

from std_msgs.msg import Int8MultiArray
from std_msgs.msg import UInt16


def talker():
    #############################################
    #
    pub=rospy.Publisher('/servo',UInt16,  queue_size=10)
    pub2=rospy.Publisher('/servo2',UInt16, queue_size=10)

    # values between 30 and 150
    # 30 50 70 90 110 130 150
    selected_column=2

    arm_position = UInt16()
    arm_position.data = 30+20*selected_column
    pub.publish(arm_position)

    open_hand = UInt16()
    open_hand.data= 50
    pub2.publish(open_hand)



    #############################################













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
