# Tkinter-Treeview-POO-

## Actividad 5: Visualización y creación

### Gestor de productos con Tkinter y POO
Nombre: Abdiel Antonio Rosario Tavarez
Matrícula: LR-2025-04460

Aplicación de escritorio para administrar productos con nombre, precio y
cantidad disponible. Permite crear, listar, editar y eliminar productos desde
un formulario y una tabla `Treeview`. El repositorio conserva los datos en
memoria mientras la aplicación está abierta.

## Ejecutar

```powershell
python main.py
```

El nombre es obligatorio, el precio debe ser numérico y no negativo, y la
cantidad debe ser un entero no negativo. Selecciona una fila para editarla o
eliminarla. Pulsa las cabeceras de nombre, precio o cantidad para ordenar la
tabla; la edición se puede cancelar con el botón visible en el formulario.

## Arquitectura

```text
models/product.py                  Modelo de producto
repositories/product_repository.py Almacenamiento en memoria
services/product_service.py        Lógica de negocio
ui/app_window.py                   Formulario y tabla
main.py                            Arranque e inyección de dependencias
```
