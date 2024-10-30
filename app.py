import subprocess

# Lista de scripts a serem executados
scripts = ['stok.py', 'fort.py', 'asun.py']

# Executa cada script
for script in scripts:
    subprocess.run(['python', script], check=True)
