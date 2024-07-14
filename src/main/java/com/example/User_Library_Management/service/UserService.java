package com.example.User_Library_Management.service;

import com.example.User_Library_Management.model.User;
import com.example.User_Library_Management.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private KafkaProducerService kafkaProducerService;

    public Mono<User> saveUser(User user) {
        user.setPassword(passwordEncoder.encode(user.getPassword()));
        user.setCreated(LocalDateTime.now());
        user.setUpdated(LocalDateTime.now());
        return userRepository.save(user)
                .doOnSuccess(savedUser -> kafkaProducerService.sendMessage("user-topic", "Usuario creado: " + savedUser.getUsername()));
    }

    public Mono<User> findById(Long id) {
        return userRepository.findById(id);
    }

    public Mono<User> findByUsername(String username) {
        return userRepository.findByUsername(username);
    }

    public Mono<User> findByEmail(String email) {
        return userRepository.findByEmail(email);
    }

    public Flux<User> findAll() {
        return userRepository.findAll();
    }

    public Mono<User> updateUser(Long id, User userDetails) {
        return userRepository.findById(id)
                .flatMap(user -> {
                    user.setUsername(userDetails.getUsername());
                    user.setEmail(userDetails.getEmail());
                    user.setFirstname(userDetails.getFirstname());
                    user.setLastname(userDetails.getLastname());
                    user.setBirthdate(userDetails.getBirthdate());
                    user.setPhone(userDetails.getPhone());
                    user.setRole(userDetails.getRole());
                    user.setStatus(userDetails.getStatus());
                    user.setUpdated(LocalDateTime.now());
                    return userRepository.save(user)
                            .doOnSuccess(updatedUser -> kafkaProducerService.sendMessage("user-topic", "Usuario actualizado: " + updatedUser.getUsername()));
                });
    }

    public Mono<Void> deleteUser(Long id) {
        return userRepository.findById(id)
                .flatMap(user -> {
                    user.setStatus("I");
                    return userRepository.save(user)
                            .then(Mono.fromRunnable(() -> kafkaProducerService.sendMessage("user-topic", "Usuario eliminado: " + user.getUsername())));
                });
    }
}
