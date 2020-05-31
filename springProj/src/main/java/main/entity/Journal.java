package main.entity;

import main.SpringProjectApplication;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.persistence.*;
import java.sql.Date;

@Entity
public class Journal {
    private static final Logger log = LoggerFactory.getLogger(SpringProjectApplication.class);

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "id")
    private Integer id;

    @ManyToOne
    @JoinColumn(name = "book_id", nullable = false)
    private Books book;

    @ManyToOne
    @JoinColumn(name = "client_id", nullable = true)
    private Clients client;

    @Column(name = "date_beg", nullable = true)
    private Date dateBegin;

    @Column(name = "date_end", nullable = true)
    private Date dateEnd;

    @Column(name = "date_ret", nullable = true)
    private Date dateReturn;

    public Journal(){
        log.info("FUCKFUCKFUCKsfdfdFUCKFUCKFUCK");
    }

    public Journal(Books book) {

        this.book = book;
        log.info("The ID ISSSSSFIFlkKFJKFHKLFKLJFJKFJSSS");
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Books getBook() {
        return book;
    }

    public void setBook(Books book) {
        this.book = book;
    }

    public Clients getClient() {
        return client;
    }

    public void setClient(Clients client) {
        this.client = client;
    }

    public Date getDateBegin() {
        return dateBegin;
    }

    public void setDateBegin(Date dateBegin) {
        this.dateBegin = dateBegin;
    }

    public Date getDateEnd() {
        return dateEnd;
    }

    public void setDateEnd(Date dateEnd) {
        this.dateEnd = dateEnd;
    }

    public Date getDateReturn() {
        return dateReturn;
    }

    public void setDateReturn(Date dateReturn) {
        this.dateReturn = dateReturn;
    }

    @Override
    public String toString() {
        return "Journal{" +
                "id=" + id +
                ", book=" + book +
                ", client=" + client +
                ", dateBegin=" + dateBegin +
                ", dateEnd=" + dateEnd +
                ", dateReturn=" + dateReturn +
                '}';
    }
}
