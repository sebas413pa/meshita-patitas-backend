# 🐾 Meshita Patitas Backend

API REST para aplicación web desarrollada en FastAPI y SQLite, creada para el centro de adopción Meshita Patitas.
Incluye módulos integrados como:

	•	Gestión de usuarios y roles
 	•	Gestión de campañas publicitarias
	•	Gestión de perros disponibles en adopción
	•	Apartado especial para gestión de solicitudes de donaciones y adopciones
 
---

## Requisitos

- Python 3.10+
- [pip](https://pip.pypa.io/en/stable/)
- [virtualenv](https://virtualenv.pypa.io/) (recomendado)

---

## Proceso de instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/sebas413pa/meshita-patitas-backend.git
   cd meshita-patitas-backend
   ````
2. **Crear el entorno virtual**
   ````bash
   python3 -m venv venv
   source venv/bin/activate   # MacOS/Linux
   venv\Scripts\activate      # Windows PowerShell
   ````
3. **Instalar dependencias**
   ````bash
   pip install -r requirements.txt
   ````
4. **Correr la aplicación**
   ````bash
   uvicorn app.main:app --reload
   ````
## Construcción y ejecución con docker 🐳
````
- docker build -t usuario/meshita-patitas-backend .
- docker push usuario/meshita-patitas-backend
- docker run -d -p 8000:8000 usuario/meshita-patitas-backend
````
