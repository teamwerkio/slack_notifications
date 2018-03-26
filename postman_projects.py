import info
import pymysql
import datetime
from slacker import Slacker

def post(msg):
	slack = Slacker(info.slacktoken)
	slackmsg = str(msg)
	slack.chat.post_message(info.slackteam, slackmsg)
	return True

def get(datetime):

	dt = str(datetime)

	connection = pymysql.connect(
		host = info.sqlhost,
		port = info.sqlport,
		user = info.sqluser,
		password = info.sqlpassword,
		db = info.sqldb,
		charset='utf8mb4',
		cursorclass=pymysql.cursors.DictCursor
	)

	rsql = ["SELECT project.usrID, users.firstname, users.lastname, project.projName, project.dt FROM project INNER JOIN users ON project.usrID = users.usrID WHERE project.dt > '", dt, "' ORDER by dt"]
	sql = ''.join(rsql)
	cursor = connection.cursor()
	cursor.execute(sql)
	cursor.close()

	data = cursor.fetchall()

	return data

def parse(data):

	newdate = None

	size = len(data)
	if size != 0:
		for dmap in data:
			uid = str(dmap['usrID'])
			uname = str(' '.join([dmap['firstname'], dmap['lastname']]))
			projname = str(dmap['projName'])
			udt = str(dmap['dt'])
			message = ''.join(["`", uname, "` userID `", uid, "` added project `", projname, "` at datetime `", udt, "`"])
			post(message)
			newdate = udt
			ldtfile = open(info.pldt, 'w')
			ldtfile.write(newdate)
			ldtfile.close()

	return newdate

def main():
	ldtfile = open(info.pldt, 'r')
	ldt = ldtfile.read()
	ldtfile.close()
	gdata = get(str(ldt))
	ldate = parse(gdata)
	if ldate == None:
		print('No new users')
	return True

if __name__ == '__main__':
	main()
