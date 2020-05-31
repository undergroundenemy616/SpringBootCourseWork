package main.service;

import main.entity.Journal;

import java.util.List;

public interface JournalService {
    List<Journal> listJournal();
    Journal findJournal(Integer id);
    Journal addJournal(Journal journal);
}
