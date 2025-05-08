package pe.edu.vallegrande.project.service;

import pe.edu.vallegrande.project.model.Categories;
import java.util.List;

public interface CategoriesService {
    List<Categories> findAll();
    Categories findById(Long id);
    Categories save(Categories category);
    Categories update(Long id, Categories category);
    void delete(Long id);
}
