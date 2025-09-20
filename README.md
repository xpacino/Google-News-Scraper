# Google News Scraper

![Logo](https://upload.wikimedia.org/wikipedia/commons/3/33/Google_News.png)

Oxylabs Realtime API kullanılarak Google Haberler’den haber başlığı ve bağlantıları toplanır. 
Sonuçlar tarih damgalı JSON ve HTML dosyalarına kaydedilir; terminal çıktısı sade tutulur. 
Python 3.8+ uyumludur.

---

## Özellikler

- İstediğiniz anahtar kelimeyle **Google News haber sonuçlarını** çekme.  
- **Ülke bazlı lokalizasyon** (ör. Turkey, Germany, United States).  
- Çekilecek sonuç sayısını (`limit`) ve sayfa sayısını (`pages`) belirleme.  
- Sonuçları **JSON ve HTML dosyalarına** kaydetme.  
- Dinamik dosya isimlendirme:  
  ```
  bursa_2025_09_20.json
  bursa_2025_09_20.html
  ```

---

## Kullanım

Örnek çalıştırmalar:

```bash
# Varsayılan: 50 sonuç, Türkiye
python googlenews.py "bursa"

# 100 sonuç, Türkiye
python googlenews.py "adidas" "Turkey" 100

# 150 sonuç, ABD (3 sayfa × 50)
python googlenews.py "galatasaray" "United States" 50 3
```

Terminal çıktısı örneği:

```
✅ 100 haber kaydedildi → adidas_2025_09_20.json, adidas_2025_09_20.html
```

---

## API Parametreleri

Oxylabs API temel kimlik doğrulaması (Basic Auth) kullanır. Kullanıcı adı ve şifrenizi almanız gerekir.  
Ücretsiz deneme sürümünü alabilirsiniz.

| Parametre    | Tip    | Açıklama                           |
|--------------|--------|------------------------------------|
| `OX_USER`    | string | **Gerekli**. Oxylabs kullanıcı adınız |
| `OX_PASS`    | string | **Gerekli**. Oxylabs şifreniz      |
| `OX_API_URL` | string | **Gerekli**. `"https://realtime.oxylabs.io/v1/queries"` |

---

## Gereksinimler

- **Python 3.8.x veya üstü**
- `requests`
- `beautifulsoup4`

Kurulum:

```bash
pip3 install requests beautifulsoup4
```

---

## Örnek Çıktı (HTML)

HTML dosyası tarayıcıda şöyle görünür:

![Uygulama Ekran Görüntüsü](https://img001.prntscr.com/file/img001/WMmYtoXOR6abeUQOx6KxfA.png)
---

## Geliştirici

- [@xpacino](https://www.github.com/xpacino)

## Destek

TRX: `TV233GGoCdokwmeuSjmMk4kGCPGdxX1iVD`

![Support](https://img001.prntscr.com/file/img001/ewmcRxGXQriBcA69B6yWuQ.png)
