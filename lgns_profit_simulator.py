import streamlit as st
import requests
import math

# =========================
# Fungsi Harga Real-Time
# =========================
def get_price(token_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_id}&vs_currencies=idr"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get(token_id, {}).get("idr", None)
    return None

# =========================
# Fungsi Compound Growth
# =========================
def compound_growth(principal, rate_per_rebase, rebase_per_day, days):
    total_rebase = rebase_per_day * days
    return principal * ((1 + rate_per_rebase) ** total_rebase)

def compound_growth_apy(principal, apr_percent, days):
    apr = apr_percent / 100
    daily_rate = apr / 365
    return principal * ((1 + daily_rate) ** days)

# =========================
# UI App Streamlit
# =========================
st.set_page_config(page_title="Simulasi Staking LGNS & AXS", layout="centered")
st.title("📈 Simulasi Profit Staking: LGNS vs AXS")

# Input jumlah modal dalam Rupiah
rupiah_input = st.text_input("Masukkan jumlah modal dalam Rupiah:", value="10.000.000")
rupiah_input_cleaned = rupiah_input.replace(".", "").replace(",", "")

try:
    modal_rupiah = int(rupiah_input_cleaned)
except ValueError:
    st.error("Format angka tidak valid. Gunakan titik sebagai pemisah ribuan, contoh: 1.000.000")
    st.stop()

# =========================
# Harga Token Real-Time
# =========================
price_lgns = get_price("origin-lgns")
price_axs = get_price("axie-infinity")

if price_lgns is None or price_axs is None:
    st.error("Gagal mengambil data harga dari CoinGecko.")
    st.stop()

st.markdown(f"💰 Harga **LGNS** saat ini: Rp {price_lgns:,.0f}")
st.markdown(f"💰 Harga **AXS** saat ini: Rp {price_axs:,.0f}")

# =========================
# LGNS Simulation
# =========================
rebase_yield = 0.0026  # 0.26% per rebase
rebase_per_day = 3
jumlah_lgns = modal_rupiah / price_lgns

hasil_lgns_1d = compound_growth(jumlah_lgns, rebase_yield, rebase_per_day, 1) * price_lgns
hasil_lgns_7d = compound_growth(jumlah_lgns, rebase_yield, rebase_per_day, 7) * price_lgns
hasil_lgns_30d = compound_growth(jumlah_lgns, rebase_yield, rebase_per_day, 30) * price_lgns

st.subheader("🔷 Estimasi Staking LGNS")
st.write(f"Setelah 1 hari: Rp {hasil_lgns_1d:,.0f}")
st.write(f"Setelah 7 hari: Rp {hasil_lgns_7d:,.0f}")
st.write(f"Setelah 30 hari: Rp {hasil_lgns_30d:,.0f}")

st.info("⚠️ **Risiko LGNS**: APY sangat tinggi (hingga 1600%+) tapi fluktuatif. Harga token bisa turun drastis dan reward bisa menurun tergantung protokol Origin. Tidak cocok untuk risiko rendah.")

# =========================
# AXS Simulation
# =========================
axs_apr = 28  # APR tahunan dalam persen
jumlah_axs = modal_rupiah / price_axs

hasil_axs_1d = compound_growth_apy(jumlah_axs, axs_apr, 1) * price_axs
hasil_axs_7d = compound_growth_apy(jumlah_axs, axs_apr, 7) * price_axs
hasil_axs_30d = compound_growth_apy(jumlah_axs, axs_apr, 30) * price_axs

st.subheader("🟢 Estimasi Staking AXS")
st.write(f"Setelah 1 hari: Rp {hasil_axs_1d:,.0f}")
st.write(f"Setelah 7 hari: Rp {hasil_axs_7d:,.0f}")
st.write(f"Setelah 30 hari: Rp {hasil_axs_30d:,.0f}")

st.info("⚠️ **Risiko AXS**: APR moderat (sekitar 28%) dan relatif stabil. Cocok untuk staking jangka menengah-panjang, namun harga AXS bisa turun mengikuti tren market crypto dan performa ekosistem Axie Infinity.")

st.caption("Data harga real-time dari CoinGecko. Semua simulasi berbasis compound interest. Bukan nasihat keuangan.")
