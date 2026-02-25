import pytest
from main import BooksCollector

class TestBooksCollector:


    @pytest.mark.parametrize('book_name', [
        'Война и мир',
        'a' * 40  # ровно 40 символов
    ])
    def test_add_new_book_valid_names(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert book_name in collector.get_books_genre()

    @pytest.mark.parametrize('test_data', [
    ('1984', 'Фантастика'),
    ('Гарри Поттер', 'Мультфильмы') 
    ])
    def test_set_book_genre_valid_genre(self, test_data):
        book_name, genre = test_data
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == genre

    @pytest.mark.parametrize('book_name, expected_genre', [
        ('Оно', 'Ужасы'),
        ('Без жанра', ''),  # книга без жанра
        ('Не существующая', None)  # несуществующая книга
    ])
    def test_get_book_genre_returns_correct_values(self, book_name, expected_genre):
        collector = BooksCollector()
        if book_name != 'Не существующая':
            collector.add_new_book(book_name)
            if expected_genre != '':
                collector.set_book_genre(book_name, expected_genre)

        assert collector.get_book_genre(book_name) == expected_genre

    @pytest.mark.parametrize('genre, expected_books', [
    ('Мультфильмы', ['Гарри Поттер', 'Винни-Пух']),
    ('Детективы', ['Шерлок Холмс'])
    ])
    def test_get_books_with_specific_genre(self, genre, expected_books):
        collector = BooksCollector()
        for book in expected_books:
            collector.add_new_book(book)
            collector.set_book_genre(book, genre)

        result_books = collector.get_books_with_specific_genre(genre)
        assert set(result_books) == set(expected_books)

    def test_get_books_genre_returns_dictionary(self):
        collector = BooksCollector()
        collector.add_new_book('Мастер и Маргарита')
        collector.set_book_genre('Мастер и Маргарита', 'Фантастика')
        collector.add_new_book('Винни-Пух')
        collector.set_book_genre('Винни-Пух', 'Мультфильмы')

        result = collector.get_books_genre()
        expected = {
            'Мастер и Маргарита': 'Фантастика',
            'Винни-Пух': 'Мультфильмы'
        }
        assert result == expected

    def test_get_books_for_children_filters_correctly(self):
        collector = BooksCollector()
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')
        collector.add_new_book('Винни-Пух')
        collector.set_book_genre('Винни-Пух', 'Мультфильмы')

        children_books = collector.get_books_for_children()
        assert 'Винни-Пух' in children_books
        assert 'Оно' not in children_books

    @pytest.mark.parametrize('favorite_book', [
        'Маленький принц',
        'Анна Каренина'
    ])
    def test_add_book_in_favorites(self, favorite_book):
        collector = BooksCollector()
        collector.add_new_book(favorite_book)
        collector.add_book_in_favorites(favorite_book)
        assert favorite_book in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_removes_book(self):
        collector = BooksCollector()
        collector.add_new_book('Преступление и наказание')
        collector.add_book_in_favorites('Преступление и наказание')
        collector.delete_book_from_favorites('Преступление и наказание')
        assert 'Преступление и наказание' not in collector.get_list_of_favorites_books()

    def test_get_list_of_favorites_books_returns_correct_list(self):
        collector = BooksCollector()
        collector.add_new_book('Война и мир')
        collector.add_book_in_favorites('Война и мир')

        favorites = collector.get_list_of_favorites_books()
        assert favorites == ['Война и мир']
