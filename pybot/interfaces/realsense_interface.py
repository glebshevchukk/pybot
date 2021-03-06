import pyrealsense2 as rs
import numpy as np
from pybot.cmn_structs import *
from pybot.sensor_structs import *

class RealsenseInterface():
    def __init__(self):
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth,1280, 720, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.accel, rs.format.motion_xyz32f, 250)
        config.enable_stream(rs.stream.gyro, rs.format.motion_xyz32f, 200)
        # Start streaming
        profile = self.pipeline.start(config)
        depth_sensor = profile.get_device().first_depth_sensor()
        align_to = rs.stream.color
        self.align = rs.align(align_to)

    def __next__(self):
        frames = self.pipeline.wait_for_frames()
        # Align the depth frame to color frame
        aligned_frames = self.align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()
        for frame in frames:
            if frame.is_motion_frame():
                pose_frame = frame.as_motion_frame().get_motion_data()

                print(pose_frame)

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            print("Either color or depth frame is invalid, skipping")
            return

        depth_image = np.array(aligned_depth_frame.get_data()).astype(np.int64)
        color_image = np.array(color_frame.get_data()).astype(np.int64)

        i = color_frame.profile.as_video_stream_profile().get_intrinsics()
        intrin = np.array([[i.fx,0,i.ppx,0],[0,i.fy,i.ppy,0],[0,0,1,0],[0,0,0,1]]).astype(np.int64)
        
        #convert to our structs
        header = make_header()
        height,width=color_image.shape[:2]
        color_image = Image(header,height,width,"BGR8",color_image)
        depth_image = Image(header,height,width,"Z16",depth_image)
        intrin = CameraInfo(height,width,None,None,intrin,None,None)
        #print(intrin)
        return intrin
        #return color_image,depth_image,intrin
