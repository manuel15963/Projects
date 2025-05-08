package pe.edu.vallegrande.project.rest;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import pe.edu.vallegrande.project.model.Categories;
import pe.edu.vallegrande.project.service.CategoriesService;

import java.util.List;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/api/categories")
@RequiredArgsConstructor
public class CategoriesController {

    private final CategoriesService service;

    @GetMapping
    public List<Categories> getAll() {
        return service.findAll();
    }

    @GetMapping("/{id}")
    public Categories getById(@PathVariable Long id) {
        return service.findById(id);
    }

    @PostMapping
    public Categories create(@RequestBody Categories category) {
        return service.save(category);
    }

    @PutMapping("/{id}")
    public Categories update(@PathVariable Long id, @RequestBody Categories category) {
        return service.update(id, category);
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) {
        service.delete(id);
    }
}
