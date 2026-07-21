import gradio as gr
import json
import os
import time

DB_FILE = "rates.json"

# Plaintext Credentials for exact matching
VALID_USER = "busalah"
VALID_PASS = "busalah2019"

def verify_credentials(username_input, password_input):
    if not username_input or not password_input:
        return False
    # Strip whitespace to prevent accidental spaces
    u = username_input.strip()
    p = password_input.strip()
    return u == VALID_USER and p == VALID_PASS

def load_live_rate():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                data = json.load(f)
                return float(data.get("usd_rate", 5500.0))
        except:
            pass
    return 5500.0

def update_usd_rate(new_rate):
    try:
        val = float(new_rate)
        if val <= 0:
            return "❌ Please enter a valid exchange rate greater than 0."
        
        data = {
            "usd_rate": val,
            "last_updated_ts": time.time()
        }
        with open(DB_FILE, "w") as f:
            json.dump(data, f)
            
        return f"✅ USD exchange rate updated successfully to {val:,.2f} SDG!"
    except ValueError:
        return "❌ Please enter a valid number for the exchange rate."

# Foggy Forest Background + iOS 26 Liquid Glass Styling
forest_glass_css = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

* {
    font-family: -apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', sans-serif !important;
    box-sizing: border-box;
}

/* Background */
body, .gradio-container {
    background: url('https://images.unsplash.com/photo-1542224566-6e85f2e6772f?q=80&w=2560') no-repeat center center fixed !important;
    background-size: cover !important;
    min-height: 100vh;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

footer, #api-link { display: none !important; }

/* Strip default Gradio wrappers and dark boxes completely */
.block, .form, fieldset, .gradio-box, .gap, div[data-testid="column"],
.input-container, .wrap, .container, [data-testid="textbox"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

.main-wrapper {
    width: 100%;
    max-width: 440px;
    margin: 0 auto;
    padding: 20px;
    display: flex;
    justify-content: center;
}

/* Glass Main Container Panel */
.glass-panel {
    background: rgba(25, 30, 20, 0.45) !important;
    backdrop-filter: blur(50px) saturate(200%) !important;
    -webkit-backdrop-filter: blur(50px) saturate(200%) !important;
    border: 1px solid rgba(255, 255, 255, 0.22) !important;
    border-radius: 36px !important;
    padding: 40px 32px !important;
    box-shadow: 0 30px 80px rgba(0, 0, 0, 0.6), 
                inset 0 1px 1px rgba(255, 255, 255, 0.35) !important;
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 18px;
}

.glass-header {
    text-align: center;
    margin-bottom: 6px;
}
.glass-icon {
    font-size: 46px;
    margin-bottom: 8px;
    filter: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.5));
}
.glass-title {
    font-size: 26px;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: -0.5px;
    margin: 0;
    text-shadow: 0 2px 10px rgba(0,0,0,0.5);
}
.glass-subtitle {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.65);
    margin-top: 4px;
}

/* Input Field Labels */
.glass-panel label {
    background: transparent !important;
    border: none !important;
    margin-bottom: 4px !important;
}

.glass-panel label span {
    color: rgba(255, 255, 255, 0.85) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

/* iOS 26 Liquid Glass Inputs */
.glass-panel input,
.glass-panel textarea,
.glass-panel .gr-input,
.glass-panel [data-testid="textbox"] textarea,
.glass-panel [data-testid="textbox"] input,
.glass-panel .input-container textarea,
.glass-panel .input-container input {
    background: rgba(255, 255, 255, 0.12) !important;
    backdrop-filter: blur(25px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(25px) saturate(180%) !important;
    border: 1px solid rgba(255, 255, 255, 0.28) !important;
    border-radius: 18px !important;
    color: #ffffff !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    padding: 14px 18px !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    box-shadow: inset 0 1.5px 1px rgba(255, 255, 255, 0.35),
                0 4px 15px rgba(0, 0, 0, 0.2) !important;
    width: 100% !important;
    outline: none !important;
    
    /* Remove slider / scrollbars & resize handles */
    resize: none !important;
    overflow: hidden !important;
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
}

.glass-panel textarea::-webkit-scrollbar,
.glass-panel input::-webkit-scrollbar {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
}

.glass-panel input::placeholder,
.glass-panel textarea::placeholder {
    color: rgba(255, 255, 255, 0.5) !important;
    font-weight: 400 !important;
}

.glass-panel input:hover,
.glass-panel textarea:hover {
    background: rgba(255, 255, 255, 0.18) !important;
    border-color: rgba(255, 255, 255, 0.4) !important;
}

.glass-panel input:focus,
.glass-panel textarea:focus {
    background: rgba(255, 255, 255, 0.22) !important;
    border-color: rgba(255, 255, 255, 0.7) !important;
    box-shadow: inset 0 1.5px 1px rgba(255, 255, 255, 0.6),
                0 0 20px rgba(255, 255, 255, 0.35),
                0 8px 25px rgba(0, 0, 0, 0.3) !important;
}

/* Pill-shaped Glass Button */
.glass-btn {
    background: rgba(255, 255, 255, 0.18) !important;
    backdrop-filter: blur(30px) saturate(200%) !important;
    -webkit-backdrop-filter: blur(30px) saturate(200%) !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    border-radius: 999px !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    padding: 14px !important;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), inset 0 1.5px 1.5px rgba(255, 255, 255, 0.6) !important;
    cursor: pointer;
    transition: all 0.25s ease !important;
    width: 100% !important;
    margin-top: 10px !important;
}

.glass-btn:hover {
    background: rgba(255, 255, 255, 0.28) !important;
    transform: translateY(-2px);
    box-shadow: 0 14px 30px rgba(0, 0, 0, 0.4), inset 0 2px 2px rgba(255, 255, 255, 0.8) !important;
}

.status-msg {
    text-align: center;
    font-size: 14px;
    font-weight: 700;
}
"""

with gr.Blocks(title="3AJIL Admin Panel") as admin_app:
    
    with gr.Column(elem_classes=["main-wrapper"]):
        
        # LOGIN VIEW
        with gr.Column(elem_classes=["glass-panel"], visible=True) as login_view:
            gr.HTML("""
            <div class="glass-header">
                <div class="glass-icon">🔒</div>
                <h1 class="glass-title">Sign In</h1>
                <p class="glass-subtitle">3AJIL Currency Rate Control Panel</p>
            </div>
            """)
            
            user_input = gr.Textbox(label="Username", placeholder="Enter your username", lines=1, max_lines=1, container=False)
            pass_input = gr.Textbox(label="Password", placeholder="••••••••", type="password", lines=1, max_lines=1, container=False)
            login_btn = gr.Button("▶ Access Panel", elem_classes=["glass-btn"])
            login_status = gr.HTML(elem_classes=["status-msg"])

        # ADMIN PANEL VIEW
        with gr.Column(elem_classes=["glass-panel"], visible=False) as admin_view:
            gr.HTML("""
            <div class="glass-header">
                <div class="glass-icon">🦊</div>
                <h1 class="glass-title">Control Panel</h1>
                <p class="glass-subtitle">Update live USD exchange rate instantly</p>
            </div>
            """)
            
            current_rate = load_live_rate()
            rate_input = gr.Number(label="Current USD Exchange Rate (SDG)", value=current_rate, precision=2, container=False)
            update_btn = gr.Button("▶ Push Live Update", elem_classes=["glass-btn"])
            update_status = gr.HTML(elem_classes=["status-msg"])

    def authenticate(u, p):
        if verify_credentials(u, p):
            return gr.update(visible=False), gr.update(visible=True), ""
        return gr.update(visible=True), gr.update(visible=False), "<span style='color: #ff8080;'>❌ Invalid username or password</span>"

    login_btn.click(
        fn=authenticate,
        inputs=[user_input, pass_input],
        outputs=[login_view, admin_view, login_status]
    )

    update_btn.click(
        fn=update_usd_rate,
        inputs=[rate_input],
        outputs=[update_status]
    )

if __name__ == "__main__":
    admin_app.launch(css=forest_glass_css, share=True)
