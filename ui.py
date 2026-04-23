import time
import streamlit as st
import clipboard

from blog_linkedin_app import generate_linkedin_post


def main():
    # Set page configuration
    st.set_page_config(
        page_title="Alwrity - AI LinkedIn Post Writer",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Global CSS styles for UI improvements
    st.markdown("""
        <style>
            body {
                background-color: #f0f2f6;
            }
            div.stButton > button:first-child {
                background-color: #007bff;
                color: white;
                padding: 12px 24px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s ease;
                border: none;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            div.stButton > button:first-child:hover {
                background-color: #0056b3;
            }
            .reportview-container .markdown-text-container {
                font-family: 'Helvetica Neue', sans-serif;
            }
        </style>
    """, unsafe_allow_html=True)

    # Hide top header and footer for a cleaner UI
    hide_elements = """
        <style>
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_elements, unsafe_allow_html=True)

    # Title and description
    st.title("✍️ Alwrity - AI LinkedIn Post Generator")
    st.write("Leverage AI to craft high-quality LinkedIn posts tailored to your audience.")

    # Initialize session state for generated post
    if "linkedin_post" not in st.session_state:
        st.session_state.linkedin_post = ""

    # Input section with an informative expander
    with st.expander("💡 **PRO TIP** - Follow these instructions for better results.", expanded=True):
        st.write("1. Use specific keywords related to your topic.\n"
                 "2. Choose a post type that aligns with your message.\n"
                 "3. Select an appropriate language and length for your audience.")

        # Input fields for the LinkedIn post generator
        input_blog_keywords = st.text_input(
            '🔑 **Enter main keywords for your post**',
            placeholder='e.g., Marketing Trends, Leadership Tips...',
            help="Use relevant keywords that define the topic of your LinkedIn post."
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            input_linkedin_type = st.selectbox('📝 **Post Type**', (
                'General', 'How-to Guides', 'Polls', 'Listicles',
                'Reality Check Posts', 'Job Posts', 'FAQs', 'Checklists/Cheat Sheets'),
                index=0, help="Choose the format that suits the message you want to deliver.")
        with col2:
            input_linkedin_length = st.selectbox('📏 **Post Length**',
                ('1000 words', 'Long Form', 'Short Form'), index=0,
                help="Decide the length of your post based on its complexity and target audience.")
        with col3:
            input_linkedin_language = st.selectbox('🌐 **Choose Language**',
                ('English', 'Vietnamese', 'Chinese', 'Hindi', 'Spanish'),
                index=0, help="Pick the language that resonates best with your audience.")

    # Button to generate the LinkedIn post
    if st.button('🚀 **Generate LinkedIn Post**'):
        if not input_blog_keywords:
            st.error('🚫 **Please provide keywords to generate a LinkedIn post!**')
        else:
            with st.spinner('🤖 Crafting your LinkedIn post...'):
                # Progress bar for user feedback
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.03)
                    progress_bar.progress(percent_complete + 1)

                # Generate the LinkedIn post
                st.session_state.linkedin_post = generate_linkedin_post(
                    input_blog_keywords, input_linkedin_type,
                    input_linkedin_length, input_linkedin_language)

            # Check if post generation succeeded
            if st.session_state.linkedin_post is not None:
                # Post generation success message
                st.success('🎉 **Your LinkedIn post is ready!**')
                st.subheader('📄 **LinkedIn Post Preview**')
                st.write(st.session_state.linkedin_post)

                # Copy to Clipboard button with success feedback
                if st.button('📋 Copy to Clipboard'):
                    clipboard.copy(st.session_state.linkedin_post)
                    st.success("✅ LinkedIn post copied to clipboard!")
            else:
                st.error('❌ **Failed to generate LinkedIn post. Please check your inputs or try again later.**')


if __name__ == "__main__":
    main()