#!/usr/bin/env python3
"""
📚 ÖĞRENME: Library Sınıfı Nasıl Oluşturulur?

Bu dosyada Library sınıfının nasıl tasarlandığını öğreneceğiz.
Library sınıfı, Book nesnelerini yöneten ana sınıftır.
"""

import json
import os
from typing import List, Optional

# Book sınıfını import et (aynı dizinde olmalı)
class Book:
    """Basit Book sınıfı"""
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
    
    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"
    
    def to_dict(self) -> dict:
        return {'title': self.title, 'author': self.author, 'isbn': self.isbn}
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        return cls(data['title'], data['author'], data['isbn'])

# 1. ADIM: Library sınıfı tanımı
class Library:
    """Kütüphane sınıfı - tüm kütüphane operasyonlarını yönetir"""
    
    def __init__(self, filename: str = "library.json"):
        """
        Constructor - kütüphane başlatılırken çalışır
        
        Args:
            filename (str): Kitapların saklanacağı JSON dosya adı
        """
        self.filename = filename
        self.books: List[Book] = []  # Kitap listesi
        self.load_books()  # Mevcut kitapları yükle
    
    # 2. ADIM: Kitap ekleme metodu
    def add_book(self, book: Book) -> bool:
        """
        Yeni bir kitabı kütüphaneye ekler
        
        Args:
            book (Book): Eklenecek kitap nesnesi
            
        Returns:
            bool: İşlem başarılı mı?
        """
        # ISBN kontrolü - aynı ISBN varsa ekleme
        if self.find_book(book.isbn):
            print(f"❌ Bu ISBN ({book.isbn}) zaten kütüphanede mevcut!")
            return False
        
        # Kitabı listeye ekle
        self.books.append(book)
        # Değişiklikleri kaydet
        self.save_books()
        print(f"✅ Kitap başarıyla eklendi: {book}")
        return True
    
    # 3. ADIM: Kitap silme metodu
    def remove_book(self, isbn: str) -> bool:
        """
        ISBN numarasına göre kitabı kütüphaneden siler
        
        Args:
            isbn (str): Silinecek kitabın ISBN'i
            
        Returns:
            bool: İşlem başarılı mı?
        """
        book = self.find_book(isbn)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"✅ Kitap başarıyla silindi: {book}")
            return True
        else:
            print(f"❌ ISBN {isbn} ile kitap bulunamadı.")
            return False
    
    # 4. ADIM: Kitap arama metodları
    def find_book(self, isbn: str) -> Optional[Book]:
        """ISBN ile belirli bir kitabı bulur"""
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def search_books(self, keyword: str) -> List[Book]:
        """Başlık veya yazar adında anahtar kelime arar"""
        keyword = keyword.lower()
        found_books = []
        
        for book in self.books:
            if (keyword in book.title.lower() or 
                keyword in book.author.lower()):
                found_books.append(book)
        
        return found_books
    
    # 5. ADIM: Veri saklama metodları (JSON)
    def save_books(self) -> None:
        """Kitapları JSON dosyasına kaydeder"""
        try:
            # Kitapları dictionary listesine çevir
            books_data = [book.to_dict() for book in self.books]
            
            # JSON dosyasına yaz
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(books_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"❌ Kitaplar kaydedilemedi: {e}")
    
    def load_books(self) -> None:
        """JSON dosyasından kitapları yükler"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    books_data = json.load(f)
                
                # Dictionary'lerden Book nesneleri oluştur
                self.books = [Book.from_dict(book_data) for book_data in books_data]
                print(f"📚 {len(self.books)} kitap yüklendi.")
            else:
                print(f"📁 '{self.filename}' dosyası bulunamadı. Yeni kütüphane oluşturuluyor.")
                
        except Exception as e:
            print(f"❌ Kitaplar yüklenemedi: {e}")
            self.books = []
    
    # 6. ADIM: Yardımcı metodlar
    def list_books(self) -> None:
        """Kütüphanedeki tüm kitapları listeler"""
        if not self.books:
            print("📚 Kütüphanede hiç kitap bulunmuyor.")
            return
        
        print(f"\n📚 Kütüphanede {len(self.books)} kitap bulunuyor:")
        print("-" * 60)
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book}")
        print("-" * 60)
    
    def get_stats(self) -> dict:
        """Kütüphane istatistiklerini döndürür"""
        return {
            'total_books': len(self.books),
            'filename': self.filename,
            'file_exists': os.path.exists(self.filename)
        }

# 7. ADIM: Sınıfı test etme
if __name__ == "__main__":
    print("🔍 LIBRARY SINIFI TEST EDİLİYOR")
    print("=" * 50)
    
    # Test kütüphanesi oluştur
    test_library = Library("test_library.json")
    
    # Kitaplar ekle
    print("\n📖 KİTAPLAR EKLENİYOR:")
    book1 = Book("Python Crash Course", "Eric Matthes", "978-1593276034")
    book2 = Book("Automate the Boring Stuff", "Al Sweigart", "978-1593275990")
    
    test_library.add_book(book1)
    test_library.add_book(book2)
    
    # Kitapları listele
    print("\n📋 KİTAPLAR LİSTELENİYOR:")
    test_library.list_books()
    
    # Kitap ara
    print("\n🔍 KİTAP ARAMA:")
    found_book = test_library.find_book("978-1593276034")
    if found_book:
        print(f"✅ Kitap bulundu: {found_book}")
    
    # Anahtar kelime ile ara
    print("\n🔎 ANAHTAR KELİME İLE ARAMA:")
    python_books = test_library.search_books("Python")
    print(f"Python kelimesi geçen {len(python_books)} kitap bulundu:")
    for book in python_books:
        print(f"  - {book}")
    
    # İstatistikler
    print("\n📊 İSTATİSTİKLER:")
    stats = test_library.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test dosyasını temizle
    if os.path.exists("test_library.json"):
        os.remove("test_library.json")
        print("\n🧹 Test dosyası temizlendi.")

"""
🎯 ÖĞRENİLEN KAVRAMLAR:

1. COMPOSITION: Library sınıfı Book nesnelerini içerir
2. DATA PERSISTENCE: JSON dosyasında veri saklama
3. ERROR HANDLING: try-except blokları ile hata yönetimi
4. TYPE HINTS: List[Book], Optional[Book] gibi tip belirtimleri
5. FILE I/O: JSON dosyası okuma/yazma
6. SEARCH ALGORITHMS: Linear search ile kitap arama

💡 İPUÇLARI:
- Her metod tek bir işi yapmalı
- Hata durumlarını mutlaka ele al
- Veri tutarlılığını koru (ISBN kontrolü gibi)
- Dosya işlemlerinde encoding belirt
"""
