package com.example.Book_catalog_service.service;

import com.example.Book_catalog_service.model.Book;
import com.example.Book_catalog_service.repository.BookRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
public class BookService {

    @Autowired
    private BookRepository bookRepository;

    public Mono<Book> saveBook(Book book) {
        book.setCreatedIfNew();
        book.setUpdated();
        return bookRepository.save(book);
    }

    public Mono<Book> findById(Long id) {
        return bookRepository.findById(id);
    }

    public Flux<Book> findAll() {
        return bookRepository.findAll();
    }

    public Mono<Book> updateBook(Long id, Book bookDetails) {
        return bookRepository.findById(id)
                .flatMap(book -> {
                    book.setTitle(bookDetails.getTitle());
                    book.setAuthor(bookDetails.getAuthor());
                    book.setIsbn(bookDetails.getIsbn());
                    book.setPublisher(bookDetails.getPublisher());
                    book.setPublishedDate(bookDetails.getPublishedDate());
                    book.setPages(bookDetails.getPages());
                    book.setLanguage(bookDetails.getLanguage());
                    book.setDescription(bookDetails.getDescription());
                    book.setUpdated();
                    return bookRepository.save(book);
                });
    }

    public Mono<Void> deleteBook(Long id) {
        return bookRepository.deleteById(id);
    }
}
