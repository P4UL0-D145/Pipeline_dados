--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;



SET default_tablespace = '';

SET default_with_oids = false;


---
--- drop tables
---

DROP TABLE IF EXISTS dim_shippers CASCADE;
DROP TABLE IF EXISTS dim_us_states CASCADE;
DROP TABLE IF EXISTS dim_categories CASCADE;
DROP TABLE IF EXISTS dim_suppliers CASCADE;
DROP TABLE IF EXISTS dim_customers CASCADE;
DROP TABLE IF EXISTS dim_employees CASCADE;
DROP TABLE IF EXISTS dim_region CASCADE;
DROP TABLE IF EXISTS dim_customer_demographics CASCADE;
DROP TABLE IF EXISTS dim_territories CASCADE;
DROP TABLE IF EXISTS dim_customer_customer_demo CASCADE;
DROP TABLE IF EXISTS dim_employee_territories CASCADE;
DROP TABLE IF EXISTS dim_products CASCADE;
DROP TABLE IF EXISTS fact_orders CASCADE;
DROP TABLE IF EXISTS fact_order_details CASCADE;

-- Criação das tabelas com chaves primárias e estrangeiras

-- Tabela de transportadoras
CREATE TABLE dim_shippers (
    shipper_id SERIAL PRIMARY KEY,
    company_name VARCHAR(40) NOT NULL,
    phone VARCHAR(24)
);


-- Tabela de estados dos EUA
CREATE TABLE dim_us_states (
    state_id SERIAL PRIMARY KEY,
    state_name VARCHAR(100),
    state_abbr VARCHAR(2),
    state_region VARCHAR(50)
);


-- Tabela de categorias
CREATE TABLE dim_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(15) NOT NULL,
    description TEXT,
    picture BYTEA
);


-- Tabela de fornecedores
CREATE TABLE dim_suppliers (
    supplier_id SERIAL PRIMARY KEY,
    company_name VARCHAR(40) NOT NULL,
    contact_name VARCHAR(30),
    contact_title VARCHAR(30),
    address VARCHAR(60),
    city VARCHAR(15),
    region VARCHAR(15),
    postal_code VARCHAR(10),
    country VARCHAR(15),
    phone VARCHAR(24),
    fax VARCHAR(24),
    homepage TEXT
);


-- Tabela de clientes
CREATE TABLE dim_customers (
    customer_id CHAR(5) PRIMARY KEY,
    company_name VARCHAR(40) NOT NULL,
    contact_name VARCHAR(30),
    contact_title VARCHAR(30),
    address VARCHAR(60),
    city VARCHAR(15),
    region VARCHAR(15),
    postal_code VARCHAR(10),
    country VARCHAR(15),
    phone VARCHAR(24),
    fax VARCHAR(24)
);


-- Tabela de empregados
CREATE TABLE dim_employees (
    employee_id SERIAL PRIMARY KEY,
    last_name VARCHAR(20) NOT NULL,
    first_name VARCHAR(10) NOT NULL,
    title VARCHAR(30),
    title_of_courtesy VARCHAR(25),
    birth_date DATE,
    hire_date DATE,
    address VARCHAR(60),
    city VARCHAR(15),
    region VARCHAR(15),
    postal_code VARCHAR(10),
    country VARCHAR(15),
    home_phone VARCHAR(24),
    extension VARCHAR(4),
    photo BYTEA,
    notes TEXT,
    reports_to SMALLINT,
    photo_path VARCHAR(255)
);


-- Tabela de regiões
CREATE TABLE dim_region (
    region_id SERIAL PRIMARY KEY,
    region_description CHAR(50) NOT NULL
);


-- Tabela de demografia de clientes
CREATE TABLE dim_customer_demographics (
    customer_type_id CHAR(10) PRIMARY KEY,
    customer_desc TEXT
);


-- Tabela de territórios
CREATE TABLE dim_territories (
    territory_id VARCHAR(20) PRIMARY KEY,
    territory_description CHAR(50) NOT NULL,
    region_id SMALLINT NOT NULL,
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id)
);


-- Tabela de demo de clientes
CREATE TABLE dim_customer_customer_demo (
    customer_id CHAR(5) NOT NULL,
    customer_type_id CHAR(10) NOT NULL,
    PRIMARY KEY (customer_id, customer_type_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    FOREIGN KEY (customer_type_id) REFERENCES dim_customer_demographics(customer_type_id)
);


-- Tabela de territórios dos empregados
CREATE TABLE dim_employee_territories (
    employee_id SMALLINT NOT NULL,
    territory_id VARCHAR(20) NOT NULL,
    PRIMARY KEY (territory_id),
    FOREIGN KEY (employee_id) REFERENCES dim_employees(employee_id)
);


-- Tabela de produtos
CREATE TABLE dim_products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(40) NOT NULL,
    supplier_id SMALLINT,
    category_id SMALLINT,
    quantity_per_unit VARCHAR(20),
    unit_price REAL,
    units_in_stock SMALLINT,
    units_on_order SMALLINT,
    reorder_level SMALLINT,
    discontinued INTEGER NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES dim_suppliers(supplier_id),
    FOREIGN KEY (category_id) REFERENCES dim_categories(category_id)
);

-- Tabela de detalhes do pedido
CREATE TABLE fact_order_details (
    order_id VARCHAR(60) NOT NULL,
    product_id SMALLINT NOT NULL,
    unit_price REAL NOT NULL,
    quantity SMALLINT NOT NULL,
    discount REAL NOT NULL,
    FOREIGN KEY (product_id) REFERENCES dim_products(product_id)
);


-- Tabela de pedidos
CREATE TABLE fact_orders (
    order_id SERIAL PRIMARY KEY,
    customer_id CHAR(5),
    employee_id SMALLINT,
    order_date DATE,
    required_date DATE,
    shipped_date DATE,
    ship_via SMALLINT,
    freight REAL,
    ship_name VARCHAR(40),
    ship_address VARCHAR(60),
    ship_city VARCHAR(15),
    ship_region VARCHAR(15),
    ship_postal_code VARCHAR(10),
    ship_country VARCHAR(15),
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    FOREIGN KEY (employee_id) REFERENCES dim_employees(employee_id)
);