# 生命週期槓桿

用生命週期法計算目前槓桿、目標槓桿、再平衡要買賣多少，以及斷頭距離。

單一 `index.html`，不需要建置。輸入的資料存在使用者自己瀏覽器的 localStorage，下次打開會自動載入，不會上傳到任何伺服器。

股價來自證交所與櫃買中心的每日收盤資料：`.github/workflows/update-prices.yml` 在每個交易日傍晚執行 `scripts/update_prices.py`，更新 `prices.json`。在 Actions 頁面按「Run workflow」可以手動更新。

這是計算工具，不是投資建議。
