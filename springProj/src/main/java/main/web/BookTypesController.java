package main.web;

import main.entity.BookTypes;
import main.exception.JournalNotFoundException;
import main.repository.BookTypesRepository;
import main.service.BookTypesService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.Optional;

@org.springframework.web.bind.annotation.RestController
@RequestMapping("/libr")
public class BookTypesController {

    @Autowired
    private BookTypesRepository bookTypesRepository;

    private BookTypesService bookTypesService;

    @PostMapping(value = "/addBookType")
    public BookTypes addBookType(@RequestBody BookTypes newBookType){
        return bookTypesService.addBookType(newBookType);
    }

    @PutMapping("/editBookType/{id}")
    public ResponseEntity<Object> updateBookType(@RequestBody BookTypes newBookType, @PathVariable Integer id) {
        Optional<BookTypes> bookTypeOptional = bookTypesRepository.findById(id);
        if (!bookTypeOptional.isPresent())
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Book Type not found");
        newBookType.setId(id);
        bookTypesRepository.save(newBookType);
        return new ResponseEntity<>(newBookType, HttpStatus.OK);
    }

    @GetMapping("/bookTypes")
    public ResponseEntity<List<BookTypes>> getAllBookTypes(){
        List<BookTypes> list = bookTypesService.listBookTypes();
        return new ResponseEntity<>(list, HttpStatus.OK);
    }

    @GetMapping("/bookType/{id}")
    public ResponseEntity<BookTypes> getBookType(@PathVariable("id") Integer id){
        Optional<BookTypes> bookTypeOptional = bookTypesRepository.findById(id);
        try{
            return new ResponseEntity<>(bookTypesService.findBookType(id), HttpStatus.OK);
        } catch (JournalNotFoundException exception) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Journal not found");
        }
    }

    @DeleteMapping("/deleteBookType/{id}")
    public boolean deleteBookType(@PathVariable Integer id) {
        bookTypesRepository.deleteById(id);
        return true;
    }

    @Autowired
    public void setBookTypesService(BookTypesService bookTypesService) {
        this.bookTypesService = bookTypesService;
    }
}
