from messager import server_host

server = server_host(port=1234,host='123.456.789')
server.bind()
server.start()
