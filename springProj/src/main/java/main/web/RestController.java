package main.web;

import main.SpringProjectApplication;
import main.entity.BookTypes;
import main.entity.Books;
import main.entity.Journal;
import main.exception.JournalNotFoundException;
import main.repository.BookTypesRepository;
import main.repository.BooksRepository;
import main.repository.JournalRepository;
import main.service.BookTypesService;
import main.service.BooksService;
import main.service.JournalService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.Optional;

@org.springframework.web.bind.annotation.RestController
@RequestMapping("/libr")
public class RestController {

    @Autowired
    private JournalRepository journalRepository;

    @Autowired
    private BooksRepository booksRepository;

    private JournalService journalService;
    private BooksService booksService;

    private static final Logger log = LoggerFactory.getLogger(SpringProjectApplication.class);

    @PostMapping(value = "/addJournal")
    public Journal addJournal(@RequestBody Journal newJourn){
        return journalService.addJournal(newJourn);
    }

    @PutMapping("/editJournal/{id}")
    public ResponseEntity<Object> updateJournal(@RequestBody Journal newJourn, @PathVariable Integer id) {
        Optional<Journal> journalOptional = journalRepository.findById(id);
        if (!journalOptional.isPresent())
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Journal not found");
        newJourn.setId(id);
        journalRepository.save(newJourn);
        return new ResponseEntity<>(newJourn, HttpStatus.OK);
    }

    @GetMapping("/journals")
    public ResponseEntity<List<Journal>> getAllJournals(){
        List<Journal> list = journalService.listJournal();
        return new ResponseEntity<>(list, HttpStatus.OK);
    }

    @GetMapping("/journal/{id}")
    public ResponseEntity<Journal> getJournal(@PathVariable("id") Integer id){
        Optional<Journal> journalOptional = journalRepository.findById(id);
        try{
            return new ResponseEntity<>(journalService.findJournal(id), HttpStatus.OK);
        } catch (JournalNotFoundException exception) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Journal not found");
        }
    }

    @DeleteMapping("/deleteJournal/{id}")
    public boolean deleteJournal(@PathVariable Integer id) {
        journalRepository.deleteById(id);
        return true;
    }

    @PostMapping(value = "/addBook")
    public Books addBook(@RequestBody Books newBook){
        return booksService.addBook(newBook);
    }

    @PutMapping("/editBook/{id}")
    public ResponseEntity<Object> updateBook(@RequestBody Books newBook, @PathVariable Integer id) {
        Optional<Books> bookslOptional = booksRepository.findById(id);
        if (!bookslOptional.isPresent())
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Book not found");
        newBook.setId(id);
        booksRepository.save(newBook);
        return new ResponseEntity<>(newBook, HttpStatus.OK);
    }

    @GetMapping("/books")
    public ResponseEntity<List<Books>> getAllBooks(){
        List<Books> list = booksService.listBooks();
        return new ResponseEntity<>(list, HttpStatus.OK);
    }

    @GetMapping("/book/{id}")
    public ResponseEntity<Books> getBook(@PathVariable("id") Integer id){
        try{
            return new ResponseEntity<>(booksService.findBook(id), HttpStatus.OK);
        } catch (JournalNotFoundException exception) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Book not found");
        }
    }

    @DeleteMapping("/deleteBook/{id}")
    public boolean deleteBook(@PathVariable Integer id) {
        booksRepository.deleteById(id);
        return true;
    }



    @Autowired
    public void setJournalService(JournalService journalService) {
        this.journalService = journalService;
    }

    @Autowired
    public void setBooksService(BooksService booksService) {
        this.booksService = booksService;
    }

}
