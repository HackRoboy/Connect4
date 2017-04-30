#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8MultiArray

#from std_msgs.msg import Int8MultiArray
from sensor_msgs.msg import Image
import numpy as np

def game_state():
    rospy.init_node('game_state', anonymous=True)

    rate = rospy.Rate(0.2) # publish every 1/rate seconds
    game_start_flag = 1
    global message_start
    message_start = 'Let"s play a game!'
    global message_explain_game
    message_explain_game ='The game Connect Four works like this. We place our pawns in turns.\
                        If four pawns of one color are in a line, the respective player wins. \
                        Lines can be  horizontally, vertically or diagonal.'
    global player_turn_msg
    player_turn_msg='Your turn.'
    global roboy_turn_msg
    roboy_turn_msg='Now it is my turn.'
    hello_str = "hello world %s" % rospy.get_time()


    rospy.loginfo('starting---------------')

    global game_state
    global player_turn
    global full_columns
    full_columns=[0,0,0,0,0,0,0]
    player_turn = 1 # 0 means roboy's turn
    game_state = Image()
    game_state.height = 6
    game_state.width = 7
    if game_start_flag == 1:
        game_state.data=[]
        for i in xrange(0,42):
            game_state.data.append(0)
            game_start_flag=0

    global pub
    pub = rospy.Publisher('/game_state', Image, queue_size=10)

    pub2 = rospy.Publisher('/life_sign', String, queue_size=10)
    rospy.Subscriber('/cv_game_update', Int8MultiArray, update_game_state)
    rospy.Subscriber('/talk_game_update', Int8MultiArray, update_game_state)
    rospy.Subscriber('/new_action', Int8MultiArray, update_game_state) #for testing
    pub2.publish(hello_str)

    #game_state_matrix=np.zeros((6,7))

    #rate.sleep()
    rospy.spin()

def game_logic():
    global player_turn
    global full_columns
    rospy.loginfo('roboy is playing now')
    # roboy says: it's my turn now
    while True: # generate random columns until column is not full
        selected_column = np.random.randint(7)
        if full_columns[selected_column]==0:
            break

    for i in range(6):
        if game_state.data[(5-i)*7+selected_column] == 0:
            game_state.data[(5-i)*7+selected_column]=2 # roboy plays
            # say turn message
            break

    # check if one new column is full
    # check if all columns are full
    full_column_count=0
    for i in range(7):
        if game_state.data[i]:
            full_columns[i]=1
            full_column_count+=1
    if full_column_count==7:
        # the game is finished
        rospy.loginfo('the game is finished')

    pub.publish(game_state)
    player_turn=1

def update_game_state(data_input):
    global message
    global player_turn
    global game_state
    global full_columns

    message = data_input.data
    msg_list=list(message)
    #msg_list= [int(msg.encode('hex'),16) for msg in message]
    rospy.loginfo('=====received data %r', [msg_list[0],msg_list[1],msg_list[2],msg_list[3]])

    if msg_list[0]==0 and player_turn==msg_list[1]: #from cv and correct turn
        if game_state.data[msg_list[2]*7+msg_list[3]] == 0:
            player_turn = 1-player_turn
            # say turn message
            game_state.data[msg_list[2]*7+msg_list[3]]=msg_list[1]


    if msg_list[0]==1 and player_turn==msg_list[1]: #from talk and correct turn
        player_turn = 1-player_turn
        column = msg_list[3]
        for i in range(6):
            if game_state.data[(5-i)*7+column] == 0:
                game_state.data[(5-i)*7+column]=msg_list[1]
                # say turn message
                break


    # check if one new column is full
    # check if all columns are full
    full_column_count=0
    for i in range(7):
        if game_state.data[i]:
            full_columns[i]=1
            full_column_count+=1
    if full_column_count==7:
        # the game is finished
        rospy.loginfo('the game is finished')

    if player_turn==0:
        game_logic()


    message = "I'm updating my game state."

    pub.publish(game_state)




if __name__ == '__main__':
    try:
        game_state()
    except rospy.ROSInterruptException:
        pass
