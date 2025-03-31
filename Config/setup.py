import os
import subprocess
import sys

def check_python():
    try:
        subprocess.run([sys.executable, '--version'], check=True)
        print("Python está instalado!")
    except subprocess.CalledProcessError:
        print("Python não está instalado! Instalando Python...")
        return False
    return True

def create_virtualenv():
    subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
    print("Ambiente virtual criado!")

def activate_virtualenv():
    if sys.platform == "win32":
        activate_script = ".venv\\Scripts\\activate"
    else:
        activate_script = "source env/bin/activate"
    subprocess.run(activate_script, shell=True, check=True)
    print("Ambiente virtual ativado!")

def install_requirements():
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "Config/requirements.txt"], check=True)
    print("Dependências instaladas!")

def run_flask():
    subprocess.run([sys.executable, "Controller/similarity.py"], check=True)
    print("Servidor Flask rodando!")

def main():
    if not check_python():
        print("Por favor, instale o Python primeiro!")
        return
    
    create_virtualenv()
    activate_virtualenv()
    install_requirements()
    run_flask()

if __name__ == "__main__":
    main()
