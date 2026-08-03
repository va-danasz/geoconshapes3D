# Reproducibility Settings
SEED = 12345

# Image & Generation Settings
IMG_W, IMG_H = 500, 500
SAMPLE_COUNT = 3
MAX_VALIDATIONS = 1000

# In test mode the program opens an interactive window
TEST_MODE = False

# Dataset Labeling & Category Options
CONCEPTS = ["ALONE", "FAR", "CLOSE", "OVERLAP"]
SHAPES = ["CUBE", "SPHERE", "CONE"]
COLORS = ["red", "green", "blue"]

# Color Assignment Configurations
BASE_COLOR_SINGLE = COLORS[0]
BASE_COLORS_GROUP = [COLORS[1], COLORS[2]]

# 3D Scene & Camera Configurations
UP = (0.0, 0.0, 1.0)
HORIZONTAL_ANGLE_RANGE = (0.0, 360.0)
ELEVATION_ANGLE_RANGE = (15.0, 60.0)
VIEW_ANGLE = 30.0

# Base Geometry Default Parameters
BASE_SHAPE_POS = (0.0, 0.0, 0.0)
BASE_SUBDIVISIONS = 5  # sphere
BASE_CONE_SECTIONS = 4

# Random Sampling Position Ranges
POS_X_RANGE = (-15.0, 15.0)
POS_Y_RANGE = (-15.0, 15.0)
POS_Z_RANGE = (-5.0, 5.0)
CUBE_SIZE_RANGE = (7.5, 12.5)
SPHERE_SIZE_RANGE = (4.0, 8.0)
CONE_SIZE_RANGE = (4.0, 8.0)
CONE_HEIGHT_RANGE = (8.0, 12.0)

# Spatial Relationship Thresholds
CLOSE_THRESHOLD = (1.0, 6.0)
FAR_THRESHOLD = (15.0, 30.0)