from login import *
from sistema import abrir_cadastro

#inicia o código
def main():
    abrir_login(on_success=abrir_cadastro)

if __name__ == "__main__":
    main()