import uuid, hashlib, os, csv, urllib.parse;

beginXML='''<?xml version="1.0" encoding="utf-8"?>
<DigitalFile xmlns="http://nationalarchives.gov.uk/2012/dri/artifact/embedded/metadata" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
''';
openUUIDtag='<UUID>';
closeUUIDtag='''</UUID>
''';
openURLtag='<URL>';
baseURL='http://datagov.nationalarchives.gov.uk/66/';
lettercode='TEST'
series=1
initialpiece=1
totalpieces=2
closeURLtag='''</URL>
''';
endXML='''<Copyright>&#169; Crown copyright: The National Archives of the UK</Copyright>
</DigitalFile>''';
fileExtension='.xml';
filenameBase=os.getcwd();
filelist=[['filepath','uuid','checksum']]

for fileCounter in range(1,11) :
	for currentpiece in range (initialpiece,initialpiece+totalpieces) : 
		UuidString=str(uuid.uuid4());
		
		fullURL=baseURL+lettercode+'/'+str(series)+'/'+str(currentpiece)+'/'+UuidString;
		fullXML=beginXML+openUUIDtag+UuidString+closeUUIDtag+openURLtag+fullURL+closeURLtag+endXML;
		
		topdir=lettercode+'_'+str(series);
		piecestring=str(currentpiece);
		
		filename=piecestring+'_'+str(fileCounter).zfill(3)+fileExtension;
		fullfilepath=os.path.join(filenameBase,topdir,piecestring,filename);
		fileURI='file:///'+topdir+'/'+piecestring+'/'+filename;

		#check for existence of the directory structure we want to put things in, else create it (probably really ought to check it's a directory too)
		if os.path.exists(os.path.join(filenameBase,topdir,piecestring)) :
			pass;
		else :
			os.makedirs(os.path.join(filenameBase,topdir,piecestring));
		
		fo=open(fullfilepath, "w");
		fo.write(fullXML);
		fo.close();
		 
		fo=open(fullfilepath, "rb");
		fileHash=hashlib.sha256(fo.read()).hexdigest();
		fo.close();
		
		filelist.append([fileURI,UuidString,fileHash]);

filelistCSV=open(os.path.join(filenameBase,lettercode+str(series)+'.csv'), 'w', newline='');
csv.writer(filelistCSV,dialect='excel').writerows(filelist);
	
	
filelistCSV.close()
print(filelist);