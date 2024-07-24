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

    @Autowired
    private KafkaProducerService kafkaProducerService;

    public Mono<Book> saveBook(Book book) {
        book.setCreatedIfNew();
        book.setUpdated();
        return bookRepository.save(book)
                .doOnSuccess(savedBook -> kafkaProducerService.sendMessage("book-topic", "Libro creado: " + savedBook.getTitle()));
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
                    book.setPublisheddate(bookDetails.getPublisheddate());
                    book.setPages(bookDetails.getPages());
                    book.setLanguage(bookDetails.getLanguage());
                    book.setDescription(bookDetails.getDescription());
                    book.setStatus(bookDetails.getStatus());
                    book.setUpdated();
                    return bookRepository.save(book)
                            .doOnSuccess(updatedBook -> kafkaProducerService.sendMessage("book-topic", "Libro actualizado: " + updatedBook.getTitle()));
                });
    }

    public Mono<Void> deleteBook(Long id) {
        return bookRepository.findById(id)
                .flatMap(book -> {
                    book.setStatus("I");
                    return bookRepository.save(book).then();
                });
    }
}
