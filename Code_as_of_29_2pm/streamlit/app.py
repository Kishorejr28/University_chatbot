import streamlit as st
from api_calls import query_lang_api, load_data_api, query_llama_api,get_llama_chat_history,get_lang_chat_history
from PIL import Image, ImageOps, ImageDraw

#Streamlit App Title 

# Function to create a circular crop of the image
def make_circle_image(image):
    # Create a circular mask
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + image.size, fill=255)
    
    # Apply the mask to the image to make it circular
    result = Image.new("RGBA", image.size)
    result.paste(image, mask=mask)
    
    return result

# Load the image
image = Image.open("SRH_Logo.png")

# Resize the image to 50x50 pixels
image = image.resize((100, 100))

# Make the image circular using the custom function
circular_image = make_circle_image(image)

# Create two columns: one for the image and one for the title
col1, col2 = st.columns([1, 7])

with col1:
    st.image(circular_image, width=75)  # Display the circular image

with col2:
    st.title("SaRaH - UniBot")  # Display the title next to the image

# Create tabs for LangChain and Llama Index
tab1, tab2 = st.tabs(["LangChain", "Llama Index"])

# Replace this block
if tab1.is_active:
    st.session_state.active_tab = "Tab 1"
else:
    st.session_state.active_tab = "Tab 2"

# With this new block to track the active tab based on selection
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Tab 1"

# Check the current tab and set the active tab accordingly
if tab1:
    st.session_state.active_tab = "Tab 1"
elif tab2:
    st.session_state.active_tab = "Tab 2"



# LangChain Tab
with tab1:
    # Initialize session state for chat messages, chat_id, and other variables
    if "tab1_messages" not in st.session_state:
        st.session_state.tab1_messages = []
    if "tab1_chat_id" not in st.session_state:
        st.session_state.tab1_chat_id = None 
    if "tab1_prev_query" not in st.session_state:
        st.session_state.tab1_prev_query = None
    if "tab1_selected_model" not in st.session_state:
        st.session_state.tab1_selected_model = "groq"
    if "tab1_recent_chats" not in st.session_state:
        st.session_state.tab1_recent_chats = []

    # Function to display chat messages for Tab 1
    def display_chat_messages_tab1():
        st.session_state.tab1_rendered_messages = []  # New list to avoid re-rendering old messages
        for message in st.session_state.tab1_messages:
            if message not in st.session_state.tab1_rendered_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                st.session_state.tab1_rendered_messages.append(message)

   
    # Accept user input for a new query in Tab 1
    if prompt := st.chat_input("What can I help you with?", key="tab1_chat_input"):
        # Check if the new query is the same as the previous one to avoid repetition
        if prompt != st.session_state.tab1_prev_query:
            st.session_state.tab1_prev_query = prompt  # Update previous query

        # Display existing chat messages
        display_chat_messages_tab1()

        # Add user query to chat
        st.session_state.tab1_messages.append({
            "role": "user",
            "content": prompt  # Display user query as is
        })

        # Display the new user query (without re-rendering existing ones)
        with st.chat_message("user"):
            st.markdown(prompt)

        # Call the API to get the response from the selected model
        response_data = query_lang_api(
            prompt, 
            st.session_state.tab1_chat_id, 
            model_choice=st.session_state.tab1_selected_model
        )

        # If response is valid, update chat history and display assistant response
        if response_data and "Response" in response_data:
            assistant_response = response_data["Bot_responce"]
            st.session_state.tab1_chat_id = response_data["Chat_ID"]  # Update chat_id for session

            # Add assistant's response to chat
            st.session_state.tab1_messages.append({
                "role": "assistant",
                "content": assistant_response  # Display assistant's response as is
            })

            # Display the assistant's response (without re-rendering existing ones)
            with st.chat_message("assistant"):
                st.markdown(assistant_response)


# Sidebar for file upload, model selection, and recent chat retrieval for Tab 1
with st.sidebar:
    # Upload section with header and reduced space
    # Custom CSS to reduce space
    st.markdown("""
        <style>
        .file-uploader {
            margin: 0; /* Remove default margin */
            padding: 0; /* Remove default padding */
        }
        </style>
        """, unsafe_allow_html=True)

    # Custom heading
    st.markdown("<h4 style='margin-bottom:10px;'>Document Upload</h4>", unsafe_allow_html=True)

    # File uploader with hidden label and reduced space
    uploaded_file = st.file_uploader("", type=["pdf"], key="uploader", label_visibility="collapsed")
    if uploaded_file:
        load_data_api(uploaded_file)  # Trigger data load when file is uploaded

    # Small gap instead of large divider
    st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)

    # Button for clearing chats
    st.markdown("<h4 style='margin-bottom:10px;'>Chat Management</h4>", unsafe_allow_html=True)
    if st.button("New Chat", help="Clear chat history and start fresh"):
        # Clear chat messages for Tab 1
        st.session_state.tab1_messages.clear()
        st.session_state.tab1_chat_id = None
        st.session_state.tab1_prev_query = None

        # Clear chat messages for Tab 2
        st.session_state.tab2_messages.clear()
        st.session_state.tab2_chat_id = None
        st.session_state.tab2_prev_query = None

    # Small gap
    st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)

    # Model selection dropdown with reduced space
    st.markdown("<h4 style='margin-bottom:10px;'>Model Selection</h4>", unsafe_allow_html=True)
    model_choice = st.selectbox(
        "Select Model", 
        ["OpenAI", "Llama"],
        index=["OpenAI", "Llama"].index(
            "OpenAI" if st.session_state.tab1_selected_model == "openai" else "Llama"
        ),
        help="""GPT-4: Broad, versatile 
        Llama 3: Fast, efficient"""""
    )
    st.session_state.tab1_selected_model = "openai" if model_choice == "OpenAI" else "groq"
    st.session_state.tab2_selected_model = st.session_state.tab1_selected_model  # Synchronize model choice for Tab 2

    # Small gap
    st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)

    # Button for fetching recent chats for Tab 1
    st.markdown("<h4 style='margin-bottom:10px;'>Chat History</h4>", unsafe_allow_html=True)
    if st.button("🔍 Fetch Latest Chats", help="Retrieve recent chats for LangChain"):
        st.session_state.tab1_recent_chats = get_lang_chat_history()

    # Display recent chats within an expander
    if st.session_state.active_tab == "Tab 1" and st.session_state.tab1_recent_chats:
        with st.expander("Click to open/close recent chats", expanded=False):
            for index, chat in enumerate(st.session_state.tab1_recent_chats):
                chat_id = chat["chat_id"]
                first_question = chat["history"][0]["Question"] if chat["history"] else "No Question"
                summary = f"Chat: {first_question} - {len(chat['history'])} messages"

                # Button to load selected chat history
                if st.button(summary, key=f"tab1_chat_{index}"):
                    st.session_state.tab1_chat_id = chat_id
                    st.session_state.tab1_messages = []
                    for msg in chat["history"]:
                        st.session_state.tab1_messages.append({"role": "user", "content": msg["Question"]})
                        st.session_state.tab1_messages.append({"role": "assistant", "content": msg["Response"]})
                    st.session_state["rerun_trigger"] = True  # Update session state to trigger rerun



# Llama Index Tab
with tab2:
    # Initialize session state for chat messages, chat_id, and other variables
    if "tab2_messages" not in st.session_state:
        st.session_state.tab2_messages = []
    if "tab2_chat_id" not in st.session_state:
        st.session_state.tab2_chat_id = None
    if "tab2_prev_query" not in st.session_state:
        st.session_state.tab2_prev_query = None
    if "tab2_selected_model" not in st.session_state:
        st.session_state.tab2_selected_model = "groq"
    if "tab2_recent_chats" not in st.session_state:
        st.session_state.tab2_recent_chats = []

    # Function to display chat messages for Tab 2
    def display_chat_messages_tab2():
        st.session_state.tab2_rendered_messages = []  # New list to avoid re-rendering old messages
        for message in st.session_state.tab2_messages:
            if message not in st.session_state.tab2_rendered_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                st.session_state.tab2_rendered_messages.append(message)

    # Display existing chat messages
    display_chat_messages_tab2()

    # Accept user input for a new query in Tab 2
    if prompt := st.chat_input("What can I help you with?", key="tab2_chat_input"):
        # Check if the new query is the same as the previous one to avoid repetition
        if prompt != st.session_state.tab2_prev_query:
            st.session_state.tab2_prev_query = prompt  # Update previous query

            # Add user query to chat
            st.session_state.tab2_messages.append({
                "role": "user",
                "content": prompt  # Display user query as is
            })

            # Display the new user query (without re-rendering existing ones)
            with st.chat_message("user"):
                st.markdown(prompt)

            # Call the API to get the response from the selected model
            response_data = query_llama_api(
                prompt, 
                st.session_state.tab2_chat_id, 
                model_choice=st.session_state.tab2_selected_model
            )

            # If response is valid, update chat history and display assistant response
            if response_data and "Response" in response_data:
                assistant_response = response_data["Bot_responce"]
                st.session_state.tab2_chat_id = response_data["Chat_ID"]  # Update chat_id for session

                # Add assistant's response to chat
                st.session_state.tab2_messages.append({
                    "role": "assistant",
                    "content": assistant_response  # Display assistant's response as is
                })

                # Display the assistant's response (without re-rendering existing ones)
                with st.chat_message("assistant"):
                    st.markdown(assistant_response)

with st.sidebar:
# Button to fetch recent chats for Tab 2
    
    # Button to fetch recent chats for Tab 1
    if st.button("🔍 Fetch Latest Chats", help="Retrieve recent chats for Llamaindex"):
        st.session_state.tab2_recent_chats = get_llama_chat_history()

    
    # Display recent chats only for Tab 2
    if st.session_state.active_tab == "Tab 1" and st.session_state.tab2_recent_chats:
        with st.expander("Click to open/close recent chats", expanded=False):
            for index, chat in enumerate(st.session_state.tab2_recent_chats):
                chat_id = chat["chat_id"]
                first_question = chat["history"][0]["Question"] if chat["history"] else "No Question"
                summary = f"Chat: {first_question} - {len(chat['history'])} messages"

                # Button to load selected chat history
                if st.button(summary, key=f"tab2_chat_{index}"):
                    st.session_state.tab2_chat_id = chat_id
                    st.session_state.tab2_messages = []
                    for msg in chat["history"]:
                        st.session_state.tab2_messages.append({"role": "user", "content": msg["Question"]})
                        st.session_state.tab2_messages.append({"role": "assistant", "content": msg["Response"]})
                    st.session_state["rerun_trigger"] = True  # Update session state to trigger rerun