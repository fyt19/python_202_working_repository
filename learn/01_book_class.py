#!/usr/bin/env python3
"""
📚 ÖĞRENME: Book Sınıfı Nasıl Oluşturulur?

Bu dosyada Book sınıfının nasıl tasarlandığını öğreneceğiz.
"""

# 1. ADIM: Basit sınıf tanımı
class Book:
    """Kitap sınıfı - her bir kitabı temsil eder"""
    
    def __init__(self, title: str, author: str, isbn: str):
        """
        Constructor (yapıcı metod) - sınıf örneği oluştururken çalışır
        
        Args:
            title (str): Kitap başlığı
            author (str): Yazar adı
            isbn (str): ISBN numarası (benzersiz kimlik)
        """
        # Instance variables (örnek değişkenleri) tanımlama
        self.title = title
        self.author = author
        self.isbn = isbn
    
    # 2. ADIM: String temsili metodları
    def __str__(self) -> str:
        """Kitap bilgilerini okunaklı formatta döndürür"""
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"
    
    def __repr__(self) -> str:
        """Debug için string temsili"""
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"
    
    # 3. ADIM: Veri dönüştürme metodları
    def to_dict(self) -> dict:
        """Kitap bilgilerini dictionary formatında döndürür"""
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """Dictionary'den Book nesnesi oluşturur (class method)"""
        return cls(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn']
        )

# 4. ADIM: Sınıfı test etme
if __name__ == "__main__":
    print("🔍 BOOK SINIFI TEST EDİLİYOR")
    print("=" * 40)
    
    # Kitap nesnesi oluştur
    book = Book("Python Programming", "John Doe", "978-0134685991")
    
    print(f"📖 Kitap oluşturuldu: {book}")
    print(f"📝 Başlık: {book.title}")
    print(f"✍️  Yazar: {book.author}")
    print(f"🔢 ISBN: {book.isbn}")
    
    # Dictionary'e çevir
    book_dict = book.to_dict()
    print(f"\n📊 Dictionary formatı: {book_dict}")
    
    # Dictionary'den yeni kitap oluştur
    new_book = Book.from_dict(book_dict)
    print(f"🔄 Dictionary'den oluşturulan: {new_book}")
    
    # String metodları test et
    print(f"\n📝 __str__ metodu: {str(book)}")
    print(f"🔍 __repr__ metodu: {repr(book)}")

"""
🎯 ÖĞRENİLEN KAVRAMLAR:

1. CLASS TANIMI: class Book: ile sınıf tanımlanır
2. CONSTRUCTOR: __init__ metodu ile nesne oluşturulur
3. INSTANCE VARIABLES: self.title, self.author, self.isbn
4. STRING METODLARI: __str__ ve __repr__ ile string temsili
5. CLASS METHOD: @classmethod decorator ile sınıf metodu
6. TYPE HINTS: -> str, -> dict gibi tip belirtimleri

💡 İPUÇLARI:
- Her sınıf tek bir sorumluluğa sahip olmalı
- Metodlar açıklayıcı isimlere sahip olmalı
- Type hints kullanarak kod okunabilirliğini artır
"""
