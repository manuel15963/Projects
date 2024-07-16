package com.example.User_Library_Management.converter;

import org.springframework.core.convert.converter.Converter;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Component
public class LocalDateToLocalDateTimeConverter implements Converter<LocalDate, LocalDateTime> {

    @Override
    public LocalDateTime convert(LocalDate source) {
        return source.atStartOfDay();
    }
}
