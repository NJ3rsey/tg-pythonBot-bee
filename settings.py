import pymysql

TO = 15891589
FROM = 5124580170
bot = '-1158vgdpmOId6m7NPe'
end = 'AAHITOAGRNMnABC'

api = (TO+FROM).__str__() + ":" + end + bot
API = api.__str__()


def sql(ppk):
    connection = pymysql.connect(host='localhost',
                                 database='TEST',
                                 user='bot',
                                 password='password')
    try:
        q = """ SELECT * FROM PPK WHERE num = """ '\'' + ppk.__str__() + '\'' """ """ # Query request of PPK needed
        cursor = connection.cursor()
        cursor.execute(q)
        connection.commit()
        rec = cursor.fetchall()
        for row in rec:
            print("number: ", row[0])
        cursor.close()
    finally:
        connection.close()
        print("MySQL connection is closed")
