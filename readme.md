# biblioteca

gestiona usuarios, libros y préstamos como si de una biblioteca real se tratase.

---

## ¿qué es esto?

una app modular en python que permite:

- crear usuarios
- añadir libros
- pedir prestado libros
- devolver libros
- controlar la reputación de los usuarios
- (próximamente) autenticación 🔐

el proyecto sigue una arquitectura limpia, diferenciando entre el dominio, la aplicación y la infraestructura del programa.

---

## cómo se usa

1. clona el repo

```bash
git clone https://github.com/ggusyyy/library.git
cd library
```

2. ejecuta el script principal

```bash
python main.py
```

---

## estructura del proyecto

```text
.
├── application/
│   ├── dtos/
│   └── use_cases/
├── domain/
│   ├── exceptions/
│   ├── models/
│   └── repositories/
├── infrastructure/
│   └── repositories/
│       ├── user/
│       └── book/
├── main.py
├── readme.md
└── tests/
```

---

## cosas que quiero añadir pronto

- [x] sistema de préstamos y devoluciones
- [x] control de reputación
- [ ] api rest con fastapi
- [ ] autenticación con jwt
- [ ] logging bonito
- [ ] persistencia en sqlite
- [ ] que solo admins puedan crear usuarios
- [ ] frontend (me gustaría, pero no estoy seguro cómo)

---

## requisitos

- python 3.10+
- (opcional) entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # en windows: venv\Scripts\activate
```

---

## contribuciones

se aceptan sugerencias, mejoras y memes. si encuentras un bug, abre un issue o mándame una paloma mensajera.

---

## licencia

esto es un proyecto educativo. usa el código como quieras. si te forras vendiendo esta app, invítame a una birra 🍻
