package com.example.user_activities.services;

import com.example.user_activities.model.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Service
public class UserServiceClient {

    @Autowired
    private WebClient.Builder webClientBuilder;

    public Mono<User> getUserById(Long userId) {
        return webClientBuilder.build()
                .get()
                .uri("http://localhost:8080/api/users/{id}", userId)
                .retrieve()
                .bodyToMono(User.class);
    }
}
