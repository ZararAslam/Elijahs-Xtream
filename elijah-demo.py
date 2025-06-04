import streamlit as st
import openai
import time
import markdown2
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Elijah's Xtream AI",
    page_icon="🌶️",
    layout="wide"
)

# Configure OpenAI
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    ASSISTANT_ID = st.secrets.get("ASSISTANT_ID", "asst_C3Mipy0XBrRiE3Bjoj3RjCoO")
except Exception as e:
    st.error("Please configure OPENAI_API_KEY in your Streamlit secrets.")
    st.stop()

# Enhanced WhatsApp-style CSS
st.markdown("""
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Full height layout */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: none;
        height: 100vh;
        display: flex;
        flex-direction: column;
    }
    
    /* Chat container styling */
    .chat-container {
        flex: 1;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        max-width: 800px;
        margin: 0 auto;
        width: 100%;
    }
    
    /* Chat messages area */
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
        margin-bottom: 0;
    }
    
    /* Input container fixed at bottom */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-top: 1px solid #e0e0e0;
        padding: 15px 20px;
        z-index: 1000;
        max-width: 800px;
        margin: 0 auto;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    }
    
    /* Message bubbles */
    .message-container {
        margin: 10px 0;
        display: flex;
        align-items: flex-end;
        clear: both;
    }
    
    .user-container {
        justify-content: flex-end;
        float: right;
        width: 100%;
    }
    
    .bot-container {
        justify-content: flex-start;
        float: left;
        width: 100%;
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #DCF8C6, #C8E6C9);
        color: #2E7D32;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        max-width: 70%;
        word-wrap: break-word;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        font-size: 14px;
        line-height: 1.4;
        display: inline-block;
        text-align: left;
    }
    
    .bot-bubble {
        background: linear-gradient(135deg, #FFFFFF, #F5F5F5);
        color: #333333;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        max-width: 70%;
        word-wrap: break-word;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        font-size: 14px;
        line-height: 1.4;
        border: 1px solid #E0E0E0;
        display: inline-block;
        text-align: left;
    }
    
    /* Markdown styling within bot bubbles */
    .bot-bubble h1, .bot-bubble h2, .bot-bubble h3 {
        margin-top: 8px;
        margin-bottom: 8px;
        color: #1976D2;
    }
    
    .bot-bubble p {
        margin: 4px 0;
    }
    
    .bot-bubble ul, .bot-bubble ol {
        margin: 8px 0;
        padding-left: 20px;
    }
    
    .bot-bubble code {
        background-color: #F0F0F0;
        padding: 2px 4px;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        font-size: 13px;
    }
    
    .bot-bubble pre {
        background-color: #F8F8F8;
        padding: 8px;
        border-radius: 6px;
        border-left: 4px solid #1976D2;
        overflow-x: auto;
        margin: 8px 0;
    }
    
    /* Timestamp styling */
    .timestamp {
        font-size: 11px;
        color: #666;
        margin: 2px 8px;
        opacity: 0.7;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #E0E0E0;
        padding: 12px 20px;
        font-size: 14px;
        background-color: #FAFAFA;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #25D366;
        box-shadow: 0 0 0 0.2rem rgba(37, 211, 102, 0.25);
    }
    
    /* Spinner styling */
    .stSpinner > div {
        text-align: center;
        color: #25D366;
    }
    
    /* Demo notice styling */
    .demo-notice {
        background: linear-gradient(135deg, #FFF9C4, #F0F4C3);
        border: 1px solid #C5CAE9;
        border-radius: 12px;
        padding: 16px;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .demo-notice strong {
        color: #F57F17;
    }
    
    /* Typing indicator */
    .typing-indicator {
        margin: 10px 0;
        display: flex;
        justify-content: flex-start;
        clear: both;
    }
    
    .typing-bubble {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 18px 18px 18px 4px;
        padding: 12px 16px;
        color: #666;
        font-style: italic;
        animation: pulse 1.5s ease-in-out infinite;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        max-width: 200px;
    }
    
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    /* Remove old scrollable chat area styles */
    
    /* Custom scrollbar */
    .chat-messages::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: #C0C0C0;
        border-radius: 10px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: #A0A0A0;
    }
    
    /* Add padding bottom to make room for fixed input */
    body {
        padding-bottom: 100px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "thread_id" not in st.session_state:
    try:
        thread = openai.beta.threads.create()
        st.session_state.thread_id = thread.id
        st.session_state.messages = []
        st.session_state.is_processing = False
    except Exception as e:
        st.error(f"Failed to create OpenAI thread: {str(e)}")
        st.stop()

# Function to get assistant response
def get_assistant_response(user_message):
    try:
        # Add user message to thread
        openai.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=user_message
        )
        
        # Create and run the assistant
        run = openai.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=ASSISTANT_ID
        )
        
        # Wait for completion with timeout
        timeout = 60  # 60 seconds timeout
        start_time = time.time()
        
        while True:
            if time.time() - start_time > timeout:
                raise Exception("Request timed out")
                
            status = openai.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
            
            if status.status == "completed":
                break
            elif status.status == "failed":
                raise Exception("Assistant run failed")
            elif status.status == "expired":
                raise Exception("Assistant run expired")
                
            time.sleep(1)
        
        # Get the latest message
        messages = openai.beta.threads.messages.list(
            thread_id=st.session_state.thread_id,
            limit=1
        )
        
        if messages.data:
            return messages.data[0].content[0].text.value
        else:
            raise Exception("No response received")
            
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Function to send message
def send_message():
    user_input = st.session_state.user_input.strip()
    if not user_input or st.session_state.is_processing:
        return
    
    # Add user message to chat immediately
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user", 
        "content": user_input,
        "timestamp": timestamp
    })
    
    # Clear input and set processing state
    st.session_state.user_input = ""
    st.session_state.is_processing = True
    
    # Force rerun to show user message immediately
    st.rerun()

# Function to get assistant response (called separately)
def process_assistant_response():
    if st.session_state.is_processing and len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        user_message = st.session_state.messages[-1]["content"]
        
        # Get assistant response
        assistant_response = get_assistant_response(user_message)
        
        # Add assistant response to chat
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "assistant", 
            "content": assistant_response,
            "timestamp": timestamp
        })
        
        # Reset processing state
        st.session_state.is_processing = False
        st.rerun()

# Main chat interface
st.title("🌶️ Elijah's Xtream AI")

# Process assistant response if needed
if st.session_state.is_processing:
    process_assistant_response()

# Chat messages container
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    # Display chat history
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f"""
                <div class="message-container user-container">
                    <div>
                        <div class="user-bubble">{msg['content']}</div>
                        <div class="timestamp" style="text-align: right;">{msg.get('timestamp', '')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Convert markdown to HTML for assistant messages
            try:
                html_content = markdown2.markdown(
                    msg['content'], 
                    extras=['fenced-code-blocks', 'tables', 'code-friendly']
                )
            except:
                html_content = msg['content']
            
            st.markdown(f"""
                <div class="message-container bot-container">
                    <div>
                        <div class="bot-bubble">{html_content}</div>
                        <div class="timestamp">{msg.get('timestamp', '')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Show typing indicator when processing
    if st.session_state.is_processing:
        st.markdown("""
            <div class="typing-indicator">
                <div class="typing-bubble">
                    Assistant is typing...
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Input section - Fixed at bottom
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Create columns for better input layout
col1, col2 = st.columns([6, 1])

with col1:
    st.text_input(
        label="Message",
        placeholder="Type your message here..." + (" (Processing...)" if st.session_state.is_processing else ""),
        key="user_input",
        on_change=send_message,
        label_visibility="collapsed",
        disabled=st.session_state.is_processing
    )

with col2:
    if st.button("📤", help="Send message", disabled=st.session_state.is_processing):
        send_message()

st.markdown('</div>', unsafe_allow_html=True)

# Demo notice
st.markdown("""
<div class="demo-notice">
    <strong>📝 Note:</strong> This is a demo of Elijah's Xtream Customer Support AI backend capabilities. 
    The final frontend will have a more polished design. For specific product information or custom features, 
    please contact us at <strong>hello@altorix.co.uk</strong>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 30px; color: #666; font-size: 12px;">
    Powered by OpenAI Assistants API | Built with Streamlit
</div>
""", unsafe_allow_html=True)

# Auto-scroll to bottom when new messages are added
if st.session_state.messages:
    st.markdown("""
        <script>
        function scrollToBottom() {
            window.scrollTo(0, document.body.scrollHeight);
        }
        
        // Scroll immediately
        scrollToBottom();
        
        // Also scroll after a short delay to handle dynamic content
        setTimeout(scrollToBottom, 100);
        setTimeout(scrollToBottom, 300);
        </script>
    """, unsafe_allow_html=True)
