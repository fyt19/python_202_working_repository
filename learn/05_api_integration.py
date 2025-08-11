#!/usr/bin/env python3
"""
📚 ÖĞRENME: API Entegrasyonu Nasıl Yapılır?

Bu dosyada harici API'ler ile nasıl çalışılacağını öğreneceğiz.
Open Library API kullanarak ISBN'den kitap bilgisi çekeceğiz.
"""

import httpx
import asyncio
import json
from typing import Optional, Dict, Any

# Book sınıfı
class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
    
    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

# 1. ADIM: Senkron HTTP istekleri (requests benzeri)
def fetch_book_info_sync(isbn: str) -> Optional[Dict[str, Any]]:
    """
    ISBN ile kitap bilgisini senkron olarak çeker
    
    Args:
        isbn (str): Kitap ISBN numarası
        
    Returns:
        Optional[Dict]: Kitap bilgileri veya None
    """
    # Open Library API endpoint'i
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    
    try:
        # HTTP GET isteği gönder
        response = httpx.get(url, timeout=10.0)
        
        # HTTP durum kodunu kontrol et
        if response.status_code == 200:
            data = response.json()
            
            # ISBN anahtarını bul
            isbn_key = f"ISBN:{isbn}"
            if isbn_key in data:
                book_data = data[isbn_key]
                
                # Kitap bilgilerini çıkar
                title = book_data.get('title', 'Bilinmeyen Başlık')
                authors = book_data.get('authors', [])
                author = authors[0].get('name', 'Bilinmeyen Yazar') if authors else 'Bilinmeyen Yazar'
                
                return {
                    'title': title,
                    'author': author,
                    'isbn': isbn,
                    'raw_data': book_data
                }
            else:
                print(f"❌ ISBN {isbn} için kitap bulunamadı.")
                return None
        else:
            print(f"❌ API hatası: HTTP {response.status_code}")
            return None
            
    except httpx.TimeoutException:
        print(f"❌ Zaman aşımı: {isbn} için istek çok uzun sürdü.")
        return None
    except httpx.RequestException as e:
        print(f"❌ Ağ hatası: {e}")
        return None
    except json.JSONDecodeError:
        print(f"❌ JSON parse hatası: {isbn} için geçersiz yanıt.")
        return None
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        return None

# 2. ADIM: Asenkron HTTP istekleri (daha hızlı)
async def fetch_book_info_async(isbn: str) -> Optional[Dict[str, Any]]:
    """
    ISBN ile kitap bilgisini asenkron olarak çeker
    
    Args:
        isbn (str): Kitap ISBN numarası
        
    Returns:
        Optional[Dict]: Kitap bilgileri veya None
    """
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                isbn_key = f"ISBN:{isbn}"
                if isbn_key in data:
                    book_data = data[isbn_key]
                    
                    title = book_data.get('title', 'Bilinmeyen Başlık')
                    authors = book_data.get('authors', [])
                    author = authors[0].get('name', 'Bilinmeyen Yazar') if authors else 'Bilinmeyen Yazar'
                    
                    return {
                        'title': title,
                        'author': author,
                        'isbn': isbn,
                        'raw_data': book_data
                    }
                else:
                    print(f"❌ ISBN {isbn} için kitap bulunamadı.")
                    return None
            else:
                print(f"❌ API hatası: HTTP {response.status_code}")
                return None
                
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None

# 3. ADIM: Birden fazla ISBN'i paralel olarak çekme
async def fetch_multiple_books_async(isbns: list) -> list:
    """
    Birden fazla ISBN'i paralel olarak çeker
    
    Args:
        isbns (list): ISBN listesi
        
    Returns:
        list: Kitap bilgileri listesi
    """
    # Tüm istekleri paralel olarak başlat
    tasks = [fetch_book_info_async(isbn) for isbn in isbns]
    
    # Tüm isteklerin tamamlanmasını bekle
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Sonuçları işle
    books = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"❌ ISBN {isbns[i]} için hata: {result}")
        elif result:
            books.append(result)
    
    return books

# 4. ADIM: API wrapper sınıfı
class OpenLibraryAPI:
    """Open Library API için wrapper sınıfı"""
    
    def __init__(self, base_url: str = "https://openlibrary.org"):
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        """Async context manager girişi"""
        self.session = httpx.AsyncClient(timeout=10.0)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager çıkışı"""
        if self.session:
            await self.session.aclose()
    
    async def get_book_by_isbn(self, isbn: str) -> Optional[Dict[str, Any]]:
        """ISBN ile kitap bilgisi çeker"""
        url = f"{self.base_url}/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
        
        try:
            response = await self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            isbn_key = f"ISBN:{isbn}"
            
            if isbn_key in data:
                return self._parse_book_data(data[isbn_key], isbn)
            return None
            
        except Exception as e:
            print(f"❌ API hatası: {e}")
            return None
    
    def _parse_book_data(self, book_data: dict, isbn: str) -> Dict[str, Any]:
        """Ham API verisini parse eder"""
        title = book_data.get('title', 'Bilinmeyen Başlık')
        authors = book_data.get('authors', [])
        author = authors[0].get('name', 'Bilinmeyen Yazar') if authors else 'Bilinmeyen Yazar'
        
        # Ek bilgiler
        publisher = book_data.get('publishers', [{}])[0].get('name', 'Bilinmeyen Yayınevi') if book_data.get('publishers') else 'Bilinmeyen Yayınevi'
        publish_date = book_data.get('publish_date', 'Bilinmeyen Tarih')
        number_of_pages = book_data.get('number_of_pages', 'Bilinmeyen Sayfa')
        
        return {
            'title': title,
            'author': author,
            'isbn': isbn,
            'publisher': publisher,
            'publish_date': publish_date,
            'number_of_pages': number_of_pages,
            'raw_data': book_data
        }

# 5. ADIM: Hata yönetimi ve retry mekanizması
async def fetch_with_retry(isbn: str, max_retries: int = 3, delay: float = 1.0) -> Optional[Dict[str, Any]]:
    """
    Retry mekanizması ile kitap bilgisi çeker
    
    Args:
        isbn (str): ISBN numarası
        max_retries (int): Maksimum deneme sayısı
        delay (float): Denemeler arası bekleme süresi (saniye)
        
    Returns:
        Optional[Dict]: Kitap bilgileri veya None
    """
    for attempt in range(max_retries):
        try:
            async with OpenLibraryAPI() as api:
                result = await api.get_book_by_isbn(isbn)
                if result:
                    return result
                    
        except Exception as e:
            print(f"❌ Deneme {attempt + 1}/{max_retries} başarısız: {e}")
            
            if attempt < max_retries - 1:
                print(f"⏳ {delay} saniye sonra tekrar denenecek...")
                await asyncio.sleep(delay)
                delay *= 2  # Exponential backoff
    
    print(f"❌ ISBN {isbn} için tüm denemeler başarısız.")
    return None

# 6. ADIM: Test ve örnek kullanım
async def main():
    """Ana fonksiyon - API entegrasyonunu test eder"""
    print("🔍 API ENTEGRASYONU TEST EDİLİYOR")
    print("=" * 50)
    
    # Test ISBN'leri
    test_isbns = [
        "978-1593276034",  # Python Crash Course
        "978-0134685991",  # Python Programming
        "978-1118883665"   # Data Science
    ]
    
    print(f"\n📚 {len(test_isbns)} ISBN test ediliyor...")
    
    # 1. Senkron test
    print("\n1️⃣ SENKRON TEST:")
    for isbn in test_isbns[:1]:  # Sadece ilkini test et
        print(f"🔍 ISBN {isbn} aranıyor...")
        book_info = fetch_book_info_sync(isbn)
        if book_info:
            print(f"✅ Bulundu: {book_info['title']} by {book_info['author']}")
        else:
            print(f"❌ Bulunamadı")
    
    # 2. Asenkron test
    print("\n2️⃣ ASENKRON TEST:")
    for isbn in test_isbns[:1]:
        print(f"🔍 ISBN {isbn} asenkron aranıyor...")
        book_info = await fetch_book_info_async(isbn)
        if book_info:
            print(f"✅ Bulundu: {book_info['title']} by {book_info['author']}")
        else:
            print(f"❌ Bulunamadı")
    
    # 3. Paralel test
    print("\n3️⃣ PARALEL TEST:")
    print(f"🔍 {len(test_isbns)} ISBN paralel olarak aranıyor...")
    books = await fetch_multiple_books_async(test_isbns)
    print(f"✅ {len(books)} kitap bulundu:")
    for book in books:
        print(f"  📖 {book['title']} by {book['author']}")
    
    # 4. Retry mekanizması test
    print("\n4️⃣ RETRY MEKANİZMASI TEST:")
    invalid_isbn = "000-000-0000"  # Geçersiz ISBN
    print(f"🔍 Geçersiz ISBN {invalid_isbn} test ediliyor...")
    result = await fetch_with_retry(invalid_isbn, max_retries=2)
    if not result:
        print("✅ Retry mekanizması çalışıyor - geçersiz ISBN için sonuç döndürülmedi")

# 7. ADIM: Program çalıştırma
if __name__ == "__main__":
    try:
        # Asenkron main fonksiyonunu çalıştır
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Program kullanıcı tarafından sonlandırıldı.")
    except Exception as e:
        print(f"\n❌ Kritik hata: {e}")

"""
🎯 ÖĞRENİLEN KAVRAMLAR:

1. HTTP REQUESTS: HTTP istekleri gönderme ve alma
2. ASYNCHRONOUS PROGRAMMING: Asenkron kod ile paralel işlemler
3. API INTEGRATION: Harici API'ler ile çalışma
4. ERROR HANDLING: Ağ hatalarını ve API hatalarını yönetme
5. RETRY MECHANISMS: Başarısız istekleri tekrar deneme
6. CONTEXT MANAGERS: Async context manager kullanımı
7. PARALLEL PROCESSING: Birden fazla isteği paralel çalıştırma

💡 API ENTEGRASYON İPUÇLARI:

1. Timeout kullan: Ağ istekleri sonsuza kadar bekleyebilir
2. Hata yönetimi: Tüm olası hataları ele al
3. Rate limiting: API limitlerini aşmamaya dikkat et
4. Caching: Aynı istekleri tekrar yapma
5. Async kullan: Performans için asenkron programlama
6. Retry mekanizması: Geçici hatalar için tekrar dene

🔧 GELİŞTİRME ÖNERİLERİ:

- API response caching ekle
- Rate limiting implementasyonu
- Daha gelişmiş hata yönetimi
- API key authentication
- Response validation
- Logging ve monitoring
"""
