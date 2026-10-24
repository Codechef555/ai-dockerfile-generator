 const express = require("express");

const app = express();
const PORT = Number(process.env.PORT) || 3000;

app.use(express.json());

// Sample product data.
const products = [
    { id: 1, name: "Laptop", price: 75000 },
    { id: 2, name: "Keyboard", price: 2500 },
    { id: 3, name: "Mouse", price: 1200 },
    { id: 4, name: "Monitor", price: 18000 },
];

app.get("/", (req, res) => {
    res.json({
        message: "Node.js API is running!",
        application: "Node API Demo",
        version: "1.0.0",
        docs: "Available endpoints: /health, /products, /products/:id",
    });
});

// Health-check endpoint.
app.get("/health", (req, res) => {
    res.status(200).json({
        status: "healthy",
    });
});

// Return all products.
app.get("/products", (req, res) => {
    res.json({
        count: products.length,
        products,
    });
});