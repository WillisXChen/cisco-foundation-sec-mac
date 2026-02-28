import logging
import sys
import structlog

import os
from logging.handlers import RotatingFileHandler

os.makedirs("logs", exist_ok=True)

def setup_logger(name: str = "cisco-foundation-sec-8b"):
    # 設定標準 library 的基礎 logging 等級
    # 這樣連第三方套件吐出來的 log 也能被攔截成 structlog 格式
    
    # 準備寫入實體檔案的 handler，加上自動滾動機制 (10MB)
    file_handler = RotatingFileHandler("logs/app.log", maxBytes=10*1024*1024, backupCount=5)
    stream_handler = logging.StreamHandler(sys.stdout)

    logging.basicConfig(
        format="%(message)s",
        handlers=[stream_handler, file_handler],
        level=logging.INFO,
    )

    # 針對 structlog 配置處理管線
    structlog.configure(
        processors=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            
            # 轉換為本地查看用的漂亮彩色輸出 (如果上生產環境要給 Loki，可改為 JSONRenderer)
            structlog.dev.ConsoleRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    return structlog.get_logger(name)

logger = setup_logger()
