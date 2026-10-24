package com.example.api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.Map;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
@RestController
@RequestMapping("/")
class ApiController{
    private final List<Map<String, Object>> products = List.of(
        Map.of("id", 1, "name", "Laptop", "price", 75000),
        Map.of("id", 2, "name", "Keyboard", "price", 2500),
        Map.of("id", 3, "name", "Mouse", "price", 1200),
        Map.of("id", 4, "name", "Monitor", "price", 18000)
    );
}