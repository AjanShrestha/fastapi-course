from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")


def get_db_conn_string():
    return f"host={config['HOST']} dbname={config['DATABASE_NAME']} user={config['USER']} password={config['PASSWORD']}"
