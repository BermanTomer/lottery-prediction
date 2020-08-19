import pandas as pd 
import datetime as dt
import shutil
import urllib.request
import codecs
from threading import Timer
import filecmp
import os.path
from os import path
from itertools import islice
import sched, time
#Get file name and which line to read - return the line string
def read_line(file,line):	
		with open(file) as fin:
			lines = fin.readlines()			
			try:
				return(lines[line])
			except:
				print(file+ " is empty - copy data from orig file")
				copy_file()

			# for line in islice(fin,line):
#function comper 2 files based on specice line
def filecmp(backupfile,updated_file,line_2_comper):
	if(path.exists(backupfile)):		
		file2 = read_line(updated_file,line_2_comper)		
		file1 = read_line(backupfile,line_2_comper)
		print(f"{file1}+ \n+ {file2}")
		return (file1 == file2 )		
	else:
		create_file(backupfile)
		filecmp(backupfile,updated_file,line_2_comper)

def create_file(name):
	f = open(name, "w")
	f.write(name + "created")
	f.close()


def get_file(arg1,arg2):
	print("Getting the file from the lotto website")	
	url = 'https://www.pais.co.il/Lotto/lotto_resultsDownload.aspx'
	urllib.request.urlretrieve(url, 'c:/Users/user/Desktop/LottoProject/Lotto_heb.csv')

def copy_file():
	with open('Lotto_heb_last_ver.csv','wb') as wfd:
		for f in ['Lotto_heb.csv']:
			with open(f,'rb') as fd:
				shutil.copyfileobj(fd, wfd)	

def first_line(*args):
	# change the header to english
	# גרלה,תאריך,1,2,3,4,5,6,המספר החזק/נוסף,מספר_זוכים_לוטו,מספר_זוכים_דאבל_לוטו,
	# number,date,1,2,3,4,5,6,strong,winners,winner_double
	new_line='number,date,1,2,3,4,5,6,strong,winners,winner_double,\n'
	f = open("header.csv", "w")
	f.write(new_line)

	with open('Lotto_heb.csv', 'r') as fin:
		data = fin.read().splitlines(True)
	with open('Lotto_temp.csv', 'w') as fout:
		fout.writelines(data[1:])


	with open('Lotto_eng.csv','wb') as wfd:
		for f in ['header.csv','Lotto_temp.csv']:
			with open(f,'rb') as fd:
				shutil.copyfileobj(fd, wfd)

def read_file():
	lotto_result = pd.read_csv('Lotto_eng.csv',encoding = "UTF-8")
	#Convet the data field to be dd/mm/yy
	df = pd.DataFrame(pd.DatetimeIndex(lotto_result['date']))
	df['date'] = pd.to_datetime(df.date)
	lotto_result["week_format"] = df['date'].dt.strftime('%d/%m/%Y')
	lotto_result["week"] = pd.DatetimeIndex(lotto_result['week_format']).week 
	# print((lotto_result[lotto_result['week']==32]))
	df = pd.DataFrame(lotto_result)

	gb= df.groupby(['1','2','3','4','5','6'],as_index=False, sort=False).size().reset_index(name='counts')
	gb = (gb.sort_values(['counts'], ascending=[False]))
	gb = gb[gb["counts"] >1]

	print(gb[['1','2','3','4','5','6','counts']] )

def main():
	file_d = {'heb':'Lotto_heb.csv'}
	try:
		with open('Lotto_heb.csv') as fin:
			pass
	except:
		fiels = ['Lotto_heb_last_ver.csv','Lotto_heb.csv','Lotto_temp.csv']
		for f in fiels:
			with open(f,'w') as f:
				f.close()
	print("####Start####")
	#the second line of the files is deffrent then the file from the looto web site has changed 
	line_2_comper = 1
	try:
		get_must_updated_file = Timer(0.0, get_file, ("arg1","arg2"))
		# is_exists= filecmp('Lotto_heb_last_ver.csv','Lotto_heb.csv',line_2_comper)
		is_exists= filecmp('Lotto_heb_last_ver.csv','Lotto_heb.csv',line_2_comper)
	except FileNotFoundError:
		print("ERROR: Wrong file or file path")
	##update the backupfile only if the orig file "lotto_heb" has changed
	if not is_exists:
		copy_file()
	parsering_heb2eng = Timer(1.5, first_line, ("arg1","arg2"))
	three = Timer(3.0, read_file)


	get_must_updated_file.start()	
	parsering_heb2eng.start()
	three.start()


if __name__ == "__main__":
    # execute only if run as a script
    main()


