package main.service;

import main.entity.Journal;
import main.exception.JournalNotFoundException;
import main.repository.JournalRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class JournalServiceImpl implements JournalService {

    @Autowired
    private JournalRepository journalRepository;

    @Override
    public List<Journal> listJournal() {
        return (List<Journal>) journalRepository.findAll();
    }

    @Override
    public Journal findJournal(Integer id) {
        Optional<Journal> optionalApp = journalRepository.findById(id);
        if (optionalApp.isPresent()) {
            return optionalApp.get();
        } else {
            throw new JournalNotFoundException("Journal not fount");
        }
    }

    @Override
    public Journal addJournal(Journal journal) {
        return journalRepository.save(journal);
    }


}
