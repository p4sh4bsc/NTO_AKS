import rospy
from std_msgs.msg import String

def callback(data):
    # rospy.loginfo("I heard %s",data.data) <- that wouldbe work 100%
    rospy.loginfo(f"I heard {data.data}")
    
def listener():
    rospy.init_node('listener')
    rospy.Subscriber("chatter", String, callback)
    rospy.spin()
    
while True:
    listener()
