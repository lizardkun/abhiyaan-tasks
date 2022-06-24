#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import sys
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from turtlesim.srv import Kill

vel = Twist()

turtles = [0, 0]
rospy.init_node("turtlesim", anonymous=True)
rate = rospy.Rate(10)

x1, y1 = 5.4, 5.4
velx = 2
vely = 1
rospy.wait_for_service("/spawn")
vels = [[velx, vely] for i in range(17)]
count = 1


class Turtle:
    def turtle_callback(self, data):
        self.x = data.x
        self.y = data.y

    def __init__(self, c, x, y, vx, vy):
        global turtles
        if c > 1 and c <= 16:
            spawn_turtle = rospy.ServiceProxy("/spawn", Spawn)
            server_response = spawn_turtle(x, y, 0, f"turtle{c}")
            turtles.append(self)
        self.pub = rospy.Publisher(f"/turtle{c}/cmd_vel", Twist, queue_size=10)

        global vels
        self.id = c
        self.x = x
        self.y = y
        self.vx = vels[c][0]
        self.vy = vels[c][1]

    def move(self):
        global count
        global turtles
        global vels
        rospy.Subscriber(f"/turtle{self.id}/pose", Pose, self.turtle_callback)

        if self.x >= 8 and self.vx > 0:
            count += 1
            if count <=16:
                vels[count][0] = -self.vx
                vels[count][1] = -self.vy
                turtles[count] = Turtle(count, self.x - 0.1, self.y, -self.vx, -self.vy)
            self.vx = -self.vx

        elif self.y >= 8 and self.vy > 0:
            count += 1
            if count <= 16:
                vels[count][0] = -self.vx
                vels[count][1] = -self.vy
                turtles[count] = Turtle(count, self.x - 0.1, self.y, -self.vx, -self.vy)
            self.vy = -self.vy

        elif self.y <= 2 and self.vy < 0:
            count += 1
            if count <= 16:
                vels[count][0] = -self.vx
                vels[count][1] = -self.vy
                turtles[count] = Turtle(count, self.x - 0.1, self.y, -self.vx, -self.vy)
            self.vy = -self.vy

        elif self.x <= 2 and self.vx < 0:
            count += 1
            if count <= 16:
                vels[count][0] = -self.vx
                vels[count][1] = -self.vy
                turtles[count] = Turtle(count, self.x - 0.1, self.y, -self.vx, -self.vy)
            self.vx = -self.vx

        vel = Twist()
        vel.linear.x = self.vx
        vel.linear.y = self.vy
        self.pub.publish(vel)


for i in range(1, min(count, 16)):
    rospy.Subscriber(f"/turtle{i}/pose", Pose, turtles[i].turtle_callback)

turtles[1] = Turtle(1, x1, y1, velx, vely)
while not rospy.is_shutdown():
    for i in range(1, min(count+1, 16)):
        turtles[i].move()
    rate.sleep()
    
    c=1
    if(len(turtles)>=16):
        killTurt=rospy.ServiceProxy("/kill", Kill)
        while(c>0 and c<17):
            server_response=killTurt(f'turtle{c}')
            c=c+1
rate = rospy.Rate(10)
