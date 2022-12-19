#!/usr/bin/env python


import struct

import rospy

from esp_now_ros.msg import Packet
from geometry_msgs.msg import PoseStamped


class ActAsAmbulance(object):

    def __init__(self):

        self.sub = rospy.Subscriber('/esp_now_ros/read', Packet, self.callback)

    def callback(self, msg):

        packet_type = ord(msg[0:1])
        if packet_type != Packet.PACKET_TYPE_EMERGENCY:
            return
        else:
            map_frame = msg[1:1+63].decode('utf-8')
            position_x = struct.unpack('<f', msg[1+63+4*0:1+63+4*1])[0]
            position_y = struct.unpack('<f', msg[1+63+4*1:1+63+4*2])[0]
            position_z = struct.unpack('<f', msg[1+63+4*2:1+63+4*3])[0]
            rotation_x = struct.unpack('<f', msg[1+63+4*3:1+63+4*4])[0]
            rotation_y = struct.unpack('<f', msg[1+63+4*4:1+63+4*5])[0]
            rotation_z = struct.unpack('<f', msg[1+63+4*5:1+63+4*6])[0]
            rotation_w = struct.unpack('<f', msg[1+63+4*6:1+63+4*7])[0]

            pose = PoseStamped()
            pose.header.frame_id = map_frame
            pose.pose.position.x = position_x
            pose.pose.position.y = position_y
            pose.pose.position.z = position_z
            pose.pose.orientation.x = rotation_x
            pose.pose.orientation.y = rotation_y
            pose.pose.orientation.z = rotation_z
            pose.pose.orientation.w = rotation_w

            rospy.loginfo('Emergency Called from {}'.format(pose))


if __name__ == '__main__':

    rospy.init_node('Ambulance')
    node = ActAsAmbulance()
    rospy.spin()
