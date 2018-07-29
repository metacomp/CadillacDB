##General Functions
import MySQLdb
import time

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
	return line[startPos+1:endPos]

def RemoveTags(line):
	while (">" in line):
		startpos = line.index("<")
		endpos = line.index(">")
		subline = line[startpos:endpos+1]
		line = line.replace(subline,"")
	return line

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
				content = ""
	return contentlist

#to post to the TextContent table
def GetTextContent():
	contentlist = SplitTextByTags("scripts/eld53srv.txt", """color="#FF0000">Car ""","</p>")
	i=1
	for line in contentlist:
		pgline = line
		while (">" in pgline):
			pgline = GettingBetweenTags(pgline,">","</")
		contentline = RemoveTags(line)
		i = pgline.replace("# ","#").split()[1][1:].split("(")[0].split("&")[0].split("[")[0]
		DatabaseUpdateCommand(contentline, "1953_"+str(i))
		

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
	contentlist = SplitImageContent("scripts/eld53srv.txt", """color="#FF0000">Car """,'<img src="',"""color="#FF0000">Car """)
	i = 1
	j = 1
	carids = []
	for line in contentlist:
		pgline = line
		while (">" in pgline):
			pgline = GettingBetweenTags(pgline,">","</")
		imgLine = GetImgFile(line)
		for img in imgLine:
			i = pgline.replace("# ","#").split()[1][1:].split("(")[0].split("&")[0].split("[")[0]
			if i.isdigit():
				carid = "1953_"+str(i)
				DatabaseInsertCommand("CarImages","Eldorado", 1953, i, j, img, "Car #"+str(i),"Initial","2017-12-11","2017-12-11",carid)
				if carid not in carids:
					DatabaseInsertCommand("CarDetails","Eldorado", 1953, i, j, img, "Car #"+str(i),"Initial","2017-12-11","2017-12-11",carid)
					carids.append(carid)
				j = j + 1
		   

# MySQL Database connection and Execution
def DatabaseInsertCommand(table,a,x,i,j,k,l,m,n,o,p):
	db = MySQLdb.connect("127.0.0.1","root","root","EL_newcadillac") 
	cur = db.cursor()
	if table == "CarImages":
		print("""INSERT INTO EL_newcadillac.EL_CarImages (CarCategory, CarYear, CarNum, ImageNum, ImagePath, Description, CreatedBy, CreateDate, LastUpdateDate, id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(a,x,i,int(j),k,l,m,n,o,p))
		cur.execute("""INSERT INTO EL_newcadillac.EL_CarImages (CarCategory, CarYear, CarNum, ImageNum, ImagePath, Description, CreatedBy, CreateDate, LastUpdateDate, id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(a,x,i,int(j),k,l,m,n,o,p))
	else:
		print("""INSERT INTO EL_newcadillac.EL_CarDetails (CarYear, CarNum, Title, Content, CreatedBy, CreateDate, LastUpdateDate, JAlbumLink, ChapterID, id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(x,i,l,l,m,n,o,'',64,p))
		cur.execute("""INSERT INTO EL_newcadillac.EL_CarDetails (CarYear, CarNum, Title, Content, CreatedBy, CreateDate, LastUpdateDate, JAlbumLink, ChapterID, id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(x,i,l,l,m,n,o,'',64,p))
	db.commit()
	db.close()

def DatabaseUpdateCommand(a,b):
	db = MySQLdb.connect("127.0.0.1","root","root","EL_newcadillac") 
	cur = db.cursor()
	print("""UPDATE EL_newcadillac.EL_CarDetails SET Content=%s WHERE id=%s""",(a,b))
	cur.execute("""UPDATE EL_newcadillac.EL_CarDetails SET Content=%s WHERE id=%s""",(a,b))
	db.commit()
	db.close()

GetImageContent()
GetTextContent()

