#!/usr/bin/env python
from roboy_comm.srv import seq2seq_predict
from roboy_comm.srv import Yaw
from roboy_comm.srv import Movement
from roboy_comm.srv import ShowEmotion

import rospy
import time

 
def stt_client():
    rospy.wait_for_service("/roboy/gnlp_predict")
    try:
	while True:
        	stt = rospy.ServiceProxy('/roboy/gnlp_predict', seq2seq_predict)
        	resp = stt("text_input: 'yo'")
        	print resp.text_output
        return resp.text_output
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def mv_client():
    rospy.wait_for_service("/roboy_move/yaw")
    rospy.wait_for_service("/roboy_move/replay")
    rospy.wait_for_service("/roboy_face/show_emotion")
    try:
	if True:
        	
        	head = rospy.ServiceProxy('/roboy_move/yaw', Yaw)
		emo = rospy.ServiceProxy('/roboy_face/show_emotion', ShowEmotion)
		body = rospy.ServiceProxy('/roboy_move/replay', Movement)
		resp = emo("lookright")
        	print "emo"+str(resp.success)
		time.sleep(10)
		return

		resp = body("Introduction")
        	print "body 1"+str(resp.success)
		time.sleep(20)

        	resp = head(7)
        	print "head r"+str(resp.success)
		time.sleep(3)
		
		resp = emo("smileblink")
        	print "emo"+str(resp.success)
		time.sleep(3)

		resp = body("GivingHand_5")
        	print "body 2"+str(resp.success)
		time.sleep(20)
		
        return resp.success
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
 

if __name__ == "__main__":
    mv_client()
