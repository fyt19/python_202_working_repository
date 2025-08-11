#!/usr/bin/env python3
"""
📚 ÖĞRENME: Test Yazma Nasıl Yapılır?

Bu dosyada Python'da test yazmanın temellerini öğreneceğiz.
pytest kütüphanesi kullanarak profesyonel testler yazacağız.
"""

import pytest
import tempfile
import os
import json

# Test edilecek sınıflar
class Book:
    """Test edilecek Book sınıfı"""
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

class Library:
    """Test edilecek Library sınıfı"""
    def __init__(self, filename: str = "library.json"):
        self.filename = filename
        self.books = []
        self.load_books()
    
    def add_book(self, book: Book) -> bool:
        if self.find_book(book.isbn):
            return False
        self.books.append(book)
        self.save_books()
        return True
    
    def find_book(self, isbn: str):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def save_books(self):
        books_data = [book.to_dict() for book in self.books]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(books_data, f, indent=2)
    
    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                books_data = json.load(f)
            self.books = [Book.from_dict(book_data) for book_data in books_data]

# 1. ADIM: Basit test fonksiyonları
def test_book_creation():
    """Book nesnesi oluşturma testi"""
    # Arrange (Hazırlık)
    title = "Test Book"
    author = "Test Author"
    isbn = "123-456-789"
    
    # Act (Eylem)
    book = Book(title, author, isbn)
    
    # Assert (Doğrulama)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn

def test_book_str_method():
    """Book.__str__ metodu testi"""
    book = Book("Ulysses", "James Joyce", "978-0199535675")
    expected = "Ulysses by James Joyce (ISBN: 978-0199535675)"
    
    assert str(book) == expected

def test_book_to_dict():
    """Book.to_dict metodu testi"""
    book = Book("Test Book", "Test Author", "123-456-789")
    book_dict = book.to_dict()
    
    assert book_dict['title'] == "Test Book"
    assert book_dict['author'] == "Test Author"
    assert book_dict['isbn'] == "123-456-789"
    assert isinstance(book_dict, dict)

# 2. ADIM: Test sınıfları (daha organize testler)
class TestBook:
    """Book sınıfı için test sınıfı"""
    
    def test_book_creation(self):
        """Book nesnesi oluşturma testi"""
        book = Book("Test Book", "Test Author", "123-456-789")
        
        assert book.title == "Test Book"
        assert book.author == "Test Author"
        assert book.isbn == "123-456-789"
    
    def test_book_from_dict(self):
        """Book.from_dict class method testi"""
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '123-456-789'
        }
        
        book = Book.from_dict(book_data)
        
        assert book.title == "Test Book"
        assert book.author == "Test Author"
        assert book.isbn == "123-456-789"
        assert isinstance(book, Book)
    
    def test_empty_strings(self):
        """Boş string'ler ile Book oluşturma testi"""
        book = Book("", "", "")
        
        assert book.title == ""
        assert book.author == ""
        assert book.isbn == ""

# 3. ADIM: Fixture'lar (test öncesi hazırlık)
@pytest.fixture
def sample_book():
    """Test için örnek kitap oluşturur"""
    return Book("Sample Book", "Sample Author", "999-999-999")

@pytest.fixture
def temp_library():
    """Test için geçici kütüphane oluşturur"""
    # Geçici dosya oluştur
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    temp_filename = temp_file.name
    temp_file.close()
    
    # Test kütüphanesi oluştur
    library = Library(temp_filename)
    
    # Test sonrası temizlik için yield
    yield library
    
    # Test sonrası geçici dosyayı sil
    if os.path.exists(temp_filename):
        os.unlink(temp_filename)

# 4. ADIM: Fixture kullanan testler
def test_library_with_fixture(sample_book, temp_library):
    """Fixture kullanan test örneği"""
    # Kitap ekle
    result = temp_library.add_book(sample_book)
    
    assert result == True
    assert len(temp_library.books) == 1
    assert temp_library.books[0] == sample_book

class TestLibrary:
    """Library sınıfı için test sınıfı"""
    
    def test_library_initialization(self, temp_library):
        """Library başlatma testi"""
        assert temp_library.books == []
        assert temp_library.filename.endswith('.json')
    
    def test_add_book(self, temp_library):
        """Kitap ekleme testi"""
        book = Book("Test Book", "Test Author", "123-456-789")
        
        result = temp_library.add_book(book)
        
        assert result == True
        assert len(temp_library.books) == 1
        assert temp_library.books[0] == book
    
    def test_add_duplicate_book(self, temp_library):
        """Aynı ISBN ile kitap ekleme testi"""
        book1 = Book("Test Book 1", "Test Author 1", "123-456-789")
        book2 = Book("Test Book 2", "Test Author 2", "123-456-789")
        
        # İlk kitabı ekle
        temp_library.add_book(book1)
        assert len(temp_library.books) == 1
        
        # Aynı ISBN ile ikinci kitabı eklemeye çalış
        result = temp_library.add_book(book2)
        
        assert result == False
        assert len(temp_library.books) == 1  # Hala 1 kitap olmalı
    
    def test_find_book(self, temp_library):
        """Kitap bulma testi"""
        book = Book("Test Book", "Test Author", "123-456-789")
        temp_library.add_book(book)
        
        found_book = temp_library.find_book("123-456-789")
        
        assert found_book == book
    
    def test_find_nonexistent_book(self, temp_library):
        """Var olmayan kitap bulma testi"""
        found_book = temp_library.find_book("999-999-999")
        
        assert found_book is None

# 5. ADIM: Parametrize edilmiş testler
@pytest.mark.parametrize("title,author,isbn", [
    ("Python Programming", "John Doe", "978-0134685991"),
    ("Data Science", "Jane Smith", "978-1118883665"),
    ("Machine Learning", "Bob Johnson", "978-0262035613"),
])
def test_book_creation_with_params(title, author, isbn):
    """Farklı parametrelerle Book oluşturma testi"""
    book = Book(title, author, isbn)
    
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn

# 6. ADIM: Exception testleri
def test_invalid_isbn_format():
    """Geçersiz ISBN formatı testi"""
    # Bu test başarısız olmalı çünkü ISBN çok kısa
    book = Book("Test", "Author", "123")
    
    # ISBN formatını kontrol et (basit kontrol)
    assert len(book.isbn) >= 5, "ISBN çok kısa olmamalı"

# 7. ADIM: Test çalıştırma
if __name__ == "__main__":
    print("🧪 TESTLER ÇALIŞTIRILIYOR...")
    print("=" * 40)
    
    # Basit testler
    test_book_creation()
    test_book_str_method()
    test_book_to_dict()
    
    print("✅ Tüm testler başarıyla geçti!")
    
    # pytest ile çalıştırmak için:
    # pytest 04_testing.py -v

"""
🎯 ÖĞRENİLEN KAVRAMLAR:

1. UNIT TESTING: Birim testleri ile kod kalitesi
2. PYTEST: Python test framework'ü
3. FIXTURES: Test öncesi hazırlık ve sonrası temizlik
4. ASSERTIONS: Beklenen sonuçları doğrulama
5. TEST CLASSES: Testleri organize etme
6. PARAMETRIZATION: Aynı testi farklı verilerle çalıştırma
7. EXCEPTION TESTING: Hata durumlarını test etme

💡 TEST YAZMA İPUÇLARI:

1. ARRANGE-ACT-ASSERT Pattern:
   - Arrange: Test verilerini hazırla
   - Act: Test edilecek kodu çalıştır
   - Assert: Sonuçları doğrula

2. Test isimleri açıklayıcı olmalı
3. Her test tek bir şeyi test etmeli
4. Testler birbirinden bağımsız olmalı
5. Fixture'lar ile kod tekrarını önle

🔧 TEST ÇALIŞTIRMA:

# Tüm testleri çalıştır
pytest 04_testing.py -v

# Belirli test sınıfını çalıştır
pytest 04_testing.py::TestBook -v

# Belirli test metodunu çalıştır
pytest 04_testing.py::TestBook::test_book_creation -v

# Coverage raporu ile
pytest 04_testing.py --cov=. --cov-report=html
"""
