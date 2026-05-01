import streamlit as st
from appDB import *
import os


create_table()
st.set_page_config(page_title="Retrievy", layout="wide")

# ----------------------------
# Session State Initialization
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "item_type" not in st.session_state:
    st.session_state.item_type = "Lost"

# ----------------------------
# Sidebar Navigation
# ----------------------------
st.sidebar.title("📌 Retrievy")
st.sidebar.subheader("Lost and Found system")

pages = ["Home", "Report Item", "Browse Items"]

selected = st.sidebar.radio(
    "Navigate",
    pages,
    index=pages.index(st.session_state.page)
)

st.session_state.page = selected

# ----------------------------
# Header
# ----------------------------
st.markdown("""
    <h1 style='text-align: center;'>🕵️Retrievy🕵️</h1>        
    <h4 style='text-align: center;'>Lost & Found System</h4>
    <hr>
""", unsafe_allow_html=True)

# ----------------------------
# Home Page
# ----------------------------
if st.session_state.page == "Home":
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 📢 Report Lost Item
        Lost something? Submit details and let others help you find it.
        """)
        if st.button("Report Lost"):
            st.session_state.page = "Report Item"
            st.session_state.item_type = "Lost"
            st.rerun()

    with col2:
        st.markdown("""
        ### 🎉 Report Found Item
        Found something? Help return it to the owner.
        """)
        if st.button("Report Found"):
            st.session_state.page = "Report Item"
            st.session_state.item_type = "Found"
            st.rerun()

    st.markdown("---")

    st.markdown("### 🚀 How It Works")
    st.markdown("""
    1. Report a lost or found item  
    2. Browse listings  
    3. Connect with the owner  
    """)

# ----------------------------
# Report Item Page
# ----------------------------
elif st.session_state.page == "Report Item":
    st.subheader("➕ Report Lost / Found Item")

    with st.form("report_form"):
        col1, col2 = st.columns(2)

        with col1:
            item_name = st.text_input("Item Name")

            item_type = st.selectbox(
                "Type",
                ["Lost", "Found"],
                index=0 if st.session_state.item_type == "Lost" else 1
            )

            category = st.selectbox(
                "Category",
                ["Electronics", "Documents", "Clothing", "Other"]
            )

        with col2:
            location = st.text_input("Location")
            date = st.date_input("Date")
            contact_info = st.text_input("Contact Info")

        description = st.text_area("Description")
        image_path = st.file_uploader(
            "Upload Image", type=["jpg", "png", "jpeg"])
        
        submit = st.form_submit_button("Submit")

        if submit:
            file_path = None

            if image_path is not None:
                UPLOAD_FOLDER = "uploads"
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)

                file_path = os.path.join(UPLOAD_FOLDER, image_path.name)

                with open(file_path, "wb") as f:
                    f.write(image_path.getvalue())

            add_item(
                item_name,
                item_type,
                location,
                str(date),
                category,
                contact_info,
                description,
                file_path
            )

            st.success("✅ Form submitted")
# ----------------------------
# Browse Items Page
# ----------------------------

elif st.session_state.page == "Browse Items":
    st.subheader("📋 Browse Items")

    col1, col2, col3 = st.columns(3)

    with col1:
        first_selectbox = st.selectbox(
            "Filter by Type", ["All", "Lost", "Found"])

    with col2:
        second_selectbox = st.selectbox(
            "Category", ["All", "Electronics", "Documents", "Clothing", "Others"])

    with col3:
        third_selectbox = st.text_input("Search")

    items = get_all_items()

    if first_selectbox != "All":
        items = [item for item in items if item["item_type"] == first_selectbox]

    if second_selectbox != "All":
        items = [item for item in items if item["category"] == second_selectbox]

    if not items:
        st.warning("No items found")
    else:
        st.write(f"Showing {len(items)} items")

    for item in items:
        st.subheader(item["item_name"])

        colA, colB,colC = st.columns(3)

        with colA:
            st.write(f"📍 {item['location']}")
            st.write(f"📅 {item['date']}")

        with colB:
            st.write(f"🔎 {item['item_type']}")
            st.write(f"📦 {item['category']}")

            st.write(f"📝 {item['description']}")
        with colC:
            if item["image_path"]:
                st.image(item["image_path"])

        st.markdown("---")

    

    # Static UI cards
    # for i in range(3):
    #     st.markdown(f"""
    #     <div style="
    #         background-color:#ffffff;
    #         padding:15px;
    #         border-radius:10px;
    #         box-shadow:0 2px 6px rgba(0,0,0,0.1);
    #         margin-bottom:15px;
    #     ">
    #         <h4>Item Name</h4>
    #         <p><b>Type:</b> Lost</p>
    #         <p>Short description of the item...</p>
    #         <p><i>Location:</i> XYZ Area</p>
    #     </div>
    #     """, unsafe_allow_html=True)
