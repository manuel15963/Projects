package pe.edu.vallegrande.project.service.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import pe.edu.vallegrande.project.model.Categories;
import pe.edu.vallegrande.project.repository.CategoriesRepository;
import pe.edu.vallegrande.project.service.CategoriesService;

import java.util.List;

@Service
@RequiredArgsConstructor
public class CategoriesServiceImpl implements CategoriesService {

    private final CategoriesRepository repository;

    @Override
    public List<Categories> findAll() {
        return repository.findByStatus("1");
    }

    @Override
    public Categories findById(Long id) {
        return repository.findById(id).orElse(null);
    }

    @Override
    public Categories save(Categories category) {
        category.setStatus("1");
        return repository.save(category);
    }

    @Override
    public Categories update(Long id, Categories category) {
        Categories existing = repository.findById(id).orElse(null);
        if (existing != null) {
            category.setId(id);
            // Validar que status solo sea "1" o "0"
            if (!"1".equals(category.getStatus()) && !"0".equals(category.getStatus())) {
                category.setStatus(existing.getStatus()); // Si es inválido, mantiene el anterior
            }

            return repository.save(category);
        }
        return null;
    }

    @Override
    public void delete(Long id) {
        Categories category = repository.findById(id).orElse(null);
        if (category != null) {
            category.setStatus("0");
            repository.save(category);
        }
    }

}
