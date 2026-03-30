-- ========================================
-- CLÍNICA VETERINARIA DAG - BASE DE DATOS
-- ========================================

-- TABLA DE USUARIOS
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLA DE MASCOTAS
CREATE TABLE IF NOT EXISTS mascotas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raza VARCHAR(100) NOT NULL,
    edad DECIMAL(3,1) NOT NULL,
    propietario VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre),
    INDEX idx_propietario (propietario)
);

-- TABLA DE CITAS
CREATE TABLE IF NOT EXISTS citas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mascota_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    motivo TEXT NOT NULL,
    veterinario VARCHAR(100) NOT NULL,
    estado VARCHAR(20) DEFAULT 'Agendada',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE,
    INDEX idx_fecha (fecha),
    INDEX idx_mascota_id (mascota_id)
);

-- TABLA DE HISTORIAL MÉDICO
CREATE TABLE IF NOT EXISTS historial (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mascota_id INT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha DATE NOT NULL,
    veterinario VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE,
    INDEX idx_mascota_id (mascota_id),
    INDEX idx_fecha (fecha),
    INDEX idx_tipo (tipo)
);

-- TABLA DE PRODUCTOS
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    cantidad INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre)
);

-- ========================================
-- INSERTAR USUARIO DE PRUEBA
-- ========================================
-- Username: admin
-- Password: admin123

INSERT INTO usuarios (usuario, password) 
VALUES ('admin', '$2b$12$KIXxPfxr3q1e8i2W3q8OaOq1d9q1d9q1d9q1d9q1d9q1d9q1d9q1d');

-- ========================================
-- INSERTAR ALGUNOS DATOS DE PRUEBA
-- ========================================

INSERT INTO mascotas (nombre, especie, raza, edad, propietario, telefono) 
VALUES 
('Max', 'Perro', 'Labrador', 3.5, 'Juan Pérez', '123456789'),
('Miau', 'Gato', 'Persa', 2, 'María García', '987654321'),
('Luna', 'Perro', 'Golden Retriever', 4, 'Carlos López', '555555555');

INSERT INTO citas (mascota_id, fecha, hora, motivo, veterinario, estado)
VALUES 
(1, '2026-04-01', '10:00', 'Revisión general', 'Dr. Rodriguez', 'Agendada'),
(2, '2026-04-02', '14:30', 'Vacunación', 'Dra. González', 'Agendada');

INSERT INTO historial (mascota_id, tipo, descripcion, fecha, veterinario)
VALUES 
(1, 'Vacuna', 'Vacuna antirrábica anual', '2025-12-15', 'Dr. Rodriguez'),
(2, 'Desparasitación', 'Desparasitación externa', '2025-11-20', 'Dra. González');

INSERT INTO productos (nombre, descripcion, precio, cantidad)
VALUES 
('Alimento Premium Perro', 'Alimento de alta calidad para perros adultos', 45.99, 50),
('Collar antipulgas', 'Collar antipulgas efectivo por 8 meses', 35.50, 20),
('Vitaminas para gatos', 'Complemento vitamínico para gatos', 28.75, 30);
