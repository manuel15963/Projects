GRANT ALL PRIVILEGES ON SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON DATABASE tienda_don_italo TO postgres;
GRANT USAGE ON SCHEMA public TO postgres;
GRANT CREATE ON SCHEMA public TO postgres;

CREATE DATABASE tienda_don_italo ENCODING 'UTF8' TEMPLATE template0;


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    doc CHAR(8) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone CHAR(9) NOT NULL,
	password VARCHAR (200) NOT NULL,
    active CHAR(1) DEFAULT 'A'

);


INSERT INTO users (username, last_name, doc, email, phone,password,active) VALUES
('Juan', 'Perez', '12345678', 'juan.perez@example.com', '123456789' , '123software', 'A'),
('Maria', 'Gomez', '87654321', 'maria.gomez@example.com', '987654321','123software', 'A');

SET client_encoding TO 'UTF8';

select * from users
	
 drop  table users
