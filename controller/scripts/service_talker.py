#!/usr/bin/env python
from roboy_comm.srv import TextSpoken
import rospy
 
rospy.ServiceProxy('TextSpoken', TextSpoken)
 
def stt_client():
    rospy.wait_for_service("TextSpoken")
    try:
        stt = rospy.ServiceProxy('TextSpoken', TextSpoken)
        resp = stt()
        print resp.text
        return resp.text
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
 
if __name__ == "__main__":
    stt_client()
