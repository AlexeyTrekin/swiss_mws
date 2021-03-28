import time
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials as SAC

from .api import Api
from TM.tournament import Fight, Round

from .google_formatting import get_data_request, get_format_request, get_pair_position, get_create_sheet_request, get_all_range

CREDENTIALS_FILE = 'google_token.json'
DEFAULT_SHEET = 1000

credentials = SAC.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                              'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
#doc_id ='1pdeBOVo3SFBAXPw6wcPfK3bn_yQfNcuNBFVpwOpdfGg'


def create_new_doc(name):
    sheets = [(
        {'properties': {'sheetType': 'GRID',
                        'sheetId': DEFAULT_SHEET,
                        'title': 'Hello',
                        'gridProperties': {'rowCount': 1, 'columnCount': 1}}})]

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
    def __init__(self, spreadsheet_id=None, num_areas=1, num_rounds=1,
                 name="", collaborators=None):
        Api.__init__(self)
        self.num_areas = num_areas
        self.num_rounds=num_rounds

        self.sheet_names = {}

        if spreadsheet_id is not None:
            self._spreadsheet_id = spreadsheet_id
        else:
            self._spreadsheet_id = create_new_doc(name)
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
        The result parsing depends on the tournament, so here we use standard parsing for the groupwise qualifications
        :param response:
        :return:
        """
        rounds = []

        '''
        
        fighter_1 = response[0][0].rstrip().strip('\"')
        fighter_2 = response[0][6].rstrip().strip('\"')

        for line in response:
            result_1 = (int(line[1].rstrip().strip('\"')))
            result_2 = (int(line[5].rstrip().strip('\"')))

            warnings_1 = (int(line[2].rstrip().strip('\"')))
            warnings_2 = (int(line[4].rstrip().strip('\"')))

            doubles = (int(response[3].rstrip().strip('\"')))

            rounds.append(Round(status='finished', score_1=result_1, score_2=result_2,
                                doubles=doubles, warnings_1=warnings_1, warnings_2=warnings_2))
        '''

        fighter_1 = response[0][0].rstrip().strip('\"')
        fighter_2 = response[0][8].rstrip().strip('\"')
        #print(response)
        for line in response:
            # Pad the line because the empty trailing cells are omitted
            while len(line) < 6:
                line.append('')
            # We do not want to fill all the fields, so if they are empty (or full of bullshit) we ignore them and put 0
            try:
                result_1 = (int(line[2].rstrip().strip('\"')))
            except ValueError:
                result_1 = 0
            try:
                result_2 = (int(line[6].rstrip().strip('\"')))
            except ValueError:
                result_2 = 0
            try:
                warnings_1 = (int(line[3].rstrip().strip('\"')))
            except ValueError:
                warnings_1 = 0
            try:
                warnings_2 = (int(line[5].rstrip().strip('\"')))
            except ValueError:
                warnings_2 = 0
            try:
                doubles = (int(line[3].rstrip().strip('\"')))
            except ValueError:
                doubles = 0

            rounds.append(Round(status='finished', score_1=result_1, score_2=result_2,
                                    doubles=doubles, warnings_1=warnings_1, warnings_2=warnings_2))

        return Fight(fighter_1, fighter_2, 'finished', rounds_num=len(rounds), rounds=rounds)

    def write(self,
              pairs,
              fighters,
              round_num,
              stage_name,
              **kwargs):
        # check if sheet exists
        sheets_info = service.spreadsheets().get(spreadsheetId=self._spreadsheet_id).execute()
        sheet_ids = [sheet['properties']['sheetId'] for sheet in sheets_info['sheets']]
        if stage_name is None:
            stage_name = f'Round {round_num}'
        # Store the id:name mapping
        self.sheet_names[round_num] = stage_name

        if not round_num in sheet_ids:
            # If we try to create existing sheet, we get an annoying error response.
            # However, we could delete-create this sheet instead to avoid format errors
            self.add_sheet(round_num, stage_name, rows=3 + len(pairs)*self.num_rounds)

        if DEFAULT_SHEET in sheet_ids:
            # remove the initial sheet - it is useless
            service.spreadsheets().batchUpdate(spreadsheetId=self._spreadsheet_id,
                                               body={'requests':[{'deleteSheet':{'sheetId': DEFAULT_SHEET}}]}).execute()

        all_data = []
        position = get_pair_position(stage_name, len(pairs), self.num_rounds)
        format_request = []

        for i, pair in enumerate(pairs):
            #

            # Add a string for every round
            #for _ in range(pair.rounds_num):
            all_data += [fighters[pair.fighter_1].to_list() + [''] + fighters[pair.fighter_2].to_list()[::-1]]*self.num_rounds
            # Merge cells
            if self.num_rounds > 0:
                format_request += [
                    {'mergeCells': {'range': {'sheetId': round_num,
                                              'startRowIndex': self.num_rounds*i + 2,
                                              'endRowIndex': self.num_rounds*(i+1) + 2,
                                              'startColumnIndex': 1,
                                              'endColumnIndex': 2},
                                    'mergeType': 'MERGE_ALL'}},
                    {'mergeCells': {'range': {'sheetId': round_num,
                                              'startRowIndex': self.num_rounds*(i) + 2,
                                              'endRowIndex': self.num_rounds*(i+1) + 2,
                                              'startColumnIndex': 7,
                                              'endColumnIndex': 8},
                                    'mergeType': 'MERGE_ALL'}}
                ]

        data_request = {
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": position,
                     "majorDimension": "ROWS",
                     # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
                     "values": all_data}
        ]}
        service.spreadsheets().values().batchUpdate(spreadsheetId=self._spreadsheet_id,
                                                    body=data_request).execute()
        if self.num_rounds > 1:
            response = service.spreadsheets().batchUpdate(spreadsheetId=self._spreadsheet_id,
                                               body={"requests": format_request}).execute()
        return self.SpreadsheetURL

    def read(self, sheet_num):
        try:
            sheet_name = self.sheet_names[sheet_num]
            print(sheet_name)
        except KeyError as ke:
            # Read the names from the file
            sheets_info = service.spreadsheets().get(spreadsheetId=self._spreadsheet_id).execute()
            sheet_names = [sheet['properties']['title'] for sheet in sheets_info['sheets']
                           if sheet['properties']['sheetId'] == sheet_num]
            if len(sheet_names) == 0:
                print(f'The sheet with ID {sheet_num} is not present in the file')
                raise ke
            else:
                sheet_name = sheet_names[0]

        # We read everything like 1-round fights and parse it later
        read_range = get_pair_position(sheet_name, 1000, self.num_rounds)
        response = service.spreadsheets().values().get(spreadsheetId=self._spreadsheet_id,
                                                        range=read_range).execute()

        # response['values'] = [[fighter1, result1, warnings1, doubles, warnings2, result2, fighter2],[...]]
        # we format it in the api standard Fight()
        fights = []
        for fight_num in range(len(response['values'])//self.num_rounds):
            fights.append([response['values'][i] for i in range(fight_num*self.num_rounds, (fight_num+1)*self.num_rounds)])
        results = [self.parse_results(fight) for fight in fights]
        return results

    def share(self, collaborators):
        drive_service = apiclient.discovery.build('drive', 'v3', http=httpAuth)
        # get current collaborators emails:
        permissions = drive_service.permissions().list(fileId=self._spreadsheet_id,
                                                       fields='permissions/emailAddress').execute()
        current_collaborators = [perm.get('emailAddress', '').lower() for perm in permissions.get('permissions', [])]
        for email in collaborators:
            if email.lower() in current_collaborators:
                continue
            time.sleep(2)
            # This request requires time delay to be accepted by google
            drive_service.permissions().create(
                    fileId=self._spreadsheet_id,
                    body={'type': 'user', 'role': 'writer', 'emailAddress': email},
                    fields='id'
            ).execute()

    def fill_heading(self, sheet_num, sheet_name):

        request = get_format_request(sheet_num)
        # Execute the request
        try:
            service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id,
                                                     body={"requests": request}).execute()
        except Exception as e:
            print('Failed to format the page {}\n'.format(sheet_name) + str(e))

        try:
            service.spreadsheets().values().clear(spreadsheetId=self.spreadsheet_id,
                                                  range=get_all_range(sheet_name)).execute()
        except Exception as e:
            print('Failed to clear the table values in the page {}\n'.format(sheet_name) + str(e))

        # Data request - fill the static data
        data_request = get_data_request(sheet_name)
        try:
            service.spreadsheets().values().batchUpdate(spreadsheetId=self._spreadsheet_id,
                                                              body=data_request).execute()
        except Exception as e:
            print('Failed to put the table header for sheet {}\n'.format(sheet_name) + str(e))
        return

    def add_sheet(self, sheet_num, sheet_name=None, rows=None, cols=None):

        request = get_create_sheet_request(sheet_id=sheet_num, sheet_name=sheet_name, rows=rows, cols=cols)
        try:
            service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id,
                                                     body={"requests": request}).execute()
        except Exception as e:
            print('Failed to create the page for round {}\n'.format(sheet_num) + str(e))
        self.fill_heading(sheet_num, sheet_name)

