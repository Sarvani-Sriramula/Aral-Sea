import streamlit as st
import numpy as np
from PIL import Image

st.markdown("""
    <style>
        body {
            zoom: 0.85;   /* 85% zoom */
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------
st.set_page_config(page_title="AI Satellite Image Analyzer", layout="wide")

st.title("AI Satellite Image Analyzer")
st.markdown("""
This dashboard analyzes satellite images using NDVI and NDWI  
and provides AI-style predictions for environmental change over time.
""")

st.markdown("---")

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def compute_indices(img):
    """Compute NDVI and NDWI (water-masked)."""
    R = img[:, :, 0].astype(float)
    G = img[:, :, 1].astype(float)
    B = img[:, :, 2].astype(float)

    NDVI = (G - R) / (G + R + 1e-6)
    NDWI = (B - R) / (B + R + 1e-6)

    # Mask NDWI to only water pixels
    water_mask = NDWI > 0
    if np.any(water_mask):
        NDWI_water = float(np.mean(NDWI[water_mask]))
    else:
        NDWI_water = float(np.mean(NDWI))

    return float(np.mean(NDVI)), NDWI_water, NDVI, NDWI


def ai_predict_change(ndvi_diff, ndwi_diff):
    """AI prediction for change between two images."""
    if ndvi_diff < 0 and ndwi_diff < 0:
        return "⚠️ Declining: Both vegetation and water decreased — continued drying."
    elif ndvi_diff < 0 and ndwi_diff > 0:
        return "🌾 Moisture reflectance increased slightly, but vegetation loss shows decline."
    elif ndvi_diff > 0 and ndwi_diff < 0:
        return "🟡 Vegetation increased but water decreased — mixed signals."
    elif ndvi_diff > 0 and ndwi_diff > 0:
        return "🌱 Improving: Vegetation and water increased."
    else:
        return "🟡 Minimal change — stable conditions."


# ---------------------------------------------------------
# SINGLE IMAGE ANALYSIS
# ---------------------------------------------------------
st.header("Single Image Analysis")

uploaded_file = st.file_uploader("Upload a satellite image", type=["png", "jpg", "jpeg"], key="single")

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", width=450)

    img = np.array(image)

    ndvi_mean, ndwi_water_mean, NDVI, NDWI = compute_indices(img)

    st.subheader("NDVI & NDWI Results")

    col1, col2 = st.columns(2)
    col1.metric("NDVI", f"{ndvi_mean:.3f}")
    col2.metric("NDWI (Water Pixels)", f"{ndwi_water_mean:.3f}")

    # Interpretation only (no AI prediction)
    st.markdown("### Interpretation")
    if ndvi_mean < 0.1:
        st.write("- Very low vegetation — mostly barren or dry land.")
    elif ndvi_mean < 0.3:
        st.write("- Moderate vegetation — sparse plant life.")
    else:
        st.write("- Healthy vegetation present.")

    if ndwi_water_mean < 0:
        st.write("- Low moisture — limited water presence.")
    elif ndwi_water_mean < 0.2:
        st.write("- Some moisture detected.")
    else:
        st.write("- Strong water presence.")

st.markdown("---")

# ---------------------------------------------------------
# MULTI-IMAGE COMPARISON
# ---------------------------------------------------------
st.header("Compare Two Images")

colA, colB = st.columns(2)

with colA:
    img1_file = st.file_uploader("Upload FIRST image", type=["png","jpg","jpeg"], key="img1")
    if img1_file:
        img1 = Image.open(img1_file).convert("RGB")
        st.image(img1, caption="First Image", width=350)

with colB:
    img2_file = st.file_uploader("Upload SECOND image", type=["png","jpg","jpeg"], key="img2")
    if img2_file:
        img2 = Image.open(img2_file).convert("RGB")
        st.image(img2, caption="Second Image", width=350)

if img1_file and img2_file:
    arr1 = np.array(img1)
    arr2 = np.array(img2)

    ndvi1, ndwi1, NDVI1, NDWI1 = compute_indices(arr1)
    ndvi2, ndwi2, NDVI2, NDWI2 = compute_indices(arr2)

    st.subheader("Comparison Results")

    col1, col2 = st.columns(2)
    col1.metric("NDVI (Image 1)", f"{ndvi1:.3f}")
    col2.metric("NDVI (Image 2)", f"{ndvi2:.3f}")

    col3, col4 = st.columns(2)
    col3.metric("NDWI (Water Pixels 1)", f"{ndwi1:.3f}")
    col4.metric("NDWI (Water Pixels 2)", f"{ndwi2:.3f}")

    # Differences
    ndvi_diff = ndvi2 - ndvi1
    ndwi_diff = ndwi2 - ndwi1

    st.markdown("### Changes Between Images")
    st.write(f"**NDVI Change:** {ndvi_diff:.3f}")
    st.write(f"**NDWI Change:** {ndwi_diff:.3f}")

    # AI Prediction (only here)
    st.markdown("### AI Prediction (Change Over Time)")
    change_prediction = ai_predict_change(ndvi_diff, ndwi_diff)

    if "Declining" in change_prediction:
        st.error(change_prediction)
    elif "Improving" in change_prediction:
        st.success(change_prediction)
    else:
        st.warning(change_prediction)
