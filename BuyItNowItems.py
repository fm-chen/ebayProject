
# coding: utf-8

# In[2]:


#predefined functions;
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
#trans time for Auction items
from datetime import datetime
def transtime(date):
    if ":" in date:
        date = "2016"+"-"+date
    else:
        date = "2000-JAN-01 00:00"
    date = datetime.strptime(date, "%Y-%b-%d %H:%M")
    return date
#trans time for Buy it now items
from datetime import datetime
def transtime1(date1):
    if ":" in date1:
        date1 = date1.split('P')
        date = date1[0].strip()
    else:
        date = "Jan 01, 2000 00:00:00"
    date = datetime.strptime(date, "%b %d, %Y %H:%M:%S")
    return date
#trans money format
def transmoney(text):
    money = text.split('$')
    return money[1].replace(',','')
#predefined functions;

def mainparse(htmlurl,candidate):
    from lxml import etree
    html=etree.parse(htmlurl,etree.HTMLParser())
    partresult = html.xpath('//div/@iid|//img[contains(@class, "mg")]//@alt')
    #for i in range (0,len(partresult)):
    #    if i%2 ==0:
    #        print(partresult[i])
    #print(partresult)
    import pymysql
    db = pymysql.connect(host='localhost',user='root',password='*****',port=3306, db='spiders')
    cursor = db.cursor()
    sql = "insert into Buy_now_result(Itemno, Itemname, Candidate, Sold_or_not, End_price, Bid_no, Best_offer_accepted, Date_Time, Ship_fee,            Top_Rated_Plus, Item_category, buyitnow_or_auction, PSA, JSA, limited_edition_book, positive_feedback) values(%s,%s,%s,%s,            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for i in range (0, len(partresult)-1):
        if i%2 ==0:
            par = (partresult[i],partresult[i+1],candidate,'NULL','0.00','NULL','NULL','2000-01-01 00:00:00','NULL','NULL','NULL','Buy_it_now','0','0','0','NULL')
            try:
                cursor.execute(sql,par)
                db.commit()
            except:
                db.rollback()
    db.close()
    from lxml import etree
    html=etree.parse(htmlurl,etree.HTMLParser())
    result = html.xpath('//div/@iid|//span[contains(@class, "bold")]//text()[normalize-space()]                            |//li[@class="lvprice prc"]/span/@class                           |//li[@class="lvformat"]/span[last()]//text()[normalize-space()]')
    #print(result)
    import pymysql
    db = pymysql.connect(host='localhost',user='root',password='*****',port=3306, db='spiders')
    cursor = db.cursor()
    sql = "update Buy_now_result set Sold_or_not = %s, End_price = %s, Best_offer_accepted = %s, Date_Time = %s where Itemno = %s"
    for i in range (0, len(result)-4):
        if len(result[i]) ==12 and is_number(result[i]):
            par = (result[i+1],transmoney(result[i+2]),result[i+3],transtime(result[i+4]),result[i])
            try:
                cursor.execute(sql,par)
                db.commit()
            except:
                db.rollback()
    db.close()
    from lxml import etree
    html=etree.parse(htmlurl,etree.HTMLParser())
    partresult1 = html.xpath('//div/@iid|                             //span[@class="bfsp"]/text()                           |//img[@class="iconETRS2"]/@alt')
    #print(partresult1)
    import pymysql
    db = pymysql.connect(host='localhost',user='root',password='*****',port=3306, db='spiders')
    cursor = db.cursor()
    sql1 = "update Buy_now_result set Ship_fee = %s where Itemno = %s"
    sql2 = "update Buy_now_result set Top_Rated_Plus = %s where Itemno = %s"
    for i in range (0, len(partresult1)-1):
        if len(partresult1[i]) ==12 and is_number(result[i]):
            if partresult1[i+1] == 'Free shipping':
                par = ('Free shipping', partresult1[i])
                try:
                    cursor.execute(sql1,par)
                    db.commit()
                except:
                    db.rollback()
            elif partresult1[i+1] == 'The item is listed as a Top Rated Plus item':
                par = ('Top_Rated_Plus', partresult1[i])
                try:
                    cursor.execute(sql2,par)
                    db.commit()
                except:
                    db.rollback()
    for i in range (0, len(partresult1)-2):
        if len(partresult1[i]) ==12 and is_number(result[i]):
            if partresult1[i+1] == 'Free shipping' and partresult1[i+2] == 'The item is listed as a Top Rated Plus item':
                    par = ('Top_Rated_Plus', partresult1[i])
                    try:
                        cursor.execute(sql2,par)
                        db.commit()
                    except:
                        db.rollback()
    db.close()
    return htmlurl
def getdatebin():
    import pymysql
    db = pymysql.connect(host='localhost',user='root',password='*****',port=3306, db='spiders')
    cursor = db.cursor()
    sql = "select Itemno from Buy_now_result"
    cursor.execute(sql)
    idlist=cursor.fetchall()
    id_list=[]
    for (row,) in idlist:
        id_list.append(row)
    cursor.close()
    db.close()
    #print(id_list)
    #all files
    import os 

    g = os.walk(r"C:\Users\fmche\ebayitempage")  
    list_file=[]
    for path,dir_list,file_list in g:  
        for file_name in file_list:  
            list_file.append(os.path.join(file_name))

    from lxml import etree
    f_result = []
    for i in range (0,len(id_list)):
        s='%s' %(id_list[i])
        if s+'.html' in list_file:
            pathurl = r"C:\Users\fmche\ebayitempage\%s.html" %(s)
            html=etree.parse(pathurl,etree.HTMLParser())
            result2 = html.xpath('//span[@id="bb_tlft"]/text()[normalize-space()]|                                //span[@class="endedDate"]/noscript/span/text()')
            f_result.append(s)
            if len(result2)>0:
                result_bin = result2[0].strip()+' '+result2[1]
                f_result.append(result_bin)
    #print(f_result)
    import pymysql
    db = pymysql.connect(host='localhost',user='root',password='*****',port=3306, db='spiders')
    cursor = db.cursor()
    sql = "update Buy_now_result set Date_Time = %s where Itemno = %s"
    for i in range (0, len(f_result)-1):
        if len(f_result[i]) ==12 and is_number(f_result[i]):
            par = (transtime1(f_result[i+1]),f_result[i])
            try:
                cursor.execute(sql,par)
                db.commit()
            except:
                db.rollback()    
    cursor.close()
    db.close()
    return None
import pymysql
db = pymysql.connect(host='localhost',user='root',password='*****',port=3306, db='spiders')
cursor = db.cursor()
sql0 = 'CREATE TABLE IF NOT EXISTS Buy_now_result (Itemno BIGINT NOT NULL, Itemname VARCHAR(255) NOT NULL, Candidate VARCHAR(255) NOT NULL, Sold_or_not VARCHAR(255) NOT NULL, End_price DECIMAL(8,2) NOT NULL,                    Bid_no VARCHAR(255) NOT NULL, Best_offer_accepted VARCHAR(255) NOT NULL, Date_Time TIMESTAMP NOT NULL, Ship_fee VARCHAR(255) NOT NULL,                     Top_Rated_Plus VARCHAR(255) NOT NULL, Item_category VARCHAR(255) NOT NULL, buyitnow_or_auction VARCHAR(255) NOT NULL, PSA BOOLEAN NOT NULL, JSA BOOLEAN NOT NULL,                   limited_edition_book BOOLEAN NOT NULL, positive_feedback VARCHAR(255) NOT NULL, PRIMARY KEY (Itemno))'
cursor.execute(sql0)
cursor.close()
db.close()

htmlurl = []
htmlurl.append('Hillary-Clinton7bn.html')
htmlurl.append('Hillary-Clinton6bn.html')
htmlurl.append('Hillary-Clinton5bn.html')
htmlurl.append('Hillary-Clinton4bn.html')
htmlurl.append('Hillary-Clinton3bn.html')
htmlurl.append('Hillary-Clinton2bn.html')
htmlurl.append('Hillary-Clinton1bn.html')

for i in range (0,len(htmlurl)):
    mainparse(htmlurl[i],'Hillary-Clinton')
    print(mainparse(htmlurl[i],'Hillary-Clinton'))
    
htmlurl1 = []
htmlurl1.append('Donald-Trump7bn.html')
htmlurl1.append('Donald-Trump6bn.html')
htmlurl1.append('Donald-Trump5bn.html')
htmlurl1.append('Donald-Trump4bn.html')
htmlurl1.append('Donald-Trump3bn.html')
htmlurl1.append('Donald-Trump2bn.html')
htmlurl1.append('Donald-Trump1bn.html')

for i in range (0,len(htmlurl1)):
    mainparse(htmlurl1[i],'Donald-Trump')
    print(mainparse(htmlurl1[i],'Donald-Trump'))    
       
getdatebin()


# In[32]:


#update category info
import pymysql
db = pymysql.connect(host='localhost',user='root',password='*****',port=3306, db='spiders')
cursor = db.cursor()
sql = "select Itemno from Buy_now_result"
cursor.execute(sql)
idlist=cursor.fetchall()
id_list=[]
for (row,) in idlist:
    id_list.append(row)
cursor.close()
db.close()
#print(id_list)
#all files
import os 
g = os.walk(r"C:\Users\fmche\ebayitempage")  
list_file=[]
for path,dir_list,file_list in g:  
    for file_name in file_list:  
        list_file.append(os.path.join(file_name))
        
from lxml import etree
ctgry_result=[]
for i in range (0,len(id_list)):
    s='%s' %(id_list[i])
    if s+'.html' in list_file:
        pathurl = r"C:\Users\fmche\ebayitempage\%s.html" %(s)
        html=etree.parse(pathurl,etree.HTMLParser())
        result2 = html.xpath('//ul/li[@class="bc-w"]/a//text()')
        ctgry_result.append(s)
        ctgry_result.append(result2)
print(ctgry_result)

def is_number(s):
    if isinstance(s,list):
        pass
    else:
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
 
    return False
#print(len(ctgry_result)/2)
import pymysql
db = pymysql.connect(host='localhost',user='root',password='*****',port=3306, db='spiders')
cursor = db.cursor()
sql = "update Buy_now_result set Item_category = %s where Itemno = %s"
for i in range (0, len(ctgry_result)-1):
    if len(ctgry_result[i]) ==12 and is_number(ctgry_result[i]) and (len(ctgry_result[i+1])>0):
        par = (','.join(ctgry_result[i+1]),ctgry_result[i])
        try:
            cursor.execute(sql,par)
            db.commit()
        except:
            db.rollback()    
cursor.close()
db.close()

