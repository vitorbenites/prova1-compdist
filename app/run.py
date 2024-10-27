# run.py

from src import app  # Importando a instância do app

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
