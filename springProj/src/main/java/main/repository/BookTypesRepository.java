package main.repository;

import main.entity.BookTypes;
import org.springframework.data.repository.CrudRepository;

public interface BookTypesRepository extends CrudRepository<BookTypes, Integer> {
}
