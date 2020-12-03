# Python-Net-Tool
Python Net Tool is a simple networking tool made in python
that allows,
read and write data over network connections, using TCP protocols
(a badly made netcat)

## Installation
you will only need python2 installed (yes python2 bruh)

## usage

```
python2 pynet.py -h
```
```
Python Net Tool

Como usar: pynet.py -t host_alvo -p
-l --listen                  - Ira "escutar" em [host]:[port] para
                               entrada de conexões
-e --execute=file_to_run     - executa o arquivo fornecido em uma
                               conexao recebida
-c --command                 - Inicia uma command shell
-u --upload=destino          - Ao receber a conexao faz um upload
                               pra [destino]
                               
```
### Flags
```
-l --listem               - will allow us to listen in [host]:[port] to
                            connections input
```
```
-e --execute=file_to_run  - runs the supplied file in a
                            incoming connection
```
```
-c --command              - Start a command shell when the connection is received
```
```
-u --upload=path          - Upon receiving the connection, upload it to [destination]
```

Examples

On target machine
```
python2 pynet.py -l -p 4444 -c
```
![pynet](https://user-images.githubusercontent.com/62577914/100960050-e7788800-34f5-11eb-8d20-a9544134cf75.png)

On attacker machine
```
python2 pynet.py -a 192.168.0.107 -p 4444
```
![eita](https://user-images.githubusercontent.com/62577914/100960122-08d97400-34f6-11eb-8319-b0aaf6a0a743.png)


### Another examples

```
pynet.py -a 192.168.0.1 -p 5555 -l -c
pynet.py -a 192.168.0.1 -p 5555 -l -u=c:\\ alvo.exe
pynet.py -a 192.168.0.1 -p 5555 -l -e="cat /etc/passwd"
echo 'ABCDEFGHI' | ./pynet.py -t 192.168.0.105 -p 135
```
