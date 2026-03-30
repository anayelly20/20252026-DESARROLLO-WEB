# 🏥 Clínica Veterinaria DAG - Guía de Setup

## 📋 Requisitos Previos

1. **MySQL Server** instalado y ejecutándose en `localhost:3306`
2. **Python 3.8+** instalado
3. **pip** (gestor de paquetes de Python)

## 🗄️ Configuración de la Base de Datos

### Paso 1: Crear la Base de Datos
```bash
mysql -u root -p
```

Luego ejecutar en MySQL:
```sql
CREATE DATABASE veterinaria;
USE veterinaria;
```

### Paso 2: Ejecutar el Script SQL
```bash
mysql -u root -p veterinaria < bd_clinica_veterinaria.sql
```

O copiar y pegar el contenido de `bd_clinica_veterinaria.sql` en MySQL.

## 🚀 Instalación y Ejecución

### Paso 1: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Ejecutar la Aplicación
```bash
python app.py
```

La aplicación estará disponible en: `http://127.0.0.1:5000`

## 🔐 Credenciales por Defecto

**Usuario:** `admin`  
**Contraseña:** `admin123`

## 📱 Funcionalidades

### 🏠 Inicio
- Panel de administrador
- Acceso rápido a todas las secciones

### 🐶 Mascotas
- Listar todas las mascotas registradas
- Agregar nueva mascota
- Ver detalles de mascota
- Editar información
- Eliminar registro

### 📅 Citas
- Agendar nuevas citas
- Ver todas las citas programadas
- Seleccionar mascota automáticamente
- Asignar veterinario
- Gestionar estado de cita

### 💉 Historial Médico
- Registrar vacunas
- Registrar tratamientos
- Registrar cirugías
- Realizar desparasitaciones
- Historial completo por mascota

### 🛒 Productos
- Inventario de productos veterinarios
- Agregar nuevos productos
- Editar precios y cantidades
- Eliminar productos

## 💾 Respaldo de la Base de Datos

Para hacer un respaldo:
```bash
mysqldump -u root -p veterinaria > respaldo_veterinaria.sql
```

Para restaurar:
```bash
mysql -u root -p veterinaria < respaldo_veterinaria.sql
```

## 🔧 Solución de Problemas

### Error: "Connection refused"
- Verificar que MySQL esté ejecutándose
- Por defecto en Windows: `C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld.exe`

### Error: "Access denied for user 'root'"
- Cambiar la contraseña en `Conexion/conexion.py`
- Línea: `password="",` (cambiar por tu contraseña MySQL)

### Error: "Table doesn't exist"
- Ejecutar nuevamente el script SQL `bd_clinica_veterinaria.sql`

## 📝 Estructura de Carpetas

```
Proyecto/
├── app.py                    # Archivo principal de Flask
├── requirements.txt          # Dependencias de Python
├── bd_clinica_veterinaria.sql # Script de base de datos
├── Conexion/
│   └── conexion.py          # Configuración de conexión MySQL
├── templates/               # Plantillas HTML
│   ├── base.html           # Plantilla base
│   ├── index.html          # Inicio
│   ├── login.html          # Login
│   ├── registro.html       # Registro
│   ├── mascotas.html       # Listar mascotas
│   ├── nueva_mascota.html  # Agregar mascota
│   ├── citas.html          # Listar citas
│   ├── nueva_cita.html     # Agendar cita
│   ├── historial.html      # Listar historial
│   ├── nuevo_historial.html# Agregar registro
│   ├── productos.html      # Listar productos
│   └── producto_form.html  # Agregar producto
└── data/                    # Archivos de datos
```

## 🎨 Estilos y Diseño

- Utiliza **Bootstrap 5** para responsive design
- Tema verde para la navegación (colores de clínica)
- Emojis para mejor interfaz visual
- Tablas con hover effect

## 📚 Endpoints Principales

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/` | GET | Página de inicio |
| `/login` | POST | Autenticación |
| `/registro` | POST | Crear cuenta |
| `/mascotas` | GET | Listar mascotas |
| `/nueva_mascota` | GET | Formulario nueva mascota |
| `/guardar_mascota` | POST | Guardar mascota |
| `/citas` | GET | Listar citas |
| `/nueva_cita` | GET | Formulario nueva cita |
| `/guardar_cita` | POST | Guardar cita |
| `/historial` | GET | Listar historial |
| `/nuevo_historial` | GET | Formulario nuevo historial |
| `/guardar_historial` | POST | Guardar historial |
| `/productos` | GET | Listar productos |

## 🎯 Próximas Mejoras Recomendadas

- [ ] Editar y eliminar mascotas
- [ ] Editar y eliminar citas
- [ ] Buscar y filtrar registros
- [ ] Exportar reportes en PDF
- [ ] Sistema de notificaciones
- [ ] Página de perfil de usuario
- [ ] Panel de estadísticas

¡Disfruta la aplicación! 🎉
