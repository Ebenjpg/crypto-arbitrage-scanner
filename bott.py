import ccxt
import pandas as pd
import time
import os

# =========================
# EXCHANGE
# =========================

exchange = ccxt.kucoin()

# =========================
# CONFIG
# =========================

FEE_RATE = 0.001
MIN_PROFIT = -0.35

BASE_ASSETS = ["BTC", "ETH", "BNB", "XRP", "ADA", "SOL", "DOT", "DOGE", "AVAX", "MATIC"]

# =========================
# AUTO LOAD ALL USDT COINS (FULL MARKET SCAN)
# =========================

markets = exchange.load_markets()

ALTCOINS = list(set([
    symbol.split("/")[0]
    for symbol in markets
    if symbol.endswith("/USDT")
]))

# =========================
# BUILD TRIANGLES
# =========================

triangles = []

for base in BASE_ASSETS:

    for alt in ALTCOINS:

        triangles.append({

            "step_a": f"{base}/USDT",
            "step_b": f"{alt}/{base}",
            "step_c": f"{alt}/USDT",

            "base": base,
            "alt": alt
        })

# =========================
# MAIN LOOP
# =========================

while True:

    try:

        tickers = exchange.fetch_tickers()

        opportunities = []

        for tri in triangles:

            try:

                a = tri["step_a"]
                b = tri["step_b"]
                c = tri["step_c"]

                if (
                    a not in tickers or
                    b not in tickers or
                    c not in tickers
                ):
                    continue

                ask_a = tickers[a]["ask"]
                ask_b = tickers[b]["ask"]
                bid_c = tickers[c]["bid"]

                if (
                    ask_a is None or
                    ask_b is None or
                    bid_c is None
                ):
                    continue

                # =====================
                # START
                # =====================

                start_usdt = 100

                # STEP A
                base_amount = start_usdt / ask_a

                # STEP B
                alt_amount = base_amount / ask_b

                # STEP C
                final_usdt = alt_amount * bid_c

                # =====================
                # RAW %
                # =====================

                raw_profit = (
                    (final_usdt - start_usdt)
                    / start_usdt
                ) * 100

                # =====================
                # FEES
                # =====================

                fees = (
                    start_usdt * FEE_RATE * 3
                )

                final_after_fees = (
                    final_usdt - fees
                )

                after_fee_profit = (
                    (final_after_fees - start_usdt)
                    / start_usdt
                ) * 100

                if after_fee_profit >= MIN_PROFIT:

                    opportunities.append({

                        "STEP A":
                        "USDT",

                        "STEP B":
                        tri["base"],

                        "STEP C":
                        tri["alt"],

                        "RAW %":
                        round(raw_profit, 2),

                        "FEES":
                        round(fees, 3),

                        "AFTER FEES %":
                        round(after_fee_profit, 2)
                    })

            except:
                continue

        # =========================
        # DISPLAY
        # =========================

        os.system("cls" if os.name == "nt" else "clear")

        print("=" * 120)
        print(" LIVE TRIANGULAR ARBITRAGE SCANNER ")
        print("=" * 120)

        if opportunities:

            df = pd.DataFrame(opportunities)

            df = df.sort_values(
                by="AFTER FEES %",
                ascending=False
            )

            print(df.head(20).to_string(index=False))

        else:

            print("No opportunities found.")

        time.sleep(1)

    except Exception as e:

        print("ERROR:", e)

        time.sleep(3)
