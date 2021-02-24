'''
This file defines common structures (same as those used by ROS) that we would like to store information in
'''
import numpy as np
import time
from uuid import uuid4

class Printable(object):
    def __init__(self):
        pass
    def __str__(self):
        return str(self.__dict__)

class Header(Printable):
    def __init__(self,timestep:float, frame_id:int):
        self.timestep=timestep
        self.frame_id=frame_id

class Vector3(Printable):
    def __init__(self,x:float,y:float,z:float):
        self.x=x
        self.y=y
        self.z=z

class Vector2(Printable):
    def __init__(self,x:float,y:float):
        self.x=x
        self.y=y

class Quaternion(Printable):
    def __init__(self,x:float=None,y:float=None,z:float=None,w:float=None):
        self.x=x
        self.y=y
        self.z=z
        self.w=w

    #adapted from https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
    def from_euler(self,yaw,pitch,roll):
        cy = np.cos(yaw * 0.5)
        sy = np.sin(yaw * 0.5)
        cp = np.cos(pitch * 0.5)
        sp = np.sin(pitch * 0.5)
        cr = np.cos(roll * 0.5)
        sr = np.sin(roll * 0.5)
        self.w = cr * cp * cy + sr * sp * sy;
        self.x = sr * cp * cy - cr * sp * sy;
        self.y = cr * sp * cy + sr * cp * sy;
        self.z = cr * cp * sy - sr * sp * cy;

    def to_euler(self):
        x = np.arctan2(2*(self.x*self.y + self.z*self.w), 1.-2(self.y**2+self.z**2))
        y = np.arcsin(2(self.x*self.z - self.w*self.y))
        z = np.arctan2(2*(self.x*self.w + self.y*self.z), 1.-2(self.z**2+self.w**2))
        return Vector3(x,y,z)

class Pose(Printable):
    def __init__(self,position:Vector3,orientation:Quaternion):
        self.position=position
        self.orientation=orientation

class Twist(Printable):
    def __init__(self,linear:Vector3,angular:Vector3):
        self.linear=linear
        self.angular=angular

class Wrench(Printable):
    def __init__(self,force:Vector3,torque:Vector3):
        self.force=force
        self.torque=torque

class Accel(Printable):
    def __init__(self,linear:Vector3,angular:Vector3):
        self.linear=linear
        self.angular=angular

class Polygon(Printable):
    def __init__(self,points:list):
        self.points=points

class Inertia(Printable):
    def __init__(self,mass:float,com:Vector3,inertia:list):
        self.mass=mass
        self.com=com
        self.inertia=inertia


def make_header():
    t = time.time()
    frame_id = str(uuid4())
    head = Header(t,frame_id)
    return head
