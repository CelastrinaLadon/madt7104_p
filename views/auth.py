
import streamlit as st
import bcrypt
from streamlit_cookies_manager import CookieManager

from models.db import SessionLocal

def auth_view():
    from models.auth import User 

    cookies = CookieManager()
    if not cookies.ready():
        st.stop()

    username = cookies.get("username")
    logged_in = username is not None

    # Auto-login via cookies
    # if not logged_in:
    #     # st.query_params["page"] = "joinzyassistant"
    #     st.rerun()

    if logged_in:
        st.success(f"คุณเข้าสู่ระบบแล้วในชื่อ {username}")
        if st.button("Logout"):
            cookies["username"] = None
            cookies.save()
            st.query_params.clear()
            st.query_params["page"] = "auth"
            st.rerun()
        return

    # Tabs for login/register
    tab = st.radio("เลือกเมนู", ["เข้าสู่ระบบ", "สมัครสมาชิก"], horizontal=True)

    if tab == "เข้าสู่ระบบ":
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_submit = st.form_submit_button("Login")

            if login_submit:
                db = SessionLocal()
                user = db.query(User).filter(User.username == username).first()
                db.close()
                if user and bcrypt.checkpw(password.encode(), user.password_hash.encode()):
                    cookies["username"] = username
                    cookies.save()
                    st.query_params["page"]= "search"
                    st.success("เข้าสู่ระบบสำเร็จ")
                    st.rerun()
                else:
                    st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

    elif tab == "สมัครสมาชิก":
        with st.form("register_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")
            register_submit = st.form_submit_button("Register")

            if register_submit:
                if password != confirm:
                    st.error("รหัสผ่านไม่ตรงกัน")
                elif username.strip() == "" or email.strip() == "":
                    st.error("กรุณากรอกข้อมูลให้ครบถ้วน")
                else:
                    db = SessionLocal()
                    if db.query(User).filter(User.username == username).first():
                        st.error("Username นี้ถูกใช้งานแล้ว")
                    else:
                        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                        new_user = User(username=username, email=email, password_hash=hashed_pw)
                        db.add(new_user)
                        db.commit()
                        cookies["username"] = username
                        cookies.save()
                        st.query_params["page"]= "joinzyassistant"
                        st.success("สมัครสมาชิกสำเร็จ 🎉")
                        st.rerun()
                    db.close()
