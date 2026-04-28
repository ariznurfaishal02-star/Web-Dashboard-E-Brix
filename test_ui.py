from playwright.sync_api import Page, expect

def test_ebrix(page: Page):
    print("\n[Robot] 1. ke web E-BRIX...")
    page.goto("https://dashboard-ebrix.streamlit.app/")
    bingkai = page.locator("iframe[title=\"streamlitApp\"]").content_frame
    
    print("[Robot] 2. Menunggu sistem utama siap...")
    expect(bingkai.get_by_text("RATA-RATA BRIX", exact=False)).to_be_visible(timeout=30000)
    
    #  MULAI 
    
    print("[Robot] 3. Membuka Dropdown BLOK LAHAN...")
    # Tambahkan force=True agar robot bisa berfungsi
    bingkai.get_by_text("Choose options").click(force=True)
    page.wait_for_timeout(1000) 
    page.keyboard.press("Escape") 
    
    print("[Robot] 4. Navigasi ke menu ANALISIS DATA...")
    bingkai.get_by_text("ANALISIS DATA", exact=False).click(force=True)
    page.wait_for_timeout(2000) 
    
    print("[Robot] 5. Kembali ke DASHBOARD PETA...")
    bingkai.get_by_text("DASHBOARD PETA", exact=False).click(force=True)
    expect(bingkai.get_by_text("RATA-RATA BRIX", exact=False)).to_be_visible(timeout=15000)
    page.wait_for_timeout(1000)
    
    print("[Robot] 6. Mengeklik tombol Reset Filter...")
    bingkai.get_by_text("Reset Filter", exact=False).click(force=True)
    page.wait_for_timeout(3000) 
    
    print("[Robot] BOOYAH! Semua skenario interaksi berhasil!")
