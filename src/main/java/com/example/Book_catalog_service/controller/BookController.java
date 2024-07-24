package com.example.Book_catalog_service.controller;

import com.example.Book_catalog_service.model.Book;
import com.example.Book_catalog_service.service.BookService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api/books")
public class BookController {

    @Autowired
    private BookService bookService;

    @PostMapping
    public Mono<ResponseEntity<Book>> createBook(@RequestBody Book book) {
        return bookService.saveBook(book)
                .map(ResponseEntity::ok);
    }

    @GetMapping("/{id}")
    public Mono<ResponseEntity<Book>> getBookById(@PathVariable Long id) {
        return bookService.findById(id)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @GetMapping
    public Flux<Book> getAllBooks() {
        return bookService.findAll();
    }

    @PutMapping("/{id}")
    public Mono<ResponseEntity<Book>> updateBook(@PathVariable Long id, @RequestBody Book bookDetails) {
        return bookService.updateBook(id, bookDetails)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public Mono<ResponseEntity<Void>> deleteBook(@PathVariable Long id) {
        return bookService.deleteBook(id)
                .then(Mono.just(ResponseEntity.noContent().build()));
    }
}