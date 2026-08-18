import streamlit as st

rows_per_page = 3
total_pages = (len(st.session_state["df"]) + rows_per_page - 1) // rows_per_page

page = st.pagination(num_pages=total_pages, )

start_idx = (page - 1) * rows_per_page
end_idx = start_idx + rows_per_page
df = st.session_state["df"].iloc[start_idx:end_idx]

for item in df.to_dict("records"):
    with st.container(border=True):
        left, right = st.columns([1,4], vertical_alignment="top")
        
        left.image(image=item.pop("imageLinks.thumbnail"), output_format="PNG", width=160, link=item.pop("infoLink"))
        right.header(f"{item.pop("title")}(Lan - {item.pop("language")})")
        right.caption(f"{item.pop("year")}, {item.pop("month")} - {item.pop("country")}")
        right.text(f"Auths:   {item.pop("authors")}")
        right.text(f"Publisher:   {item.pop("publisher")}")
        right.text(f"Category:   {item.pop("categories")}")

        expander_subtitle = st.expander("Subtitle")
        expander_subtitle.text(item.pop("subtitle"))
        expander_description = st.expander("Description")
        expander_description.text(item.pop("description"))
        st.divider()
        st.header("About")
        about1, about2, about3, about4, about5 = st.columns(5, border=True)
        about1.text(f"Print:   {item.pop("printType")}")
        about2.text(f"Pages:   {item.pop("pageCount")}")
        about3.text(item.pop("isFree"))
        about4.badge("For Sale", color= "green" if item.pop("saleability") == 1 else "red")
        about5.badge("Ebook", color= "green" if item.pop("isEbook") == 1 else "red")

    st.space("small")