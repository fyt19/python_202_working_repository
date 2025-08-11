#!/usr/bin/env python3
"""
📚 ÖĞRENME: FastAPI Web Servisi Nasıl Oluşturulur?

Bu dosyada FastAPI kullanarak RESTful web servisi nasıl geliştirileceğini öğreneceğiz.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

# 1. ADIM: Pydantic modelleri (veri doğrulama)
class BookBase(BaseModel):
    """Kitap temel modeli"""
    title: str = Field(..., min_length=1, description="Kitap başlığı")
    author: str = Field(..., min_length=1, description="Yazar adı")
    isbn: str = Field(..., min_length=1, description="ISBN numarası")

class BookCreate(BookBase):
    """Kitap oluşturma modeli"""
    pass

class BookResponse(BookBase):
    """Kitap yanıt modeli"""
    id: int = Field(..., description="Kitap ID'si")
    
    class Config:
        """Pydantic konfigürasyonu"""
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Python Crash Course",
                "author": "Eric Matthes",
                "isbn": "978-1593276034"
            }
        }

class BookUpdate(BaseModel):
    """Kitap güncelleme modeli"""
    title: Optional[str] = Field(None, min_length=1, description="Kitap başlığı")
    author: Optional[str] = Field(None, min_length=1, description="Yazar adı")
    isbn: Optional[str] = Field(None, min_length=1, description="ISBN numarası")

class MessageResponse(BaseModel):
    """Mesaj yanıt modeli"""
    message: str = Field(..., description="Yanıt mesajı")
    success: bool = Field(..., description="İşlem başarılı mı?")

class BookList(BaseModel):
    """Kitap listesi modeli"""
    books: List[BookResponse] = Field(..., description="Kitap listesi")
    total: int = Field(..., description="Toplam kitap sayısı")

# 2. ADIM: Veri katmanı (basit in-memory storage)
class BookStore:
    """Basit kitap veri deposu"""
    
    def __init__(self):
        self.books = []
        self.next_id = 1
    
    def add_book(self, book_data: BookCreate) -> BookResponse:
        """Yeni kitap ekler"""
        # ISBN kontrolü
        if self.find_by_isbn(book_data.isbn):
            raise ValueError(f"ISBN {book_data.isbn} zaten mevcut")
        
        # Yeni kitap oluştur
        book = BookResponse(
            id=self.next_id,
            title=book_data.title,
            author=book_data.author,
            isbn=book_data.isbn
        )
        
        self.books.append(book)
        self.next_id += 1
        
        return book
    
    def get_all_books(self) -> List[BookResponse]:
        """Tüm kitapları döndürür"""
        return self.books.copy()
    
    def get_book_by_id(self, book_id: int) -> Optional[BookResponse]:
        """ID ile kitap bulur"""
        for book in self.books:
            if book.id == book_id:
                return book
        return None
    
    def find_by_isbn(self, isbn: str) -> Optional[BookResponse]:
        """ISBN ile kitap bulur"""
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def update_book(self, book_id: int, book_data: BookUpdate) -> Optional[BookResponse]:
        """Kitabı günceller"""
        book = self.get_book_by_id(book_id)
        if not book:
            return None
        
        # Sadece verilen alanları güncelle
        if book_data.title is not None:
            book.title = book_data.title
        if book_data.author is not None:
            book.author = book_data.author
        if book_data.isbn is not None:
            # ISBN değişiyorsa kontrol et
            existing = self.find_by_isbn(book_data.isbn)
            if existing and existing.id != book_id:
                raise ValueError(f"ISBN {book_data.isbn} zaten mevcut")
            book.isbn = book_data.isbn
        
        return book
    
    def delete_book(self, book_id: int) -> bool:
        """Kitabı siler"""
        book = self.get_book_by_id(book_id)
        if book:
            self.books.remove(book)
            return True
        return False
    
    def search_books(self, keyword: str) -> List[BookResponse]:
        """Anahtar kelime ile kitap arar"""
        keyword = keyword.lower()
        found_books = []
        
        for book in self.books:
            if (keyword in book.title.lower() or 
                keyword in book.author.lower()):
                found_books.append(book)
        
        return found_books

# 3. ADIM: FastAPI uygulaması oluşturma
app = FastAPI(
    title="📚 Kütüphane Yönetim Sistemi API",
    description="Python 202 Bootcamp projesi - FastAPI ile geliştirilmiş kütüphane yönetim sistemi",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Global veri deposu
book_store = BookStore()

# 4. ADIM: Ana sayfa endpoint'i
@app.get("/", response_model=MessageResponse)
async def root():
    """Ana sayfa"""
    return MessageResponse(
        message="📚 Kütüphane Yönetim Sistemi API'ye Hoş Geldiniz!",
        success=True
    )

# 5. ADIM: CRUD endpoint'leri
@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreate):
    """Yeni kitap oluşturur"""
    try:
        book = book_store.add_book(book_data)
        return book
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.get("/books", response_model=BookList)
async def get_books():
    """Tüm kitapları listeler"""
    books = book_store.get_all_books()
    return BookList(books=books, total=len(books))

@app.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: int):
    """ID ile kitap getirir"""
    book = book_store.get_book_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {book_id} ile kitap bulunamadı"
        )
    return book

@app.put("/books/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, book_data: BookUpdate):
    """Kitabı günceller"""
    try:
        book = book_store.update_book(book_id, book_data)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID {book_id} ile kitap bulunamadı"
            )
        return book
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.delete("/books/{book_id}", response_model=MessageResponse)
async def delete_book(book_id: int):
    """Kitabı siler"""
    success = book_store.delete_book(book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {book_id} ile kitap bulunamadı"
        )
    
    return MessageResponse(
        message=f"ID {book_id} ile kitap başarıyla silindi",
        success=True
    )

# 6. ADIM: Arama endpoint'i
@app.get("/books/search/{keyword}", response_model=BookList)
async def search_books(keyword: str):
    """Anahtar kelime ile kitap arar"""
    books = book_store.search_books(keyword)
    return BookList(books=books, total=len(books))

# 7. ADIM: İstatistik endpoint'i
@app.get("/stats")
async def get_stats():
    """Kütüphane istatistiklerini döndürür"""
    total_books = len(book_store.books)
    
    # Yazar istatistikleri
    authors = {}
    for book in book_store.books:
        author = book.author
        authors[author] = authors.get(author, 0) + 1
    
    # En çok kitabı olan yazar
    top_author = max(authors.items(), key=lambda x: x[1]) if authors else None
    
    return {
        "total_books": total_books,
        "unique_authors": len(authors),
        "top_author": {
            "name": top_author[0],
            "book_count": top_author[1]
        } if top_author else None,
        "authors": authors
    }

# 8. ADIM: Health check endpoint'i
@app.get("/health", response_model=MessageResponse)
async def health_check():
    """API sağlık kontrolü"""
    return MessageResponse(
        message="API çalışıyor ve sağlıklı",
        success=True
    )

# 9. ADIM: Hata yönetimi
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP exception'ları için özel handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            "success": False,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Genel exception'lar için handler"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Beklenmeyen bir hata oluştu",
            "success": False,
            "status_code": 500
        }
    )

# 10. ADIM: Middleware ve CORS
from fastapi.middleware.cors import CORSMiddleware

# CORS middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da spesifik origin'ler belirt
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 11. ADIM: Startup event
@app.on_event("startup")
async def startup_event():
    """Uygulama başlatıldığında çalışır"""
    # Örnek veriler ekle
    sample_books = [
        BookCreate(title="Python Crash Course", author="Eric Matthes", isbn="978-1593276034"),
        BookCreate(title="Automate the Boring Stuff", author="Al Sweigart", isbn="978-1593275990"),
        BookCreate(title="Fluent Python", author="Luciano Ramalho", isbn="978-1491946008"),
    ]
    
    for book_data in sample_books:
        try:
            book_store.add_book(book_data)
        except ValueError:
            pass  # Zaten varsa ekleme
    
    print("🚀 Kütüphane API'si başlatıldı!")
    print(f"📚 {len(book_store.books)} örnek kitap yüklendi")

# 12. ADIM: Program çalıştırma
if __name__ == "__main__":
    print("🌐 FastAPI Web Servisi Başlatılıyor...")
    print("📖 Swagger UI: http://localhost:8000/docs")
    print("📚 ReDoc: http://localhost:8000/redoc")
    print("🔍 API: http://localhost:8000")
    print("=" * 50)
    
    # Uvicorn server'ı başlat
    uvicorn.run(
        "06_fastapi_web_service:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Geliştirme için auto-reload
        log_level="info"
    )

"""
🎯 ÖĞRENİLEN KAVRAMLAR:

1. FASTAPI: Modern Python web framework'ü
2. PYDANTIC: Veri doğrulama ve serialization
3. REST API: RESTful web servisi tasarımı
4. CRUD OPERATIONS: Create, Read, Update, Delete işlemleri
5. MIDDLEWARE: Request/response işleme
6. EXCEPTION HANDLING: Hata yönetimi
7. API DOCUMENTATION: Otomatik API dokümantasyonu
8. CORS: Cross-Origin Resource Sharing

💡 FASTAPI İPUÇLARI:

1. Pydantic modelleri kullan: Veri doğrulama için
2. Type hints kullan: Kod okunabilirliği için
3. HTTP status codes: Doğru HTTP kodları döndür
4. Exception handling: Hataları düzgün şekilde ele al
5. API documentation: Swagger ve ReDoc otomatik oluşur
6. Middleware: CORS, authentication gibi işlemler için

🔧 GELİŞTİRME ÖNERİLERİ:

- Authentication ve authorization ekle
- Database entegrasyonu (SQLAlchemy, PostgreSQL)
- API rate limiting
- Request/response logging
- API versioning
- Docker containerization
- Unit ve integration testler
- CI/CD pipeline

🚀 ÇALIŞTIRMA:

# Gerekli paketleri yükle
pip install fastapi uvicorn[standard] pydantic

# Uygulamayı çalıştır
python 06_fastapi_web_service.py

# Veya uvicorn ile
uvicorn 06_fastapi_web_service:app --reload --host 0.0.0.0 --port 8000
"""
