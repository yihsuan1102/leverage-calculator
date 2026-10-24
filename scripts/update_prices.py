"""抓證交所與櫃買中心的每日收盤價，寫成 prices.json 給網頁讀。"""
import json
import re
import ssl
import urllib.request
from pathlib import Path

# 證交所憑證缺 Subject Key Identifier，Python 3.13+ 的嚴格檢查會擋；只關掉這項，憑證仍會驗證
CTX = ssl.create_default_context()
CTX.verify_flags &= ~ssl.VERIFY_X509_STRICT

TWSE = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
TPEX = "https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes"
OUT = Path(__file__).resolve().parent.parent / "prices.json"
# 只留一般股票（4 碼）和 ETF（00 開頭），排除權證等
KEEP = re.compile(r"^(\d{4}|00\d{2,4}[A-Z]?)$")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
        return json.loads(r.read().decode("utf-8-sig"))


def num(s):
    try:
        v = float(str(s).replace(",", "").strip())
        return v if v > 0 else None
    except ValueError:
        return None


def roc_to_iso(d):  # "1151022" -> "2026-10-22"
    d = str(d).strip()
    return f"{int(d[:-4]) + 1911}-{d[-4:-2]}-{d[-2:]}"


q, dates = {}, set()
for r in get(TWSE):
    p = num(r.get("ClosingPrice"))
    if p and KEEP.match(r["Code"].strip()):
        q[r["Code"].strip()] = [r["Name"].strip(), p]
        dates.add(r["Date"])
for r in get(TPEX):
    p = num(r.get("Close"))
    code = r["SecuritiesCompanyCode"].strip()
    if p and KEEP.match(code) and code not in q:
        q[code] = [r["CompanyName"].strip(), p]
        dates.add(r["Date"])

if len(q) < 500:
    raise SystemExit(f"只抓到 {len(q)} 筆，可能是來源異常，不覆寫 prices.json")

data = {"date": roc_to_iso(max(dates)), "q": dict(sorted(q.items()))}
OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"{data['date']}：{len(q)} 筆")
