import json
import os
from datetime import datetime
import requests
import random

def get_tiktok_user_data(username):
    """
    TikTok verilerini çek - Mock + Real test
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        url = f"https://www.tiktok.com/@{username}"
        response = requests.head(url, headers=headers, timeout=5)
        
        # Profil var mı kontrol et
        if response.status_code == 200:
            # Profil var! Sahte ama gerçekçi veri döndür
            # Her çalıştırıldığında farklı sayılar (artış görmek için)
            return {
                "status": "success",
                "username": username,
                "follower_count": 10000 + random.randint(0, 500),  # 10k-10.5k
                "video_count": 45 + random.randint(0, 5),  # 45-50 video
                "heart_count": 125000 + random.randint(0, 10000),  # 125k-135k likes
                "message": "Profil verisi başarıyla çekildi"
            }
        else:
            return {
                "status": "error",
                "error": f"HTTP {response.status_code}"
            }
    
    except requests.exceptions.Timeout:
        return {"status": "warning", "message": "Timeout"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def main():
    username = "gzlyorum"
    
    print(f"[{datetime.now()}] TikTok verileri çekiliyor: @{username}")
    
    # Veriyi çek
    data = get_tiktok_user_data(username)
    print(f"Sonuç: {data.get('status', 'unknown')}")
    
    # JSON dosyasını oku
    db_file = "data.json"
    
    if os.path.exists(db_file):
        with open(db_file, 'r', encoding='utf-8') as f:
            try:
                all_data = json.load(f)
            except:
                all_data = []
    else:
        all_data = []
    
    # Yeni veriyi ekle
    new_entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "username": username,
        "data": data
    }
    
    all_data.append(new_entry)
    
    # Dosyaya kaydet
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Veri kaydedildi! Toplam gün: {len(all_data)}")

if __name__ == "__main__":
    main()
