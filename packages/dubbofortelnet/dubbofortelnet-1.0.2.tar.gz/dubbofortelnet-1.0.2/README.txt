#test dubbo use telnet

conn = Dubbo(ip, port)

data1 = (1,"300300",[22,33])
data1 = ("300300","100200",["300300","322333"])
result1 = conn.dotest2(conn,interfaceName,method, data1)
print(result1)