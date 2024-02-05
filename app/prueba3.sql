create database aplicacion;
use aplicacion;

#Tabla usuarios con acceso a app
create table administrador (
	id int primary key auto_increment,
    usuario varchar(20) not null,
    clave varchar(20) not null
);

INSERT INTO administrador (usuario, clave) values
('fernando','123456a');


#Tabla usuarios
CREATE TABLE usuarios (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    documentacion VARCHAR(9) NOT NULL,
    fecha_nacimiento date not null,
    genero ENUM('M', 'F') NOT NULL,
    correo VARCHAR(50) NOT NULL,
    institucion VARCHAR(50) NOT NULL,
    cargo ENUM('Coordinador', 'Profesor', 'Tutor', 'Alumno') NOT NULL,
    telefono VARCHAR(25) NOT NULL,
    direccion VARCHAR(150) NOT NULL,
    direccionp VARCHAR(150) NOT NULL
);


# Tabla curso
CREATE TABLE curso (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(ID),
    edicion INT NOT NULL,
    modulo INT NOT NULL,
    temas INT NOT NULL
);

# Tabla licencias
CREATE TABLE licencias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(ID),
    nombre_licencia VARCHAR(50) NOT NULL,
    fecha_alta DATE NOT NULL,
    fecha_baja DATE NOT NULL
);


INSERT INTO usuarios (nombre, apellidos, documentacion, fecha_nacimiento, genero, correo, institucion, cargo, telefono, direccion, direccionp)
VALUES ('Juan', 'Cigarran Recuero', '12345678P', '2000-01-01', 'M', 'correo1@example.com', 'Institucion1', 'Profesor', '123456789', 'Direccion1', 'DireccionP1'),
       ('Ana', 'García Serrano', '12345678Q', '2000-01-02', 'F', 'correo2@example.com', 'Institucion2', 'Coordinador', '987654321', 'Direccion2', 'DireccionP2'),
       ('Luis Manuel', 'Ruiz Gómez', '12345678E', '2000-01-03', 'M', 'correo3@example.com', 'Institucion3', 'Coordinador', '987652321', 'Direccion3', 'DireccionP3'),
       ('Elena','Ruiz Larrocha','12345678B','2000-01-04','F','correo4@example.com','Institucion4','Tutor','987652678','Direccion4','DireccionP4'),
       ('Fernando Javier', 'Chuquimarca Bolaños', '12345678F', '2000-01-05', 'M', 'correo5@example.com', 'Institucion5', 'Alumno', '987668321', 'Direccion5', 'DireccionP5');


-- Insertar licencias para usuarios específicos
INSERT INTO licencias (usuario_id, nombre_licencia, fecha_alta, fecha_baja) VALUES
(1, 'CANVA', '2022-01-29', '2023-01-29'),
(2, 'CLIP CHAMP', '2022-01-29', '2023-01-29'),
(3, 'CAP CUT', '2022-01-29', '2023-01-29'),
(4, 'FILMORA', '2022-01-29', '2023-01-29'),
(4, 'HOOTSUITE', '2022-01-29', '2023-01-29'),
(3, 'BUFFER', '2022-01-29', '2023-01-29'),
(2, 'ADOBE CCC Photoshop', '2022-01-29', '2023-01-29'),
(1, 'ADOBE CCC Premiere', '2022-01-29', '2023-01-29'),
(2, 'ADOBE CCC Lightroom', '2022-01-29', '2023-01-29'),
(3, 'ADOBE CCC Acrobat', '2022-01-29', '2023-01-29'),
(1, 'CHAT GPT4', '2022-01-29', '2023-01-29'),
(4, 'MIDJOURNEY 6', '2022-01-29', '2023-01-29'),
(4, 'Themis', '2022-01-29', '2023-01-29'),
(1, 'INLEXA', '2022-01-29', '2023-01-29');


select * from usuarios where genero = "F";

select * from usuarios inner join licencias on usuarios.id = licencias.usuario_id where usuarios.genero = "F";

select * from usuarios inner join licencias on usuarios.id = licencias.usuario_id where licencias.nombre_licencia = "CHAT GPT4";
