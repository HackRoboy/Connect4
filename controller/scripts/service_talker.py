#!/usr/bin/env python
from roboy_comm.srv import TextSpoken
from roboy_comm.srv import Talk
from roboy_comm.srv import seq2seq_predict
import rospy
 
def stt_client():
    rospy.wait_for_service("TextSpoken")
    rospy.wait_for_service("/speech_synthesis/talk")
    rospy.wait_for_service("/roboy/gnlp_predict")
    try:
	if True:
        	stt = rospy.ServiceProxy('TextSpoken', TextSpoken)
		talk = rospy.ServiceProxy('/speech_synthesis/talk', Talk)
		respond = rospy.ServiceProxy('/roboy/gnlp_predict', seq2seq_predict)

        	resp = stt()
        	print resp.text
		if "profanity" in resp.text: 
			resp2="Profanity! Profanity! Profanity!"					
		else:
			resp2 =respond(resp.text).text_output		
	        print resp2
		talk(resp2)
        return resp.text
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
 
if __name__ == "__main__":
    stt_client()
