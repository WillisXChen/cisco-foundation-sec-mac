document.addEventListener("DOMContentLoaded", () => {
    console.log("🛡️ Cisco Sec 8B: UI Loaded with 8 Languages (v8)");
    // Hide HUD by default on load
    document.body.classList.add("hud-is-hidden");

    const urlParams = new URLSearchParams(window.location.search);
    const lang = urlParams.get('lang') || 'en-US';

    fetch(`/api/translations?lang=${lang}`)
        .then(response => response.json())
        .then(translations => {
            const textHistory = translations["History"] || "History";
            const textPerfMon = translations["PerfMon"] || "PerfMon";

            const createToggleButton = () => {
                if (document.getElementById("hud-toggle-btn")) return;
                if (document.getElementById("history-btn")) return;

                const btn = document.createElement("button");
                btn.id = "hud-toggle-btn";
                btn.innerHTML = `
                    <div style="display: flex; align-items: center; justify-content: center; gap: 8px; flex-wrap: nowrap; white-space: nowrap;">
                        <img src="/public/png/performance.png" width="28" height="28" style="vertical-align: middle; position: relative; top: -1px;" alt="icon">
                        <span style="vertical-align: middle; line-height: 1;">${textPerfMon}</span>
                    </div>
                `;

                Object.assign(btn.style, {
                    position: "fixed",
                    bottom: "20px",
                    right: "20px",
                    zIndex: "10000",
                    padding: "10px 20px",
                    borderRadius: "50px",
                    background: "linear-gradient(135deg, rgba(0, 85, 119, 0.9) 0%, rgba(0, 119, 153, 0.9) 100%)",
                    border: "1px solid rgba(0, 255, 255, 0.4)",
                    color: "#00ffff",
                    boxShadow: "0 0 12px rgba(0, 255, 255, 0.18)",
                    cursor: "pointer",
                    fontWeight: "bold",
                    fontFamily: "'JetBrains Mono', monospace",
                    transition: "all 0.2s ease",
                    backdropFilter: "blur(10px)",
                    minWidth: "fit-content",
                    width: "auto"
                });

                btn.onclick = () => {
                    document.body.classList.toggle("hud-is-hidden");
                };

                btn.onmouseover = () => {
                    btn.style.boxShadow = "0 0 24px rgba(0, 255, 255, 0.45)";
                    btn.style.transform = "translateY(-2px)";
                };
                btn.onmouseout = () => {
                    btn.style.boxShadow = "0 0 12px rgba(0, 255, 255, 0.18)";
                    btn.style.transform = "none";
                };

                document.body.appendChild(btn);

                // --- Create History Button ---
                const historyBtn = document.createElement("button");
                historyBtn.id = "history-btn";
                historyBtn.innerHTML = `
                    <div style="display: flex; align-items: center; justify-content: center; gap: 8px; flex-wrap: nowrap; white-space: nowrap;">
                        <img src="/public/png/statisctics.png" width="22" height="22" style="vertical-align: middle; position: relative; top: -1px;" alt="history">
                        <span style="vertical-align: middle; line-height: 1;">${textHistory}</span>
                    </div>
                `;

                Object.assign(historyBtn.style, {
                    position: "fixed",
                    bottom: "20px",
                    right: "auto",
                    zIndex: "10000",
                    padding: "10px 20px",
                    borderRadius: "50px",
                    background: "linear-gradient(135deg, rgba(85, 0, 119, 0.9) 0%, rgba(119, 0, 153, 0.9) 100%)",
                    border: "1px solid rgba(255, 0, 255, 0.4)",
                    color: "#ff00ff",
                    boxShadow: "0 0 12px rgba(255, 0, 255, 0.18)",
                    cursor: "pointer",
                    fontWeight: "bold",
                    fontFamily: "'JetBrains Mono', monospace",
                    transition: "all 0.2s ease",
                    backdropFilter: "blur(10px)",
                    minWidth: "fit-content",
                    width: "auto"
                });

                historyBtn.onclick = () => {
                    // Locate the invisible chat input and try to send the action command
                    const event = new MouseEvent('click', {
                        view: window,
                        bubbles: true,
                        cancelable: true
                    });
                    // Chainlit specific trick to trigger action - looking for the existing action button and clicking it
                    const existingBtn = Array.from(document.querySelectorAll('button')).find(el => el.textContent === 'view_hw_history');
                    if (existingBtn) {
                        existingBtn.dispatchEvent(event);
                    } else {
                        alert("The 'view_hw_history' action action hasn't been initialized by the server yet.");
                    }
                };

                historyBtn.onmouseover = () => {
                    historyBtn.style.boxShadow = "0 0 24px rgba(255, 0, 255, 0.45)";
                    historyBtn.style.transform = "translateY(-2px)";
                };
                historyBtn.onmouseout = () => {
                    historyBtn.style.boxShadow = "0 0 12px rgba(255, 0, 255, 0.18)";
                    historyBtn.style.transform = "none";
                };

                document.body.appendChild(historyBtn);

                // --- Create Language Selector (Top Center) ---
                if (!document.getElementById("lang-selector-container")) {
                    const langBtn = document.createElement("div");
                    langBtn.id = "lang-selector-container";
                    langBtn.innerHTML = `
                        <div style="position: relative; display: flex; align-items: center; justify-content: center;">
                            <div id="lang-select-wrapper" style="
                                background: rgba(15, 23, 42, 0.85);
                                backdrop-filter: blur(12px);
                                border: 1px solid rgba(255, 255, 255, 0.15);
                                border-radius: 12px;
                                padding: 6px 12px;
                                display: flex;
                                align-items: center;
                                gap: 10px;
                                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
                                pointer-events: auto;
                            ">
                                <span style="font-size: 18px; line-height: 1;">
                                    ${lang === 'zh-TW' ? '🇹🇼' :
                            lang === 'ja' ? '🇯🇵' :
                                lang === 'es' ? '🇪🇸' :
                                    lang === 'ko' ? '🇰🇷' :
                                        lang === 'th' ? '🇹🇭' :
                                            lang === 'vi' ? '🇻🇳' :
                                                lang === 'hi' ? '🇮🇳' : '🇺🇸'}
                                </span>
                                <select id="lang-select" style="
                                    background: transparent;
                                    color: #cbd5e1;
                                    border: none;
                                    font-family: 'JetBrains Mono', monospace;
                                    font-weight: 600;
                                    font-size: 13px;
                                    cursor: pointer;
                                    outline: none;
                                    appearance: none;
                                    -webkit-appearance: none;
                                    padding-right: 20px;
                                ">
                                    <option value="en-US" ${lang === 'en-US' || lang === 'en' ? 'selected' : ''} style="background: #1e293b; color: #fff;">English (US)</option>
                                    <option value="zh-TW" ${lang === 'zh-TW' ? 'selected' : ''} style="background: #1e293b; color: #fff;">繁體中文 (TW)</option>
                                    <option value="ja" ${lang === 'ja' ? 'selected' : ''} style="background: #1e293b; color: #fff;">日本語 (JP)</option>
                                    <option value="es" ${lang === 'es' ? 'selected' : ''} style="background: #1e293b; color: #fff;">Español (ES)</option>
                                    <option value="ko" ${lang === 'ko' ? 'selected' : ''} style="background: #1e293b; color: #fff;">한국어 (KO)</option>
                                    <option value="th" ${lang === 'th' ? 'selected' : ''} style="background: #1e293b; color: #fff;">ไทย (TH)</option>
                                    <option value="vi" ${lang === 'vi' ? 'selected' : ''} style="background: #1e293b; color: #fff;">Tiếng Việt (VI)</option>
                                    <option value="hi" ${lang === 'hi' ? 'selected' : ''} style="background: #1e293b; color: #fff;">हिन्दी (HI)</option>
                                </select>
                                <div style="position: absolute; right: 12px; pointer-events: none; border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 5px solid #94a3b8;"></div>
                            </div>
                        </div>
                    `;

                    Object.assign(langBtn.style, {
                        position: "fixed",
                        top: "15px",
                        left: "50%",
                        transform: "translateX(-50%)",
                        zIndex: "11000",
                        pointerEvents: "none", // Container is transparent, only inner wrapper is clickable
                        transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)"
                    });

                    document.body.appendChild(langBtn);

                    const select = document.getElementById("lang-select");
                    const wrapper = document.getElementById("lang-select-wrapper");

                    select.onchange = (e) => {
                        window.location.href = `/?lang=${e.target.value}`;
                    };

                    wrapper.onmouseover = () => {
                        wrapper.style.borderColor = "rgba(0, 255, 255, 0.4)";
                        wrapper.style.boxShadow = "0 0 15px rgba(0, 255, 255, 0.15)";
                        langBtn.style.top = "17px";
                    };
                    wrapper.onmouseout = () => {
                        wrapper.style.borderColor = "rgba(255, 255, 255, 0.15)";
                        wrapper.style.boxShadow = "0 4px 20px rgba(0, 0, 0, 0.4)";
                        langBtn.style.top = "15px";
                    };
                }

                // --- Create Fixed HUD Panel ---
                if (!document.getElementById("asitop-hud-container")) {
                    // Inject styles dynamically to bypass Chainlit static CSS caching
                    const style = document.createElement("style");
                    style.innerHTML = `
                        .asitop-hud-container {
                            position: fixed !important;
                            bottom: 80px !important;
                            right: 20px !important;
                            z-index: 9999 !important;
                            background: linear-gradient(135deg, rgba(0, 15, 30, 0.95), rgba(0, 30, 60, 0.9)) !important;
                            border: 1px solid rgba(0, 255, 255, 0.4) !important;
                            box-shadow: 0 4px 15px rgba(0, 255, 255, 0.2) !important;
                            width: 450px !important;
                            max-width: calc(100vw - 40px) !important;
                            padding: 15px 20px !important;
                            border-radius: 12px !important;
                            backdrop-filter: blur(10px) !important;
                            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
                            visibility: visible;
                            opacity: 1;
                            transform: translateY(0) scale(1) !important;
                            transform-origin: bottom right !important;
                        }
                        body.hud-is-hidden .asitop-hud-container {
                            opacity: 0 !important;
                            visibility: hidden !important;
                            transform: translateY(20px) scale(0.95) !important;
                            pointer-events: none !important;
                        }
                    `;
                    document.head.appendChild(style);

                    const panel = document.createElement("div");
                    panel.id = "asitop-hud-container";
                    panel.className = "asitop-hud-container";
                    // Also apply inline style fallbacks just in case
                    Object.assign(panel.style, {
                        position: "fixed", bottom: "80px", right: "20px",
                        width: "450px", zIndex: "9999", borderRadius: "12px",
                        background: "#0d1117", overflow: "hidden"
                    });
                    panel.innerHTML = `
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 1rem; margin-bottom: 5px; color: #b8e8f8; font-weight: bold; background: transparent; padding: 5px 10px; display: flex; align-items: center; gap: 8px;">
                            <img src="/public/png/performance.png" width="24" height="24" alt="icon">
                            <span style="padding-top: 1px;">${textPerfMon}</span>
                        </div>
                        <iframe src='http://localhost:8501/?embed=true' width='100%' height='620' frameborder='0' style='border-radius: 8px; border: 1px solid rgba(0, 255, 255, 0.4); background: #0d1117;'></iframe>
                    `;
                    document.body.appendChild(panel);
                }

                // Adjust positioning after buttons are added
                setTimeout(() => {
                    const toggleBtn = document.getElementById("hud-toggle-btn");
                    const histBtn = document.getElementById("history-btn");
                    const langContainer = document.getElementById("lang-selector-container");

                    if (toggleBtn && histBtn) {
                        const toggleRect = toggleBtn.getBoundingClientRect();
                        histBtn.style.right = (window.innerWidth - toggleRect.left + 15) + "px";
                    }
                }, 200);
            };

            // Chainlit heavily uses React, use MutationObserver to persist the button
            const observer = new MutationObserver(() => {
                // Prevent infinite loop from our own mutations triggering the observer again
                observer.disconnect();

                if (!document.getElementById("hud-toggle-btn")) {
                    createToggleButton();
                }

                // Keep keeping right margin updated if window resizes subtly
                const toggleBtn = document.getElementById("hud-toggle-btn");
                const histBtn = document.getElementById("history-btn");
                const langContainer = document.getElementById("lang-selector-container");

                if (toggleBtn && histBtn) {
                    const toggleRect = toggleBtn.getBoundingClientRect();
                    histBtn.style.right = (window.innerWidth - toggleRect.left + 15) + "px";
                }

                // Force hide the original 'view_hw_history' button in the chat if it appears
                document.querySelectorAll('button').forEach(btn => {
                    if (btn.textContent.trim() === 'view_hw_history') {
                        btn.style.setProperty('display', 'none', 'important');
                    }
                });

                // Translate specific UI elements dynamically
                const textareas = document.querySelectorAll('textarea');
                textareas.forEach(ta => {
                    if (ta.placeholder === "在此輸入您的訊息..." || ta.placeholder === "Type your message here...") {
                        const t = translations["Type your message here..."];
                        if (t && ta.placeholder !== t) {
                            ta.placeholder = t;
                        }
                    }
                });

                // Iterate over generic text nodes that need translating
                const walkTextNodes = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
                let n;
                while (n = walkTextNodes.nextNode()) {
                    let v = n.nodeValue.trim();
                    if (v === "說明" || v === "Help") {
                        let t = translations["Help"];
                        if (t && n.nodeValue !== t) n.nodeValue = t;
                    } else if (n.nodeValue.includes("大型語言模型可能會犯錯") || n.nodeValue.includes("LLMs can make mistakes")) {
                        let t = translations["LLMs can make mistakes. Please verify important info."];
                        if (t && n.nodeValue !== t) n.nodeValue = t;
                    } else if (v === "新對話" || v === "New Chat") {
                        let t = translations["New Chat"];
                        if (t && n.nodeValue !== t) n.nodeValue = t;
                    } else if (v === "對話設定" || v === "Chat Settings") {
                        let t = translations["Chat Settings"];
                        if (t && n.nodeValue !== t) n.nodeValue = t;
                    }
                }

                // Reconnect observer after modifications are done
                observer.observe(document.body, { childList: true, subtree: true, attributes: true, characterData: true });
            });

            observer.observe(document.body, { childList: true, subtree: true, attributes: true, characterData: true });
            createToggleButton();
        })
        .catch(err => console.error("Could not fetch translations:", err));
});
