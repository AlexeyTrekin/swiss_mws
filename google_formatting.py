
def get_format_request(sheetId, rows=1000):
    # set column width
    request = []
    for col in [2, 3, 4, 5, 7, 9, 10, 11, 12]:
        request.append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sheetId,
                    "dimension": "COLUMNS",  # COLUMNS - потому что столбец
                    "startIndex": col,  # Столбцы нумеруются с нуля
                    "endIndex": col + 1  # startIndex берётся включительно, endIndex - НЕ включительно,
                    # т.е. размер будет применён к столбцам в диапазоне [0,1), т.е. только к столбцу A
                },
                "properties": {
                    "pixelSize": 35  # размер в пикселях
                },
                "fields": "pixelSize"  # нужно задать только pixelSize и не трогать другие параметры столбца
            }
        })
    # merge cells for the header
    request += [
        {'mergeCells': {'range': {'sheetId': sheetId,
                                  'startRowIndex': 0,
                                  'endRowIndex': 1,
                                  'startColumnIndex': 1,
                                  'endColumnIndex': 7},
                        'mergeType': 'MERGE_ALL'}},
        {'mergeCells': {'range': {'sheetId': sheetId,
                                  'startRowIndex': 0,
                                  'endRowIndex': 1,
                                  'startColumnIndex': 8,
                                  'endColumnIndex': 14},
                        'mergeType': 'MERGE_ALL'}}]

    # color the fighters
    request += [
        {'repeatCell': {'range': {'sheetId': sheetId,
                                  'startRowIndex': 1,
                                  'endRowIndex': rows,
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

        {'repeatCell': {'range': {'sheetId': sheetId,
                                  'startRowIndex': 1,
                                  'endRowIndex': rows,
                                  'startColumnIndex': 8,
                                  'endColumnIndex': 11},
                        'cell': {"userEnteredFormat": {
                            "backgroundColor": {
                                "red": 1,
                                "green": 0.6,
                                "blue": 0.6,
                                "alpha": 0.6
                            }}},
                        'fields': 'userEnteredFormat'}},

        {'repeatCell': {'range': {'sheetId': sheetId,
                                  'startRowIndex': 1,
                                  'endRowIndex': rows,
                                  'startColumnIndex': 4,
                                  'endColumnIndex': 7},
                        'cell': {"userEnteredFormat": {
                            "backgroundColor": {
                                "red": 0.6,
                                "green": 0.6,
                                "blue": 1,
                                "alpha": 0.6
                            }}},
                        'fields': 'userEnteredFormat'}},

        {'repeatCell': {'range': {'sheetId': sheetId,
                                  'startRowIndex': 1,
                                  'endRowIndex': rows,
                                  'startColumnIndex': 11,
                                  'endColumnIndex': 14},
                        'cell': {"userEnteredFormat": {
                            "backgroundColor": {
                                "red": 0.6,
                                "green": 0.6,
                                "blue": 1,
                                "alpha": 0.6
                            }}},
                        'fields': 'userEnteredFormat'}},

    ]

    # maybe add bold or text size increase to header?
    return request


def get_data_request(sheetId):
    data_request = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": "Round_{}!B1:B1".format(sheetId+1),
             "majorDimension": "ROWS",
             # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
             "values": [["1 ристалище"]]},

            {"range": "Round_{}!I1:I1".format(sheetId+1),
             "majorDimension": "COLUMNS",
             # сначала заполнять столбцы, затем ряды (т.е. самые внутренние списки в values - это столбцы)
             "values": [["2 ристалище"]]},

            {"range": "Round_{}!B2:N2".format(sheetId+1),
             "majorDimension": "ROWS",
             # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
             "values": [
                 ["Фамилия", "HP", "Бой", "Бой", "HP", "Фамилия", "", "Фамилия", "HP", "Бой", "Бой", "HP", "Фамилия"]]},
        ]}
    return data_request


def get_pair_position(round_number, area, pair_num):
    """
    Gets the position in format Round_1!A1:A3
    :param round_number:
    :param area:
    :param pair_num:
    :return:
    """
    # 1-based area
    if area == 0:
        columns = ('B', 'G')
    elif area == 1:
        columns = ('I', 'N')
    else:
        raise NotImplementedError('Only 0 and 1 are valid areas')
    sheet = 'Round_' + str(round_number)
    row = pair_num + 3  # heading
    return '{sheet}!{begin}3:{end}{row}'.format(sheet=sheet, row=row, begin=columns[0], end=columns[1])
