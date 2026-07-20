import gradio as gr
import json
import os
import time

DB_FILE = "rates.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({"usd_rate": 5500.0, "last_updated_ts": time.time()}, f)

def save_new_rates(usd_rate):
    data = {
        "usd_rate": float(usd_rate),
        "last_updated_ts": time.time() # Automatically tracks when the update happened
    }
    with open(DB_FILE, "w") as f:
        json.dump(data, f)
    return f"🟢 Price updated successfully!"

with gr.Blocks(title="3AJIL | Admin Panel") as admin:
    gr.Markdown("# 🦊 3AJIL Central Control Admin Panel")
    
    try:
        with open(DB_FILE, "r") as f:
            initial_data = json.load(f)
    except:
        initial_data = {"usd_rate": 5500.0}

    usd_input = gr.Number(value=initial_data.get("usd_rate", 5500.0), label="Set USD Base Rate (in SDG)")
    submit_btn = gr.Button("🚀 Push Changes Globally", variant="primary")
    status_output = gr.Textbox(label="System Status", interactive=False)
        
    submit_btn.click(fn=save_new_rates, inputs=[usd_input], outputs=[status_output])

if __name__ == "__main__":
    # Changed 'port' to 'server_port' to fix the TypeError
    admin.launch(server_port=7861)