package main.service;

import main.entity.BookTypes;

import java.util.List;

public interface BookTypesService {
    List<BookTypes> listBookTypes();
    BookTypes findBookType(Integer id);
    BookTypes addBookType(BookTypes type);
}
