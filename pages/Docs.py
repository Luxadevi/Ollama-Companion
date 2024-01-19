import streamlit as st
from modules.docs_inline import docs
from st_pages import Page,  add_indentation

add_indentation()

# Create Tabs for Main Subjects
tab_main = st.tabs(list(docs.keys()))

for i, subject in enumerate(docs.keys()):
    with tab_main[i]:
        # Create Tabs for Sub-Subjects within each Main Subject
        tab_sub = st.tabs(list(docs[subject].keys()))

        for j, sub_subject in enumerate(docs[subject].keys()):
            with tab_sub[j]:
                # Display the Documentation for each Sub-Subject
                st.markdown(docs[subject][sub_subject])# st.divider()

