"""
Compute similarity transform (scale + rotation + translation)
from 3 source points to 3 target points.

Tutorial :

Report three coordinates of track point in the global q1, q2, q3
Report three coordinates of the corresponding point p1, p2, p3 in the imported trained GS (with no transform)
Run the script

Copy the computed transfoms into the object transform of the imported trained GS

Usage:
    python compute_transform.py

One can edit the p_points and q_points arrays below.
"""

import numpy as np

def compute_similarity_transform(p_points, q_points):
    """
    Compute scale (s), rotation matrix (R), and translation vector (t)
    such that q_i = s * R @ p_i + t, using the Procrustes / Kabsch method.
    p_points and q_points must be 3x3 numpy arrays (each row = [x,y,z]).
    """

    assert p_points.shape == (3, 3)
    assert q_points.shape == (3, 3)

    # 1. Compute centroids
    p_centroid = np.mean(p_points, axis=0)
    q_centroid = np.mean(q_points, axis=0)

    # 2. Center the points
    P = (p_points - p_centroid).T  # shape 3x3
    Q = (q_points - q_centroid).T  # shape 3x3

    # 3. Covariance matrix
    H = P @ Q.T

    # 4. SVD
    U, S, Vt = np.linalg.svd(H)
    V = Vt.T

    # 5. Rotation
    R = V @ U.T
    if np.linalg.det(R) < 0:
        V[:, -1] *= -1
        R = V @ U.T

    # 6. Uniform scale
    s = np.sum(S) / np.sum(P ** 2)

    # 7. Translation
    t = q_centroid - s * R @ p_centroid

    return s, R, t

def rotation_matrix_to_euler_xyz(R):
    """Extract Euler angles (XYZ order) from rotation matrix."""
    sy = -R[2, 0]
    if abs(sy) < 0.999999:
        ry = np.arcsin(sy)
        rx = np.arctan2(R[2, 1], R[2, 2])
        rz = np.arctan2(R[1, 0], R[0, 0])
    else:
        # Gimbal lock case
        ry = np.pi/2 if sy < 0 else -np.pi/2
        rx = np.arctan2(-R[1, 2], R[1, 1])
        rz = 0.0
    return np.degrees([rx, ry, rz])

def make_matrix_world(s, R, t):
    """Return 4x4 transformation matrix in Blender's format."""
    M = np.eye(4)
    M[:3, :3] = s * R
    M[:3, 3] = t
    return M

if __name__ == "__main__":


    # --- Example: edit these points as needed ---
    # 3 vertices before transformation (rows)
    p_points = np.array([
        [1.00264, 0.745977, 0.457183],
        [-0.722978, 1.13666, 0.356606],
        [-1.13744, 0.712282, -0.278075]
    ])

    # 3 vertices after transformation (rows)
    q_points = np.array([
        [-0.86103, 1.96258, 0.371532],
        [0.035991, 0.045529, -0.006658],
        [0.810169, -0.206292, 0.385508]
    ])

    s, R, t = compute_similarity_transform(p_points, q_points)
    euler = rotation_matrix_to_euler_xyz(R)
    M = make_matrix_world(s, R, t)

    print("=== Similarity Transform ===")
    print(f"Scale (uniform): {s:.6f}")
    print("Rotation matrix:\n", R)
    print(f"Euler angles (XYZ degrees): {euler}")
    print(f"Translation vector: {t}")
    print("\nMatrix (Blender matrix_world):\n", M)
