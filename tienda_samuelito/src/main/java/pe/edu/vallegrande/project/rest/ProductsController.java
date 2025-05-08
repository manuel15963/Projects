package pe.edu.vallegrande.project.rest;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import pe.edu.vallegrande.project.model.Products;
import pe.edu.vallegrande.project.service.ProductsService;

import java.util.List;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/api/products")
@RequiredArgsConstructor
public class ProductsController {

    private final ProductsService service;

    @GetMapping
    public List<Products> getAll() {
        return service.findAll();
    }

    @GetMapping("/{id}")
    public Products getById(@PathVariable Long id) {
        return service.findById(id);
    }

    @PostMapping
    public Products create(@RequestBody Products product) {
        return service.save(product);
    }

    @PutMapping("/{id}")
    public Products update(@PathVariable Long id, @RequestBody Products product) {
        return service.update(id, product);
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) {
        service.delete(id);
    }
}
