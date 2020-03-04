import time
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials as SAC

from .api import Api
from .utils import split_to_areas
from TM.tournament import Fight, Fighter, Round

from .google_formatting import get_data_request, get_format_request, get_pair_position, get_create_sheet_request, get_all_range

CREDENTIALS_FILE = 'google_token.json'


credentials = SAC.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                              'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
#doc_id ='1pdeBOVo3SFBAXPw6wcPfK3bn_yQfNcuNBFVpwOpdfGg'


def create_new_doc(name, rows=1000, columns=25):
    sheets = [(
        {'properties': {'sheetType': 'GRID',
                        'sheetId': 1000,
                        'title': 'Hello',
                        'gridProperties': {'rowCount': rows, 'columnCount': columns}}})]

    try:
        spreadsheet = service.spreadsheets().create(body={
            'properties': {'title': name, 'locale': 'ru_RU'},
            'sheets': sheets
        }).execute()
    except Exception as e:
        print('Creation failed\n' + str(e))
        return ''
    return spreadsheet['spreadsheetId']


class GoogleAPI(Api):
    def __init__(self, spreadsheet_id=None, num_areas=2,
                 name="", collaborators=None, **kwargs):
        Api.__init__(self)
        self.num_areas = num_areas
        if spreadsheet_id is not None:
            self._spreadsheet_id = spreadsheet_id
        else:
            self._spreadsheet_id = create_new_doc(name, **kwargs)
        if collaborators:
            self.share(collaborators)
        #for r in range(rounds):
        #    self.fill_heading(r)

    @property
    def spreadsheet_id(self):
        return self._spreadsheet_id

    @property
    def SpreadsheetURL(self):
        return 'https://docs.google.com/spreadsheets/d/{}/edit#gid=0'.format(self._spreadsheet_id)

    @staticmethod
    def parse_results(response):
        """
        The result parsing depends on the tournament, so here we use the MWS rules where all points are negative
        :param response:
        :return:
        """

        fighter_1 = response[0].rstrip().strip('\"')
        result_1 = -abs(int(response[2].rstrip().strip('\"')))
        fighter_2 = response[5].rstrip().strip('\"')
        result_2 = -abs(int(response[3].rstrip().strip('\"')))
        r = Round(status='finished', score_1=result_1, score_2=result_2)

        return Fight(fighter_1, fighter_2, 'finished', rounds_num=1, rounds=[r],
                     rating_score_1=result_1, rating_score_2=result_2)

    def write(self,
              pairs,
              fighters, round_num):
        self.add_sheet(round_num)

        area_index = split_to_areas(len(pairs), self.num_areas)
        area_pairs = [pairs[area_index[i][0]:area_index[i][1]] for i in range(self.num_areas)]

        for i, area in enumerate(area_pairs):
            position = get_pair_position(round_num, i, len(area))
            pair_data = [fighters[pair.fighter_1].to_list() + fighters[pair.fighter_2].to_list()[::-1] for pair in area]
            data_request = {
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        {"range": position,
                         "majorDimension": "ROWS",
                         # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
                         "values": pair_data}
            ]}
            service.spreadsheets().values().batchUpdate(spreadsheetId=self._spreadsheet_id,
                                                                  body=data_request).execute()
        return self.SpreadsheetURL

    def read(self, round_num):
        data = []
        for area in range(self.num_areas):
            read_range = get_pair_position(round_num, area, 1000)
            response = service.spreadsheets().values().get(spreadsheetId=self._spreadsheet_id,
                                                           range=read_range).execute()
            # response['values'] = [[fighter1, hp1, result1, result2, hp2, fighter2],[...]]
            # we format it in the api standard Fight()
            results = [self.parse_results(fight) for fight in response['values']]
            data += results
        return data

    def share(self, collaborators):
        drive_service = apiclient.discovery.build('drive', 'v3', http=httpAuth)
        for email in collaborators:
            time.sleep(2)
            drive_service.permissions().create(
                fileId=self._spreadsheet_id,
                body={'type': 'user', 'role': 'writer', 'emailAddress': email},
                fields='id'
            ).execute()

    def fill_heading(self, sheet_id):
        request = get_format_request(sheet_id)
        # Execute the request
        try:
            service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id,
                                                     body={"requests": request}).execute()
        except Exception as e:
            print('Failed to format the page {}\n'.format(sheet_id) + str(e))

        try:
            service.spreadsheets().values().clear(spreadsheetId=self.spreadsheet_id,
                                                  range=get_all_range(sheet_id + 1)).execute()
        except Exception as e:
            print('Failed to clear the table values in the page {}\n'.format(sheet_id) + str(e))

        # Data request - fill the static data
        data_request = get_data_request(sheet_id)
        try:
            service.spreadsheets().values().batchUpdate(spreadsheetId=self._spreadsheet_id,
                                                              body=data_request).execute()
        except Exception as e:
            print('Failed to put the table header {}\n'.format(sheet_id) + str(e))
        return

    def add_sheet(self, round_num):
        request = get_create_sheet_request(sheet_id=round_num-1)
        try:
            service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id,
                                                     body={"requests": request}).execute()
        except Exception as e:
            print('Failed to create the page for round {}\n'.format(round_num) + str(e))
        self.fill_heading(round_num-1)

