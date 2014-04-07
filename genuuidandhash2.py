import uuid, hashlib, os, csv;

beginXML='''<?xml version="1.0" encoding="utf-8"?>
<DigitalFile xmlns="http://nationalarchives.gov.uk/2012/dri/artifact/embedded/metadata" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
''';
openUUIDtag='<UUID>';
closeUUIDtag='''</UUID>
''';
openURLtag='<URL>';
baseURL='http://datagov.nationalarchives.gov.uk/66/';
pieceRef='TEST/1/1/'
closeURLtag='''</URL>
''';
endXML='''<Copyright>&#169; Crown copyright: The National Archives of the UK</Copyright>
</DigitalFile>''';
fileExtension='.xml';
filenameBase='y:\\dunderdown\\TEST_1\\1\\';
filelist=[['filepath','checksum']]

for fileCounter in range(1,11) :
	UuidString=str(uuid.uuid4());
	fullURL=baseURL+pieceRef+UuidString;

	fullXML=beginXML+openUUIDtag+UuidString+closeUUIDtag+openURLtag+fullURL+closeURLtag+endXML;
	fullfilename=filenameBase+str(fileCounter).zfill(3)+fileExtension

	fo=open(fullfilename, "w");
	fo.write(fullXML);
	fo.close();
	 
	fo=open(fullfilename, "rb");
	fileHash=hashlib.sha256(fo.read()).hexdigest();
	fo.close();
	
	filelist.append([fullfilename,UuidString]);

filelistCSV=open('y:\dunderdown\TEST1.csv', 'w', newline='')
csv.writer(filelistCSV,dialect='excel').writerows(filelist);
	
	
filelistCSV.close()
print(filelist);