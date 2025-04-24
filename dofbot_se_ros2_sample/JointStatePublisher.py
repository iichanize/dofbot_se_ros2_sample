import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import sys
import tty
import termios
import select

class JointStatePublisher(Node):
    def __init__(self):
        super().__init__('joint_state_publisher', namespace='dofbot_test')
        self.publisher = self.create_publisher(JointState, 'joint_command', 10)
        self.timer = self.create_timer(0.1, self.publish_joint_state)
        self.joint_positions = [0.0] * 11
        self.key_mapping = {
            'q': (0, 0.1), 'a': (0, -0.1),
            'w': (1, 0.1), 's': (1, -0.1),
            'e': (2, 0.1), 'd': (2, -0.1),
            'r': (3, 0.1), 'f': (3, -0.1),
            't': (4, 0.1), 'g': (4, -0.1),
            'y': (5, 0.1), 'h': (5, -0.1)
        }

    def publish_joint_state(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['joint1', 'joint2', 'joint3', 'joint4', 'Wrist_Twist_RevoluteJoint', 'Finger_Left_01_RevoluteJoint', 'Finger_Right_01_RevoluteJoint', 'Finger_Left_02_RevoluteJoint', 'Finger_Right_02_RevoluteJoint', 'Finger_Left_03_RevoluteJoint', 'Finger_Right_03_RevoluteJoint']
        
        # Update controlled joints (0-5)
        for i in range(6):
            self.joint_positions[i] = max(-1.57, min(1.57, self.joint_positions[i]))
        
        # Set joint 7 to negative of joint 6
        self.joint_positions[6] = -self.joint_positions[5]
        
        # Set joints 8-11 to 0
        for i in range(7, 11):
            self.joint_positions[i] = 0.0
        
        msg.position = self.joint_positions
        self.publisher.publish(msg)

    def update_joint_position(self, key):
        if key in self.key_mapping:
            joint, increment = self.key_mapping[key]
            self.joint_positions[joint] += increment
            if joint == 5:
                self.joint_positions[6] -= increment

def get_key():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main(args=None):
    global settings
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init(args=args)
    joint_state_publisher = JointStatePublisher()
    
    print("Use q,w,e,r,t,y to increase joint angles 1-6")
    print("Use a,s,d,f,g,h to decrease joint angles 1-6")
    print("Press Ctrl-C to quit")
    
    try:
        while rclpy.ok():
            key = get_key()
            if key == '\x03':  # Ctrl-C
                break
            joint_state_publisher.update_joint_position(key)
            rclpy.spin_once(joint_state_publisher, timeout_sec=0.1)
    except Exception as e:
        print(e)
    finally:
        joint_state_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
