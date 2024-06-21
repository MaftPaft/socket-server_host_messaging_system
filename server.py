from messager import server_host

server = server_host(5050)
server.bind()
server.start()
