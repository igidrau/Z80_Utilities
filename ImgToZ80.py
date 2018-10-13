import sys
from PIL import Image


def getColorsOrdered(image):
	col1=image.getcolors()[0]
	col2=image.getcolors()[1]
	if (sum(col1[1])>=sum(col2[1])):
		return(col1[1],col2[1])
	else:
		return(col2[1],col1[1])


image = Image.open(sys.argv[1])
if image.size[0]>96 and image.size[1]>64 or len(image.getcolors())>2:
	print("The image is wrongly formated (check size and colour number)")
else:
	colours = getColorsOrdered(image)
	white=colours[0]
	black=colours[1]
	datas = list(image.getdata())

	i=0
	outputData=[]
	while i<len(datas):
		byte=0
		for k in range(8):
			if datas[i+k]==black:
				byte+=2**(7-k)
		outputData.append(byte)
		i+=8
	print(outputData)

	outputText=open(sys.argv[1]+".z80","w")
	outputText.write(sys.argv[1]+":\n")
	i=0
	while i<len(outputData):
		line="\t.db\t\t"
		if len(outputData)-i<31:
			while i<len(outputData):
				line+=str(outputData[i])+","
				i+=1
		else:
			for k in range(31):
				line+=str(outputData[i+k])+","

		outputText.write(line[:-1]+"\n")
		i+=31