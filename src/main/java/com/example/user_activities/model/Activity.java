package com.example.user_activities.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Table("user_activities")
public class Activity {
    @Id
    private Long id;
    private Long userId;
    private Long bookId;
    private String action;
    private LocalDateTime timestamp;
    private LocalDate dueDate;
    private Double fine;
}
