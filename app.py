import numpy as np
import pandas as pd
import streamlit as st

st.title("2D Matrix Transformation Web App")

st.write("Aplikasi ini menunjukkan transformasi matriks 2D untuk sebuah persegi.")

# Bentuk awal: persegi dengan 4 titik
# Urutan titik: P1, P2, P3, P4
original_points = np.array([
    [0, 0],
    [1, 0],
    [1, 1],
    [0, 1]
])

st.subheader("Koordinat Awal Persegi")
df_original = pd.DataFrame(original_points, columns=["x", "y"])
df_original.index = ["P1", "P2", "P3", "P4"]
st.table(df_original)

# Pilih jenis transformasi
st.sidebar.header("Pengaturan Transformasi")
transform_type = st.sidebar.selectbox(
    "Pilih jenis transformasi",
    ["Translation", "Scaling", "Rotation", "Shearing", "Reflection"]
)

def apply_translation(points, tx, ty):
    """
    Translation dengan matriks homogen 3x3.
    """
    n = points.shape[0]
    homog = np.hstack([points, np.ones((n, 1))])  # (x, y, 1)
    T = np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
    transformed_homog = homog @ T.T
    return transformed_homog[:, :2]

def apply_scaling(points, sx, sy):
    S = np.array([
        [sx, 0],
        [0, sy]
    ])
    return points @ S.T

def apply_rotation(points, angle_deg):
    theta = np.deg2rad(angle_deg)
    R = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])
    return points @ R.T

def apply_shearing(points, direction, k):
    if direction == "Shear X":
        H = np.array([
            [1, k],
            [0, 1]
        ])
    else:  # Shear Y
        H = np.array([
            [1, 0],
            [k, 1]
        ])
    return points @ H.T

def apply_reflection(points, mode):
    if mode == "Refleksi terhadap sumbu X":
        F = np.array([
            [1, 0],
            [0, -1]
        ])
    elif mode == "Refleksi terhadap sumbu Y":
        F = np.array([
            [-1, 0],
            [0, 1]
        ])
    else:  # Refleksi terhadap garis y = x
        F = np.array([
            [0, 1],
            [1, 0]
        ])
    return points @ F.T

# Ambil parameter dari sidebar sesuai jenis transformasi
if transform_type == "Translation":
    tx = st.sidebar.number_input("tx (geser arah x)", value=1.0, step=0.5)
    ty = st.sidebar.number_input("ty (geser arah y)", value=1.0, step=0.5)
    transformed_points = apply_translation(original_points, tx, ty)

elif transform_type == "Scaling":
    sx = st.sidebar.number_input("sx (skala arah x)", value=2.0, step=0.5)
    sy = st.sidebar.number_input("sy (skala arah y)", value=2.0, step=0.5)
    transformed_points = apply_scaling(original_points, sx, sy)

elif transform_type == "Rotation":
    angle = st.sidebar.number_input("Sudut rotasi (derajat, ccw)", value=45.0, step=5.0)
    transformed_points = apply_rotation(original_points, angle)

elif transform_type == "Shearing":
    direction = st.sidebar.selectbox("Arah shear", ["Shear X", "Shear Y"])
    k = st.sidebar.number_input("Faktor shear (k)", value=1.0, step=0.5)
    transformed_points = apply_shearing(original_points, direction, k)

else:  # Reflection
    mode = st.sidebar.selectbox(
        "Mode refleksi",
        ["Refleksi terhadap sumbu X", "Refleksi terhadap sumbu Y", "Refleksi terhadap garis y = x"]
    )
    transformed_points = apply_reflection(original_points, mode)

# Tampilkan hasil transformasi
st.subheader("Koordinat Setelah Transformasi")
df_transformed = pd.DataFrame(transformed_points, columns=["x'", "y'"])
df_transformed.index = ["P1", "P2", "P3", "P4"]
st.table(df_transformed)

# Gabung untuk visualisasi scatter sederhana
st.subheader("Visualisasi Titik Sebelum dan Sesudah Transformasi")

plot_df = pd.DataFrame({
    "x": np.concatenate([original_points[:, 0], transformed_points[:, 0]]),
    "y": np.concatenate([original_points[:, 1], transformed_points[:, 1]]),
    "status": ["Awal"] * 4 + ["Transformed"] * 4
})

st.scatter_chart(
    plot_df,
    x="x",
    y="y",
    color="status"
)