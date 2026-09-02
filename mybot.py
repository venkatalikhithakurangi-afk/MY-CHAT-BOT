import streamlit as st
from google import genai

# ============================================================
# 🤖 MY HeALPING BOT
# Streamlit + Gemini AI Chatbot
# ============================================================


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MY HeALPING BOT",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# 2. GEMINI API KEY
# ============================================================

# Replace this with your actual Gemini API key.

API_KEY = "ENTER YOUR API KEY"

# Create Gemini client
client = genai.Client(api_key=API_KEY)


# ============================================================
# 3. FIND AVAILABLE GEMINI MODELS
# ============================================================

@st.cache_resource
def get_available_models():
    """
    Ask the Gemini API which models are available
    for the current API key.

    We only select models that support generateContent,
    because our chatbot needs text generation.
    """

    available_models = []

    try:

        # Ask Gemini API for the available models.
        for model in client.models.list():

            # Google returns model names such as:
            # models/gemini-2.5-flash
            #
            # We remove "models/" so that we can use
            # the model name directly.

            model_name = model.name

            if model_name.startswith("models/"):
                model_name = model_name.replace(
                    "models/",
                    "",
                    1
                )

            # Check whether this model supports
            # generateContent.

            supported_actions = getattr(
                model,
                "supported_actions",
                []
            )

            if "generateContent" in supported_actions:

                available_models.append(model_name)

    except Exception as error:

        # If model listing fails, return an empty list.
        # The chatbot will show the error later.

        return []


    return available_models


# ============================================================
# 4. SELECT THE BEST MODEL
# ============================================================

def select_best_model(available_models):
    """
    Select a suitable model from the models actually
    available to our API key.

    The order below represents our preference.
    """

    # Preferred models for a general chatbot.
    #
    # Flash models are generally a good choice for
    # interactive applications.

    preferred_models = [

        "gemini-3.7-flash",

        "gemini-3.6-flash",

        "gemini-3.5-flash",

        "gemini-2.5-flash",

        "gemini-3.5-flash-lite",

        "gemini-3.1-flash-lite",

        "gemini-2.5-flash-lite",

        "gemini-2.5-pro"
    ]


    # Check our preferred models one by one.

    for preferred in preferred_models:

        if preferred in available_models:

            return preferred


    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    # If none of our preferred models are available,
    # select any available generateContent model.

    if available_models:

        return available_models[0]


    # Nothing available.
    return None


# ============================================================
# 5. GET MODELS
# ============================================================

available_models = get_available_models()

selected_model = select_best_model(
    available_models
)


# ============================================================
# 6. CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       MAIN BACKGROUND
       ======================================================== */

    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a,
            #1e1b4b,
            #312e81
        );
    }


    /* ========================================================
       NORMAL TEXT
       ======================================================== */

    .stApp p {
        color: #ffffff !important;
    }

    .stApp li {
        color: #ffffff !important;
    }

    .stApp label {
        color: #ffffff !important;
    }


    /* ========================================================
       MAIN TITLE
       ======================================================== */

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-top: 15px;
        margin-bottom: 5px;
        color: #ffffff !important;
    }


    /* ========================================================
       SUBTITLE
       ======================================================== */

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #e2e8f0 !important;
        margin-bottom: 25px;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #111827;
    }

    section[data-testid="stSidebar"] p {
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"] span {
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"] label {
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }


    /* ========================================================
       CHAT MESSAGES
       ======================================================== */

    [data-testid="stChatMessage"] p {
        color: #ffffff !important;
    }

    [data-testid="stChatMessage"] li {
        color: #ffffff !important;
    }


    /* ========================================================
       CHAT INPUT
       ======================================================== */

    [data-testid="stChatInput"] textarea {
        color: #111827 !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #64748b !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 12px;
        font-weight: bold;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;
        color: #cbd5e1 !important;
        margin-top: 30px;
        padding: 20px;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 7. HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🤖 MY HeALPING BOT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your friendly AI assistant • Ask me anything!'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# 8. SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 MY HeALPING BOT")

    st.write(
        "Welcome to MY HeALPING BOT!"
    )

    st.write(
        "I can help you with programming, "
        "learning, projects, interviews and general questions."
    )

    st.divider()

    st.subheader("✨ Features")

    st.write("💬 AI Chat")
    st.write("🐍 Python Help")
    st.write("☕ Java Help")
    st.write("🗄️ SQL Help")
    st.write("📚 Study Support")
    st.write("💻 Project Guidance")

    st.divider()

    # --------------------------------------------------------
    # MODEL INFORMATION
    # --------------------------------------------------------

    st.subheader("🧠 AI Model")

    if selected_model:

        st.success(
            f"Using: {selected_model}"
        )

    else:

        st.error(
            "No compatible Gemini model found."
        )


    # --------------------------------------------------------
    # CLEAR CHAT
    # --------------------------------------------------------

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# 9. CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# 10. WELCOME MESSAGE
# ============================================================

if len(st.session_state.messages) == 0:

    st.markdown("### 👋 Hello!")

    st.write(
        "I am **MY HeALPING BOT**."
    )

    st.write(
        "Ask me anything about Python, Java, SQL, "
        "projects, studies, interviews or coding."
    )

    st.write(
        "🚀 Let's learn together!"
    )


# ============================================================
# 11. DISPLAY OLD MESSAGES
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        avatar = "👤"

    else:

        avatar = "🤖"


    with st.chat_message(
        message["role"],
        avatar=avatar
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# 12. CHAT INPUT
# ============================================================

user_prompt = st.chat_input(
    "💬 Type your message here..."
)


# ============================================================
# 13. PROCESS USER MESSAGE
# ============================================================

if user_prompt:

    # Save user's message.

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )


    # Display user's message.

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.markdown(user_prompt)


    # Generate AI response.

    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        with st.spinner(
            "MY HeALPING BOT is thinking... 🤔"
        ):

            try:

                # =================================================
                # CHECK MODEL
                # =================================================

                if not available_models:

                    raise Exception(
                        "Your Gemini API key does not have "
                        "access to a compatible generateContent model."
                    )


                # =================================================
                # BUILD CONVERSATION
                # =================================================

                conversation = ""

                for message in st.session_state.messages:

                    if message["role"] == "user":

                        conversation += (
                            "User: "
                            + message["content"]
                            + "\n"
                        )

                    else:

                        conversation += (
                            "Assistant: "
                            + message["content"]
                            + "\n"
                        )


                # =================================================
                # BOT INSTRUCTIONS
                # =================================================

                instructions = """
You are MY HeALPING BOT.

You are a friendly, patient and helpful AI assistant.

Your goals are:

1. Help beginners understand programming.
2. Explain Python clearly.
3. Explain Java clearly.
4. Explain SQL and databases.
5. Help debug programming errors.
6. Help students with projects.
7. Give step-by-step explanations.
8. Help with interview preparation.
9. Use simple English.
10. Encourage learners.

When explaining programming:

- Explain the concept first.
- Give a simple example.
- Provide code when needed.
- Explain important lines of code.
- Keep explanations beginner-friendly.

Do not unnecessarily make answers complicated.
"""


                # =================================================
                # TRY MODELS
                # =================================================

                # Put the selected model first.
                #
                # If it fails, the code automatically tries
                # another compatible model.

                models_to_try = []

                if selected_model:

                    models_to_try.append(
                        selected_model
                    )


                # Add other available models as fallbacks.

                for model in available_models:

                    if model not in models_to_try:

                        models_to_try.append(model)


                bot_reply = None

                used_model = None

                last_error = None


                # =================================================
                # MODEL FALLBACK LOOP
                # =================================================

                for model in models_to_try:

                    try:

                        response = client.models.generate_content(

                            model=model,

                            contents=(
                                instructions
                                + "\n\n"
                                + conversation
                            )
                        )


                        # If successful, stop trying models.

                        bot_reply = response.text

                        used_model = model

                        break


                    except Exception as model_error:

                        # Save the error and try the next model.

                        last_error = model_error


                # =================================================
                # CHECK RESPONSE
                # =================================================

                if bot_reply is None:

                    raise Exception(
                        "All compatible models failed.\n"
                        f"Last error: {last_error}"
                    )


                # =================================================
                # DISPLAY RESPONSE
                # =================================================

                st.markdown(bot_reply)


                # Show the model used in a small caption.

                st.caption(
                    f"🤖 Model used: {used_model}"
                )


                # =================================================
                # SAVE RESPONSE
                # =================================================

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": bot_reply
                    }
                )


            # =====================================================
            # ERROR HANDLING
            # =====================================================

            except Exception as error:

                st.error(
                    "❌ MY HeALPING BOT could not generate "
                    "a response.\n\n"
                    f"Error: {error}"
                )


# ============================================================
# 14. FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🤖 MY HeALPING BOT
        <br>
        Powered by Gemini • Built with Streamlit
    </div>
    """,
    unsafe_allow_html=True
)