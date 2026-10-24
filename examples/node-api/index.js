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

// Return a product by ID.
app.get("/products/:id", (req, res) => {
    const productId = Number(req.params.id);

    if (!Number.isInteger(productId) || productId <= 0) {
        return res.status(400).json({
            error: "Product ID must be a positive integer.",
        });
    }
    const product = products.find((item) => item.id === productId);

    if (!product) {
        return res.status(404).json({
            error: `Product with ID ${productId} was not found.`,
        });
    }

    return res.json(product);
});

// Handle unknown routes.
app.use((req, res) => {
    res.status(404).json({
        error: "Route not found.",
    });
});

// Start the server.
app.listen(PORT, "0.0.0.0", () => {
    console.log(`Node.js API listening on port ${PORT}`);
});