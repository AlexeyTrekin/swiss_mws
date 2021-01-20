ROWS = 100
COLS = 9


def get_format_request(sheet_id): #, rows=1000):
    # set column width
    widths = {1: 150, 2:50, 3:35, 4:60, 5:35, 6:50, 7:150}
    request = []
    for col, w in widths.items():
        request.append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS",  # COLUMNS - потому что столбец
                    "startIndex": col,  # Столбцы нумеруются с нуля
                    "endIndex": col + 1  # startIndex берётся включительно, endIndex - НЕ включительно,
                    # т.е. размер будет применён к столбцам в диапазоне [0,1), т.е. только к столбцу A
                },
                "properties": {
                    "pixelSize": w  # размер в пикселях
                },
                "fields": "pixelSize"  # нужно задать только pixelSize и не трогать другие параметры столбца
            }
        })

    # merge cells for the header
    request += [
        {'mergeCells': {'range': {'sheetId': sheet_id,
                                  'startRowIndex': 0,
                                  'endRowIndex': 1,
                                  'startColumnIndex': 1,
                                  'endColumnIndex': 5},
                        'mergeType': 'MERGE_ALL'}}]

    # color the fighters
    request += [
        {'repeatCell': {'range': {'sheetId': sheet_id,
                                  'startRowIndex': 1,
                                  'endRowIndex': ROWS,
                                  'startColumnIndex': 1,
                                  'endColumnIndex': 4},
                        'cell': {"userEnteredFormat": {
                            "backgroundColor": {
                                "red": 1,
                                "green": 0.6,
                                "blue": 0.6,
                                "alpha": 0.6
                            }}},
                        'fields': 'userEnteredFormat'}},

        {'repeatCell': {'range': {'sheetId': sheet_id,
                                  'startRowIndex': 1,
                                  'endRowIndex': ROWS,
                                  'startColumnIndex': 5,
                                  'endColumnIndex': 8},
                        'cell': {"userEnteredFormat": {
                            "backgroundColor": {
                                "red": 0.6,
                                "green": 0.6,
                                "blue": 1,
                                "alpha": 0.6
                            }}},
                        'fields': 'userEnteredFormat'}}
    ]

    # maybe add bold or text size increase to header?
    return request


def get_data_request(sheet_id):

    data_request = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": "Group_{}!B1:B1".format(sheet_id),
             "majorDimension": "ROWS",
             # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
             "values": [["1 ристалище"]]},

            {"range": "Group_{}!B2:J2".format(sheet_id),
             "majorDimension": "ROWS",
             # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
             "values": [
                 ["Фамилия", "Баллы", "!", "Обоюдки", "!", "Баллы", "Фамилия"]]},
        ]}
    return data_request


def get_create_sheet_request(sheet_id):
    request = [{'addSheet':
                {'properties': {
                      "sheetId": sheet_id,
                      "title": 'Group_{}'.format(sheet_id),
                      "gridProperties": {
                          "rowCount": ROWS,
                          "columnCount": COLS
                      },
                   }
                 }
                }]
    return request


def get_pair_position(sheet_num, pair_num, num_rounds):
    """
    Gets the position in format Round_1!A1:A3
    The position is 1-column only
    :param round_number:
    :param area:
    :param pair_num:
    :return:
    """
    # 1-based area

    column_begin = 'B'
    column_end = 'J'

    sheet = f'Group_{sheet_num}'
    row_begin = pair_num * num_rounds + 3  # heading
    row_end = row_begin + num_rounds

    return f'{sheet}!{column_begin}3:{column_end}{row_end}'


def get_all_range(round_number):
    return 'Group_{}!A1:J{}'.format(round_number, ROWS)
