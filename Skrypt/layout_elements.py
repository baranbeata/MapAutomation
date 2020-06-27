#Pobranie wartosci parametrow od uzytkownika
ttl = arcpy.GetParameterAsText(0)
out = arcpy.GetParameterAsText(1)
nm = arcpy.GetParameterAsText(2)

#Obiekt klasy MapDocument
mxd = arcpy.mapping.MapDocument('CURRENT')
#Lista zawierajaca elementy wydruku
elements = arcpy.mapping.ListLayoutElements(mxd)
lrs = arcpy.mapping.ListLayers(mxd)

other = []

for i in elements:
	if i.type == "DATAFRAME_ELEMENT":
		df = i
	elif i.name == "Title":
		title = i
	elif i.name == "Date":
		date = i
	elif i.name == "Single Division Scale Bar":
		sbar = i
	elif i.name == "Scale":
		scale = i
	elif i.name == "Author":
		author = i
	elif i.name == "Legend":
		legend = i
	elif i.name == "North Arrow":
		arrow = i
	elif i.name == "Credits":
		cred = i

	else:
		other.append(i)


#Wstêpne pokrycie ramki danych ze strona wydruku z zostawieniem marginesu po bokach
df.elementPositionX = 0.5
df.elementPositionY = 0
df.elementHeight = 29.7
df.elementWidth = 20


#*********TYTUL*********


title.text = ttl

title.fontSize = 48
while title.elementWidth > 19:
	title.fontSize -= 2

title.elementPositionX = df.elementPositionX + df.elementWidth*0.5 - title.elementWidth*0.5
title.elementPositionY = 28 - title.elementHeight


#*****RAMKA DANYCH******

df.elementHeight = 15
df.elementPositionY = title.elementPositionY - df.elementHeight
for l in lrs:
        df.extent = l.getExtent()
df.scale = math.ceil(float(df.scale)/100)*100



#*********DATA**********

now = datetime.datetime.now()
date.text = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
date.fontSize = 14
date.elementPositionY = 1
date.elementPositionX = df.elementPositionX + df.elementWidth - date.elementWidth



#*********AUTOR*********

if (mxd.author):
	author.text = mxd.author
else:
	author.text = " "

author.fontSize = 14
author.elementPositionX = df.elementPositionX + df.elementWidth - author.elementWidth
author.elementPositionY = date.elementPositionY + date.elementHeight



#****PRAWA AUTORSKIE****

if (mxd.credits):
	cred.text = mxd.credits
else:
	cred.text = " "

cred.fontSize = 14
cred.elementPositionX = df.elementPositionX + df.elementWidth - cred.elementWidth
cred.elementPositionY = author.elementPositionY + author.elementHeight



#*********SKALA*********

scale.text = "Skala   1 : " + str(int(df.scale))
scale.elementPositionX = df.elementPositionX + df.elementWidth - scale.elementWidth
scale.elementPositionY = cred.elementPositionY + cred.elementHeight + 1



#****PODZIALKA SKALI****

sbar.elementHeight = 6
sbar.elementHeight = 1.5
sbar.elementPositionX = df.elementPositionX + df.elementWidth - sbar.elementWidth
sbar.elementPositionY = scale.elementPositionY + scale.elementHeight



#***STRZALKA POLNOCY****

arrow.elementHeight = 3.5
arrow.elementPositionX = df.elementPositionX + df.elementWidth - arrow.elementWidth
arrow.elementPositionY = df.elementPositionY - (arrow.elementHeight + 0.5)



#********LEGENDA********

legend.title = "LEGENDA"
legend.elementPositionX = 1.5
legend.elementPositionY = 1
legend.elementWidth = 6
legend.elementHeight = 10
if (legend.isOverflowing):
        print "UWAGA: NIEPOPRAWNIE WYSWIETLANA LEGENDA!"


#*********INNE**********

for j in other:
	i.elementPositionX = 22

arcpy.RefreshActiveView()

arcpy.mapping.ExportToPDF(mxd, out + '\\' + nm)

del mxd
