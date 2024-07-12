package com.example.User_Library_Management.model;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Column;
import org.springframework.data.relational.core.mapping.Table;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@Table("users")
public class User {

    @Id
    private Long id;
    private String username;
    private String password;
    private String email;
    private String firstname;
    private String lastname;
    private LocalDate birthdate;
    private String phone;
    private String role;
    private String status;

    @Column("created")
    private LocalDateTime created;

    @Column("updated")
    private LocalDateTime updated;
}
