#!/usr/bin/env python
# license removed for brevity
import rospy
import time
from std_msgs.msg import String
from std_msgs.msg import Int8MultiArray

from roboy_comm.srv import TextSpoken

from random import randint


from roboy_comm.srv import Talk
from roboy_comm.srv import seq2seq_predict

from roboy_comm.srv import ShowEmotion

from roboy_comm.srv import Yaw
from roboy_comm.srv import Movement


def talker():
    pub = rospy.Publisher('/new_action', Int8MultiArray, queue_size=10)
    rospy.init_node('talker', anonymous=True)

    rate = rospy.Rate(0.5) # publish every 1/rate seconds

    rospy.wait_for_service("TextSpoken")
    rospy.wait_for_service("/speech_synthesis/talk")
    rospy.wait_for_service("/roboy/gnlp_predict")
    rospy.wait_for_service("/roboy_face/show_emotion")
    rospy.wait_for_service("/roboy_move/yaw")
    
    stt = rospy.ServiceProxy('TextSpoken', TextSpoken)
    talk = rospy.ServiceProxy('/speech_synthesis/talk', Talk)
    respond = rospy.ServiceProxy('/roboy/gnlp_predict', seq2seq_predict)
    emo = rospy.ServiceProxy('/roboy_face/show_emotion', ShowEmotion)
    head = rospy.ServiceProxy('/roboy_move/yaw', Yaw)

    talk("It's time to duel!")
    emo("smileblink")
    print "It's time to duel!"

    respond_data=["That's a smart move","I see your strategy","Yo","Yo", "You won't win like this", "Hurry up, it's not chess", "Move it grandma", "Even a baby would know not to do this move", "Ha ha","Are you sure you want to do that move?"]

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
		text="You chose one"
		random=0
	elif "two" in resp.text: 
		new_act.data=[1,1,2,1]
	        pub.publish(new_act)
		text="You chose two"
		random=0
	elif "three" in resp.text: 
		new_act.data=[1,1,2,2]
	        pub.publish(new_act)
		text="You chose three"
		random=0
	elif "four" in resp.text: 
		new_act.data=[1,1,2,3]
	        pub.publish(new_act)
		text="You chose four"
		random=0
	elif "five" in resp.text: 
		new_act.data=[1,1,2,4]
	        pub.publish(new_act)
		text="You chose five"
		random=0
	elif "six" in resp.text: 
		new_act.data=[1,1,2,5]
	        pub.publish(new_act)
		text="You chose six"
		random=0
	elif "seven" in resp.text: 
		new_act.data=[1,1,2,6]
	        pub.publish(new_act)
		text="You chose seven"
		random=0
	else:
		random=random+1

	if random==4:
		new_act.data=[1,1,2,randint(0,6)]
	        pub.publish(new_act)
		text="I guess you chose "+str(new_act.data[3]+1)
		random=0
	elif random>0:
		text="What did you say? "+respond(resp.text).text_output
	else:
		text=text+". "+respond_data[randint(0,len(respond_data)-1)]

	if "profanity" in resp.text: 
		text="Profanity! Profanity Profanity! Watch your language! "+text
                head(10)
		time.sleep(2)
                head(-10)
		time.sleep(2)
                head(0)
		time.sleep(2)

		random=0	
	print text
	talk(text)
	

#	rospy.spin()
        rate.sleep()



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
