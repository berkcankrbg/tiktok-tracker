import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_tiktok_data(username):
    try:
        # TikTok profil sayfasını çek
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        url = f"https://www.tiktok.com/@{username}"
        response = requests.get(url, headers=headers, timeout=10)
        
        # Sayfadan veriyi çıkart
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # JSON verisi sayfada gömülü
        scripts = soup.find_all('script')
        data_dict = {}
        
        for script in scripts:
            if 'SIGI_STATE' in script.string or 'UserModule' in script.string:
                try:
                    # Basit parsing
                    content = script.string
                    if 'videoCount' in content:
                        data_dict['found'] = True
                        break
                except:
                    pass
        
        return {
            'username': username,
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        }
    
    except Exception as e:
        print(f"Hata: {str(e)}")
        return {'status': 'error', 'error': str(e)}

# Ana işlem
def main():
    username = "gzlyorum"  # BU KISMI DEĞİŞTİRME!
    
    # Veriyi çek
    data = get_tiktok_data(username)
    
    # JSON dosyasını oku
    db_file = "data.json"
    
    if os.path.exists(db_file):
        with open(db_file, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
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
    
    print("✅ Veri kaydedildi!")

if __name__ == "__main__":
    main()
