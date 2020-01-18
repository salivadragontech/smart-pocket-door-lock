import RFID
import sqlite3

def sqlTool(query):
    sqlCon = sqlite3.connect("access.db")
    result = sqlCon.cursor()
    result.execute(query)
    sqlCon.commit()
    return result.fetchall()

#insert card
def insertCard():
    print "Insert Card"
    pId = raw_input("Person Id:")
    print "Please inductive your RFID card..."
    uId = RFID.getUid()
    print "Card Uid:%s" % uId
    cId = raw_input("Card Cid(Optional):")
    query = "INSERT INTO Card(Uid, Cid, Owner) VALUES(\'%s\', \'%s\', \'%s\');" % (uId, cId, pId)
    try:
        sqlTool(query)
        print "Success"
    except:
        print "Fail"
    
#insert person
def insertPerson():
    print "Insert Person"
    pId = raw_input("Id:")
    pName = raw_input("Name(Optional):")
    query = "INSERT INTO Person(Id, Name, Status) VALUES(\'%s\', \'%s\', 1)" % (pId, pName)
    print query
    try:
        sqlTool(query)
        print "Success(Id=\'%s\', Name=\'%s\')" % (pId, pName)
    except:
        print "Fail"

#ban/unbad person
def banPerson():
    print "Ban Person"
    pId = raw_input("Person Id:")
    status = raw_input("Ban(0) or UnBan(1)")
    query = "UPDATE Person SET Status = \'%s\' WHERE Id = \'%s\';" % (status, pId)
    try:
        sqlTool(query)
        print "Success (%s-%s)" % (pId, status)
    except:
        print "Fail"

def showPerson():
    query = "SELECT * FROM Person"
    result = sqlTool(query)
    for value in result:
        print value

#exit
def exit():
    quit()

def menu_main():
    print ""
    print "**Access Management**"
    for key, value in cmds.iteritems():
        print "%s : %s" % (key, value[0])
    

cmds = {
        '-c': ["Insert Card", insertCard],
        '-p': ["Insert Person", insertPerson],
        '-b': ["Ban Person", banPerson],
        '-s': ["Show All Person", showPerson],
        '-q': ["Quit", exit],
    }

def main():
    while True:
        menu_main()
        cmd = raw_input().replace('\r','')
        if cmd in cmds:
            command = cmds[cmd][1]
            command()



if __name__=='__main__':
    main()
