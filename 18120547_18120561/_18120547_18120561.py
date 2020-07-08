from socket import *
SERVER, PORT = '127.0.0.1', 9000

#file web
inforGroup = "info.html"
backGround = "index.html"
error404 =  "404.html"


#hàm xử lí request từ Client
def handleClient(client):
    request = client.recv(1024).decode('utf-8') #Nhận Request từ client, maximum buffer 1024 byte = 1mb
    if not request :
        print("Not received any request\n")
        return
    print("Client request: \n" + request)
    request_list = request.split(' ') #tách chuỗi
    method = request_list[0] #Method ở đầu              

    if method == "GET": #xử lí method GET
        req_file = request_list[1] #tên file
        req_file = req_file.lstrip('/')
        if not req_file: #nếu không có tên file => mặc định là màn hình đầu vào
            req_file = backGround
     
        file = open(req_file, 'rb')
        response = file.read() #đọc nội dung file vào response
        file.close()
        header = "HTTP/1.1 200 OK\n" #header của response

        Type = "Content-Type: " #gắn vào header Content Type
        if req_file.endswith(".html"): 
            header += Type + "text/html\n\n"
        elif req_file.endswith(".css"):
            header += Type + "text/css\n\n"
        else:
            header += Type + "*/*\n\n"
     
        finalReponse = header.encode('utf-8') + response #kết quả cuối cùng của response


    elif method == "POST": #xử lí method POST
        str_split = request.split('\n') #xử lí chuỗi để lấy username và password
        loginInfo = str_split[-1]
        str_account = loginInfo.split('&')
        user, passW = str_account[0].split('='), str_account[1].split('=') 

      
        userName = user[1] #user
        passWord = passW[1] #password
        if userName == "admin" and passWord == "admin": #chuyển hướng sang info.html
            header = "HTTP/1.1 301 Moved Permanently\nLocation: /" + inforGroup + "\n" #header của HTTP Redirection
            finalReponse = header.encode('utf-8') 
        else: #sai -> lỗi 404
            header = "HTTP/1.1 404 Not Found\n"
            file = open(error404, "rb")
            response = file.read()
            file.close()
            finalReponse = header.encode('utf-8') + response

    client.send(finalReponse) #final response cho client

#hàm khởi tạo Server và lắng nghe kết nối
def startServer():
    serversocket = socket(AF_INET, SOCK_STREAM) #Khởi tạo socket
    try :
        serversocket.bind((SERVER, PORT)) #gán IP Address và Port
        serversocket.listen(5) #lắng nghe kết nối, hàng chờ tối đa 5
        print("Server is listening at http://" + SERVER + ":" + str(PORT))
        while (1):
            connect, address = serversocket.accept() #chấp nhận kết nối từ Client
            print("Connected to " + str(address))
            handleClient(connect) #gọi hàm để xử lí request
            connect.close()    #đóng kết nối đến Client và xử lí các request khác
    except KeyboardInterrupt:
        print("\nShutting down...\n")
    except Exception as exc:
        print("Error:\n")
        print(exc)
 
    print("Server is closed...")
    serversocket.close()

startServer()