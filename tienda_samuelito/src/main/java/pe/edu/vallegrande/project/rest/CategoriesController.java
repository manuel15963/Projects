package pe.edu.vallegrande.project.rest;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import pe.edu.vallegrande.project.model.Categories;
import pe.edu.vallegrande.project.repository.CategoriesRepository;

import java.util.List;

@RestController
@RequestMapping("/api/categories")
@RequiredArgsConstructor
public class CategoriesController {

    private final CategoriesRepository repository;

    // ✅ Lista TODAS las categorías (activas e inactivas)
    @GetMapping
    public List<Categories> getAll() {
        return repository.findAll();
    }

    // ✅ Lista SOLO las activas
    @GetMapping("/active")
    public List<Categories> getActive() {
        return repository.findByStatus("1");
    }

    // 🆕 Obtener por ID (opcional)
    @GetMapping("/{id}")
    public Categories getById(@PathVariable Long id) {
        return repository.findById(id).orElse(null);
    }

    // 🆕 Crear
    @PostMapping
    public Categories create(@RequestBody Categories category) {
        category.setStatus("1"); // por defecto activa
        return repository.save(category);
    }

    // 🆕 Actualizar
    @PutMapping("/{id}")
    public Categories update(@PathVariable Long id, @RequestBody Categories category) {
        category.setId(id);
        return repository.save(category);
    }

    // 🆕 "Eliminar" lógico (cambia el status)
    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) {
        Categories category = repository.findById(id).orElse(null);
        if (category != null) {
            category.setStatus("0");
            repository.save(category);
        }
    }
}
