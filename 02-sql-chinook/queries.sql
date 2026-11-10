-- ============================================================
--  Project 02 · Chinook Customer & Sales Analysis
--  Database : Chinook (SQLite)
--  Run      : DB Browser for SQLite -> Execute (F5), or paste into
--             sqliteonline.com after importing the .sqlite file
-- ============================================================
--
--  HOW TO USE THIS FILE (important)
--  1. Read the query AND the comment above it.
--  2. Run it. Look at the result. Change the filter. Run again.
--  3. Close the file and REWRITE the query from memory.
--  4. Replace these comments with your own notes before you push.
--     If you can explain it, it is yours.
--
--  Coverage: SELECT, WHERE, JOIN, GROUP BY, ORDER BY, CTE,
--            window function, subquery, CASE WHEN
-- ============================================================


-- Q1 · BASIC FILTER
-- Question: which customers are based in the UK?
SELECT CustomerId, FirstName, LastName, City, Email
FROM Customer
WHERE Country = 'United Kingdom'
ORDER BY City;


-- Q2 · JOIN
-- Question: show tracks together with their genre, album and artist.
-- LEFT JOIN keeps tracks that have no album.
SELECT ar.Name  AS artist,
       al.Title AS album,
       t.Name   AS track,
       g.Name   AS genre,
       t.UnitPrice
FROM Track t
JOIN      Genre  g  ON g.GenreId  = t.GenreId
LEFT JOIN Album  al ON al.AlbumId = t.AlbumId
LEFT JOIN Artist ar ON ar.ArtistId = al.ArtistId
ORDER BY ar.Name, al.Title
LIMIT 50;


-- Q3 · GROUP BY
-- Question: revenue by billing country.
SELECT BillingCountry          AS country,
       COUNT(*)                AS invoices,
       ROUND(SUM(Total), 2)    AS revenue
FROM Invoice
GROUP BY BillingCountry
ORDER BY revenue DESC;


-- Q4 · JOIN + GROUP BY + ORDER BY + LIMIT
-- Question: who are the top 10 customers by total spend?
-- Note: || concatenates strings in SQLite.
SELECT c.CustomerId,
       c.FirstName || ' ' || c.LastName AS customer,
       c.Country,
       COUNT(i.InvoiceId)               AS orders,
       ROUND(SUM(i.Total), 2)           AS total_spend
FROM Customer c
JOIN Invoice i ON i.CustomerId = c.CustomerId
GROUP BY c.CustomerId
ORDER BY total_spend DESC
LIMIT 10;


-- Q5 · DATE FUNCTIONS
-- Question: monthly revenue trend.
-- strftime('%Y-%m', ...) works in SQLite. In SQL Server use FORMAT(),
-- in PostgreSQL use TO_CHAR().
SELECT strftime('%Y-%m', InvoiceDate) AS month,
       COUNT(*)                       AS invoices,
       ROUND(SUM(Total), 2)           AS revenue
FROM Invoice
GROUP BY month
ORDER BY month;


-- Q6 · AGGREGATES
-- Question: what does a typical invoice look like?
SELECT COUNT(*)              AS invoice_count,
       ROUND(AVG(Total), 2)  AS avg_invoice,
       ROUND(MIN(Total), 2)  AS min_invoice,
       ROUND(MAX(Total), 2)  AS max_invoice
FROM Invoice;


-- Q7 · CTE (WITH clause)
-- Question: which customers spend more than the average customer?
-- A CTE lets you build a result, then query it like a table.
WITH customer_spend AS (
    SELECT CustomerId, SUM(Total) AS total_spend
    FROM Invoice
    GROUP BY CustomerId
)
SELECT c.FirstName || ' ' || c.LastName AS customer,
       ROUND(cs.total_spend, 2)          AS total_spend
FROM customer_spend cs
JOIN Customer c ON c.CustomerId = cs.CustomerId
WHERE cs.total_spend > (SELECT AVG(total_spend) FROM customer_spend)
ORDER BY cs.total_spend DESC;


-- Q8 · WINDOW FUNCTION
-- Question: rank customers by spend inside each country.
-- RANK() OVER (PARTITION BY ... ORDER BY ...) is the pattern to memorise.
WITH spend AS (
    SELECT c.Country,
           c.CustomerId,
           c.FirstName || ' ' || c.LastName AS customer,
           SUM(i.Total)                     AS total_spend
    FROM Customer c
    JOIN Invoice i ON i.CustomerId = c.CustomerId
    GROUP BY c.CustomerId
)
SELECT Country,
       customer,
       ROUND(total_spend, 2) AS total_spend,
       RANK() OVER (PARTITION BY Country ORDER BY total_spend DESC) AS rank_in_country
FROM spend
ORDER BY Country, rank_in_country
LIMIT 40;


-- Q9 · SUBQUERY
-- Question: which tracks have never been sold?
SELECT t.TrackId, t.Name AS track, g.Name AS genre
FROM Track t
JOIN Genre g ON g.GenreId = t.GenreId
WHERE t.TrackId NOT IN (SELECT DISTINCT TrackId FROM InvoiceLine)
ORDER BY t.Name;


-- Q10 · CASE WHEN
-- Question: segment customers into High / Medium / Low spenders.
-- Adjust the thresholds after you look at Q4's results.
WITH spend AS (
    SELECT CustomerId, SUM(Total) AS total_spend
    FROM Invoice
    GROUP BY CustomerId
)
SELECT CASE
         WHEN total_spend >= 45 THEN 'High'
         WHEN total_spend >= 40 THEN 'Medium'
         ELSE 'Low'
       END                       AS segment,
       COUNT(*)                  AS customers,
       ROUND(AVG(total_spend), 2) AS avg_spend,
       ROUND(SUM(total_spend), 2) AS total_revenue
FROM spend
GROUP BY segment
ORDER BY total_revenue DESC;


-- ============================================================
--  YOUR TURN  (add your own query below this line)
--  Ideas:
--   - Which genre earns the most revenue?
--   - Which employee (support rep) looks after the most customers?
--   - What is the average number of tracks per invoice?
-- ============================================================
