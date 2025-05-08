package pe.edu.vallegrande.project.service.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import pe.edu.vallegrande.project.model.Products;
import pe.edu.vallegrande.project.repository.ProductsRepository;
import pe.edu.vallegrande.project.service.ProductsService;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ProductsServiceImpl implements ProductsService {

    private final ProductsRepository repository;

    @Override
    public List<Products> findAll() {
        return repository.findByStatus("1");    }

    @Override
    public Products findById(Long id) {
        return repository.findById(id).orElse(null);
    }

    @Override
    public Products save(Products product) {
        product.setStatus("1");
        return repository.save(product);
    }

    @Override
    public Products update(Long id, Products product) {
        Products existing = repository.findById(id).orElse(null);
        if (existing != null) {
            product.setId(id);
            // Validación del status
            if (!"1".equals(product.getStatus()) && !"0".equals(product.getStatus())) {
                product.setStatus(existing.getStatus()); // mantener el valor anterior si es inválido
            }
            return repository.save(product);
        }
        return null;
    }


    @Override
    public void delete(Long id) {
        Products product = repository.findById(id).orElse(null);
        if (product != null) {
            product.setStatus("0");
            repository.save(product);
        }
    }

}
