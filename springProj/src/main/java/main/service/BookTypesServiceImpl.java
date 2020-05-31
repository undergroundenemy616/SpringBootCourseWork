
package main.service;

import main.entity.BookTypes;
import main.exception.JournalNotFoundException;
import main.repository.BookTypesRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class BookTypesServiceImpl implements BookTypesService{

    @Autowired
    private BookTypesRepository bookTypesRepository;

    @Override
    public List<BookTypes> listBookTypes() {
        return (List<BookTypes>) bookTypesRepository.findAll();
    }

    @Override
    public BookTypes findBookType(Integer id) {
        Optional<BookTypes> optionalApp = bookTypesRepository.findById(id);
        if (optionalApp.isPresent()) {
            return optionalApp.get();
        } else {
            throw new JournalNotFoundException("BookType not fount");
        }
    }

    @Override
    public BookTypes addBookType(BookTypes type) {
        return bookTypesRepository.save(type);
    }
}