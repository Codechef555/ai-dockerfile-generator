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
    @GetMapping
    public Map<String, Object> home() {
        return Map.of(
            "message", "Java API is running!",
            "application", "Java API Demo",
            "version", "1.0.0",
            "endpoints", List.of(
                "/health",
                "/products",
                "/products/{id}"
            )
        );
    }
    @GetMapping("/health")
    public Map<String, String> healthCheck() {
        return Map.of("status", "healthy");
    }
    @GetMapping("/products")
    public Map<String, Object> getProducts() {
        return Map.of(
            "count", products.size(),
            "products", products
        );
    }
    @GetMapping("/products/{id}")
    public Map<String, Object> getProduct(@PathVariable int id) {
        return products.stream()
            .filter(product -> product.get("id").equals(id))
            .findFirst()
            .orElseThrow(() -> new ResponseStatusException(
                HttpStatus.NOT_FOUND,
                "Product with ID " + id + " was not found."
            ));
    }

}