package main;

import main.entity.Books;
import main.repository.BooksRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;


@SpringBootApplication
public class SpringProjectApplication {

    private static final Logger log = LoggerFactory.getLogger(SpringProjectApplication.class);
    public static void main(String[] args) {
        SpringApplication.run(SpringProjectApplication.class, args);

    }
    @Bean
    public CommandLineRunner test(BooksRepository repository){
        return args -> {
            repository.save(new Books("Fiasko", 25));

            for (Books app : repository.findAll()){
                log.info("The Book is: " + app.toString());
            }
        };
    }
}
