package com.example.user_activities.services;

import com.example.user_activities.model.Book;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Service
public class BookServiceClient {

    @Autowired
    private WebClient.Builder webClientBuilder;

    public Mono<Book> getBookById(Long bookId) {
        return webClientBuilder.build()
                .get()
                .uri("http://localhost:8081/api/books/{id}", bookId)
                .retrieve()
                .bodyToMono(Book.class);
    }
}
