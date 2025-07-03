from PIL import Image
import streamlit as st
import json

# ---------- Helper Function: Update Cart ----------
def update_cart(category, item_name, item_info, quantity):
    if quantity > 0:
        if "price_per_100g" in item_info:
            unit_price = item_info["price_per_100g"]
            total_price = (quantity / 100) * unit_price
        else:
            unit_price = item_info.get("price_per_kg") or item_info.get("price_per_litre", 0)
            total_price = quantity * unit_price

        st.session_state.cart[item_name] = {
            "category": category,
            "quantity": quantity,
            "total": round(total_price, 2)
        }
    else:
        st.session_state.cart.pop(item_name, None)


# ---------- Load Item Data ----------
with open("data/items_data.json", "r") as f:
    items_data = json.load(f)

# ---------- Initialize Session State ----------
if "cart" not in st.session_state:
    st.session_state.cart = {}

# ---------- Sidebar ----------
st.sidebar.title("📂 Categories")
category_list = list(items_data.keys())
selected_categories = st.sidebar.multiselect("Select categories", category_list)

# Sidebar option to show bill
show_bill = st.sidebar.checkbox("🧾 Show Current Bill")

# ---------- Show Current Bill ----------
if show_bill:
    st.title("🧾 Current Bill Summary")

    if st.session_state.cart:
        total_all = 0
        for item, data in st.session_state.cart.items():
            st.markdown(
                f"✅ **{item}** ({data['category']}) — {data['quantity']} kg/L — ₹{data['total']}"
            )
            total_all += data['total']

        st.markdown("---")
        st.markdown(f"### 🧮 Grand Total: ₹{round(total_all, 2)}")
    else:
        st.info("No items selected yet.")

# ---------- Show Product Items ----------
else:
    for category in selected_categories:
        st.title(f"🛒 {category} Items")
        cols = st.columns(3)

        for idx, (item_name, item_info) in enumerate(items_data[category].items()):
            with cols[idx % 3]:
                # Display image
                image_path = f"assets/images/{item_info['image']}"
                try:
                    img = Image.open(image_path)
                    img = img.resize((180, 180))
                    st.image(img, caption=item_name)
                except FileNotFoundError:
                    st.error(f"Image not found: {item_info['image']}")

                # Quantity input
                quantity = st.number_input(
                    label="",
                    min_value=0.0,
                    step=0.1,
                    placeholder="kg/L",
                    key=f"{category}_{item_name}",
                    label_visibility="collapsed"
                )

                # Update cart
                update_cart(category, item_name, item_info, quantity)

                # Show calculated price (live)
                if quantity > 0:
                    if "price_per_100g" in item_info:
                        unit_price = item_info["price_per_100g"]
                        total_price = (quantity / 100) * unit_price
                    else:
                        unit_price = item_info.get("price_per_kg") or item_info.get("price_per_litre", 0)
                        total_price = quantity * unit_price
                    st.markdown(f"**Total: ₹{round(total_price, 2)}**")
