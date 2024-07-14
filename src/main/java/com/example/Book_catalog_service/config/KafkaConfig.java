package com.example.Book_catalog_service.config;

import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.TopicBuilder;

@Configuration
public class KafkaConfig {

    @Bean
    public NewTopic userTopic() {
        return TopicBuilder.name("user-topic").build();
    }

    @Bean
    public NewTopic bookTopic() {
        return TopicBuilder.name("book-topic").build();
    }

    @Bean
    public NewTopic activityTopic() {
        return TopicBuilder.name("activity-topic").build();
    }
}
