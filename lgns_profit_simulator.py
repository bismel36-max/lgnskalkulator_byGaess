import streamlit as st
import requests
import math

# Fungsi untuk mengambil harga LGNS real-time dari CoinGecko
def get_lgns_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=origin-lgns&vs_currencies=idr"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("origin-lgns", {}).get("idr", None)
    else:
        return None

# Fungsi perhitungan compound interest
def compound_growth(principal, rate_per_rebase, rebase_per_day, days):
    total_rebase = rebase_per_day * days
    return principal * ((1 + rate_per_rebase) ** total_rebase)

# Streamlit Web App
st.set_page_config(page_title="LGNS Profit Simulator", layout="centered")
st.title("📈 LGNS Staking Profit Simulator by GaEES")

# Ambil harga LGNS sekarang
price_lgns = get_lgns_price()
if price_lgns is None:
    st.error("Gagal mengambil harga LGNS dari CoinGecko. Coba beberapa saat lagi.")
    st.stop()

st.success(f"💰 Harga LGNS saat ini: Rp {price_lgns:,.0f} (coingecko)")

# Input nilai modal awal
rupiah_input = st.number_input("Masukkan jumlah modal dalam Rupiah:", min_value=1000, value=10000000, step=1000)

# Parameter staking LGNS
rebase_yield = 0.0026  # 0.26% per rebase
rebase_per_day = 3     # 3 rebases per day

# Konversi rupiah ke LGNS
jumlah_lgns = rupiah_input / price_lgns

# Simulasi pertumbuhan
hasil_1_hari = compound_growth(jumlah_lgns, rebase_yield, rebase_per_day, 1) * price_lgns
hasil_7_hari = compound_growth(jumlah_lgns, rebase_yield, rebase_per_day, 7) * price_lgns
hasil_30_hari = compound_growth(jumlah_lgns, rebase_yield, rebase_per_day, 30) * price_lgns

# Tampilkan hasil
st.subheader("📊 Estimasi Nilai Staking:")
st.write(f"💵 **Setelah 1 hari:** Rp {hasil_1_hari:,.0f}")
st.write(f"💵 **Setelah 1 minggu (7 hari):** Rp {hasil_7_hari:,.0f}")
st.write(f"💵 **Setelah 1 bulan (30 hari):** Rp {hasil_30_hari:,.0f}")

st.caption("Suku bunga: 0.26% setiap 8 jam (3x rebase/hari). Harga LGNS diperbarui dari CoinGecko.")
