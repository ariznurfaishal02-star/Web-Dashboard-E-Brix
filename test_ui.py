import re
from playwright.sync_api import Page, expect

def test_buka_dashboard(page: Page):
    print("\n[Robot] Membuka Chrome...")
    
    # 1. Menyuruh robot membuka web E-BRIX kamu
    page.goto("https://dashboard-ebrix.streamlit.app/")
    
    # 2. Tunggu sebentar (3 detik) agar Streamlit selesai loading data
    page.wait_for_timeout(3000)
    
    print("[Robot] Mengecek judul halaman...")
    
    # 3. Robot mengecek: Apakah ada teks "Dashboard Monitoring Brix" di layar?
    # (Sesuaikan teks ini dengan judul asli yang ada di web kamu ya)
    expect(page.locator("text=Dashboard Monitoring Brix")).to_be_visible()
    
    print("[Robot] Tes Selesai! Web aman.")
