package pe.edu.vallegrande.project.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pe.edu.vallegrande.project.model.Categories;

import java.util.List;
import java.util.Optional;

public interface CategoriesRepository extends JpaRepository<Categories, Long> {
    Optional<Categories> findByNameIgnoreCase(String name);
    List<Categories> findByStatus(String status);

}
