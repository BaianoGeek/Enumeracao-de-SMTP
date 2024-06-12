#!/usr/bin/python

import socket, sys, re

if len(sys.argv) != 2:
    print("Modo de uso: python3 smtpenum.py IP")
    sys.exit(0)

try:
    with open("lista.txt") as file:
        for linha in file:
            linha = linha.strip()  # Remove espaços em branco ao redor do nome do usuário
            try:
                # Cria um socket TCP e conecta ao servidor SMTP na porta 25
                tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp.connect((sys.argv[1], 25))
                
                # Recebe e exibe o banner do servidor SMTP (opcional, pode ser removido)
                banner = tcp.recv(1024).decode().strip()
                print(banner)
                
                # Envia o comando VRFY com o nome do usuário
                tcp.send(b"VRFY " + linha.encode() + b"\r\n")
                
                # Recebe a resposta do servidor
                user = tcp.recv(1024).decode()
                
                # Verifica se a resposta contém o código 252
                if re.search(r"^252", user):
                    # Exibe o nome do usuário encontrado
                    print("Usuário encontrado: " + user.split()[1].strip())
                
            except Exception as e:
                print(f"Erro ao conectar com {sys.argv[1]}: {e}")
            finally:
                tcp.close()  # Fecha o socket após cada tentativa
except FileNotFoundError:
    print("Arquivo lista.txt não encontrado")
