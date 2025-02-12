from sqladmin import Admin, ModelView
from app.core.database import engine, SessionLocal
from app.models.user import User
from fastapi import FastAPI

# Initialize Admin
def create_admin(app: FastAPI):
    admin = Admin(app=app, engine=engine)

    class UserAdmin(ModelView, model=User):
        column_list = [User.id, User.email, User.full_name, User.email_verified]
        name = "User"
        name_plural = "Users"
        icon = "fa fa-user"

    admin.add_view(UserAdmin)

    return admin
