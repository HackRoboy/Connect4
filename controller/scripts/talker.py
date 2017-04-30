#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

from std_msgs.msg import Int8MultiArray

from roboy_comm.srv import TextSpoken

from random import randint


def talker():
    pub = rospy.Publisher('/new_action', Int8MultiArray, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    new_act = Int8MultiArray()
    new_act.layout.dim = []
    new_act.data=[1,1,2,0]
    pub.publish(new_act)

    rate = rospy.Rate(0.5) # publish every 1/rate seconds

    rospy.wait_for_service("TextSpoken")
    stt = rospy.ServiceProxy('TextSpoken', TextSpoken)

    random=0
    while not rospy.is_shutdown():

	new_act = Int8MultiArray()
        new_act.layout.dim = []

        # 1st cell: 0 -> cv; 1 -> talk; 2 -> logic
        # 2nd cell: 1 -> player; 2 -> Roboy
        # 3rd cell: row-coordinate
        # 4th cell: column-coordinate

	resp = stt()
        print resp.text
	if "one" in resp.text: 
		new_act.data=[1,1,2,0]
		rospy.loginfo('roboy heared a one, %r', new_act.data[3])
		#import pdb;pdb.set_trace()	        
		pub.publish(new_act)
		random=0
	elif "two" in resp.text: 
		new_act.data=[1,1,2,1]
	        pub.publish(new_act)
		random=0
	elif "three" in resp.text: 
		new_act.data=[1,1,2,2]
	        pub.publish(new_act)
		random=0
	elif "four" in resp.text: 
		new_act.data=[1,1,2,3]
	        pub.publish(new_act)
		random=0
	elif "five" in resp.text: 
		new_act.data=[1,1,2,4]
	        pub.publish(new_act)
		random=0
	elif "six" in resp.text: 
		new_act.data=[1,1,2,5]
	        pub.publish(new_act)
		random=0
	elif "seven" in resp.text: 
		new_act.data=[1,1,2,6]
	        pub.publish(new_act)
		random=0
	else:
		random=random+1

	if random==3:
		new_act.data=[1,1,2,randint(0,6)]
	        pub.publish(new_act)
		random=0
	elif random>0:
		text="What?"

#	rospy.spin()
        rate.sleep()



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
