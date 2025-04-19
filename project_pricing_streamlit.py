
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="تسعير عروض المشاريع", layout="wide")
st.title("💰 برنامج تسعير عروض مشاريع المقاولات")

st.markdown("📤 **ارفع ملف Excel يحتوي على بنود الأعمال والكميات والمواصفات.**")
uploaded_file = st.file_uploader("اختر ملف Excel", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        if "بند" not in df.columns or "الوصف" not in df.columns or "الوحدة" not in df.columns or "الكمية" not in df.columns:
            st.error("❌ تأكد أن الملف يحتوي على الأعمدة التالية: بند، الوصف، الوحدة، الكمية.")
        else:
            st.success("✅ تم تحميل الملف بنجاح. يمكنك الآن إدخال الأسعار لكل بند.")

            df["سعر الوحدة (ريال)"] = df.get("سعر الوحدة (ريال)", 0.0)
            df["التكلفة الإجمالية"] = df["الكمية"] * df["سعر الوحدة (ريال)"]

            edited_df = st.data_editor(
                df[["بند", "الوصف", "الوحدة", "الكمية", "سعر الوحدة (ريال)", "التكلفة الإجمالية"]],
                num_rows="dynamic",
                use_container_width=True
            )

            st.subheader("📦 ملخص العرض:")
            total_cost = edited_df["التكلفة الإجمالية"].sum()
            st.metric("إجمالي تكلفة العرض", f"{total_cost:,.2f} ريال")

            @st.cache_data
            def convert_to_excel(df):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name="عرض السعر")
                return output.getvalue()

            excel_data = convert_to_excel(edited_df)

            st.download_button(
                label="📥 تحميل عرض السعر بصيغة Excel",
                data=excel_data,
                file_name="عرض_السعر.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"حدث خطأ أثناء المعالجة: {e}")
