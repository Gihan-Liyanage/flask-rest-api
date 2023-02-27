from src import create_app
from src.utils import db
from werkzeug.security import generate_password_hash

def start():
    app = create_app()

    app.app_context().push()

    db.create_all()

    pwd = str(generate_password_hash('1234'))

    with db.engine.begin() as conn:
        response = conn.exec_driver_sql(f"INSERT INTO public.\"user\" (username, passwordhash, usertype) VALUES ('admin', 'pbkdf2:sha256:260000$b4TD3EOb7HrOpl58$077f8941e50b3458e21f5abf6df5ad393975b3684a42f786691732f5e0cab215', 'ADMIN')")
        print("SUPER USER Created:::::::::::::::::::;", response)
    
    app.run(use_reloader=False)

if __name__ == "__main__":
    start()