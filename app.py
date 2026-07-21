import json
import os
import gradio as gr

# File path for rate data storage
DATA_FILE = "rates.json"

# Default rates fallback
DEFAULT_RATES = {
    "USD_BUY": "89.50",
    "USD_SELL": "90.00",
    "LAST_UPDATED": "Not set",
}


def load_rates():
  """Loads rates from rates.json or returns default values."""
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except Exception:
      return DEFAULT_RATES
  return DEFAULT_RATES


def save_rates(buy_rate, sell_rate, timestamp):
  """Saves updated rates to rates.json."""
  data = {
      "USD_BUY": str(buy_rate),
      "USD_SELL": str(sell_rate),
      "LAST_UPDATED": str(timestamp),
  }
  try:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
      json.dump(data, f, ensure_ascii=False, indent=2)
    return "✅ Rates updated successfully!"
  except Exception as e:
    return f"❌ Error saving rates: {str(e)}"


def authenticate(username, password):
  """Validates administrator login credentials."""
  if username == "busalah" and password == "busalah2019":
    return True, "Login successful!"
  return False, "Invalid username or password."


# Custom CSS styling (Liquid Glass / Foggy Forest Theme)
custom_css = """
body, .gradio-container {
    background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                url('https://images.unsplash.com/photo-1448375240586-882707db888b?q=80&w=1920&auto=format&fit=crop') no-repeat center center fixed;
    background-size: cover;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.glass-panel {
    background: rgba(255, 255, 255, 0.15) !important;
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 20px !important;
    padding: 25px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

.title-header h1 {
    color: #ffffff !important;
    text-align: center;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    text-shadow: 0 2px 10px rgba(0,0,0,0.5);
}
"""

# Build Interface without passing css inside gr.Blocks (Fixes Gradio 6 warning)
with gr.Blocks(title="3AJIL | عاجل") as demo:

  with gr.Row(elem_classes=["title-header"]):
    gr.Markdown("# 3AJIL | عاجل - Control Panel")

  # Login Section
  with gr.Group(elem_classes=["glass-panel"]):
    gr.Markdown("### 🔐 Admin Authentication")
    user_input = gr.Textbox(
        label="Username", placeholder="Enter admin username"
    )
    pass_input = gr.Textbox(
        label="Password", type="password", placeholder="Enter password"
    )
    login_btn = gr.Button("Login", variant="primary")
    auth_output = gr.Textbox(label="Status", interactive=False)

  # Control Panel Section (Hidden until logged in)
  with gr.Group(visible=False, elem_classes=["glass-panel"]) as admin_panel:
    gr.Markdown("### 💵 Update USD Exchange Rates")

    current_data = load_rates()

    buy_input = gr.Textbox(
        label="USD Buy Rate", value=current_data.get("USD_BUY", "")
    )
    sell_input = gr.Textbox(
        label="USD Sell Rate", value=current_data.get("USD_SELL", "")
    )
    time_input = gr.Textbox(
        label="Timestamp / Note",
        placeholder="e.g. Updated July 2026 at 10:00 AM",
    )

    update_btn = gr.Button("Save New Rates", variant="primary")
    save_output = gr.Textbox(label="Result", interactive=False)

  # Handlers
  def handle_login(u, p):
    is_valid, msg = authenticate(u, p)
    if is_valid:
      return gr.update(value=msg), gr.update(visible=True)
    return gr.update(value=msg), gr.update(visible=False)

  login_btn.click(
      fn=handle_login,
      inputs=[user_input, pass_input],
      outputs=[auth_output, admin_panel],
  )

  update_btn.click(
      fn=save_rates,
      inputs=[buy_input, sell_input, time_input],
      outputs=[save_output],
  )


# Server Execution for Railway Deployment
if __name__ == "__main__":
  # Retrieve the dynamic environment PORT provided by Railway
  port = int(os.environ.get("PORT", 7860))

  # Pass custom_css inside launch() to fix Gradio 6 deprecation
  demo.launch(server_name="0.0.0.0", server_port=port, css=custom_css)
