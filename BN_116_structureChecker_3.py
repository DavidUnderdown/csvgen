import os, os.path, logging, datetime, csv;

#check these settings are correct for the current drive
drive='K:\\'; #if working from copy eg T:\\WORK\\WO_95_sample\\5th sample' need double slashes as it's escape character
batchCode='BN116';
#these settings should only need to be changed once per project, when a new copy of this script should be created
lettercode='BN';
series='116';
items=True;
zeroFill=4;
pieceListFolder=os.path.join(os.getcwd(),'Piece lists');

#Following are standing data or calculate values derived from above and should not be altered
okFiles=0;
basePath=os.path.join(drive,lettercode+'_'+series);
basePathLength=len(basePath.split('\\'));

#set up basic logging to record outputs, level should usually be at .INFO, unless performing DEBUG diagnostics
def setup_logger(logger_name,log_file,logmode='w',level=logging.INFO) :
	l=logging.getLogger(logger_name);
	formatter=logging.Formatter('%(levelname)s\t: %(asctime)s : %(message)s');
	fileHandler=logging.FileHandler(log_file,logmode);
	fileHandler.setFormatter(formatter);
	l.setLevel(level);
	l.addHandler(fileHandler);

today=datetime.date.today().isoformat();
setup_logger('generalLog',os.path.join(os.getcwd(),'Logs',batchCode+'_folder_structure_check_'+today+'.log'),'a');
genlog=logging.getLogger('generalLog');

genlog.info('Starting Structure Checker for '+batchCode);
try :
	pieceListFile=open(os.path.join(pieceListFolder,batchCode+'_piece_list.csv'), "r", newline='');
except OSError :
	genlog.exception(os.path.join(pieceListFolder,batchCode+'_piece_list.csv')+' cannot be opened, structure checking unsuccesful, exiting...');
	exit();

dataIn=csv.DictReader(pieceListFile);
header=dataIn.fieldnames;
missingPieceList=[];
unexpectedPieceList=[];
header=dataIn.fieldnames;
if 'piece' != str.lower(header[0]) :
	genlog.error(batchCode+'_piece_list.csv does not contain piece column, structure checking unsuccesful, exiting...');
	exit();
pieceList=[]
for row in dataIn :
		pieceList.append(row[header[0]]);
pieceSet=set(pieceList);
pieceList=list(pieceSet); #this deduplicates the original list
pieceList.sort();
	
for dirPath, subdirList, fileList in os.walk(basePath) :
#for each directory starting at the given point, list the full path of the current directory, then list its subdirectories and files
	pathLength=len(dirPath.split('\\'));
	#this allows us to check how far down the structure we are
	genlog.debug('basePathLength='+str(basePathLength));
	genlog.debug('pathLength='+str(pathLength));
	genlog.debug('dirPath='+dirPath);
	genlog.debug('pieceList='+str(pieceList));
	genlog.debug('missingPieceList='+str(missingPieceList));
	genlog.debug('unexpectedPieceList='+str(unexpectedPieceList));
	genlog.debug('subdirList='+str(subdirList));
	genlog.debug('fileList='+str(fileList));
	if pathLength==basePathLength :
		if len(subdirList)==1 and subdirList[0]=='content' :
			pass;
		else :
			genlog.error('Content folder is missing');
	elif pathLength==basePathLength+1 :
	#We're looking at the contents of the content folder
		subdirList.sort()
		if pieceList==subdirList :
			genlog.info('all pieces from Piece List are present: '+str(pieceList));
		else :
			for piece in pieceList :
				genlog.debug('piece '+str(piece));
				if piece in subdirList :
					pass;
				else :
					missingPieceList.append(piece);
					genlog.debug('missingPieceList '+str(missingPieceList));
			for piece in subdirList :
				genlog.debug('piece '+str(piece));
				if piece in pieceList :
					pass;
				else :
					unexpectedPieceList.append(piece);
					genlog.debug('unexpectedPieceList '+str(unexpectedPieceList));
			if unexpectedPieceList :
				genlog.error('Extra piece(s) '+str(unexpectedPieceList)+' not in piece list are on disk');
			if missingPieceList :
				genlog.error('Piece(s) '+str(missingPieceList)+' in piece list are missing from disk');
	elif pathLength==basePathLength+2 :
	#We're looking at the contents of a piece level folder
		if items :
		#should we have items for this project? If so, wouldn't generally expect files in this folder
		#some projects may have mixed content, so may need re-work
			if len(fileList)>0 :
				genlog.error('item folders expected but files found at piece level');
			else :
			#Rebuild the subdirectory list as integers, not strings.   
			#Produce error message if there are no item folders.  Items should always start at 1 for each piece
			#(again, sometimes item numbering runs throughout a piece eg if service number used as item ref,
			#so this may need rework
				intSubdirList=[];
				currItem=1;
				if len(subdirList)==0 :
					genlog.error('no item level folders found for piece '+dirPath);
				for subdir in subdirList :
					intSubdirList.append(int(subdir));
					intSubdirList.sort();
				for intSubdir in intSubdirList :
					if intSubdir==currItem :
						currItem=currItem+1;
					else :
						genlog.error('missing item folder: '+str(currItem));
						currItem=intSubdir+1;
		else :
		#if we don't have items, the individual image files should be within the piece folder. At image level, we
		#apply zero padding to the running number in the file name, so sorting as strings should be fine
			fileList.sort();
			fileNumber=1;
			if len(fileList) > 0 :
				for file in fileList :
				#break the file name into its component parts, first split of the extension, following a full stop and check it's jp2
				#Then break at the underscore, first part should be piece number which is checked against the containing folder name
				#second part should be a running number starting at 1 (zero-padded to usually 3 or 4 digits)
					fileParts=file.split('.');
					if fileParts[-1]!='jp2' :
						genlog.error('non-jp2 file found: '+os.path.join(dirPath,file));
					elif len(fileParts)>2 :
						genlog.error('more than one full stop in filename: '+os.path.join(dirPath,file));
					else :
						filenameStruct=fileParts[0].split('_');
						genlog.debug('filenameStruct='+str(filenameStruct));
						if len(filenameStruct)!=2 :
							genlog.error(os.path.join(dirPath,file)+' wrong number of underscores ('+str(len(filenameStruct))+') in image name, expected 1');
						elif filenameStruct[0]==dirPath.split('\\')[-1] and str(fileNumber).zfill(zeroFill)==filenameStruct[-1] :
							fileNumber=fileNumber+1;
							okFiles=okFiles+1;
						else :
							genlog.error('missing or inconsistently named image at or before: '+os.path.join(dirPath,file));
							fileNumber=int(filenameStruct[-1])+1;
			else :
							genlog.error('no files found at piece level '+dirPath);
	elif pathLength==basePathLength+3 :
	#We're looking at an item level folder.  First check we do actually have files in the folder
	#Then for each file break down the filename as above for pieces, only here we have both piece and item incorporated in name
		if len(fileList)>0 :
			fileList.sort();
			fileNumber=1;
			for file in fileList :
				fileParts=file.split('.');
				if fileParts[-1]!='jp2' :
					genlog.error('non-jp2 file found: '+file);
				elif len(fileParts)>2 :
					genlog.error('more than one full stop in filename: '+os.path.join(dirPath,file));
				else :
					filenameStruct=fileParts[0].split('_');
					genlog.debug('filenameStruct='+str(filenameStruct));
					if len(filenameStruct)!=3 :
						genlog.error(os.path.join(dirPath,file)+' wrong number of underscores ('+str(len(filenameStruct))+') in image name, expected 2');
					elif filenameStruct[0]==dirPath.split('\\')[-2] and filenameStruct[1]==dirPath.split('\\')[-1] and str(fileNumber).zfill(zeroFill)==filenameStruct[-1] :
						fileNumber=fileNumber+1;
						okFiles=okFiles+1;
					else :
						genlog.error('missing or inconsistently named image at or before: '+os.path.join(dirPath,file));
						fileNumber=int(filenameStruct[-1])+1;
		else :
			genlog.error('no files found at item level '+dirPath);
genlog.info('Structure checking completed successfully: '+str(okFiles)+' files are correctly named');
#This count is correct if all files are present as expected, if errors are found the number of files indicated, plus number of errors, probably won't equal the total number of files 
#it is included only to give a visual confirmation that the script has actually run correctly.  If no output is found, some of fatal error has occurred.
