package main.entity;


import javax.persistence.*;

@Entity
public class BookTypes {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "id")
    private Integer id;

    @Column(name = "name")
    private String name;

    @Column(name = "fine")
    private Integer fine;

    @Column(name = "day_count")
    private Integer dayCount;

    public BookTypes(){
    }

    public BookTypes(String name, Integer fine, Integer dayCount) {
        this.name = name;
        this.fine = fine;
        this.dayCount = dayCount;
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

    public Integer getFine() {
        return fine;
    }

    public void setFine(Integer fine) {
        this.fine = fine;
    }

    public Integer getDayCount() {
        return dayCount;
    }

    public void setDayCount(Integer dayCount) {
        this.dayCount = dayCount;
    }

    @Override
    public String toString() {
        return "BookTypes{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", fine=" + fine +
                ", dayCount=" + dayCount +
                '}';
    }
}
