CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    sale_date DATE NOT NULL
);