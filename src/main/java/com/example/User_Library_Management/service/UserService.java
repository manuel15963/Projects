package com.example.User_Library_Management.service;

import com.example.User_Library_Management.model.User;
import com.example.User_Library_Management.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    public Mono<User> saveUser(User user) {
        user.setPassword(passwordEncoder.encode(user.getPassword()));
        return userRepository.save(user);

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

    public  Mono<User> updateUser(Long id , User userDetails) {
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
                    return userRepository.save(user);
                });
    }

    public Mono<Void> deleteUser(Long id) {
    return userRepository.findById(id)
            .flatMap(user -> {
                user.setStatus("I");
                return userRepository.save(user).then();
            });
    }
}
