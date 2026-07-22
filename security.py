"""
Aiven Entertainment 관리 시스템 - 삭제 보안 모듈
데이터 삭제 시 비밀번호 확인 팝업을 띄워 무단 삭제를 방지합니다.
Streamlit Secrets에 ADMIN_PASSWORD를 설정해야 동작합니다.
"""
import streamlit as st
import db


def get_admin_password():
    try:
        return st.secrets.get("ADMIN_PASSWORD", None)
    except Exception:
        return None


@st.dialog("🔒 삭제 확인")
def confirm_delete_dialog(table: str, row_id: int, display_name: str):
    st.write(f"**'{display_name}'** 항목을 정말 삭제하시겠습니까?")
    st.caption("삭제 후에는 복구할 수 없습니다. 계속하려면 관리 비밀번호를 입력하세요.")

    admin_pw = get_admin_password()
    if not admin_pw:
        st.warning(
            "⚠️ 관리 비밀번호가 아직 설정되지 않았습니다. "
            "Streamlit Secrets에 ADMIN_PASSWORD를 추가하기 전까지는 "
            "비밀번호 확인 없이 삭제할 수 있습니다."
        )

    pwd = st.text_input("삭제 비밀번호", type="password", key=f"pwd_{table}_{row_id}")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("취소", use_container_width=True, key=f"cancel_{table}_{row_id}"):
            st.rerun()
    with c2:
        if st.button("🗑 삭제 확정", type="primary", use_container_width=True, key=f"confirm_{table}_{row_id}"):
            if admin_pw and pwd != admin_pw:
                st.error("비밀번호가 올바르지 않습니다.")
            else:
                db.delete_row(table, row_id)
                st.success("삭제되었습니다.")
                st.rerun()


def delete_button(label: str, table: str, row_id: int, display_name: str, key: str):
    """비밀번호 확인 팝업을 여는 삭제 버튼. 각 페이지의 삭제 버튼을 이 함수로 교체해서 사용합니다."""
    if st.button(label, key=key):
        confirm_delete_dialog(table, row_id, display_name)
