import uuid, hashlib, os, csv, urllib.parse;

beginXML='''<?xml version="1.0" encoding="utf-8"?>
<DigitalFile xmlns="http://nationalarchives.gov.uk/2012/dri/artifact/embedded/metadata" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
''';
openUUIDtag='<UUID>';
closeUUIDtag='''</UUID>
''';
openURLtag='<URI>';
baseURL='http://datagov.nationalarchives.gov.uk/66/';
lettercode='TEST'
series=2
closeURLtag='''</URI>
''';
endXML='''<Copyright>&#169; Crown copyright: The National Archives of the UK</Copyright>
</DigitalFile>''';
infileExtension='xml';
outfileExtension='txt';
concatLettercodeAndPiece=True;
filenameBase=os.getcwd();
if concatLettercodeAndPiece :
	topdir=lettercode+'_'+str(series);
else :
	topdir=lettercode;

for dirName, subdirList, fileList in os.walk(topdir): 
	piece='';
	item='';
	print('Found directory: %s' % dirName);
	parentFolders=dirName.split(sep='\\');			
	if concatLettercodeAndPiece :
		if len(parentFolders)==2 :
			print(parentFolders);
			piece=os.path.basename(dirName);
		elif len(parentFolders)==3 :
			print(parentFolders);
			item=os.path.basename(dirName);
			piece=parentFolders[-1]
	elif len(parentFolders)==3 :
		print(parentFolders);
		piece=os.path.basename(dirName);
	elif len(parentFolders)==4 :
		print(parentFolders);
		item=os.path.basename(dirName);
		piece=parentFolders[-1];
		
	urlPiece=piece+'/';
	if item :
		urlItem=item+'/';
	else :
		urlItem='';

	for fname in fileList:
		print('\t%s' % fname);
		filenameParts=fname.split(sep='.');
		print(filenameParts[0]);
		print(filenameParts[-1]);
		print('Piece: %s' % piece);
		print('Item: %s' % item);
		if filenameParts[-1]==infileExtension :
			UuidString=str(uuid.uuid4());
			fullURL=baseURL+lettercode+'/'+str(series)+'/'+urlPiece+urlItem+UuidString;
			fullXML=beginXML+openUUIDtag+UuidString+closeUUIDtag+openURLtag+fullURL+closeURLtag+endXML;
			print(fullXML);
			
			outfilepath=os.path.join(filenameBase,dirName,filenameParts[0]+'.'+outfileExtension);
			print(outfilepath);
			fo=open(outfilepath, "w");
			fo.write(fullXML);
			fo.close();



