from envparse import env
env.read_envfile()

sqlhost = env.str('sqlhost')
sqlport = env.int('sqlport')
sqluser = env.str('sqluser')
sqlpassword = env.str('sqlpassword')
sqldb = env.str('sqldb')

slacktoken = env.str('slacktoken')
slackteam = 'user_activity'

uldt = 'ldt_users.txt'
pldt = 'ldt_projects.txt'
