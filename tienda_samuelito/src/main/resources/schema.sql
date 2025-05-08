create database tienda

use tienda
-- tables
-- Table: Categories
CREATE TABLE Categories (
                            category_id int  NOT NULL,
                            name varchar(60)  NULL,
                            CONSTRAINT Categories_pk PRIMARY KEY  (category_id)
);

-- Table: Customer
CREATE TABLE Customer (
                          customer_id int  NOT NULL,
                          name varchar(60)  NULL,
                          last_name varchar(60)  NULL,
                          email varchar(100)  NULL,
                          phone_number char(9)  NULL,
                          Identification_number char(8)  NULL,
                          password varchar(120)  NULL,
                          state varchar(10)  NULL,
                          CONSTRAINT Cliente_pk PRIMARY KEY  (customer_id)
);

-- Table: Detail_Sale
CREATE TABLE Detail_Sale (
                             id_detail int  NOT NULL,
                             product_id int  NOT NULL,
                             sale_id int  NOT NULL,
                             amount char(100)  NULL,
                             price decimal(8,2)  NULL,
                             CONSTRAINT Detalle_Venta_pk PRIMARY KEY  (id_detail)
);

-- Table: Products
CREATE TABLE Products (
                          product_id int  NOT NULL,
                          category_id int  NOT NULL,
                          name varchar(100)  NULL,
                          description varchar(100)  NULL,
                          unit_price decimal(8,2)  NULL,
                          stocks int  NULL,
                          expiration_date date  NULL,
                          CONSTRAINT Productos_pk PRIMARY KEY  (product_id)
);

-- Table: Sales
CREATE TABLE Sales (
                       sale_id int  NOT NULL,
                       customer_id int  NOT NULL,
                       date timestamp  NULL,
                       total decimal(8,2)  NULL,
                       state varchar(10)  NULL,
                       CONSTRAINT Ventas_pk PRIMARY KEY  (sale_id)
);

-- Table: Shopping
CREATE TABLE Shopping (
                          shopping_id int  NOT NULL,
                          supplier_id int  NOT NULL,
                          date date  NOT NULL,
                          total int  NOT NULL,
                          CONSTRAINT  Compras_pk PRIMARY KEY  (shopping_id)
);

-- Table: Shopping_Details
CREATE TABLE Shopping_Details (
                                  details_id int  NOT NULL,
                                  product_id int  NOT NULL,
                                  Shopping_id int  NOT NULL,
                                  amount char(200)  NULL,
                                  purchase_price decimal(8,2)  NULL,
                                  CONSTRAINT Detalle_Compra_pk PRIMARY KEY  (details_id)
);

-- Table: Suppliers
CREATE TABLE Suppliers (
                           supplier_id int  NOT NULL,
                           company_name varchar(100)  NULL,
                           phone char(9)  NULL,
                           address varchar(200)  NOT NULL,
                           status char(1)  NULL,
                           CONSTRAINT Proveedores_pk PRIMARY KEY  (supplier_id)
);

-- Table: User
CREATE TABLE "User" (
                        user_id int  NOT NULL,
                        username varchar(60)  NULL,
                        Email varchar(100)  NULL,
                        Password varchar(120)  NULL,
                        CONSTRAINT Usuario_pk PRIMARY KEY  (user_id)
);

-- foreign keys
-- Reference: Detail_Sale_Products (table: Detail_Sale)
ALTER TABLE Detail_Sale ADD CONSTRAINT Detail_Sale_Products
    FOREIGN KEY (product_id)
        REFERENCES Products (product_id);

-- Reference: Detail_Sale_Sales (table: Detail_Sale)
ALTER TABLE Detail_Sale ADD CONSTRAINT Detail_Sale_Sales
    FOREIGN KEY (sale_id)
        REFERENCES Sales (sale_id);

-- Reference: Products_categories (table: Products)
ALTER TABLE Products ADD CONSTRAINT Products_categories
    FOREIGN KEY (category_id)
        REFERENCES Categories (category_id);

-- Reference: Purchase_Details_Shopping (table: Shopping_Details)
ALTER TABLE Shopping_Details ADD CONSTRAINT Purchase_Details_Shopping
    FOREIGN KEY (Shopping_id)
        REFERENCES Shopping (shopping_id);

-- Reference: Sales_Customer (table: Sales)
ALTER TABLE Sales ADD CONSTRAINT Sales_Customer
    FOREIGN KEY (customer_id)
        REFERENCES Customer (customer_id);

-- Reference: Shopping_Details_Products (table: Shopping_Details)
ALTER TABLE Shopping_Details ADD CONSTRAINT Shopping_Details_Products
    FOREIGN KEY (product_id)
        REFERENCES Products (product_id);

-- Reference: Shopping_Suppliers (table: Shopping)
ALTER TABLE Shopping ADD CONSTRAINT Shopping_Suppliers
    FOREIGN KEY (supplier_id)
        REFERENCES Suppliers (supplier_id);

-- sequences
-- Sequence: Categorias_seq
CREATE SEQUENCE Categorias_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    NO CYCLE
    NO CACHE;

-- Sequence: Cliente_seq
CREATE SEQUENCE Cliente_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    NO CYCLE
    NO CACHE;

-- Sequence: Detalle_Compra_seq
CREATE SEQUENCE Detalle_Compra_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    NO CYCLE
    NO CACHE;

-- Sequence: Detalle_Venta_seq
CREATE SEQUENCE Detalle_Venta_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    NO CYCLE
    NO CACHE;

-- Sequence: Productos_seq
CREATE SEQUENCE Productos_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    NO CYCLE
    NO CACHE;

-- Sequence: Proveedores_seq
CREATE SEQUENCE Proveedores_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    NO CYCLE
    NO CACHE;

-- Sequence: Usuario_seq
CREATE SEQUENCE Usuario_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    NO CYCLE
    NO CACHE;

-- Sequence: Ventas_seq
CREATE SEQUENCE Ventas_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    NO CYCLE
    NO CACHE;

-- Sequence: compras_seq
CREATE SEQUENCE compras_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    NO CYCLE
    NO CACHE;

-- End of file.

