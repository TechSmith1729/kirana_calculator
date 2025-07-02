from PIL import Image
import streamlit as st
import json

# Load item data
with open("data/items_data.json", "r") as f:
    items_data = json.load(f)

# Sidebar section
st.sidebar.title("📂 Categories")
category_list = list(items_data.keys())
selected_category = st.sidebar.radio("Choose a section",category_list)


st.title(f"🛒 {selected_category} Items")

cols = st.columns(3)

for idx, (item_name, item_info) in enumerate(items_data[selected_category].items()):
    with cols[idx % 3]:
        # Load and resize image
        image_path = f"assets/images/{item_info['image']}"
        try:
            img = Image.open(image_path)
            img = img.resize((180, 180))
            st.image(img, caption=item_name)
        except FileNotFoundError:
            st.error(f"Image not found: {item_info['image']}")

        # Quantity input (in kg/L/grams — user defined)
        quantity = st.number_input(
            f"Quantity of {item_name}",
            min_value=0.0,
            step=0.1,
            key=f"{selected_category}_{item_name}"
        )
