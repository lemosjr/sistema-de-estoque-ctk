from login import abrir_login
from cadastro import abrir_cadastro

def main():
    abrir_login(on_success=abrir_cadastro)

if __name__ == "__main__":
    main()
