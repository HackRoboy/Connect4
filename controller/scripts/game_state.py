#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8MultiArray
from std_msgs.msg import UInt16


from roboy_comm.srv import Talk

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
response=["I played ","My move is column ","Check this out, I'm playing ","Yo, "]


def game_logic():
    global player_turn
    global full_columns

    rospy.wait_for_service("/speech_synthesis/talk")
    talk = rospy.ServiceProxy('/speech_synthesis/talk', Talk)

    rospy.loginfo('roboy is playing now')
    # roboy says: it's my turn now
    while True: # generate random columns until column is not full
        selected_column = np.random.randint(7)
        if full_columns[selected_column]==0:
            break
    talk(response[np.random.randint(0,len(response)-1)]+str(selected_column)+"."
    rospy.loginfo('roboy is playing in column %r', selected_column+1)
    
    
    #------------- Roboy Moves Arm to Column -------------------------
    pub3=rospy.Publisher('/servo',UInt16,  queue_size=10)
    pub4=rospy.Publisher('/servo2',UInt16, queue_size=10)

    # values between 30 and 150
    # 30 50 70 90 110 130 150

    arm_position = UInt16()
    arm_position.data = 30+20*selected_column
    pub3.publish(arm_position)

    open_hand = UInt16()
    open_hand.data= 50
    pub4.publish(open_hand)
    # -------------- End of Movement ---------------------------


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
    findWinner(game_state)

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
        rospy.loginfo('the human is playing in column %r', msg_list[3]+1)
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
    findWinner(game_state)

BOARDWIDTH = 6
BOARDHEIGHT = 7

def findWinner(gameState):

	if isWinner(gameState,2):
		print("roboy win")
		talk("Yo, I won! Ha Ha Ha!")
		rospy.signal_shutdown("Initiate Skynet!")
	if isWinner(gameState,1):
		print("player win")
		talk("Tsssk! I guess even you can win ... from time to time")
		rospy.signal_shutdown("Humans suck")


def isWinner(game_state, tile):
    # check horizontal spaces
    board=np.reshape(game_state,(6,7))
    #print(board)

    for y in range(BOARDHEIGHT):
        for x in range(BOARDWIDTH - 3):
            if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
                return True

    # check vertical spaces
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 3):
        	#print(x,y)
            if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
                return True

    # check / diagonal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(3, BOARDHEIGHT):
            if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
                return True

    # check \ diagonal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT - 3):
        	#print("test")
            if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
                return True

    return False




if __name__ == '__main__':
    try:
        game_state()
    except rospy.ROSInterruptException:
    pass
