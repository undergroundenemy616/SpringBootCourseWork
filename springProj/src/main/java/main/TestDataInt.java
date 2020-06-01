package main;

import main.entity.Books;
import main.entity.User;
import main.repository.BooksRepository;
import main.repository.JournalRepository;
import main.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import java.util.Collections;

@Component
public class TestDataInt implements CommandLineRunner {

    @Autowired
    BooksRepository booksRepository;

    @Autowired
    UserRepository userRepository;

    @Autowired
    PasswordEncoder pwdEncoder;

    @Override
    public void run(String... args) throws Exception {
        //booksRepository.save(new Books("Django", 25));

        //userRepository.save(new User("ruby", pwdEncoder.encode("pwd"), Collections.singletonList("ROLE_USER")));
        //userRepository.save(new User("ruby2", pwdEncoder.encode("pwd"), Collections.singletonList("ROLE_ADMIN")));
    }
}
