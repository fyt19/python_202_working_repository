#!/usr/bin/env python3
"""
📚 ÖĞRENME: Terminal Uygulaması Nasıl Oluşturulur?

Bu dosyada kullanıcı arayüzü olan terminal uygulamasının nasıl tasarlandığını öğreneceğiz.
"""

import sys
import os

# Book ve Library sınıflarını import et
class Book:
    """Basit Book sınıfı"""
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
    
    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

class Library:
    """Basit Library sınıfı"""
    def __init__(self):
        self.books = []
    
    def add_book(self, book: Book) -> bool:
        if not any(b.isbn == book.isbn for b in self.books):
            self.books.append(book)
            print(f"✅ Kitap eklendi: {book}")
            return True
        else:
            print(f"❌ Bu ISBN zaten mevcut!")
            return False
    
    def list_books(self):
        if not self.books:
            print("📚 Kütüphanede hiç kitap yok.")
            return
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book}")

# 1. ADIM: Ekran temizleme fonksiyonu
def clear_screen():
    """İşletim sistemine göre ekranı temizler"""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # macOS, Linux
        os.system('clear')

# 2. ADIM: Başlık ve menü fonksiyonları
def print_header():
    """Uygulama başlığını yazdırır"""
    print("=" * 60)
    print("📚 KÜTÜPHANE YÖNETİM SİSTEMİ 📚")
    print("=" * 60)

def print_menu():
    """Ana menüyü yazdırır"""
    print("\n🔍 MENÜ:")
    print("1. 📖 Kitap Ekle")
    print("2. 📋 Kitapları Listele")
    print("3. 🔍 Kitap Ara")
    print("4. 🚪 Çıkış")
    print("-" * 40)

# 3. ADIM: Kullanıcı girişi alma fonksiyonları
def get_user_input(prompt: str) -> str:
    """
    Kullanıcıdan güvenli giriş alır
    
    Args:
        prompt (str): Kullanıcıya gösterilecek mesaj
        
    Returns:
        str: Kullanıcının girdiği metin
    """
    try:
        user_input = input(prompt).strip()
        return user_input
    except KeyboardInterrupt:
        print("\n\n❌ İşlem iptal edildi.")
        return ""
    except EOFError:
        print("\n\n❌ Giriş hatası.")
        return ""

def get_validated_input(prompt: str, validator_func=None) -> str:
    """
    Doğrulanmış kullanıcı girişi alır
    
    Args:
        prompt (str): Kullanıcıya gösterilecek mesaj
        validator_func: Doğrulama fonksiyonu (opsiyonel)
        
    Returns:
        str: Doğrulanmış giriş
    """
    while True:
        user_input = get_user_input(prompt)
        
        if not user_input:
            print("❌ Giriş boş olamaz!")
            continue
        
        if validator_func and not validator_func(user_input):
            print("❌ Geçersiz giriş! Lütfen tekrar deneyin.")
            continue
        
        return user_input

# 4. ADIM: İş mantığı fonksiyonları
def add_book_manually(library: Library):
    """Manuel olarak kitap ekler"""
    print("\n📖 YENİ KİTAP EKLEME")
    print("-" * 30)
    
    # Kitap bilgilerini al
    title = get_validated_input("Kitap başlığı: ")
    if not title:
        return
    
    author = get_validated_input("Yazar adı: ")
    if not author:
        return
    
    isbn = get_validated_input("ISBN numarası: ")
    if not isbn:
        return
    
    # Kitap nesnesi oluştur ve ekle
    new_book = Book(title, author, isbn)
    library.add_book(new_book)

def search_books(library: Library):
    """Kitap arama işlemi"""
    print("\n🔍 KİTAP ARAMA")
    print("-" * 20)
    
    keyword = get_user_input("Aranacak kelime: ")
    if not keyword:
        return
    
    # Basit arama
    found_books = []
    for book in library.books:
        if (keyword.lower() in book.title.lower() or 
            keyword.lower() in book.author.lower()):
            found_books.append(book)
    
    if found_books:
        print(f"\n✅ '{keyword}' kelimesi geçen {len(found_books)} kitap bulundu:")
        for book in found_books:
            print(f"  📖 {book}")
    else:
        print(f"\n❌ '{keyword}' kelimesi geçen kitap bulunamadı.")

# 5. ADIM: Ana uygulama döngüsü
def main():
    """Ana uygulama fonksiyonu"""
    # Kütüphane nesnesi oluştur
    library = Library()
    
    # Ana döngü
    while True:
        try:
            # Ekranı temizle ve menüyü göster
            clear_screen()
            print_header()
            print_menu()
            
            # Kullanıcı seçimini al
            choice = get_user_input("Seçiminizi yapın (1-4): ")
            
            # Seçime göre işlem yap
            if choice == "1":
                add_book_manually(library)
            elif choice == "2":
                print("\n📋 KİTAPLAR LİSTELENİYOR:")
                library.list_books()
            elif choice == "3":
                search_books(library)
            elif choice == "4":
                print("\n👋 Kütüphane yönetim sisteminden çıkılıyor...")
                break
            else:
                print("❌ Geçersiz seçim! Lütfen 1-4 arasında bir sayı girin.")
            
            # Kullanıcıya devam etmesi için bekle
            if choice in ["1", "2", "3"]:
                input("\n⏸️  Devam etmek için Enter'a basın...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Program sonlandırılıyor...")
            break
        except Exception as e:
            print(f"\n❌ Beklenmeyen hata: {e}")
            input("Devam etmek için Enter'a basın...")

# 6. ADIM: Program başlatma
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Kritik hata: {e}")
        sys.exit(1)

"""
🎯 ÖĞRENİLEN KAVRAMLAR:

1. USER INTERFACE: Terminal tabanlı kullanıcı arayüzü
2. INPUT VALIDATION: Kullanıcı girişi doğrulama
3. ERROR HANDLING: Hata yönetimi ve kullanıcı dostu mesajlar
4. MAIN LOOP: Ana uygulama döngüsü
5. FUNCTIONAL PROGRAMMING: Fonksiyonlar ile kod organizasyonu
6. USER EXPERIENCE: Kullanıcı deneyimi iyileştirmeleri

💡 İPUÇLARI:
- Her fonksiyon tek bir işi yapmalı
- Kullanıcı girişlerini mutlaka doğrula
- Hata durumlarını kullanıcı dostu şekilde ele al
- Program akışını net ve anlaşılır tut
- Kullanıcıya ne yapacağını açıkça belirt

🔧 GELİŞTİRME ÖNERİLERİ:
- Renkli çıktılar ekle
- Dosya kaydetme/yükleme
- Daha gelişmiş arama algoritmaları
- Kitap kategorileri
- Kullanıcı hesapları
"""
