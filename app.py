import streamlit as st
from database import *
import os
import uuid

create_table()

st.set_page_config(page_title="Retrievy", layout="wide")

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "item_type" not in st.session_state:
    st.session_state.item_type = "Lost"

st.sidebar.title("📌 Retrievy")
st.sidebar.subheader("Lost and Found system")

if st.session_state.user:
    st.sidebar.write(f"👤 User ID: {st.session_state.user['id']}")


pages = ["Home", "Login", "Register", "Report Item", "Browse Items","My Items"]

selected = st.sidebar.radio(
    "Navigate",
    pages,
    index=pages.index(st.session_state.page)
)


st.session_state.page = selected

if st.session_state.user:
    st.sidebar.write(f"Logged in as {st.session_state.user['username']}")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

st.markdown("""
    <h1 style='text-align: center;'>🕵️Retrievy🕵️</h1>
    <h4 style='text-align: center;'>Lost & Found System</h4>
    <hr>
""", unsafe_allow_html=True)


if st.session_state.page == "Login":
    st.subheader("🔑 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not username.strip():
            st.error("Username cannot be empty")
            st.stop()

        user = login_user(username, password)
        if user:
            st.session_state.user = user
            st.session_state.page = "Home"
            st.rerun()
            
        else:
            st.error("Invalid credentials")

elif st.session_state.page == "Register":
    st.subheader("📝 Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if not username.strip():
            st.error("Username cannot be empty")
            st.stop()
        if len(password) < 4:
            st.error("Password must be at least 4 characters")
            st.stop()

        success = register_user(username, password)

        if success:
            st.success("User created")
        else:
            st.error("Username exists")

elif st.session_state.page == "Home":
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

elif st.session_state.page == "Report Item":

    if not st.session_state.user:
        st.warning("You must be logged in")
        st.stop()

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
            if not item_name or not location:
                st.error("Item name and location are required")
                st.stop()

            file_path = None

            if image_path is not None:
                UPLOAD_FOLDER = "uploads"
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)

                filename = str(uuid.uuid4()) + "_" + image_path.name
                file_path = os.path.join(UPLOAD_FOLDER, filename)

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
                file_path,
                st.session_state.user["id"]
            )

            st.success("✅ Form submitted")


elif st.session_state.page == "Browse Items":
    st.subheader("📋 Browse Items")

    col1, col2, col3 = st.columns(3)

    with col1:
        first_selectbox = st.selectbox(
            "Filter by Type", ["All", "Lost", "Found"])

    with col2:
        second_selectbox = st.selectbox(
            "Category", ["All", "Electronics", "Documents", "Clothing", "Other"])

    with col3:
        third_selectbox = st.text_input("Search")

    items = get_all_items()

    if first_selectbox != "All":
        items = [item for item in items if item["item_type"] == first_selectbox]

    if second_selectbox != "All":
        items = [item for item in items if item["category"] == second_selectbox]

    if third_selectbox:
        query = third_selectbox.lower()
        items = [
            item for item in items
            if query in item["item_name"].lower()
            or (item["description"] and query in item["description"].lower())
        ]

    if not items:
        st.warning("No items found")
    else:
        st.write(f"Showing {len(items)} items")

    for item in items:
        st.subheader(item["item_name"])

        colA, colB, colC = st.columns(3)

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

elif st.session_state.page == "My Items":
    if not st.session_state.user:
        st.warning("You must be logged in")
        st.stop()

    st.subheader("📋 My Items")

    items = get_all_items()

    my_items = [
        item for item in items
        if item["user_id"] == st.session_state.user["id"]
    ]

    if not my_items:
        st.info("No items posted yet")
    else:
        for item in my_items:
            st.subheader(item["item_name"])

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"📍 {item['location']}")
                st.write(f"📅 {item['date']}")

            with col2:
                st.write(f"📦 {item['category']}")
                st.write(f"📝 {item['description']}")

                if st.button(f"Delete {item['id']}", key=f"del_{item['id']}"):
                    delete_item(item["id"])
                    st.success("Item deleted")
                    st.rerun()

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
