import streamlit as st
import asyncio
from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport

st.set_page_config(layout="wide", page_title="ASITOP Monitor")

# ======= 黑客/終端機風格 CSS =======
st.markdown("""
<style>
    /* 全局背景與字型 */
    .stApp {
        background-color: #0d1117 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    
    /* 移除頂部控制條與邊距 */
    header[data-testid="stHeader"] {display: none;}
    .block-container {padding-top: 0rem; padding-bottom: 0rem; margin-top: -10px;}
    
    /* 所有的字都是綠色的，類似 ASITOP */
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #00ff00 !important;
        font-family: 'Courier New', Courier, monospace !important;
        margin-bottom: 0px !important;
        line-height: 1.2 !important;
    }

    /* 區塊框線 */
    .terminal-box {
        border: 1px solid #30363d;
        border-radius: 4px;
        padding: 4px 8px;
        margin-bottom: 4px;
        background-color: #010409;
    }
    
    /* 進度方塊的 CSS，密集且無縫 */
    .bar-filled {
        color: #00ff00;
        font-weight: 900;
        letter-spacing: -2px;
        font-size: 0.9em;
    }
    .bar-empty {
        color: #30363d;
        font-weight: 900;
        letter-spacing: -2px;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# 這裡是 Chainlit 裡我們剛才建好的 Strawberry GraphQL 伺服器網址
GRAPHQL_WS_URL = "ws://localhost:8000/graphql"

def draw_blocks(pct, max_blocks=60):
    """將百分比轉換成如 |||█████||| 樣式的純粹 ASCII 綠色方塊"""
    filled = int((pct / 100.0) * max_blocks)
    empty = max_blocks - filled
    # 使用 █ (U+2588) 代表進度條，以確保填滿與空白的字元寬度一致
    bar_str = f"<span class='bar-filled'>{'█' * filled}</span><span class='bar-empty'>{'|' * empty}</span>"
    return bar_str

# 畫面佔位符，這樣能做到畫面原地刷新而不會一直往下長
placeholder = st.empty()

def render_stats(stats):
    with placeholder.container():
        # 第一區塊：CPU info
        st.markdown(f"**{stats['chipLabel']}<br>CPU Cores: {stats['eCores']}E+{stats['pCores']}P<br>GPU Cores: {stats['gpuCores']}**", unsafe_allow_html=True)
        
        # 使用兩欄佈局並排 E-CPU 與 P-CPU
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="terminal-box">E-CPU Usage: {stats["eCpuPct"]:.1f}%<br>{draw_blocks(stats["eCpuPct"], 40)}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="terminal-box">P-CPU Usage: {stats["pCpuPct"]:.1f}%<br>{draw_blocks(stats["pCpuPct"], 40)}</div>', unsafe_allow_html=True)
            
        # 第二區塊：功耗 (Power)
        col3, col4 = st.columns(2)
        with col3:
            cpu_p = f"{stats['cpuPowerW']}W" if stats['cpuPowerW']>=0 else 'N/A'
            cpu_val = max(stats['cpuPowerW'], 0)
            cpu_pct = min((cpu_val / 40.0) * 100, 100)
            st.markdown(f'<div class="terminal-box">CPU Power: {cpu_p}<br>{draw_blocks(cpu_pct, 40)}</div>', unsafe_allow_html=True)
        with col4:
            gpu_p = f"{stats['gpuPowerW']}W" if stats['gpuPowerW']>=0 else 'N/A'
            gpu_val = max(stats['gpuPowerW'], 0)
            gpu_pct = min((gpu_val / 40.0) * 100, 100)
            st.markdown(f'<div class="terminal-box">GPU Power: {gpu_p}<br>{draw_blocks(gpu_pct, 40)}</div>', unsafe_allow_html=True)

        # 第三區塊：整行顯示 (GPU, Memory, Total Power)
        st.markdown(f'<div class="terminal-box">GPU Usage: {stats["gpuPct"]}%<br>{draw_blocks(stats["gpuPct"], 80)}</div>', unsafe_allow_html=True)
        
        ram_actual_pct = (stats["ramUsedGb"] / stats["ramTotalGb"]) * 100 if stats["ramTotalGb"] > 0 else 0
        st.markdown(f'<div class="terminal-box">Memory RAM Usage: {stats["ramUsedGb"]:.1f}/{stats["ramTotalGb"]:.1f}GB ({ram_actual_pct:.1f}%)<br>{draw_blocks(ram_actual_pct, 80)}</div>', unsafe_allow_html=True)

        tot_p = f"{stats['totalPowerW']}W" if stats['totalPowerW']>=0 else 'N/A'
        tot_val = max(stats['totalPowerW'], 0)
        tot_pct = min((tot_val / 80.0) * 100, 100)
        st.markdown(f'<div class="terminal-box">CPU+GPU+ANE Total Power: {tot_p}<br>{draw_blocks(tot_pct, 80)}</div>', unsafe_allow_html=True)

async def run_subscription():
    while True:
        try:
            transport = WebsocketsTransport(url=GRAPHQL_WS_URL)
            async with Client(transport=transport, fetch_schema_from_transport=False) as session:
                query = gql("""
                subscription {
                  watchStats {
                    eCpuPct
                    pCpuPct
                    gpuPct
                    ramPct
                    ramUsedGb
                    ramTotalGb
                    eCores
                    pCores
                    gpuCores
                    cpuPowerW
                    gpuPowerW
                    totalPowerW
                    chipLabel
                  }
                }
                """)
                async for result in session.subscribe(query):
                    stats = result.get('watchStats')
                    if stats:
                        render_stats(stats)
        except Exception as e:
            with placeholder.container():
                st.error(f"等待 Chainlit 伺服器的 GraphQL 訂閱 API 連線中 (發生失敗: {e})...")
            await asyncio.sleep(2)

try:
    asyncio.run(run_subscription())
except Exception as e:
    st.error(f"Subscription loop exited: {e}")
