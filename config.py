# Reproducibility Settings
SEED = 12345

# Image & Generation Settings
IMG_W, IMG_H = 800, 450
SAMPLE_COUNT = 3
RENDER_COUNT = 5
MAX_VALIDATIONS = 1000

# In test mode the program opens an interactive window
TEST_MODE = False
RENDER_BACKGROUND = False
RENDER_TEXTURE = False
OUTPUT_PATH = "output"
BACKGROUND_PATH = "backgrounds"
TEXTURE_PATH = "textures"
CSV_PATH_MESH = f"{OUTPUT_PATH}/meta_data_mesh.csv"
CSV_PATH_RENDER = f"{OUTPUT_PATH}/meta_data_render.csv"

# 3D Scene & Camera Configurations
HORIZONTAL_ANGLE_RANGE = (0.0, 360.0)
ELEVATION_ANGLE_RANGE = (15.0, 60.0)
VIEW_ANGLE = 30.0

# Base Geometry Default Parameters
BASE_SHAPE_POS = (0.0, 0.0, 0.0)
BASE_SUBDIVISIONS = 5  # sphere
BASE_CONE_SECTIONS = 4

# Random Sampling Position Ranges
POS_X_RANGE = (-25.0, 25.0)
POS_Y_RANGE = (-25.0, 25.0)
POS_Z_RANGE = (-15.0, 15.0)
CUBE_SIZE_RANGE = (7.5, 12.5)
SPHERE_SIZE_RANGE = (4.0, 8.0)
CONE_RADIUS_RANGE = (4.0, 8.0)
CONE_HEIGHT_RANGE = (8.0, 12.0)

# Spatial Relationship Thresholds
# 3D Relation thresholds (world units)
CLOSE_THRESHOLD = (2.0, 8.0)
FAR_THRESHOLD = (10.0, 30.0)
# 2D Projection threshold (normalized)
THRESHOLD_2D_CLOSE_FAR = 0.1

# Plotting for world adn local axis directions
ENABLE_WORLD_DIRECTIONS = False
ENABLE_RELATIVE_DIRECTIONS = True
# left, right, top, bottom, front, back
INCLUDE_WORLD_DIRECTIONS = ["left", "right", "top", "bottom", "front", "back"]
INCLUDE_RELATIVE_DIRECTIONS = ["rel_front", "rel_back", "rel_rot0", "rel_rot0_neg", "rel_rot90", "rel_rot90_neg"]