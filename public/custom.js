document.addEventListener("DOMContentLoaded", () => {
    // Hide HUD by default on load
    document.body.classList.add("hud-is-hidden");

    const createToggleButton = () => {
        if (document.getElementById("hud-toggle-btn")) return;

        const btn = document.createElement("button");
        btn.id = "hud-toggle-btn";
        btn.innerHTML = "🎛️ HUD";

        Object.assign(btn.style, {
            position: "fixed",
            bottom: "20px",
            right: "20px",
            zIndex: "10000",
            padding: "10px 20px",
            borderRadius: "30px",
            background: "linear-gradient(135deg, rgba(0, 85, 119, 0.9) 0%, rgba(0, 119, 153, 0.9) 100%)",
            border: "1px solid rgba(0, 255, 255, 0.4)",
            color: "#00ffff",
            boxShadow: "0 0 12px rgba(0, 255, 255, 0.18)",
            cursor: "pointer",
            fontWeight: "bold",
            fontFamily: "'JetBrains Mono', monospace",
            transition: "all 0.2s ease",
            backdropFilter: "blur(10px)"
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
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; margin-bottom: 5px; color: #b8e8f8; font-weight: bold; background: transparent; padding: 5px 10px;">
                    🚀 ASITOP HUD
                </div>
                <iframe src='http://localhost:8501/?embed=true' width='100%' height='510' frameborder='0' style='border-radius: 8px; border: 1px solid rgba(0, 255, 255, 0.4); background: #0d1117;'></iframe>
            `;
            document.body.appendChild(panel);
        }
    };

    // Chainlit heavily uses React, use MutationObserver to persist the button
    const observer = new MutationObserver(() => {
        if (!document.getElementById("hud-toggle-btn")) {
            createToggleButton();
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });
    createToggleButton();
});
