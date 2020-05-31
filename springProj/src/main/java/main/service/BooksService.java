package main.service;

import main.entity.Books;

import java.util.List;

public interface BooksService {
    List<Books> listBooks();
    Books findBook(Integer id);
    Books addBook(Books book);
}
