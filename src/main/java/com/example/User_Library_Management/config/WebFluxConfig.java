package com.example.User_Library_Management.config;

import com.example.User_Library_Management.converter.LocalDateToLocalDateTimeConverter;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.convert.converter.Converter;
import org.springframework.data.convert.ReadingConverter;
import org.springframework.data.convert.WritingConverter;
import org.springframework.format.FormatterRegistry;
import org.springframework.web.reactive.config.WebFluxConfigurer;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

@Configuration
public class WebFluxConfig implements WebFluxConfigurer {

    private final LocalDateToLocalDateTimeConverter localDateToLocalDateTimeConverter;

    public WebFluxConfig(LocalDateToLocalDateTimeConverter localDateToLocalDateTimeConverter) {
        this.localDateToLocalDateTimeConverter = localDateToLocalDateTimeConverter;
    }

    @Override
    public void addFormatters(FormatterRegistry registry) {
        registry.addConverter(localDateToLocalDateTimeConverter);
    }
}
