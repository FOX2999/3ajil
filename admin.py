import gradio as gr
import json
import os
import time

DB_FILE = "rates.json"

FLAGS_SVG = {
    "SDG": '''<svg class="currency-flag" viewBox="0 0 512 512"><path fill="#007229" d="M0 0h170.7v512H0z"/><path fill="#fff" d="M170.7 0H512v170.7H170.7z"/><path fill="#c60c30" d="M170.7 170.7H512v170.6H170.7z"/><path fill="#000" d="M170.7 341.3H512V512H170.7z"/></svg>''',
    "US": '''<svg class="currency-flag" viewBox="0 0 512 512"><path fill="#bd3d44" d="M0 0h512v512H0z"/><path fill="#fff" d="M0 39.3h512v39.4H0zm0 78.8h512v39.4H0zm0 78.8h512v39.4H0zm0 78.8h512v39.4H0zm0 78.8h512v39.4H0zm0 78.8h512v39.4H0z"/><path fill="#192f5d" d="M0 0h256v275.7H0z"/></svg>''',
    "EUR": '''<svg class="currency-flag" viewBox="0 0 512 512"><path fill="#003399" d="M0 0h512v512H0z"/><g fill="#ffcc00"><polygon points="256,75 261,90 276,90 264,99 268,114 256,105 244,114 248,99 236,90 251,90"/><polygon points="256,397 261,412 276,412 264,421 268,436 256,427 244,436 248,421 236,412 251,412"/><polygon points="95,236 100,251 115,251 103,260 107,275 95,266 83,275 87,260 75,251 90,251"/><polygon points="417,236 422,251 437,251 425,260 429,275 417,266 405,275 409,260 397,251 412,251"/><polygon points="138,118 143,133 158,133 146,142 150,157 138,148 126,157 130,142 118,133 133,133"/><polygon points="374,354 379,369 394,369 382,378 386,393 374,384 362,393 366,378 354,369 369,369"/><polygon points="374,118 379,133 394,133 382,142 386,157 374,148 362,157 366,142 354,133 369,133"/><polygon points="138,354 143,369 158,369 146,378 150,393 138,384 126,393 130,378 118,369 133,369"/></g></svg>''',
    "EGP": '''<svg class="currency-flag" viewBox="0 0 512 512"><path fill="#e11c24" d="M0 0h512v170.7H0z"/><path fill="#fff" d="M0 170.7h512v170.6H0z"/><path fill="#000" d="M0 341.3h512V512H0z"/><path fill="#c0932c" d="M230 220h52v70h-52z"/></svg>''',
    "SAR": '''<svg class="currency-flag" viewBox="0 0 512 512"><path fill="#007a3d" d="M0 0h512v512H0z"/><path fill="#fff" d="M120 330l10-10h210v10H140l-20 20v-20zM140 220h230v80H140z"/><path fill="#007a3d" d="M150 230h210v60H150z"/><path fill="#fff" d="M160 240h20v40h-20zm40 0h20v40h-20zm40 0h20v40h-20zm40 0h20v40h-20zm40 0h20v40h-20z"/></svg>''',
    "QAR": '''<svg class="currency-flag" viewBox="0 0 512 512"><path fill="#8a1538" d="M0 0h512v512H0z"/><path fill="#fff" d="M0 0h140l60 28.4-60 28.5 60 28.4-60 28.5 60 28.4-60 28.5 60 28.4-60 28.5 60 28.4-60 28.5 60 28.4-60 28.5 60 28.4-60 28.5 60 28.4-60 28.5V512H0z"/></svg>''',
    "OMR": '''<svg class="currency-flag" viewBox="0 0 512 512"><path fill="#fff" d="M0 0h512v170.7H0z"/><path fill="#db161b" d="M0 170.7h512v170.6H0z"/><path fill="#008000" d="M0 341.3h512V512H0z"/><path fill="#db161b" d="M0 0h170.7v512H0z"/></svg>''',
    "AED": '''<svg class="currency-flag" viewBox="0 0 512 512"><path fill="#00732f" d="M0 0h512v170.7H0z"/><path fill="#fff" d="M0 170.7h512v170.6H0z"/><path fill="#000" d="M0 341.3h512V512H0z"/><path fill="#f00" d="M0 0h150v512H0z"/></svg>''',
    "MAD": '''<svg class="currency-flag" viewBox="0 0 512 512"><path fill="#c1272d" d="M0 0h512v512H0z"/><path fill="none" stroke="#006233" stroke-width="15" d="M256 180l25 77h81l-66 48 25 77-65-48-65 48 25-77-66-48h81z"/></svg>''',
    "KWD": '''<svg class="currency-flag" viewBox="0 0 512 512"><path fill="#007a3d" d="M0 0h512v170.7H0z"/><path fill="#fff" d="M0 170.7h512v170.6H0z"/><path fill="#ce1126" d="M0 341.3h512V512H0z"/><polygon fill="#000" points="0,0 170.7,170.7 170.7,341.3 0,512"/></svg>'''
}

CROSS_RATES = {"EUR": 0.92, "EGP": 48.5, "SAR": 3.75, "QAR": 3.64, "OMR": 0.385, "AED": 3.67, "MAD": 9.80, "KWD": 0.31}
CURRENCY_INFO = {
    "EUR": {"name_ar": "يورو أوروبي", "name_en": "Euro", "flag_key": "EUR", "change": "-0.1%", "is_up": False},
    "EGP": {"name_ar": "جنيه مصري", "name_en": "Egyptian Pound", "flag_key": "EGP", "change": "+1.2%", "is_up": True},
    "SAR": {"name_ar": "ريال سعودي", "name_en": "Saudi Riyal", "flag_key": "SAR", "change": "-0.0%", "is_up": False},
    "QAR": {"name_ar": "ريال قطري", "name_en": "Qatari Riyal", "flag_key": "QAR", "change": "+0.3%", "is_up": True},
    "OMR": {"name_ar": "ريال عماني", "name_en": "Omani Rial", "flag_key": "OMR", "change": "-0.2%", "is_up": False},
    "AED": {"name_ar": "درهم إماراتي", "name_en": "UAE Dirham", "flag_key": "AED", "change": "+0.0%", "is_up": True},
    "MAD": {"name_ar": "درهم مغربي", "name_en": "Moroccan Dirham", "flag_key": "MAD", "change": "+0.5%", "is_up": True},
    "KWD": {"name_ar": "دينار كويتي", "name_en": "Kuwaiti Dinar", "flag_key": "KWD", "change": "-0.1%", "is_up": False},
}

SPARKLINE_GREEN = '<svg class="sparkline" viewBox="0 0 100 30"><path d="M0,20 Q15,5 30,22 T60,10 T90,18 L100,8" fill="none" stroke="#22c55e" stroke-width="2.5"/></svg>'
SPARKLINE_RED = '<svg class="sparkline" viewBox="0 0 100 30"><path d="M0,10 Q20,25 40,12 T70,22 L100,15" fill="none" stroke="#ef4444" stroke-width="2.5"/></svg>'

def load_live_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"usd_rate": 5500.0, "last_updated_ts": time.time()}

def get_relative_time_string(timestamp, lang="ar"):
    diff = time.time() - timestamp
    if diff < 60:
        return "تم التحديث الأن" if lang == "ar" else "Updated Now"
    
    minutes = int(diff // 60)
    if minutes < 60:
        if lang == "ar":
            return f"منذ {minutes} دقيقة" if minutes > 2 else "منذ دقيقة"
        return f"Updated {minutes}m ago"
        
    hours = int(minutes // 60)
    if hours < 24:
        if lang == "ar":
            return f"منذ {hours} ساعة" if hours > 2 else "منذ ساعة"
        return f"Updated {hours}h ago"
        
    days = int(hours // 24)
    if lang == "ar":
        return f"منذ {days} يوم" if days > 2 else "منذ يوم"
    return f"Updated {days}d ago"

def calculate_currency_cards(lang="ar"):
    live_data = load_live_data()
    usd_sdg_value = live_data["usd_rate"]
    
    unit = "ج.س" if lang == "ar" else "SDG"
    cards_html = '<div class="rates-grid">'
    
    for code, info in CURRENCY_INFO.items():
        rate_in_sdg = float(usd_sdg_value) / CROSS_RATES[code]
        flag_svg = FLAGS_SVG.get(info['flag_key'], '')
        sparkline = SPARKLINE_GREEN if info['is_up'] else SPARKLINE_RED
        change_class = "green-text" if info['is_up'] else "red-text"
        curr_name = info['name_ar'] if lang == "ar" else info['name_en']
        
        cards_html += f"""
        <div class="rate-card">
            <div class="card-left">
                <div class="flag-container">{flag_svg}</div>
                <div class="symbol-info">
                    <span class="symbol-code">{code}</span>
                    <span class="symbol-name">{curr_name}</span>
                </div>
            </div>
            <div class="card-center">{sparkline}</div>
            <div class="card-right">
                <span class="change-tag {change_class}">{info['change']}</span>
                <span class="price-val">{rate_in_sdg:,.1f} <small>{unit}</small></span>
            </div>
        </div>
        """
    cards_html += '</div>'
    return cards_html

def get_main_usd_card(lang="ar"):
    live_data = load_live_data()
    usd_sdg_value = live_data["usd_rate"]
    ts = live_data.get("last_updated_ts", time.time())
    notification_msg = get_relative_time_string(ts, lang)
    
    title = "سعر الدولار اليوم مقابل الجنيه السوداني" if lang == "ar" else "USD Exchange Rate vs SDG Today"
    unit = "ج.س" if lang == "ar" else "SDG"
    copy_tooltip = "تم النسخ!" if lang == "ar" else "Copied!"
    
    try:
        val_float = float(usd_sdg_value)
        int_part = f"{int(val_float):,}"
        dec_part = f".{int(round((val_float - int(val_float)) * 100)):02d}"
    except:
        int_part = str(usd_sdg_value)
        dec_part = ".00"

    return f"""
    <div class="datetime-bar">
        <div class="live-indicator"><span class="pulse-dot"></span><span class="live-label">{notification_msg}</span></div>
        <div class="datetime-values"><span id="realtime-date">---</span> • <span id="realtime-clock">--:--:--</span></div>
    </div>
    <div class="asset-section">
        <div class="asset-header-row">
            <div class="asset-title-row">
                <div class="main-flag-container">{FLAGS_SVG['US']}</div>
                <span class="asset-title">{title}</span>
            </div>
            <button class="copy-btn" onclick="window.copyAmount(this, '{val_float:.2f}')">
                <svg viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
                <span class="copy-tooltip">{copy_tooltip}</span>
            </button>
        </div>
        <div class="asset-amount-wrapper">
            <span class="asset-amount">{int_part}<span class="cents">{dec_part}</span></span>
            <span class="currency-symbol">{unit}</span>
        </div>
        <div class="growth-badge">▲ Realtime Stream</div>
    </div>
    """

def get_header_html(lang="ar"):
    lang_title = "تغيير اللغة" if lang == "ar" else "Change Language"
    theme_title = "الوضع المظلم/المضيء" if lang == "ar" else "Dark/Light Mode"
    return f"""
    <div class="top-header">
        <div class="brand-wrapper"><span class="fox-emoji">🦊</span><span class="brand-title">3AJIL</span></div>
        <div class="header-actions">
            <button class="header-btn px-btn" onclick="document.getElementById('lang_trigger_btn').click();" title="{lang_title}">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="2" y1="12" x2="22" y2="12"></line>
                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10z"></path>
                </svg>
            </button>
            <button class="header-btn px-btn" onclick="window.toggleTheme();" title="{theme_title}">
                <svg class="sun-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="5"></circle>
                    <line x1="12" y1="1" x2="12" y2="3"></line>
                    <line x1="12" y1="21" x2="12" y2="23"></line>
                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                    <line x1="1" y1="12" x2="3" y2="12"></line>
                    <line x1="21" y1="12" x2="23" y2="12"></line>
                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                </svg>
            </button>
        </div>
    </div>
    """

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Tajawal:wght@500;700;900&display=swap');
* { font-family: 'Tajawal', 'Plus Jakarta Sans', sans-serif !important; box-sizing: border-box; }

:root {
    --bg-main: #0c0809 url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2560') no-repeat center/cover fixed;
    --bg-wrapper: rgba(26, 11, 14, 0.45);
    --bg-card: rgba(255, 255, 255, 0.04);
    --bg-asset: rgba(239, 68, 68, 0.06);
    --border-color: rgba(255, 255, 255, 0.08);
    --border-hover: rgba(255, 255, 255, 0.18);
    --text-primary: #ffffff;
    --text-muted: rgba(255, 255, 255, 0.55);
    --icon-bg: rgba(255, 255, 255, 0.06);
    --icon-hover: rgba(255, 255, 255, 0.15);
}

.light-mode, body.light-mode {
    --bg-main: #f0f2f5 url('https://images.unsplash.com/photo-1634017839464-5c339ebe3cb4?q=80&w=2560') no-repeat center/cover fixed !important;
    --bg-wrapper: rgba(255, 255, 255, 0.4);
    --bg-card: rgba(255, 255, 255, 0.5);
    --bg-asset: rgba(255, 228, 230, 0.45);
    --border-color: rgba(0, 0, 0, 0.06);
    --border-hover: rgba(0, 0, 0, 0.12);
    --text-primary: #1c1c1e;
    --text-muted: rgba(0, 0, 0, 0.5);
    --icon-bg: rgba(0, 0, 0, 0.05);
    --icon-hover: rgba(0, 0, 0, 0.1);
}

body.light-mode .datetime-bar, body.light-mode .datetime-values { color: #000000 !important; }
body, .gradio-container { background: var(--bg-main) !important; margin: 0 !important; min-height: 100vh; }
footer, #api-link { display: none !important; }

.app-wrapper {
    max-width: 1000px; margin: 40px auto; padding: 30px;
    background: var(--bg-wrapper) !important; backdrop-filter: blur(30px) saturate(190%);
    border: 1px solid var(--border-color); border-radius: 32px;
}

.top-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 25px; border-bottom: 1px solid var(--border-color); padding-bottom: 20px; }
.brand-wrapper { display: flex; align-items: center; gap: 14px; }
.fox-emoji { font-size: 38px; }
.brand-title { font-size: 32px; font-weight: 900; color: #ef4444; letter-spacing: -0.5px; }
.header-actions { display: flex; gap: 16px; align-items: center; }

.header-btn.px-btn { 
    background: var(--icon-bg); 
    border: 1px solid var(--border-color); 
    border-radius: 14px; 
    width: 48px; 
    height: 48px; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    cursor: pointer; 
    color: var(--text-primary); 
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); 
}
.header-btn.px-btn:hover { background: var(--icon-hover); border-color: var(--border-hover); transform: translateY(-2px); }
.header-btn.px-btn svg { width: 24px; height: 24px; stroke-width: 2.2px; }
.hidden-trigger { display: none !important; }

.datetime-bar { display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 13px; font-weight: 700; color: var(--text-muted); }
.live-indicator { display: flex; align-items: center; gap: 6px; color: #22c55e; }
.pulse-dot { width: 8px; height: 8px; background: #22c55e; border-radius: 50%; animation: pulse 1.6s infinite; }
@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(34,197,94,0.7); } 70% { box-shadow: 0 0 0 6px rgba(34,197,94,0); } }
.datetime-values { direction: ltr; }

.asset-section { background: var(--bg-asset) !important; border: 1px solid var(--border-color); border-radius: 24px; padding: 24px; margin-bottom: 30px; position: relative; }
.asset-header-row { display: flex; justify-content: space-between; }
.asset-title-row { display: flex; align-items: center; gap: 10px; color: var(--text-muted); font-size: 15px; font-weight: 600; }
.main-flag-container { width: 28px; height: 28px; border-radius: 50%; overflow: hidden; }
.copy-btn { background: var(--icon-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 8px 12px; cursor: pointer; position: relative; }
.copy-btn svg { width: 18px; height: 18px; fill: var(--text-muted); }
.copy-tooltip { position: absolute; top: -30px; left: 50%; transform: translateX(-50%); background: #ef4444; color: white; font-size: 11px; padding: 3px 8px; border-radius: 6px; opacity: 0; pointer-events: none; transition: opacity 0.2s; }
.copy-btn.copied .copy-tooltip { opacity: 1; }
.asset-amount-wrapper { display: flex; align-items: baseline; gap: 10px; margin-top: 10px; }
.asset-amount { font-size: 48px; font-weight: 900; color: var(--text-primary); direction: ltr; }
.asset-amount .cents { font-size: 28px; color: var(--text-muted); }
.currency-symbol { font-size: 24px; font-weight: 700; color: var(--text-primary); }
.growth-badge { display: inline-flex; background: rgba(34, 197, 94, 0.2); color: #22c55e; font-weight: 800; font-size: 13px; padding: 6px 14px; border-radius: 20px; margin-top: 15px; }

.rates-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.rate-card { background: var(--bg-card) !important; border: 1px solid var(--border-color); border-radius: 22px; padding: 18px 16px; display: flex; align-items: center; justify-content: space-between; transition: transform 0.2s; }
.rate-card:hover { transform: translateY(-4px); border-color: var(--border-hover); }
.card-left { display: flex; align-items: center; gap: 12px; }
.flag-container { width: 38px; height: 38px; border-radius: 50%; overflow: hidden; }
.currency-flag { width: 100%; height: 100%; object-fit: cover; }
.symbol-info { display: flex; flex-direction: column; }
.symbol-code { font-size: 16px; font-weight: 800; color: var(--text-primary); }
.symbol-name { font-size: 11px; color: var(--text-muted); }
.sparkline { width: 60px; height: 25px; }
.card-right { display: flex; flex-direction: column; align-items: flex-end; }
.change-tag { font-size: 12px; font-weight: 700; }
.green-text { color: #22c55e; }
.red-text { color: #ef4444; }
.price-val { font-size: 16px; font-weight: 800; color: var(--text-primary); direction: ltr; }

.rtl-layout { direction: rtl; }
.ltr-layout { direction: ltr; }

/* 📱 SMARTPHONE & IPHONE MAX ULTRA RESPONSIVE DESIGN */
@media (max-width: 768px) {
    .app-wrapper { margin: 12px auto; padding: 18px; border-radius: 24px; width: 95% !important; }
    .brand-title { font-size: 26px; }
    .fox-emoji { font-size: 30px; }
    .header-btn.px-btn { width: 42px; height: 42px; border-radius: 11px; }
    .header-btn.px-btn svg { width: 20px; height: 20px; }
    
    .datetime-bar { flex-direction: column; gap: 4px; font-size: 11px; align-items: flex-start; }
    .rtl-layout .datetime-bar { align-items: flex-start; }
    
    .asset-section { padding: 18px; border-radius: 18px; }
    .asset-amount { font-size: 36px; }
    .asset-amount .cents { font-size: 20px; }
    .currency-symbol { font-size: 18px; }
    .asset-title { font-size: 13px; }
    
    .rates-grid { grid-template-columns: 1fr; gap: 12px; }
    .rate-card { padding: 14px 12px; border-radius: 16px; }
    .symbol-code { font-size: 15px; }
    .price-val { font-size: 15px; }
    .sparkline { width: 50px; }
}
"""

custom_js = """
function() {
    window.copyAmount = function(btn, text) {
        navigator.clipboard.writeText(text);
        btn.classList.add('copied');
        setTimeout(() => btn.classList.remove('copied'), 1800);
    };

    window.toggleTheme = function() {
        document.body.classList.toggle('light-mode');
        document.querySelectorAll('.app-wrapper').forEach(el => el.classList.toggle('light-mode'));
    };

    function updateLiveDateTime() {
        const liveLabelEl = document.querySelector('.live-label');
        const contentStr = liveLabelEl ? liveLabelEl.innerText.trim() : '';
        const isEnglish = (contentStr === 'Updated Now' || contentStr.startsWith('Updated'));
        const langCode = isEnglish ? 'en-US' : 'ar-EG';
        
        const now = new Date();
        const dateStr = now.toLocaleDateString(langCode, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
        const timeStr = now.toLocaleTimeString(langCode);
        
        const dateEl = document.getElementById('realtime-date');
        const clockEl = document.getElementById('realtime-clock');
        if (dateEl) dateEl.innerText = dateStr;
        if (clockEl) clockEl.innerText = timeStr;
    }

    if(window.liveTimer) clearInterval(window.liveTimer);
    window.liveTimer = setInterval(updateLiveDateTime, 1000);
    setTimeout(updateLiveDateTime, 400);

    document.getElementById('lang_trigger_btn').addEventListener('click', () => {
        setTimeout(updateLiveDateTime, 250); 
    });
}
"""

with gr.Blocks(title="3AJIL | عاجل", css=custom_css) as demo:
    lang_state = gr.State("ar")
    lang_trigger = gr.Button(elem_id="lang_trigger_btn", elem_classes=["hidden-trigger"])

    with gr.Column(elem_classes=["app-wrapper", "rtl-layout"]) as main_wrapper:
        header_widget = gr.HTML(get_header_html("ar"))
        main_usd_card = gr.HTML(get_main_usd_card("ar"))
        currency_grid_output = gr.HTML(calculate_currency_cards("ar"))

    def toggle_language(current_lang):
        new_lang = "en" if current_lang == "ar" else "ar"
        new_direction_class = "ltr-layout" if new_lang == "en" else "rtl-layout"
        
        return (
            new_lang,
            get_header_html(new_lang),
            get_main_usd_card(new_lang),
            calculate_currency_cards(new_lang),
            gr.update(elem_classes=["app-wrapper", new_direction_class])
        )

    lang_trigger.click(
        fn=toggle_language,
        inputs=[lang_state],
        outputs=[lang_state, header_widget, main_usd_card, currency_grid_output, main_wrapper]
    )

    refresh_component = gr.Timer(value=4.0)
    
    def auto_refresh_from_file(current_lang):
        return [get_main_usd_card(current_lang), calculate_currency_cards(current_lang)]
        
    refresh_component.tick(
        fn=auto_refresh_from_file,
        inputs=[lang_state],
        outputs=[main_usd_card, currency_grid_output]
    )

    demo.load(None, None, None, js=custom_js)

if __name__ == "__main__":
    demo.launch(css=forest_glass_css, share=True)
