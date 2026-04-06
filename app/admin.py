from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.core.database import engine
from app.models.user import User


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        # TODO: replace with DB-based admin validation
        if username == "admin@example.com" and password == "admin123":
            request.session.update({"admin_logged_in": True})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return bool(request.session.get("admin_logged_in"))


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.full_name, User.email_verified]
    name = "User"
    name_plural = "Users"
    icon = "fa fa-user"


def create_admin(app: FastAPI):
    authentication_backend = AdminAuth(secret_key="super-secret-admin-key")

    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=authentication_backend,
    )

    admin.add_view(UserAdmin)
    return admin