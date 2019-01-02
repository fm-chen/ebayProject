
# coding: utf-8

# In[146]:


htmlurl = 'Donald-Trump7.html'
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
from datetime import datetime
def transtime(date):
    if ":" in date:
        date = "2016"+"-"+date
    else:
        date = "2000-JAN-01 00:00"
    date = datetime.strptime(date, "%Y-%b-%d %H:%M")
    return date
def transmoney(text):
    money = text.split('$')
    return money[1].replace(',','')
#predefined functions;

from lxml import etree
html=etree.parse(htmlurl,etree.HTMLParser())
partresult = html.xpath('//div/@iid|//img[@class="img"]//@alt')
#for i in range (0,len(partresult)):
#    if i%2 ==0:
#        print(partresult[i])
#print(partresult)
import pymysql
db = pymysql.connect(host='localhost',user='root',password='****',port=3306, db='spiders')
cursor = db.cursor()
sql0 = 'CREATE TABLE IF NOT EXISTS Auction_result (Itemno BIGINT NOT NULL, Itemname VARCHAR(255) NOT NULL, Candidate VARCHAR(255) NOT NULL, Sold_or_not VARCHAR(255) NOT NULL, End_price DECIMAL(8,2) NOT NULL,                     Bid_no VARCHAR(255) NOT NULL, Best_offer_accepted VARCHAR(255) NOT NULL, Date_Time TIMESTAMP NOT NULL, Ship_fee VARCHAR(255) NOT NULL,                    Top_Rated_Plus VARCHAR(255) NOT NULL, Item_category VARCHAR(255) NOT NULL, buyitnow_or_auction VARCHAR(255) NOT NULL, PSA BOOLEAN NOT NULL, JSA BOOLEAN NOT NULL,                    limited_edition_book BOOLEAN NOT NULL, positive_feedback VARCHAR(255) NOT NULL, PRIMARY KEY (Itemno))'
cursor.execute(sql0)
sql = "insert into Auction_result(Itemno, Itemname, Candidate, Sold_or_not, End_price, Bid_no, Best_offer_accepted, Date_Time, Ship_fee,        Top_Rated_Plus, Item_category, buyitnow_or_auction, PSA, JSA, limited_edition_book, positive_feedback) values(%s,%s,%s,%s,        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
for i in range (0, len(partresult)-1):
    if i%2 ==0:
        par = (partresult[i],partresult[i+1],'Donald-Trump','NULL','0.00','NULL','NULL','2000-01-01 00:00:00','NULL','NULL','NULL','Auction','0','0','0','NULL')
        try:
            cursor.execute(sql,par)
            db.commit()
        except:
            db.rollback()
db.close()
from lxml import etree
html=etree.parse(htmlurl,etree.HTMLParser())
result = html.xpath('//div/@iid|//span[@class="tme"]/span/text()|//li[@class="lvprice prc"]/span/@class|                        //span[contains(@class, "bold")]//text()|                        //li[@class="lvformat"]/span/text()')
#print(result)
import pymysql
db = pymysql.connect(host='localhost',user='root',password='*****',port=3306, db='spiders')
cursor = db.cursor()
sql = "update Auction_result set Sold_or_not = %s, End_price = %s, Bid_no = %s, Date_Time = %s where Itemno = %s"
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
partresult1 = html.xpath('//div/@iid|                         //span[@class="bfsp"]/text()                       |//img[@class="iconETRS2"]/@alt')
#print(partresult1)
import pymysql
db = pymysql.connect(host='localhost',user='root',password='*****',port=3306, db='spiders')
cursor = db.cursor()
sql1 = "update Auction_result set Ship_fee = %s where Itemno = %s"
sql2 = "update Auction_result set Top_Rated_Plus = %s where Itemno = %s"
for i in range (1, len(partresult1)):
    if len(partresult1[i-1]) ==12 and is_number(result[i]):
        if partresult1[i] == 'Free shipping':
            par = ('Free shipping', partresult1[i-1])
            try:
                cursor.execute(sql1,par)
                db.commit()
            except:
                db.rollback()
            if partresult1[i+1] == 'The item is listed as a Top Rated Plus item':
                par = ('Top_Rated_Plus', partresult1[i-1])
                try:
                    cursor.execute(sql2,par)
                    db.commit()
                except:
                    db.rollback()
        elif partresult1[i] == 'The item is listed as a Top Rated Plus item':
            par = ('Top_Rated_Plus', partresult1[i-1])
            try:
                cursor.execute(sql2,par)
                db.commit()
            except:
                db.rollback()
db.close()

