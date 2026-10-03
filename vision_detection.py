"""
Image Recognition App
Classifies an image into 1,000 ImageNet categories using a pretrained
Vision Transformer / ResNet model from Hugging Face. Runs fully offline
after the first model download. No API key needed.
"""
import streamlit as st
from PIL import Image
from transformers import pipeline

st.set_page_config(page_title="Image Recognition", page_icon="🖼️", layout="centered")

MODELS = {
    "ViT Base (Google)": "google/vit-base-patch16-224",
    "ResNet-50 (Microsoft)": "microsoft/resnet-50",
}


@st.cache_resource(show_spinner="Loading model (first run downloads it, please wait)...")
def load_classifier(model_id: str):
    return pipeline("image-classification", model=model_id)


# ---------------- Sidebar ----------------
st.sidebar.header("Settings")
model_name = st.sidebar.selectbox("Model", list(MODELS.keys()))
top_k = st.sidebar.slider("Number of predictions", 1, 10, 5)
st.sidebar.markdown("---")
st.sidebar.caption("Models are trained on ImageNet (1,000 everyday object classes).")

# ---------------- Main ----------------
st.title("🖼️ Image Recognition")
st.write("Upload an image or take a photo, and the model will tell you what it sees.")

tab_upload, tab_camera = st.tabs(["📁 Upload", "📷 Camera"])
image = None

with tab_upload:
    file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "webp", "bmp"])
    if file:
        image = Image.open(file).convert("RGB")

with tab_camera:
    photo = st.camera_input("Take a picture")
    if photo:
        image = Image.open(photo).convert("RGB")

if image is not None:
    st.image(image, caption="Input image")

    if st.button("🔍 Recognize", type="primary"):
        classifier = load_classifier(MODELS[model_name])
        with st.spinner("Analyzing image..."):
            results = classifier(image, top_k=top_k)

        best = results[0]
        st.success(f"**Top prediction:** {best['label']}  ({best['score'] * 100:.2f}%)")

        st.subheader("All predictions")
        for r in results:
            st.write(f"{r['label']} — {r['score'] * 100:.2f}%")
            st.progress(float(r["score"]))
else:
    st.info("👆 Upload an image or use the camera to get started.")
