package main.entity;

import main.SpringProjectApplication;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.persistence.*;

@Entity
public class Books {
    private static final Logger log = LoggerFactory.getLogger(SpringProjectApplication.class);

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "id")
    private Integer id;

    @Column(name = "name")
    private String name;

    @Column(name = "cnt")
    private Integer cnt;

    @ManyToOne
    @JoinColumn(name = "type_id")
    private BookTypes bookType;

    public Books(){
        log.info("fffsdfhdksjhfjdshfdshfdshfdsjfds");
    }

    public Books(String name, Integer cnt) {
        log.info("The ID ISSSSSFIFlkKFJKFHKLFKLJFJKFJSSS");
        this.name = name;
        this.cnt = cnt;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getCnt() {
        return cnt;
    }

    public void setCnt(Integer cnt) {
        this.cnt = cnt;
    }

    public BookTypes getBookType() {
        return bookType;
    }

    public void setBookType(BookTypes bookType) {
        this.bookType = bookType;
    }

    @Override
    public String toString() {
        return "Books{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", cnt=" + cnt +
                ", bookType=" + bookType +
                '}';
    }
}
