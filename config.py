# Reproducibility Settings
seed = 12345

# Image & Generation Settings
IMG_W = 500
IMG_H = 500
SAMPLE_COUNT = 1

# In test mode the program opens an interactive window
TEST_MODE = False
OUTPUT_DIR = "output"

# Dataset Labeling & Category Options
CONCEPTS = ["ALONE", "FAR", "CLOSE", "OVERLAP"]
SHAPES = ["CUBE", "SPHERE", "CONE"]
COLORS = ["red", "green", "blue"]

# Color Assignment Configurations
BASE_COLOR_SINGLE = COLORS[0]
BASE_COLORS_GROUP = [COLORS[1], COLORS[2]]

# 3D Scene & Camera Configurations
UP = (0.0, 0.0, 1.0)
BASE_CAMERA_XYZ = (40.0, -40.0, 40.0)
BASE_CAMERA_LOOK = (0.0, 0.0, 0.0)

# Base Geometry Default Parameters
BASE_SHAPE_POS = (0.0, 0.0, 0.0)
BASE_CUBE_SIZE = (10, 10, 10)
BASE_RADIUS = 10  # cone + sphere
BASE_SUBDIVISIONS = 5  # sphere
BASE_CONE_HEIGHT = 10
BASE_CONE_SECTIONS = 4

# Random Sampling Position Ranges
POS_RANGE_X = (-30.0, 30.0)
POS_RANGE_Y = (-30.0, 30.0)
POS_RANGE_Z = (-10.0, 10.0)

# Spatial Relationship Thresholds
CLOSE_THRESHOLD = 15.0
FAR_THRESHOLD = 35.0