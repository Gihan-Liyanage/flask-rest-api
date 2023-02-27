from src import create_app
from src.utils import db
from decouple import config

def start():
    app = create_app()

    app.app_context().push()

    db.create_all()

    pwd = config('ADMIN_PASSWORD_HASH')

    with db.engine.begin() as conn:
        admin = conn.exec_driver_sql("SELECT * from public.\"user\" where username = 'admin'").first()
        if admin is None:
            conn.exec_driver_sql(f"INSERT INTO public.\"user\" (username, passwordhash, usertype) VALUES ('admin', \'{pwd}\', 'ADMIN')")
    
    app.run(use_reloader=False)

if __name__ == "__main__":
    start()