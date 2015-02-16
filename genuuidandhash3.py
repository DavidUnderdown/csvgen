import uuid, hashlib, os, csv, urllib.parse, random;

beginXML='''<?xml version="1.0" encoding="utf-8"?>
<DigitalFile xmlns="http://nationalarchives.gov.uk/2012/dri/artifact/embedded/metadata" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
''';
openUUIDtag='<UUID>';
closeUUIDtag='''</UUID>
''';
openURLtag='<URI>';
baseURL='http://datagov.nationalarchives.gov.uk/66/';
department='TEST';
series=1;
initialpiece=1;
totalpieces=2;
initialitem=1;
totalitems=2;
closeURLtag='''</URI>
''';
endXML='''<Copyright>&#169; Crown copyright: The National Archives of the UK</Copyright>
</DigitalFile>''';
fileExtension='.xml';
filenameBase=os.getcwd();
filelist=[['batch_code','department','division','series','sub_series','sub_sub_series','piece','item','file_uuid','file_path','file_checksum','resource_uri','scan_operator','scan_id','scan_location','image_resolution','image_width','image_height','image_tonal_resolution','image_format','image_compression','image_colour_space','image_split','image_split_other_uuid','image_crop','image_deskew','comments']];
batch_code='TESTBATCH000';
division='';
sub_series='';
sub_sub_series='';
scan_operator='scanop';
scan_id='scanner';
scan_location='The National Archives, TW9 4DU';
image_resolution='300';
image_tonal_resolution='24-bit colour';
image_format='x-fmt/392';
image_compression='6';
image_colour_space='sRGB';
image_split='no';
image_split_other_uuid='';
image_crop='auto';
image_deskew='no'
comments='Files would normally be JPEG2000s, but to keep to a manageable size, for these examples only the XML which would normally be embedded is presented';

def checksum(fullfilepath) :
	fo=open(fullfilepath, "rb");
	fileHash=hashlib.sha256(fo.read()).hexdigest();
	fo.close();
	return fileHash;
	
def addToFilelist(currentpiece,currentitem,UuidString,fileURI,fullURL,filepath,filename) :
	filelist.append([batch_code,department,division,str(series),sub_series,sub_sub_series,currentpiece,currentitem,UuidString,fileURI,checksum(os.path.join(filepath,filename)),fullURL,scan_operator+str(random.randint(1,5)).zfill(2),scan_id+str(random.randint(1,3)).zfill(2),scan_location,image_resolution,str(random.randint(2400,2600)),str(random.randint(3450,3650)),image_tonal_resolution,image_format,image_compression,image_colour_space,image_split,image_split_other_uuid,image_crop,image_deskew,comments]);

def buildURL(piecestring,itemstring,UuidString) :
	if itemstring : #ie if itemstring is not the empty string
		itempart=itemstring+'/';
	else :
		itempart=itemstring;
	
	return baseURL+department+'/'+str(series)+'/'+piecestring+'/'+itempart+UuidString;

def buildXML(UuidString,fullURL) :
	return beginXML+openUUIDtag+UuidString+closeUUIDtag+openURLtag+fullURL+closeURLtag+endXML;

def buildFileMetadata(topdir,piecestring,itemstring) :
	if itemstring : #ie if itemstring is not the empty string
		filenameitempart=itemstring+'_';
		itempart=itemstring+'/';
	else :
		itempart=itemstring;
		
	filename=piecestring+'_'+filenameitempart+str(fileCounter).zfill(3)+fileExtension;
	if itemstring : #ie if itemstring is not the empty string
		filepath=os.path.join(filenameBase,topdir,piecestring,itemstring);
	else :
		filepath=os.path.join(filenameBase,topdir,piecestring);

	fileURI='file:///'+topdir+'/'+piecestring+'/'+itempart+filename;
	
	return (filename,filepath,fileURI);

def buildDirectoriesAndWriteFile(filename,filepath,fullXML) :
	if os.path.exists(filepath) :
		pass;
	else :
		os.makedirs(filepath);

	fo=open(os.path.join(filepath,filename), "w");
	fo.write(fullXML);
	fo.close();
				
for fileCounter in range(1,11) :
	for currentpiece in range(initialpiece,initialpiece+totalpieces) : 
		topdir=department+'_'+str(series);
		piecestring=str(currentpiece);
		
		if initialitem :
			for currentitem in range(initialitem,initialitem+totalitems) :
				UuidString=str(uuid.uuid4());
				
				fullURL=buildURL(piecestring,str(currentitem),UuidString);
				fullXML=buildXML(UuidString,fullURL);
				
				fileMetadata=buildFileMetadata(topdir,piecestring,str(currentitem));
				fileURI=fileMetadata[2];
				
				buildDirectoriesAndWriteFile(fileMetadata[0],fileMetadata[1],fullXML)
				addToFilelist(currentpiece,currentitem,UuidString,fileURI,fullURL,fileMetadata[1],fileMetadata[0]);

		else :
			currentitem='';
			UuidString=str(uuid.uuid4());
		
			fullURL=buildURL(piecestring,currentitem,UuidString);
			fullXML=buildXML(UuidString,fullURL);
		
			fileMetadata=buildFileMetadata(topdir,piecestring,str(currentitem));
			fileURI=fileMetadata[2];

			buildDirectoriesAndWriteFile(fileMetadata[0],fileMetadata[1],fullXML)
			addToFilelist(currentpiece,currentitem,UuidString,fileURI,fullURL,fileMetadata[1],fileMetadata[0]);

CSVfilepath=os.path.join(filenameBase,'digitised_surrogate_tech_acq_metadata_v1_'+batch_code+'.csv');			
filelistCSV=open(CSVfilepath, 'w', newline='');
csv.writer(filelistCSV,dialect='excel').writerows(filelist);
filelistCSV.close()

CSVchecksum=checksum(CSVfilepath);
sha256file=open(CSVfilepath+'.sha256', 'w', newline='');
sha256file.write(CSVchecksum+'\t'+'digitised_surrogate_tech_acq_metadata_v1_'+batch_code+'.csv');
sha256file.close;