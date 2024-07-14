package com.example.user_activities.services;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
public class KafkaConsumerService {

    @KafkaListener(topics = "user-topic", groupId = "user-library-management-group")
    public void consumeUserMessages(Object message) {
        System.out.println("Received user message: " + message);
    }

    @KafkaListener(topics = "book-topic", groupId = "book-catalog-service-group")
    public void consumeBookMessages(Object message) {
        System.out.println("Received book message: " + message);
    }

    @KafkaListener(topics = "activity-topic", groupId = "activities-service-group")
    public void consumeActivityMessages(Object message) {
        System.out.println("Received activity message: " + message);
    }
}
