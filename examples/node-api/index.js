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