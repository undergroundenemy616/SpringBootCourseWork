package main.service;

import main.entity.Books;
import main.exception.JournalNotFoundException;
import main.repository.BooksRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class BooksServiceImpl implements BooksService {

    @Autowired
    private BooksRepository booksRepository;

    @Override
    public List<Books> listBooks() {
        return (List<Books>) booksRepository.findAll();
    }

    @Override
    public Books findBook(Integer id) {
        Optional<Books> optionalApp = booksRepository.findById(id);
        if (optionalApp.isPresent()) {
            return optionalApp.get();
        } else {
            throw new JournalNotFoundException("Book not fount");
        }
    }

    @Override
    public Books addBook(Books book) {
        return booksRepository.save(book);
    }
}
