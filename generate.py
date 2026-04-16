#!/usr/bin/env python3
"""
Big 7 + GTLB/XOM + Swing Scanner Dashboard
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
import os

BIG7 = {
    "AAPL":  {"name": "Apple",     "target": 236.00},
    "MSFT":  {"name": "Microsoft", "target": 497.00},
    "GOOGL": {"name": "Alphabet",  "target": 207.00},
    "AMZN":  {"name": "Amazon",    "target": 245.00},
    "META":  {"name": "Meta",      "target": 675.00},
    "NVDA":  {"name": "NVIDIA",    "target": 163.00},
    "TSLA":  {"name": "Tesla",     "target": 320.00},
}

MY_POSITIONS = {
    "GTLB": {"name": "GitLab",      "target": 41.67, "hold_above": 22.40, "sell_above": 25.20, "stop_loss": 22.00, "hard_sell": 24.00},
    "XOM":  {"name": "Exxon Mobil", "target": 120.00, "watch_level": 160.00},
}

SP500_NASDAQ = list(set([
    "AAL","AAP","ABNB","ABT","ACN","ADBE","ADI","ADP","ADSK","AEE","AEP","AES","AFL","AIG",
    "AKAM","ALB","ALGN","ALK","ALL","AMAT","AMD","AME","AMGN","AMP","AMT","ANET","ANSS","AON",
    "APA","APD","APH","APTV","ARE","ATO","AVB","AVGO","AVY","AWK","AXP","AZO","BA","BAC",
    "BALL","BAX","BBY","BDX","BEN","BIIB","BK","BKNG","BKR","BLK","BMY","BR","BRO","BSX",
    "BWA","C","CAG","CAH","CARR","CAT","CB","CBOE","CBRE","CCI","CCL","CDNS","CDW","CF",
    "CFG","CHD","CHRW","CHTR","CI","CINF","CL","CLX","CMA","CMCSA","CME","CMG","CMI","CMS",
    "CNC","CNP","COF","COO","COP","COST","CPB","CPRT","CPT","CRL","CRM","CSCO","CSX","CTAS",
    "CTRA","CTSH","CTVA","CVS","CVX","D","DAL","DD","DE","DFS","DG","DGX","DHI","DHR","DIS",
    "DLR","DLTR","DOV","DOW","DPZ","DRI","DTE","DUK","DVA","DVN","DXCM","EA","EBAY","ECL",
    "ED","EFX","EIX","EL","EMN","EMR","ENPH","EOG","EQIX","EQR","EQT","ES","ESS","ETN","ETR",
    "ETSY","EW","EXC","EXPD","EXPE","EXR","F","FANG","FAST","FCX","FDX","FE","FFIV","FIS",
    "FISV","FITB","FLT","FMC","FRT","FTNT","FTV","GD","GE","GILD","GIS","GL","GLW","GM",
    "GNRC","GOOGL","GPC","GPN","GRMN","GS","GWW","HAL","HAS","HBAN","HCA","HD","HES","HIG",
    "HII","HLT","HOLX","HON","HPE","HPQ","HRL","HSIC","HST","HSY","HUM","HWM","IBM","ICE",
    "IDXX","IEX","IFF","ILMN","INCY","INTC","INTU","INVH","IP","IPG","IQV","IR","IRM","ISRG",
    "IT","ITW","IVZ","JBHT","JCI","JKHY","JNJ","JPM","K","KDP","KEY","KEYS","KHC","KIM",
    "KLAC","KMB","KMI","KMX","KO","KR","L","LDOS","LEN","LH","LHX","LIN","LKQ","LLY","LMT",
    "LNC","LNT","LOW","LRCX","LUV","LVS","LW","LYB","LYV","MA","MAA","MAR","MAS","MCD",
    "MCHP","MCK","MCO","MDLZ","MDT","MET","MGM","MKC","MKTX","MLM","MMC","MMM","MNST","MO",
    "MOH","MOS","MPC","MPWR","MRK","MRNA","MRO","MS","MSCI","MSFT","MSI","MTB","MTCH","MTD",
    "MU","NCLH","NEE","NEM","NFLX","NI","NKE","NOC","NOW","NRG","NSC","NTAP","NTRS","NUE",
    "NVR","NWL","NXPI","O","ODFL","OGN","OKE","OMC","ON","ORCL","ORLY","OXY","PAYX","PCAR",
    "PCG","PEG","PEP","PFE","PFG","PG","PGR","PH","PHM","PKG","PLD","PM","PNC","PNR","PNW",
    "POOL","PPG","PPL","PRU","PSA","PSX","PTC","PWR","PYPL","QCOM","RCL","RE","REG","REGN",
    "RF","RJF","RL","RMD","ROK","ROL","ROP","ROST","RSG","RTX","SBAC","SBUX","SEDG","SEE",
    "SHW","SJM","SLB","SNA","SNPS","SO","SPG","SPGI","SRE","STE","STT","STX","STZ","SWK",
    "SWKS","SYF","SYK","SYY","T","TAP","TDG","TDY","TEL","TER","TFC","TFX","TGT","TJX",
    "TMO","TMUS","TPR","TRMB","TROW","TRV","TSCO","TSLA","TT","TTWO","TXN","TXT","TYL",
    "UAL","UDR","UHS","ULTA","UNH","UNP","UPS","URI","USB","V","VFC","VICI","VLO","VMC",
    "VNO","VRSK","VRSN","VRTX","VTR","VTRS","VZ","WAB","WAT","WBA","WBD","WDC","WEC","WELL",
    "WFC","WHR","WM","WMB","WMT","WRB","WRK","WST","WTW","WY","WYNN","XEL","XOM","XYL",
    "YUM","ZBH","ZBRA","ZION","ZTS",
    # Nasdaq extras
    "CRWD","DDOG","LULU","OKTA","PANW","TEAM","WDAY","ZM","ZS","SIRI","SGEN",
]))

SWING_MAX_PRICE  = 100.0
SWING_MIN_VOLUME = 1_000_000
TOP_N_SWINGS     = 8
OUTPUT_HTML      = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")



BLUE_CHIPS = {
    "V":    {"name": "Visa",           "sector": "💳 Financial",  "target": 380.00},
    "MA":   {"name": "Mastercard",     "sector": "💳 Financial",  "target": 560.00},
    "JPM":  {"name": "JP Morgan",      "sector": "💳 Financial",  "target": 280.00},
    "AXP":  {"name": "Amex",           "sector": "💳 Financial",  "target": 340.00},
    "GS":   {"name": "Goldman Sachs",  "sector": "💳 Financial",  "target": 650.00},
    "WMT":  {"name": "Walmart",        "sector": "🛒 Consumer",   "target": 115.00},
    "COST": {"name": "Costco",         "sector": "🛒 Consumer",   "target": 1050.00},
    "PG":   {"name": "Procter&Gamble", "sector": "🛒 Consumer",   "target": 185.00},
    "KO":   {"name": "Coca-Cola",      "sector": "🛒 Consumer",   "target": 75.00},
    "PEP":  {"name": "PepsiCo",        "sector": "🛒 Consumer",   "target": 175.00},
    "JNJ":  {"name": "J&J",            "sector": "🏥 Healthcare", "target": 175.00},
    "UNH":  {"name": "UnitedHealth",   "sector": "🏥 Healthcare", "target": 620.00},
    "ABT":  {"name": "Abbott",         "sector": "🏥 Healthcare", "target": 145.00},
    "LLY":  {"name": "Eli Lilly",      "sector": "🏥 Healthcare", "target": 1050.00},
    "TMO":  {"name": "Thermo Fisher",  "sector": "🏥 Healthcare", "target": 620.00},
    "CAT":  {"name": "Caterpillar",    "sector": "⚙️ Industrial", "target": 420.00},
    "HON":  {"name": "Honeywell",      "sector": "⚙️ Industrial", "target": 240.00},
    "DE":   {"name": "John Deere",     "sector": "⚙️ Industrial", "target": 480.00},
    "RTX":  {"name": "RTX Corp",       "sector": "⚙️ Industrial", "target": 145.00},
    "GE":   {"name": "GE Aerospace",   "sector": "⚙️ Industrial", "target": 220.00},
    "CVX":  {"name": "Chevron",        "sector": "⛽ Energy",     "target": 185.00},
    "SLB":  {"name": "Schlumberger",   "sector": "⛽ Energy",     "target": 58.00},
    "LIN":  {"name": "Linde",          "sector": "🧪 Materials",  "target": 520.00},
    "AMT":  {"name": "American Tower", "sector": "🏢 REIT",       "target": 230.00},
    "NEE":  {"name": "NextEra Energy", "sector": "⚡ Utilities",  "target": 85.00},
}

def compute_rsi(series, period=14):
    delta = series.diff()
    gain  = delta.clip(lower=0).rolling(period).mean()
    loss  = (-delta.clip(upper=0)).rolling(period).mean()
    rs    = gain / loss
    return 100 - (100 / (1 + rs))


def get_signal(rsi, price, ma50, ma200):
    if rsi is None: return "❓", "#f5f5f5"
    if rsi > 70:    return "🔴 OVERBOUGHT", "#ffebee"
    if rsi < 35 and ma200 and price > ma200: return "🟢 OVERSOLD/BUY ZONE", "#e8f5e9"
    above50  = ma50  and price > ma50
    above200 = ma200 and price > ma200
    if above50 and above200:   return "🟢 BULLISH",  "#e8f5e9"
    if not above50 and not above200: return "🔴 BEARISH", "#ffebee"
    return "🟡 NEUTRAL", "#fffde7"


def fetch_data(ticker):
    try:
        hist = yf.Ticker(ticker).history(period="1y")
        if hist.empty or len(hist) < 30: return None
        close = hist["Close"]; vol = hist["Volume"]
        price = round(float(close.iloc[-1]), 2)
        prev  = round(float(close.iloc[-2]), 2)
        chg   = round(((price - prev) / prev) * 100, 2)
        ma50  = round(float(close.rolling(50).mean().iloc[-1]),  2) if len(close) >= 50  else None
        ma200 = round(float(close.rolling(200).mean().iloc[-1]), 2) if len(close) >= 200 else None
        rsi_series = compute_rsi(close)
        rsi   = round(float(rsi_series.iloc[-1]), 1)
        avg_v = int(vol.rolling(20).mean().iloc[-1])

        # Confirmation: consecutive days RSI < 45
        rsi_days_oversold = 0
        for i in range(1, min(10, len(rsi_series))):
            if rsi_series.iloc[-i] < 45:
                rsi_days_oversold += 1
            else:
                break

        # Entry signal: oversold 3+ days AND today green
        entry_signal = None
        entry_price  = None
        if rsi_days_oversold >= 3 and chg > 0 and rsi < 45:
            entry_price  = round(price * 0.995, 2)
            entry_signal = f"🎯 ΕΙΣΟΔΟΣ ~${entry_price} (RSI oversold {rsi_days_oversold} μέρες · +{chg:.2f}% σήμερα)"

        return {"price": price, "prev": prev, "chg": chg, "ma50": ma50, "ma200": ma200,
                "rsi": rsi, "avg_vol": avg_v,
                "rsi_days_oversold": rsi_days_oversold,
                "entry_signal": entry_signal,
                "entry_price": entry_price,
                "arrow": "▲" if chg >= 0 else "▼",
                "chg_color": "#2e7d32" if chg >= 0 else "#c62828"}
    except Exception:
        return None


def fetch_weekly_rsi(ticker):
    try:
        hist = yf.Ticker(ticker).history(period="2y", interval="1wk")
        if hist.empty or len(hist) < 20: return None
        return round(float(compute_rsi(hist["Close"]).iloc[-1]), 1)
    except Exception:
        return None


def swing_score(d, rsi_w):
    s = 0
    if   d["rsi"] < 25: s += 35
    elif d["rsi"] < 30: s += 28
    elif d["rsi"] < 35: s += 20
    elif d["rsi"] < 40: s += 12
    if rsi_w:
        if   rsi_w < 30: s += 25
        elif rsi_w < 35: s += 18
        elif rsi_w < 40: s += 12
        elif rsi_w < 45: s += 6
    if d["ma200"] and d["price"] > d["ma200"]: s += 20
    if d["ma50"]  and d["price"] > d["ma50"]:  s += 10
    if d["avg_vol"] > 3_000_000:   s += 10
    elif d["avg_vol"] > 1_500_000: s += 5
    return min(s, 100)


def run_swing_scanner():
    print("\n🔍 Swing Scanner...")
    candidates = []
    for i, ticker in enumerate(SP500_NASDAQ):
        if (i+1) % 50 == 0: print(f"  ...{i+1}/{len(SP500_NASDAQ)}")
        d = fetch_data(ticker)
        if not d or d["price"] > SWING_MAX_PRICE or d["avg_vol"] < SWING_MIN_VOLUME: continue
        if d["rsi"] > 40:
            rsi_w = fetch_weekly_rsi(ticker)
            if not rsi_w or rsi_w > 45: continue
        else:
            rsi_w = fetch_weekly_rsi(ticker)
        sc = swing_score(d, rsi_w)
        if sc >= 20:
            candidates.append({"ticker": ticker, "price": d["price"],
                                "rsi_daily": d["rsi"], "rsi_weekly": rsi_w,
                                "ma50": d["ma50"], "ma200": d["ma200"],
                                "avg_vol": d["avg_vol"], "score": sc})
    candidates.sort(key=lambda x: x["score"], reverse=True)
    print(f"  ✅ {len(candidates)} candidates → Top {min(len(candidates), TOP_N_SWINGS)}")
    return candidates[:TOP_N_SWINGS]


def build_html(big7_r, pos_r, swings, bc_results, date_str):
    def row_big7(t, info, d):
        if not d: return f"<tr><td><b>{t}</b></td><td colspan='7'>❌</td></tr>"
        sig, bg = get_signal(d["rsi"], d["price"], d["ma50"], d["ma200"])
        dist = round(((info["target"] - d["price"]) / d["price"]) * 100, 1)
        dc   = "#2e7d32" if dist > 0 else "#c62828"
        a50  = "✅" if d["ma50"]  and d["price"] > d["ma50"]  else "❌"
        a200 = "✅" if d["ma200"] and d["price"] > d["ma200"] else "❌"
        return f"""<tr style="background:{bg}">
          <td><b>{t}</b><br><small style="color:#666">{info['name']}</small></td>
          <td><b>${d['price']}</b><br><small style="color:{d['chg_color']}">{d['arrow']} {d['chg']:+.2f}%</small></td>
          <td>${d['ma50'] or '—'}</td>
          <td>${d['ma200'] or '—'}</td>
          <td>{a50} / {a200}</td>
          <td><b>{d['rsi']}</b></td>
          <td style="color:{dc}"><b>{dist:+.1f}%</b><br><small>target ${info['target']}</small></td>
          <td>{sig}{f"<br><small style='color:#1a73e8'>{d['entry_signal']}</small>" if d.get('entry_signal') else ""}</td></tr>"""

    big7_rows = "".join(row_big7(t, info, big7_r.get(t)) for t, info in BIG7.items())

    # GTLB row
    gtlb_d = pos_r.get("GTLB"); gi = MY_POSITIONS["GTLB"]
    if gtlb_d:
        if   gtlb_d["price"] < gi["stop_loss"]:   gsig, gbg = "🔴 SELL — Stop Loss", "#ffebee"
        elif gtlb_d["price"] > gi["sell_above"]:  gsig, gbg = "🟡 HOLD/SELL — Take Profit", "#fffde7"
        else:                                      gsig, gbg = "🟢 HOLD", "#e8f5e9"
        gtlb_row = f"""<tr style="background:{gbg}">
          <td><b>GTLB</b><br><small>GitLab</small></td>
          <td><b>${gtlb_d['price']}</b><br><small style="color:{gtlb_d['chg_color']}">{gtlb_d['arrow']} {gtlb_d['chg']:+.2f}%</small></td>
          <td>${gtlb_d['ma50'] or '—'}</td>
          <td>${gtlb_d['ma200'] or '—'}</td>
          <td><b>{gtlb_d['rsi']}</b></td>
          <td>${gi['target']}</td>
          <td colspan="2"><b>{gsig}</b><br><small>Πώληση μόνο αν τιμή &gt; ${gi['hard_sell']}</small>{f"<br><small style='color:#1a73e8'>{gtlb_d['entry_signal']}</small>" if gtlb_d.get('entry_signal') else ""}</td></tr>"""
    else:
        gtlb_row = "<tr><td colspan='8'>❌ GTLB</td></tr>"

    # XOM row
    xom_d = pos_r.get("XOM"); xi = MY_POSITIONS["XOM"]
    if xom_d:
        xsig, xbg = get_signal(xom_d["rsi"], xom_d["price"], xom_d["ma50"], xom_d["ma200"])
        watch = "⚠️ Κάτω από $160!" if xom_d["price"] < xi["watch_level"] else "✅ Πάνω από $160"
        xom_row = f"""<tr style="background:{xbg}">
          <td><b>XOM</b><br><small>Exxon</small></td>
          <td><b>${xom_d['price']}</b><br><small style="color:{xom_d['chg_color']}">{xom_d['arrow']} {xom_d['chg']:+.2f}%</small></td>
          <td>${xom_d['ma50'] or '—'}</td>
          <td>${xom_d['ma200'] or '—'}</td>
          <td><b>{xom_d['rsi']}</b></td>
          <td>${xi['target']}</td>
          <td colspan="2"><b>{xsig}</b><br><small>{watch}</small>{f"<br><small style='color:#1a73e8'>{xom_d['entry_signal']}</small>" if xom_d.get('entry_signal') else ""}</td></tr>"""
    else:
        xom_row = "<tr><td colspan='8'>❌ XOM</td></tr>"

    # Swing rows
    if swings:
        swing_rows = ""
        for s in swings:
            sc_col = "#2e7d32" if s["score"] >= 70 else "#f57f17" if s["score"] >= 50 else "#c62828"
            a200 = "✅" if s["ma200"] and s["price"] > s["ma200"] else "❌"
            swing_rows += f"""<tr>
              <td><b>{s['ticker']}</b></td>
              <td><b>${s['price']}</b></td>
              <td>{s['rsi_daily']}</td>
              <td>{s['rsi_weekly'] or '—'}</td>
              <td>${s['ma50'] or '—'}</td>
              <td>${s['ma200'] or '—'}</td>
              <td>{a200}</td>
              <td style="color:{sc_col}"><b>{s['score']}/100</b>{f"<br><small style='color:#1a73e8'>{s['entry_signal']}</small>" if s.get('entry_signal') else ""}</td></tr>"""
    else:
        swing_rows = "<tr><td colspan='8' style='padding:20px'>Δεν βρέθηκαν setups αυτή τη στιγμή</td></tr>"


    # Blue Chip rows grouped by sector
    bc_rows = ""
    last_sector = ""
    for t, info in BLUE_CHIPS.items():
        d = bc_results.get(t)
        if not d:
            bc_rows += f"<tr><td><b>{t}</b></td><td colspan='7'>❌</td></tr>"
            continue
        sig, bg = get_signal(d["rsi"], d["price"], d["ma50"], d["ma200"])
        dist = round(((info["target"] - d["price"]) / d["price"]) * 100, 1)
        dc   = "#2e7d32" if dist > 0 else "#c62828"
        a50  = "✅" if d["ma50"]  and d["price"] > d["ma50"]  else "❌"
        a200 = "✅" if d["ma200"] and d["price"] > d["ma200"] else "❌"
        if info["sector"] != last_sector:
            bc_rows += f"<tr style=\"background:#e8eaf6\"><td colspan='8'><b>{info['sector']}</b></td></tr>"
            last_sector = info["sector"]
        entry_html = f"<br><small style=\"color:#1a73e8\">{d['entry_signal']}</small>" if d.get("entry_signal") else ""
        bc_rows += f"""<tr style="background:{bg}">
          <td><b>{t}</b><br><small style="color:#666">{info['name']}</small></td>
          <td><b>${d['price']}</b><br><small style="color:{d['chg_color']}">{d['arrow']} {d['chg']:+.2f}%</small></td>
          <td>${d['ma50'] or '—'}</td>
          <td>${d['ma200'] or '—'}</td>
          <td>{a50} / {a200}</td>
          <td><b>{d['rsi']}</b></td>
          <td style="color:{dc}"><b>{dist:+.1f}%</b><br><small>target ${info['target']}</small></td>
          <td>{sig}{entry_html}</td></tr>"""

    return f"""<!DOCTYPE html>
<html lang="el"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Market Dashboard</title>
<style>
* {{box-sizing:border-box}}
body {{font-family:'Segoe UI',Arial,sans-serif;margin:0;background:#f0f2f5}}
.hdr {{background:#0d1b2a;color:white;padding:22px 28px}}
.hdr h1 {{margin:0;font-size:1.4em}}
.hdr p {{margin:4px 0 0;opacity:.65;font-size:.83em}}
.wrap {{padding:18px 28px}}
h2 {{color:#0d1b2a;border-left:4px solid #1a73e8;padding-left:10px;margin:24px 0 10px;font-size:.95em;text-transform:uppercase;letter-spacing:.5px}}
table {{width:100%;border-collapse:collapse;background:white;border-radius:10px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.07);margin-bottom:6px}}
th {{background:#1a237e;color:white;padding:9px 11px;text-align:center;font-size:.78em;text-transform:uppercase;letter-spacing:.4px}}
th:first-child {{text-align:left}}
td {{padding:9px 11px;border-bottom:1px solid #f0f0f0;font-size:.86em;vertical-align:middle;text-align:center}}
td:first-child {{text-align:left}}
tr:last-child td {{border-bottom:none}}
.note {{background:#e8f0fe;border-left:4px solid #1a73e8;padding:9px 13px;border-radius:6px;font-size:.8em;color:#1a237e;margin-bottom:8px}}
.legend {{background:white;border-radius:10px;padding:13px 17px;box-shadow:0 2px 8px rgba(0,0,0,.06);margin-top:6px}}
.legend p {{margin:3px 0;font-size:.8em;color:#555}}
.footer {{text-align:center;color:#aaa;font-size:.72em;margin-top:20px;padding-bottom:20px}}
</style></head><body>
<div class="hdr">
  <h1>📊 Market Dashboard — Big 7 · Θέσεις · Swing Scanner</h1>
  <p>Ενημέρωση: {date_str} &nbsp;|&nbsp; Yahoo Finance &nbsp;|&nbsp; RSI-14</p>
</div>
<div class="wrap">
  <h2>🔮 Big 7</h2>
  <table><thead><tr><th>Μετοχή</th><th>Τιμή</th><th>MA50</th><th>MA200</th><th>MA50/200</th><th>RSI</th><th>↔ Target</th><th>Σήμα</th></tr></thead>
  <tbody>{big7_rows}</tbody></table>

  <h2>🦊 Θέσεις μου — GTLB & XOM</h2>
  <table><thead><tr><th>Μετοχή</th><th>Τιμή</th><th>MA50</th><th>MA200</th><th>RSI</th><th>Target</th><th colspan="2">Σήμα</th></tr></thead>
  <tbody>{gtlb_row}{xom_row}</tbody></table>

  <h2>🚀 Swing Scanner — Ευκαιρίες &lt;$100</h2>
  <div class="note">📋 Κριτήρια: Τιμή &lt;$100 · Volume &gt;1M · RSI daily &lt;40 ή weekly &lt;45 · Score βάσει RSI+MA+Volume</div>
  <table><thead><tr><th>Ticker</th><th>Τιμή</th><th>RSI Daily</th><th>RSI Weekly</th><th>MA50</th><th>MA200</th><th>Πάνω MA200</th><th>Score</th></tr></thead>
  <tbody>{swing_rows}</tbody></table>


  <h2>💎 Blue Chips — Non-Tech S&P 500</h2>
  <table><thead><tr><th>Μετοχή</th><th>Τιμή</th><th>MA50</th><th>MA200</th><th>MA50/200</th><th>RSI</th><th>↔ Target</th><th>Σήμα</th></tr></thead>
  <tbody>{bc_rows}</tbody></table>

    <div class="legend">
    <p>🟢 <b>BULLISH</b> — Πάνω από MA50 &amp; MA200 &nbsp;|&nbsp; 🟢 <b>OVERSOLD/BUY ZONE</b> — RSI &lt;35 &amp; πάνω από MA200</p>
    <p>🟡 <b>NEUTRAL</b> — Μικτά σήματα &nbsp;|&nbsp; 🔴 <b>BEARISH</b> — Κάτω από MA50 &amp; MA200 &nbsp;|&nbsp; 🔴 <b>OVERBOUGHT</b> — RSI &gt;70</p>
    <p style="margin-top:6px">📊 <b>Swing Score 0–100</b>: RSI daily (35pts) + RSI weekly (25pts) + πάνω MA200 (20pts) + MA50 (10pts) + volume (10pts)</p>
  </div>
  <div class="footer">Παράχθηκε αυτόματα · Δεν αποτελεί επενδυτική συμβουλή · {date_str}</div>
</div></body></html>"""


def main():
    date_str = datetime.now().strftime("%d %B %Y, %H:%M")
    print(f"\n📊 Market Dashboard — {date_str}\n{'='*55}")

    print("\n📈 Big 7...")
    big7_r = {}
    for t in BIG7:
        print(f"  {t}...", end=" ", flush=True)
        big7_r[t] = fetch_data(t)
        d = big7_r[t]
        print(f"${d['price']} RSI:{d['rsi']}" if d else "ΣΦΑΛΜΑ")

    print("\n🦊 GTLB & XOM...")
    pos_r = {}
    for t in MY_POSITIONS:
        print(f"  {t}...", end=" ", flush=True)
        pos_r[t] = fetch_data(t)
        d = pos_r[t]
        print(f"${d['price']} RSI:{d['rsi']}" if d else "ΣΦΑΛΜΑ")

    swings = run_swing_scanner()

    print("\n💎 Blue Chips...")
    bc_results = {}
    for t in BLUE_CHIPS:
        print(f"  {t}...", end=" ", flush=True)
        bc_results[t] = fetch_data(t)
        d = bc_results[t]
        print(f"${d['price']} RSI:{d['rsi']}" if d else "ΣΦΑΛΜΑ")

    html = build_html(big7_r, pos_r, swings, bc_results, date_str)
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n── QUICK SUMMARY ───────────────────────────────")
    for t, d in {**big7_r, **pos_r}.items():
        if d:
            sig, _ = get_signal(d["rsi"], d["price"], d["ma50"], d["ma200"])
            print(f"  {t:<6} ${d['price']:>8}  RSI:{d['rsi']:>5}  {sig}")

    if swings:
        print(f"\n🚀 Top Swing Picks:")
        for s in swings:
            print(f"  {s['ticker']:<6} ${s['price']:>7}  D:{s['rsi_daily']}  W:{s['rsi_weekly'] or '—'}  Score:{s['score']}")

    print(f"\n✅ HTML αποθηκεύτηκε → open big7_dashboard.html")


if __name__ == "__main__":
    main()
