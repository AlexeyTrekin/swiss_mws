import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials as SAC

CREDENTIALS_FILE = 'mws-tournament-fa7e5f4c8445.json'


credentials = SAC.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                              'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
doc_id ='1pdeBOVo3SFBAXPw6wcPfK3bn_yQfNcuNBFVpwOpdfGg'