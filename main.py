from repositories.product_repository import ProductRepository
from services.product_service import ProductService
from ui.app_window import AppWindow


def main():
    repository = ProductRepository()
    service = ProductService(repository)

    app_window = AppWindow(service)
    app_window.mainloop()


if __name__ == "__main__":
    main()
