'''
This file defines structures that might come from image,depth,or other types of sensors (same as those used by ROS) 
'''
from pybot.cmn_structs import *

class BatteryState(Printable):
    def __init__(self,header:Header,voltage:float,temperature:float,\
                        current:float,charge:float,capacity:float,\
                        design_capacity:float,percentage:float,present:bool,\
                        cell_voltage:list,cell_temperature:list,location:str,\
                        serial:str):
        self.header=header
        self.voltage=voltage
        self.temperature=temperature
        self.current=current
        self.charge=charge
        self.capacity=capacity
        self.design_capacity=design_capacity
        self.percentage=percentage
        self.present=present
        self.cell_voltage=cell_voltage
        self.cell_temperature=cell_temperature
        self.location=location
        self.serial=serial

class CameraInfo(Printable):
    def __init__(self,height:int=None,width:int=None,distortion_model:str=None,distortion_params:np.ndarray=None,\
                intrinsics:np.ndarray=None,rectification:np.ndarray=None,processed_intrinsic:np.ndarray=None):
        self.height=height
        self.width=width
        self.distortion_model=distortion_model
        self.distortion_params=distortion_params
        self.intrinsics=intrinsics
        self.rectification=rectification
        self.processed_intrinsic=processed_intrinsic

class Image(Printable):
    def __init__(self,header:Header,height:int,width:int,encoding:str,data:np.ndarray):
        self.header=header
        self.height=height
        self.width=width
        self.encoding=encoding
        self.data=data

class Imu(Printable):
    def __init__(self,header:Header,orientation:Quaternion,orientation_covariance:np.ndarray,\
                angular_velocity:Vector3,angular_velocity_covariance:np.ndarray,\
                linear_acceleration:Vector3,linear_acceleration_covariance:np.ndarray):
        self.header=header
        self.orientation=orientation
        self.orientation_covariance=orientation_covariance
        self.angular_velocity=angular_velocity
        self.angular_velocity_covariance=angular_velocity_covariance
        self.linear_acceleration=linear_acceleration
        self.linear_acceleration_covariance=linear_acceleration_covariance

class JointState(Printable):
    def __init__(self,header:Header,name:str,position:list,velocity:list,effort:list):
        self.header=header
        self.name=name
        self.position=position
        self.velocity=velocity
        self.effort=effort

class PointCloud(Printable):
    def __init__(self,header:Header,points:list,channels:list):
        self.header=header
        self.points=points
        self.channels=channels