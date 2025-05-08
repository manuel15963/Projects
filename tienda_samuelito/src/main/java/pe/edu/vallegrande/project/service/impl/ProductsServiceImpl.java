package pe.edu.vallegrande.project.service.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import pe.edu.vallegrande.project.model.Categories;
import pe.edu.vallegrande.project.model.Products;
import pe.edu.vallegrande.project.repository.CategoriesRepository;
import pe.edu.vallegrande.project.repository.ProductsRepository;
import pe.edu.vallegrande.project.service.ProductsService;

import java.text.Normalizer;
import java.util.List;
import java.util.Optional;
import java.util.regex.Pattern;

@Service
@RequiredArgsConstructor
@Transactional
public class ProductsServiceImpl implements ProductsService {

    private final ProductsRepository   productsRepository;
    private final CategoriesRepository categoriesRepository;

    /* ───────────────────────── utilidades */
    private String normalize(String text) {
        String n = Normalizer.normalize(text, Normalizer.Form.NFD);
        return Pattern.compile("\\p{M}").matcher(n).replaceAll("").toLowerCase().trim();
    }

    /** Busca categoría por nombre (ignorando tildes y mayúsculas) o la crea */
    private Categories findOrCreateCategory(String rawName) {
        String normalized = normalize(rawName);

        // 1) intenta encontrarla
        Optional<Categories> opt = categoriesRepository.findAll().stream()
                .filter(c -> normalize(c.getName()).equals(normalized))
                .findFirst();

        if (opt.isPresent()) return opt.get();

        // 2) no existe → la crea
        Categories cat = new Categories();
        cat.setName(rawName.trim());
        cat.setStatus("1");
        return categoriesRepository.save(cat);
    }

    /* ───────────────────────── CRUD producto */
    @Override
    public List<Products> findAll() {
        return productsRepository.findByStatus("1");
    }

    @Override
    public Products findById(Long id) {
        return productsRepository.findById(id).orElse(null);
    }

    @Override
    public Products save(Products product) {
        // categoría nueva o existente
        Categories cat = findOrCreateCategory(product.getCategory().getName());
        product.setCategory(cat);

        product.setStatus("1");
        return productsRepository.save(product);
    }

    @Override
    public Products update(Long id, Products product) {
        return productsRepository.findById(id).map(existing -> {
            // categoría
            Categories cat = findOrCreateCategory(product.getCategory().getName());
            product.setCategory(cat);

            // copia campos que cambian
            product.setId(id);
            product.setStatus(("0".equals(product.getStatus()) || "1".equals(product.getStatus()))
                    ? product.getStatus() : existing.getStatus());

            return productsRepository.save(product);
        }).orElse(null);
    }

    @Override
    public void delete(Long id) {
        productsRepository.findById(id).ifPresent(p -> {
            p.setStatus("0");            // borrado lógico
            productsRepository.save(p);
        });
    }
}
