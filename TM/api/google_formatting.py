ROWS = 100
COLS = 9


def get_format_request(sheet_num):
    # set column width
    widths = {1: 150, 2:50, 3:35, 4:60, 5:35, 6:50, 7:150}
    request = []
    for col, w in widths.items():
        request.append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sheet_num,
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
        {'mergeCells': {'range': {'sheetId': sheet_num,
                                  'startRowIndex': 0,
                                  'endRowIndex': 1,
                                  'startColumnIndex': 1,
                                  'endColumnIndex': 5},
                        'mergeType': 'MERGE_ALL'}}]

    # color the fighters
    request += [
        {'repeatCell': {'range': {'sheetId': sheet_num,
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

        {'repeatCell': {'range': {'sheetId': sheet_num,
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


def get_data_request(sheet_name: str):

    data_request = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": "{}!B1:B1".format(sheet_name),
             "majorDimension": "ROWS",
             # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
             "values": [["1 ристалище"]]},

            {"range": "{}!B2:J2".format(sheet_name),
             "majorDimension": "ROWS",
             # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
             "values": [
                 ["Фамилия", "Баллы", "!", "Обоюдки", "!", "Баллы", "Фамилия"]]},
        ]}
    return data_request


def get_create_sheet_request(sheet_id, sheet_name, rows=None, cols=None):
    rows = rows or ROWS
    cols = cols or COLS
    request = [{'addSheet':
                {'properties': {
                      "sheetId": sheet_id,
                      "title": sheet_name,
                      "gridProperties": {
                          "rowCount": rows,
                          "columnCount": cols
                      },
                   }
                 }
                }]
    return request


def get_pair_position(sheet_name, pair_num, num_rounds):
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

    row_begin = pair_num * num_rounds + 3  # heading
    row_end = row_begin + num_rounds

    return f'{sheet_name}!{column_begin}3:{column_end}{row_end}'


def get_all_range(sheet_name):
    return f'{sheet_name}!A1:J{ROWS}'
