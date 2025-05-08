package pe.edu.vallegrande.project.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pe.edu.vallegrande.project.model.Categories;

import java.util.List;

public interface CategoriesRepository extends JpaRepository<Categories, Long> {
    List<Categories> findByStatus(String status);
}
