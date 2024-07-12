package com.example.user_activities.model;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.Transient;
import org.springframework.data.relational.core.mapping.Table;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@Table("books")
public class Book {
    @Id
    private Long id;
    private String title;
    private String author;
    private String isbn;
    private String publisher;
    private LocalDate publishedDate;
    private Integer pages;
    private String language;
    private String description;
    private LocalDateTime created;
    private LocalDateTime updated;

    @Transient
    public void setCreatedIfNew() {
        if (this.created == null) {
            this.created = LocalDateTime.now();
        }
    }

    @Transient
    public void setUpdated() {
        this.updated = LocalDateTime.now();
    }
}
