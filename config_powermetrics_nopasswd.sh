#!/bin/bash
# 此腳本將 powermetrics 加入到 /etc/sudoers.d/ 中，使其執行時不需免密碼。
# 這樣一來 Chainlit 在背景收集 Apple Silicon 的電力數據時，就不用使用 Root 執行整個伺服器。

echo "這會將 powermetrics 加入 sudo 免密碼清單中。"
echo "正在請求管理員權限..."
sudo bash -c "echo \"${USER} ALL=(ALL) NOPASSWD: /usr/bin/powermetrics\" > /etc/sudoers.d/powermetrics-nopasswd"
sudo chmod 0440 /etc/sudoers.d/powermetrics-nopasswd

echo "✅ 設定完成！現在 Chainlit 可以即時取得 ASITOP 的電力數據了。"
