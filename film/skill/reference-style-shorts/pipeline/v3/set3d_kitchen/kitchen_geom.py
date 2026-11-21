"""bpy-free numbers of the kitchen set (checked against kitchen3d.anchors() / wb_point())."""
TOP = 1.30
WBC = (0.225, -0.9439, 1.6378)      # weather box centre (page 1.0, 1.42)
W1 = (0.225, -0.965, 1.5981)        # 'ฝนตก' centre (bleed target, page 1.0, 1.47)
HDR = (0.225, -0.7918, 1.9239)      # header line
W2 = (0.225, -1.0622, 1.4153)       # 'ลมกระโชก'
CAM_TABLE = ((0.225, -2.42, 1.80), (0.225, -0.30, 1.07))
CAM_STEEP = ((0.225, -1.62, 2.30), (0.225, -0.9439, 1.6178))
CAM_WINDOW = ((0.25, -1.05, 2.48), (0.25, 0.0, 2.50))
CUP_REST = (0.38, -1.40)
CUP_ROT = -50.0                      # the cup turns its handle toward camera right
HANDLE = (0.165, 0.0, 0.114)        # outer point of the cup handle in the cup rig
