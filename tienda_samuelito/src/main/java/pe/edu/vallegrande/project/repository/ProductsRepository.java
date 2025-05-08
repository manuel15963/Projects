package pe.edu.vallegrande.project.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pe.edu.vallegrande.project.model.Products;

import java.util.List;

public interface ProductsRepository extends JpaRepository<Products, Long> {
    List<Products> findByStatus(String status);
}
