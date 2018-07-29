##General Functions
import MySQLdb
import time
import re

#to get the text
def GettingBetweenTags(line, beginTag, endTag):
	if beginTag not in line:
		startPos = 0
	else:
		startPos = line.index(beginTag)
	if endTag not in line:
		endPos = len(line)
	else:
		endPos = line.index(endTag)
# 		For populating image table
# 	return line[startPos+1:endPos]  
#       For populating car details Table  
	return line[startPos+23:endPos]

def RemoveTags(line):
	if ("</td><td" in line):
		startpos = line.index("</td><td")
		subline = line[startpos+9:]
		if ("</td><td" in subline):
			startpos = subline.index("</td><td")
			subsubline = subline[startpos+9:]
			if (">" in subsubline):
				startpos = subsubline.index(">")
				subsubsubline = subsubline[startpos+1:]

# 		endpos = line.index(">")
# 		subline = line[startpos:endpos+1]
# 		line = line.replace(subsubsubline,"")
	return subsubsubline


#to get the pageName 
def FindPageName(text):
	for line in text:
		# Break up the line
		print "#1" + line
		if "<title>" in line:
			pgName = GettingBetweenTags(line)
		

##To get text type contents from a html file

#to get the required sectios to pull text content			
def SplitTextByTags(filePath, search_begin_str, search_end_str):
	
	txtfile = open(filePath,"r")
	contentlist = []
	content = ""
	flag = 0
	for line in txtfile:
		if(search_begin_str in line) or (flag == 1):
			content = content + line.strip()
			if not(search_end_str in line):
				flag = 1
			else:
				flag = 0
				contentlist.append(content.strip())
# 				print content
				content = ""
	return contentlist

#to post to the TextContent table
def GetTextContent():
	contentlist = SplitTextByTags("V16_1930-31.txt","""<font face="Times New Roman">#""","</tr>")
# 	i=1
	char1 = "#"
	char2 = "<"
	count = 1
	for line in contentlist:
		pgline = line
		while ("""face="Times New Roman">#""" in pgline):
			pgline = GettingBetweenTags(pgline,"""face="Times New Roman">#""","</tr>")
# 			print pgline
		contentline = RemoveTags(pgline)
		i = pgline[pgline.find(char1)+1 : pgline.find(char2)]
		DatabaseCommand('1930', i, "Car #"+str(i), contentline, "Initial","2016-12-15","2016-08-11","J",63,str(count))
		count=count +1
		

#to get the image file from 
def GetImgFile(line):
	imgFile = []
	while '<img src="' in line:
		startpos = line.find('<img src="')
		endpos = line.find('"',startpos+10)
		subline = line[startpos:endpos]
		imgFile.append(subline.replace('<img src="',""))
		line = line.replace(subline,"")
	return imgFile


#to get the required sectios to pull text content  
def SplitImageContent(filePath, search_begin_str, search_image_str, search_end_str):
	txtfile = open(filePath,"r")
	contentlist = []
	content = ""
	sameContextFlag = 0
	booleanimg = False
	
	line = txtfile.readlines()
	for i in xrange(len(line)):
		if(search_begin_str in line[i]) or (sameContextFlag == 1):
			content = content + line[i].strip()
			if search_image_str in line[i]:
				booleanimg = True
			if i < len(line)-1:
				if (search_end_str in line[i+1]):
					sameContextFlag = 0
					if booleanimg == True:
						contentlist.append(content.strip())
					content = ""
			sameContextFlag = 1
	return contentlist

def GetImageContent():
	print "inside image content"
	contentlist = SplitImageContent("scripts/V16_1930-31.txt", """<font face="Times New Roman">#""",'<img src="',"""<font face="Times New Roman">#""")
	i = 1
	j = 1
	carids = []
	for line in contentlist:
		pgline = line
		while ("<img" in pgline):
			pgline = GettingBetweenTags(pgline,">#","</")
		imgLine = GetImgFile(line)
		for img in imgLine:
			i = pgline.replace("#", "").replace("?","").replace("""<strong><sup><fontcolor="FF0000">1""","")
			print i
			if i.isdigit():
				carid = "1930_"+str(i)
				#DatabaseCommand("TS", "1930-31", i, j, img, "Car #"+str(i),"Initial","2016-12-15","2016-08-11","1930_"+str(i))
				j = j + 1

def GetImageContent():
	contentlist = SplitImageContent("scripts/eld53srv.txt", """color="#FF0000">Car """,'<img src="',"""color="#FF0000">Car """)
	i = 1
	j = 1
	carids = []
	for line in contentlist:
		pgline = line
		while (">" in pgline):
			pgline = GettingBetweenTags(pgline,">","</")
			print pgline
		imgLine = GetImgFile(line)
		for img in imgLine:
			print pgline.replace("# ","#")
			i = pgline.replace("# ","#").split()[1][1:].split("(")[0].split("&")[0].split("[")[0]
			if i.isdigit():
				carid = "1953_"+str(i)
				DatabaseInsertCommand("CarImages","Eldorado", 1953, i, j, img, "Car #"+str(i),"Initial","2017-12-11","2017-12-11",carid)
				if carid not in carids:
					DatabaseInsertCommand("CarDetails","Eldorado", 1953, i, j, img, "Car #"+str(i),"Initial","2017-12-11","2017-12-11",carid)
					carids.append(carid)
				j = j + 1
		   


# MySQL Database Connection and Execution
def DatabaseInsertCommand(table,a,x,i,j,k,l,m,n,o,p):
	db = MySQLdb.connect("127.0.0.1","root","root","V16_newcadillac") 
	cur = db.cursor()
	if table == "CarImages":
		print("""INSERT INTO V16_newcadillac.V16_CarImages (CarCategory, CarYear, CarNum, ImageNum, ImagePath, Description, CreatedBy, CreateDate, LastUpdateDate, id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(a,x,i,int(j),k,l,m,n,o,p))
		cur.execute("""INSERT INTO EL_newcadillac.EL_CarImages (CarCategory, CarYear, CarNum, ImageNum, ImagePath, Description, CreatedBy, CreateDate, LastUpdateDate, id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(a,x,i,int(j),k,l,m,n,o,p))
	else:
		print("""INSERT INTO V16_newcadillac.V16_CarDetails (CarYear, CarNum, Title, Content, CreatedBy, CreateDate, LastUpdateDate, JAlbumLink, ChapterID, id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(x,i,l,l,m,n,o,'',64,p))
		cur.execute("""INSERT INTO V16_newcadillac.V16_CarDetails (CarYear, CarNum, Title, Content, CreatedBy, CreateDate, LastUpdateDate, JAlbumLink, ChapterID, id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(x,i,l,l,m,n,o,'',64,p))
	db.commit()
	db.close()

def DatabaseUpdateCommand(a,b):
	db = MySQLdb.connect("127.0.0.1","root","root","V16_newcadillac") 
	cur = db.cursor()
	print("""UPDATE V16_newcadillac.V16_CarDetails SET Content=%s WHERE id=%s""",(a,b))
	cur.execute("""UPDATE V16_newcadillac.V16_CarDetails SET Content=%s WHERE id=%s""",(a,b))
	db.commit()
	db.close()

GetImageContent()
#GetTextContent()

