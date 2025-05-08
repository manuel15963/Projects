package pe.edu.vallegrande.project.service;

import pe.edu.vallegrande.project.model.Products;
import java.util.List;

public interface ProductsService {
    List<Products> findAll();
    Products findById(Long id);
    Products save(Products product);
    Products update(Long id, Products product);
    void delete(Long id);
}
