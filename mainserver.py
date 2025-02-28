from socket import *
import pymysql

db = pymysql.connect(host='rm-uf69z6cza1t8b04c1yo.mysql.rds.aliyuncs.com',
                     port=3306,
                     user='testing',
                     password='solaire0L005@',
                     database='internetwww')


cursor = db.cursor()

def addPoster(autor_name, poster_name):

    sql = """INSERT INTO posters(author,
          poster)
          VALUES ('{a_name}', '{p_name}')""".format(a_name=autor_name, p_name=poster_name)

    try:

        cursor.execute(sql)

        db.commit()
        print("Insert Successfully.")
    except:

        db.rollback()
    return sql


def getPoster():
    reslist=[]
    sql="SELECT * FROM posters"
    try:

        cursor.execute(sql)
        result = cursor.fetchall()
        for element in result:
            reslist.append(element)


        db.commit()
        return reslist
    except:

        db.rollback()

def show_html(client_socket,fin_target):
    response_headers = "HTTP/1.1 200 OK\r\n"
    response_headers += "\r\n"
    s = open(fin_target, 'r')
    response_body = s.read()
    response = response_headers + response_body
    client_socket.send(response.encode("utf-8"))
    client_socket.close()

def upload(client_socket,reslist):
    response_headers = "HTTP/1.1 200 OK\r\n"
    response_headers += "\r\n"
    s = open("upload.html", 'r')
    response_body = s.read()
    response = response_headers + response_body

    poster=reslist[2].replace('\\','/')
    addPoster(reslist[1],poster)
    client_socket.send(response.encode("utf-8"))
    client_socket.close()

def download(client_socket,ip):
    response_headers = "HTTP/1.1 200 OK\r\n"
    response_headers += "\r\n"
    reslist=getPoster()
    #######图片的代码在这 reslist是返回的信息

    s = open("upload.html", 'r')
    response_body = s.read()
    response = response_headers + response_body
    client_socket.send(response.encode("utf-8"))
    client_socket.close()

def requesthandler(client_socket):
    recv_data = client_socket.recv(4096).decode("utf-8")
    request_header_lines = recv_data.splitlines()
    file_counter = 0
    aut_counter = 0
    reslist=[]
    target = request_header_lines[0].split("/")[1]
    fin_target = target.split(" ")[0]
    reslist.append(fin_target)
    print(request_header_lines[0])
    if(len(fin_target.split("."))==1):
        for element in request_header_lines:
            if(element== "Content-Disposition: form-data; name=\"filename\""):
                file_counter+=1
                continue
            if(file_counter==1):
                file_counter+=1
                continue
            if(file_counter==2):
                reslist.append(element)
                file_counter=0
                continue

            if (element == "Content-Disposition: form-data; name=\"author\""):
                aut_counter += 1
                continue
            if (aut_counter == 1):
                aut_counter += 1
                continue
            if (aut_counter == 2):
                reslist.append(element)
                aut_counter = 0
                continue


    return reslist

def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(('', 8000))
    server_socket.listen(128)
    while True:
        client_socket, clientAddr = server_socket.accept()
        result=requesthandler(client_socket)

        if(len(result)==1):
            if (result[0] == "download"):
                download(client_socket, clientAddr)
            elif(result[0]=="upload"):
                show_html(client_socket, "upload.html")
            else:
                show_html(client_socket,result[0])
        else:
            if(result[0]=="upload"):
                upload(client_socket,result)



if __name__ == "__main__":
    main()
