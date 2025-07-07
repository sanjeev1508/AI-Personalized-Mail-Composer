import streamlit as st
from fetch_sent_emails import fetch_sent_emails
from style_extractor import load_email_samples, get_style_context
from prompt_generator import build_prompt
from nvidia_llm import generate_email
from smtp_sender import send_email_smtp

# --- Page Setup ---
st.set_page_config(page_title="Email Assistant", layout="centered")
st.title("PERSONALIZED EMAIL COMPOSER")
st.markdown("Generate personalized, professional emails based on your past writing style.")

# --- Session State Initialization ---
for key in [
    "chat_history", "authenticated", "recipient_name", "signature_name",
    "email_purpose", "extra_details", "generated_email", "step"
]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "chat_history" else []

# --- Login Phase ---
if not st.session_state.authenticated:
    st.markdown("### Login to Access Your Sent Email Style")
    email_input = st.text_input("Your Gmail Address")

    # Style block for inline tooltip icon
    st.markdown("""
    <style>
    .tooltip-icon {
        position: relative;
        display: inline-block;
        margin-left: 6px;
        color: crimson;
        font-weight: bold;
        cursor: pointer;
    }

    .tooltip-icon .tooltiptext {
        visibility: hidden;
        width: 240px;
        background-color: #555;
        color: #fff;
        text-align: left;
        border-radius: 6px;
        padding: 8px;
        position: absolute;
        z-index: 1;
        top: 100%;
        left: 50%;
        margin-left: -120px;
        opacity: 0;
        transition: opacity 0.3s;
    }

    .tooltip-icon .tooltiptext::after {
        content: "";
        position: absolute;
        top: 0;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: transparent transparent #555 transparent;
    }

    .tooltip-icon:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """, unsafe_allow_html=True)

    # Label with tooltip inline
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: -10px;">
        <label style="font-weight: 500; font-size: 14px;">Your App Password</label>
        <div class="tooltip-icon">❓
            <span class="tooltiptext">
                <b>How to get App Password:</b><br>
                1. Go to <a href='https://myaccount.google.com/' target='_blank' style='color:lightblue;'>Google Account</a><br>
                2. Search for "App Passwords"<br>
                3. Generate a name<br>
                4. Copy the password and paste it here
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    app_password_input = st.text_input(label="", type="password")

    if st.button("Fetch My Sent Emails"):
        if email_input and app_password_input:
            try:
                fetch_sent_emails(
                    user_email=email_input,
                    app_password=app_password_input,
                    output_path="data/sent_emails.json"
                )
                st.session_state.authenticated = True
                st.session_state.step = "recipient"
                st.success("Fetched sent emails successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to fetch emails: {e}")
        else:
            st.warning("Please enter both email and app password.")
    st.stop()


# --- Conversational Step Form ---
st.markdown("## Let's Draft Your Email")

if st.session_state.step == "recipient" or st.session_state.step is None:
    recipient = st.text_input("Who is the recipient (name)?")
    if st.button("Next", key="step1"):
        if recipient:
            st.session_state.recipient_name = recipient
            st.session_state.step = "signature"
            st.rerun()
        else:
            st.warning("Please enter the recipient name.")
    st.stop()

if st.session_state.step == "signature":
    sig = st.text_input("What's your full name for the signature?")
    if st.button("Next", key="step2"):
        if sig:
            st.session_state.signature_name = sig
            st.session_state.step = "purpose"
            st.rerun()
        else:
            st.warning("Please enter your signature name.")
    st.stop()

if st.session_state.step == "purpose":
    purpose = st.text_input("What’s the main purpose of this email? (one line)")
    if st.button("Next", key="step3"):
        if purpose:
            st.session_state.email_purpose = purpose
            st.session_state.step = "details"
            st.rerun()
        else:
            st.warning("Please enter the email purpose.")
    st.stop()

if st.session_state.step == "details":
    extra = st.text_area("Any extra details to include?", placeholder="(Optional)")
    if st.button("Generate Email"):
        st.session_state.extra_details = extra
        st.session_state.step = "done"
        st.rerun()

# --- Generate Final Email ---
if st.session_state.step == "done":
    emails = load_email_samples()
    style = get_style_context(emails)

    purpose_text = st.session_state.email_purpose
    if st.session_state.extra_details:
        purpose_text += f"\n\nAdditional context: {st.session_state.extra_details}"

    prompt = build_prompt(
        recipient=st.session_state.recipient_name,
        purpose=purpose_text,
        full_name=st.session_state.signature_name,
        email_samples=style["emails"],
        signature=style["signature"]
    )

    response = generate_email(prompt).strip()
    st.session_state.generated_email = response
    st.session_state.chat_history.append(("assistant", "Here’s your drafted email:"))
    st.session_state.step = "preview"
    st.rerun()

# --- Display Final Output ---
if st.session_state.step == "preview":
    st.markdown("### Draft Preview")
    st.markdown("---")
    st.markdown(st.session_state.generated_email.replace("\n", "  \n"))
    st.markdown("---")

    if st.checkbox("Edit Email"):
        edited = st.text_area("Edit your draft:", value=st.session_state.generated_email, height=300)
    else:
        edited = st.session_state.generated_email

    recipient_email = st.text_input("Recipient Email")
    subject = st.text_input("Email Subject")

    if st.button("Send Email"):
        if not recipient_email or not subject or not edited.strip():
            st.error("Please fill in all fields to send the email.")
        else:
            send_email_smtp(recipient_email, subject, edited)
            st.success("Email sent successfully!")
            st.session_state.generated_email = None
            st.session_state.step = None  # reset to allow new email
