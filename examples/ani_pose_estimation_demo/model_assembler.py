import trimesh
import numpy as np

small_model_path = "ani_model_library/m12_screw/assets/m12_screw_v2.STL"
big_model_path = "ani_model_library/m12_screw/assets/bin_of_screws.stl"
bin_model_path = "ani_model_library/ikea_bin/assets/ikea_bin_v4.STL"

def read_input() -> list:
    '''
    read input file with pose data
    '''
    # list_of_poses = sample_pose_input.split(' --')
    f = open("examples/ani_pose_estimation_demo/screw_poses.txt", 'r')
    pose_data = f.read().strip().split()
    f.close()
    return pose_data


def format_input(pose_data):
    '''
    format input into a 4x4 homogenous transformation matrix
    '''
    list_of_poses = []
    message_size = 22

    for i in range(0, len(pose_data), message_size):
        model_name = pose_data[i+1].strip()
        # translation = [float(x.strip().split()[1]) for x in list_of_poses[i+1].strip().split('\n')[2:5]]
        translation = list(map(float, [pose_data[i+5], pose_data[i+7], pose_data[i+9]]))
        rotation = [
            list(map(lambda x: float(x.strip(',')), pose_data[i+12:i+15])),
            list(map(lambda x: float(x.strip(',')), pose_data[i+15:i+18])),
            list(map(lambda x: float(x.strip(',')), pose_data[i+18:i+21]))
        ]
        list_of_poses.append(
            {
                "name": model_name,
                "translation": translation,
                "rotation": rotation,
            }
        )
    # for i in list_of_poses:
    #     for k, v in i.items():
    #         print(k, v)
    #     input()

    list_of_transforms = []
    for pose in list_of_poses:
        tmat = np.eye(4)
        _, t, r = pose.items()
        tmat[:3, :3] = np.array(r[1])
        tmat[:3,  3] = np.array(t[1])*1000
        # print(tmat)
        list_of_transforms.append(tmat)
    
    # return list_of_poses
    return list_of_transforms


def make_transform(translation, rotation_deg):
    '''
    create 4x4 homogenous transformation matrix
    inputs:
    translation: (x, y, z)
    rotation_deg: (rx, ry, rz) in degrees
    '''
    T = np.eye(4)
    rx, ry, rz = np.deg2rad(rotation_deg)
    Rx = trimesh.transformations.rotation_matrix(rx, [1, 0, 0])
    Ry = trimesh.transformations.rotation_matrix(ry, [0, 1, 0])
    Rz = trimesh.transformations.rotation_matrix(rz, [0, 0, 1])
    R = trimesh.transformations.concatenate_matrices(Rx, Ry, Rz)
    T[:3, :3] = R[:3, :3]
    T[:3, 3] = translation
    return T

# example poses for testing
poses = [
    make_transform((0, 0, 0), (0, 0, 0)),
    make_transform((100, 0, 0), (0, 45, 0)),
    make_transform((0, 100, 0), (0, 0, 90)),
    make_transform((100, 100, 50), (30, 45, 60)),
]

# ==================================
#                               MAIN
# ==================================

pose_data = read_input()
# list_of_poses = format_input(pose_data)
list_of_transforms = format_input(pose_data)

# -----------------------------------------------------------------------------
base_mesh = trimesh.load(small_model_path)
print(f"loaded base model: {len(base_mesh.faces)} faces")
bin_mesh = trimesh.load(bin_model_path)
print(f"loaded bin model: {len(bin_mesh.faces)} faces")

all_meshes = []

# for i, pose in enumerate(poses):
#     m_copy = base_mesh.copy()
#     m_copy.apply_transform(pose)
#     all_meshes.append(m_copy)
for i, pose in enumerate(list_of_transforms[1:]):
    m_copy = base_mesh.copy()
    m_copy.apply_transform(pose)
    all_meshes.append(m_copy)

# Adding in the bin model
# bin_mesh.apply_transform(list_of_transforms[0])
# all_meshes.append(bin_mesh)


composite = trimesh.util.concatenate(all_meshes)

composite.export(big_model_path)
print(f"[tick] Exported composite model to: {big_model_path}")

