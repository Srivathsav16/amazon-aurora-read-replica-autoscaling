SELECT
    product_id,
    SUM(amount) AS total_sales
FROM sales
GROUP BY product_id
ORDER BY total_sales DESC;

SELECT
    sale_date,
    SUM(amount) AS daily_sales
FROM sales
GROUP BY sale_date
ORDER BY sale_date;

SELECT
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_revenue,
    AVG(amount) AS average_sale
FROM sales;