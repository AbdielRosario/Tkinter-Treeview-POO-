import math
import tkinter as tk
from tkinter import messagebox, ttk
from uuid import UUID

from services.product_service import ProductService


class AppWindow(tk.Tk):
    def __init__(self, service: ProductService) -> None:
        super().__init__()
        self.service = service

        self.title("Gestor de productos")
        self.geometry("760x480")
        self.minsize(600, 400)
        self._editing_product_id: UUID | None = None
        self._sort_directions = {
            "name": False,
            "price": False,
            "quantity": False,
        }

        self.create_widgets()
        self.render_data_table()

    def create_widgets(self) -> None:
        container = ttk.Frame(self, padding=16)
        container.pack(fill="both", expand=True)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(5, weight=1)

        ttk.Label(container, text="Nombre").grid(
            row=0, column=0, sticky="w", padx=(0, 12), pady=5
        )
        self.entry_name = ttk.Entry(container)
        self.entry_name.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(container, text="Precio").grid(
            row=1, column=0, sticky="w", padx=(0, 12), pady=5
        )
        self.entry_price = ttk.Entry(container)
        self.entry_price.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(container, text="Cantidad disponible").grid(
            row=2, column=0, sticky="w", padx=(0, 12), pady=5
        )
        self.entry_quantity = ttk.Entry(container)
        self.entry_quantity.grid(row=2, column=1, sticky="ew", pady=5)

        self.save_button = ttk.Button(
            container, text="Crear producto", command=self.create_product
        )
        self.save_button.grid(row=3, column=1, sticky="e", pady=(8, 16))
        self.cancel_button = ttk.Button(
            container,
            text="Cancelar edición",
            command=self.cancel_edit,
            state="disabled",
        )
        self.cancel_button.grid(row=3, column=0, sticky="w", pady=(8, 16))

        actions = ttk.Frame(container)
        actions.grid(row=4, column=0, columnspan=2, sticky="e", pady=(0, 8))
        ttk.Button(
            actions, text="Editar seleccionado", command=self.edit_product
        ).pack(side="left", padx=(0, 8))
        ttk.Button(
            actions, text="Eliminar seleccionado", command=self.delete_product
        ).pack(side="left")

        table_frame = ttk.Frame(container)
        table_frame.grid(row=5, column=0, columnspan=2, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "name", "price", "quantity"),
            show="headings",
        )
        self.tree.heading("id", text="ID")
        self.tree.heading(
            "name",
            text="Nombre",
            command=lambda: self.sort_table("name"),
        )
        self.tree.heading(
            "price",
            text="Precio",
            command=lambda: self.sort_table("price"),
        )
        self.tree.heading(
            "quantity",
            text="Cantidad",
            command=lambda: self.sort_table("quantity"),
        )
        self.tree.column("id", width=250, anchor="center")
        self.tree.column("name", width=200, anchor="w")
        self.tree.column("price", width=120, anchor="e")
        self.tree.column("quantity", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def create_product(self) -> None:
        name = self.entry_name.get().strip()
        price_text = self.entry_price.get().strip()
        quantity_text = self.entry_quantity.get().strip()
        errors = []

        if not name:
            errors.append("El nombre es obligatorio.")

        try:
            price = float(price_text)
            if not math.isfinite(price) or price < 0:
                errors.append("El precio debe ser un número no negativo.")
        except ValueError:
            errors.append("El precio debe ser un número válido.")

        try:
            quantity = int(quantity_text)
            if quantity < 0:
                errors.append("La cantidad debe ser un entero no negativo.")
        except ValueError:
            errors.append("La cantidad debe ser un número entero válido.")

        if errors:
            messagebox.showwarning(
                title="Datos inválidos",
                message="\n".join(errors),
                parent=self,
            )
            return

        if self._editing_product_id is None:
            self.service.create_one(name, price, quantity)
            success_message = "El producto se creó correctamente."
            success_title = "Producto creado"
        else:
            updated = self.service.update_one(
                self._editing_product_id, name, price, quantity
            )
            if not updated:
                messagebox.showwarning(
                    title="Producto no encontrado",
                    message="El producto ya no existe. Se actualizará la tabla.",
                    parent=self,
                )
                self.cancel_edit()
                self.render_data_table()
                return
            success_message = "El producto se actualizó correctamente."
            success_title = "Producto actualizado"

        self.cancel_edit()
        self.render_data_table()
        messagebox.showinfo(
            title=success_title,
            message=success_message,
            parent=self,
        )

    def edit_product(self) -> None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo(
                title="Selecciona un producto",
                message="Selecciona el producto que deseas editar.",
                parent=self,
            )
            return

        values = self.tree.item(selection[0], "values")
        self._editing_product_id = UUID(values[0])
        self.entry_name.delete(0, "end")
        self.entry_name.insert(0, values[1])
        self.entry_price.delete(0, "end")
        self.entry_price.insert(0, values[2])
        self.entry_quantity.delete(0, "end")
        self.entry_quantity.insert(0, values[3])
        self.save_button.config(text="Guardar cambios")
        self.cancel_button.config(state="normal")
        self.entry_name.focus_set()

    def delete_product(self) -> None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo(
                title="Selecciona un producto",
                message="Selecciona el producto que deseas eliminar.",
                parent=self,
            )
            return

        values = self.tree.item(selection[0], "values")
        product_id = UUID(values[0])
        confirmed = messagebox.askyesno(
            title="Confirmar eliminación",
            message=f"¿Deseas eliminar el producto «{values[1]}»?",
            parent=self,
        )
        if not confirmed:
            return

        deleted = self.service.delete_one(product_id)
        if not deleted:
            messagebox.showwarning(
                title="Producto no encontrado",
                message="El producto ya no existe. Se actualizará la tabla.",
                parent=self,
            )
        if self._editing_product_id == product_id:
            self.cancel_edit()
        self.render_data_table()

    def cancel_edit(self) -> None:
        self._editing_product_id = None
        self.save_button.config(text="Crear producto")
        self.cancel_button.config(state="disabled")
        self.clear_entries()

    def clear_entries(self) -> None:
        self.entry_name.delete(0, "end")
        self.entry_price.delete(0, "end")
        self.entry_quantity.delete(0, "end")
        self.entry_name.focus_set()

    def render_data_table(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for product in self.service.find_all():
            self.tree.insert(
                "",
                "end",
                values=(
                    str(product.id),
                    product.name,
                    product.price,
                    product.available_quantity,
                ),
            )

    def sort_table(self, column: str) -> None:
        reverse = self._sort_directions[column]
        items = self.tree.get_children("")

        if column == "name":
            key = lambda item: self.tree.set(item, column).casefold()
        elif column == "price":
            key = lambda item: float(self.tree.set(item, column))
        else:
            key = lambda item: int(self.tree.set(item, column))

        for index, item in enumerate(sorted(items, key=key, reverse=reverse)):
            self.tree.move(item, "", index)

        self._sort_directions[column] = not reverse
