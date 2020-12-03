# -*- coding: utf-8 -*-

# Feito por Kripto-Sec(Jean)
#   Apenas para propositos educativos
#       Nao use para fins maliciosos
#           github: github.com/Kripto-Sec
#               Conhecimento nao e crime


import sys
import socket
import getopt
import threading
import subprocess

# Definindo algumas variaveis globais
listen               = False
command              = False
upload               = False
execute              = ""
alvo                 = ""
upload_destino       = ""
port                 = 0




def run_command(command):
    # corta a nova linha 
    command = command.rstrip()

    # executa o comando e obtem a saida de volta
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Erro ao executar comando. \r\n"
    
    #envia o output de volta ao client
    return output




def client_handler(client_socket):
    global upload
    global execute
    global command

    #check o upload
    if len(upload_destino):

        #Le em todos os bytes e escreve no destino
        file_buffer = ""

        # Continua lendo a data ate nenhuma esta mais disponivel
        while True:
            data = client_socket.recv(1024)

            if not data:
                break

            else:
                file_buffer += data
        
        # agora pegamos os byts e tentamos escrevê-los
        try:
            
            file_descriptor = open(upload_destino, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            # reconhece que escrevemos o arquivo
            client_socket.send("Arquivo salvo com sucesso em %s\r\n"% upload_destino)
        except:
            client_socket.send("Falha ao tentar salvar em %s\r\n"% upload_destino)

    # Check pra execucao do comando
    if len(execute):

        #roda o comando
        output = run_command(execute)      

        client_socket.send(output)

    # Agora vamos para outro loop se a command shell for chamada
    if command:
        
        while True:
            # Mostra um prompt simples
            client_socket.send("Command >> ")

                #agora recebe ate vermos um feed de linhas
                
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            # Envia de volta o output do comando
            response = run_command(cmd_buffer)    

            # Manda de volta  o response
            client_socket.send(response)



def server_loop():
    global alvo
    global port

    # se nenhum alvo for definido
    # nos iremos ouvir em todas as interfaces
    if not len(alvo):
        alvo = "0.0.0.0"

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((alvo,port))
    print ('\033[1;96m'+"[+] Aguardando conexao em %s:%s"%(alvo, port))+'\033[0;0m'

    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        print ('\033[1;96m'+"[+] Conexao iniciada em %s:%s"%(alvo, port))+'\033[0;0m'

        # Cria um topico novo para o client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   #print ("Conexão em %s:%s" %(alvo, port))
    try:
        # conecta ao seu host alvo
        client.connect((alvo,port))

        if len(buffer):
            client.send(buffer)

        while True:
            #agora espera a data voltar 
            recv_len = 1
            response = ""

            while recv_len:

                data    = client.recv(4096)
                recv_len = len(data)
                response+= data

                if recv_len < 4096:
                    break

            print '\033[1;97m'+response,

            #espera por mais inputs   
            buffer = raw_input("")
            buffer += "\n"

            # envia ela off
            client.send(buffer)
    
    except:

        print ('\033[1;31m'+"[*] Saindo!."+'\033[0;0m')

        #rompe a conexao
        client.close()


def usar():
    print ('\033[1;96m'+"Python Net Tool")
    print ("")
    print ("Como usar: pynet.py -t host_alvo -p")
    print ("-l --listen                  - Ira \"escutar\" em [host]:[port] para")
    print ("                               entrada de conexões")

    print ("-e --execute=file_to_run     - executa o arquivo fornecido em uma")
    print ("                               conexao recebida")

    print ("-c --command                 - Inicia uma command shell")
    print ("-u --upload=destino          - Ao receber a conexao faz um upload")
    print ("                               pra [destino]")
    
    print ("")
    print ("")
    print ("Exemplos: ")
    print ("pynet.py -a 192.168.0.1 -p 5555 -l -c")
    print ("pynet.py -a 192.168.0.1 -p 5555 -l -u=c:\\\ alvo.exe")
    print ("pynet.py -a 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print "echo 'ABCDEFGHI' | ./pynet.py -t 192.168.0.105 -p 135"+'\033[0;0m'
    sys.exit(0)




def main():
    global listen
    global port
    global execute
    global command
    global upload_destino
    global alvo

    if not len(sys.argv[1:]):
        usar()
    # Le as opcoes de linha de comando
    try:

        opts, args = getopt.getopt(sys.argv[1:],"hle:a:p:cu",
        ["help","listen", "execute", "alvo", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print str(err)    
        usar()
    
    for o,a in opts:
        if o in ("-h", "--help"):
            usar()
        
        elif o in ("-l", "--listen"):
            listen =  True
        
        elif o in ("-e", "--execute"):
            execute = a
        
        elif o in ("-c", "--commnadshell"):
            command = True
        
        elif o in ("-u", "upload"):
            upload_destino = a

        elif o in ("-a","--alvo" ):
            alvo = a

        elif o in ("-p", "--port"):
            port = int(a)
        
        else:
            assert False,"Opcao invalida"

# vamos ouvir ou apenas enviar dados de stdin?
    if not listen and len(alvo) and port > 0:

        # ler no buffer a partir da linha de comando
        # isso ira bloquear, entao use CTRL-D se nao enviar input 
        # para stdin
        print '\033[1;96m'+"Pressione CTRL-D para iniciar"+'\033[0;0m'
        buffer = sys.stdin.read()

        # envia data off
        client_sender(buffer)

    # nos iremos ouvir e potencialmente 
    # upar coisas, executar comandos, e drop uma shell de volta
    # dependendo de nossas opções de linha de comando acima
    if listen:
        server_loop()
        


main() 


