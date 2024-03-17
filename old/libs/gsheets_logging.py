"""
Google Sheets interaction lib. Configuration settings:
[gapps]
api_scope = https://www.googleapis.com/auth/spreadsheets
spreadsheet_id =
spreadsheet_range =
"""

import configparser
import traceback
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# setup the config
config = configparser.RawConfigParser()
config.read('config.conf')

# If modifying these scopes, delete the file token.json.
api_scope = config.get('gapps', 'api_scope')
spreadsheet_id = config.get('gapps', 'spreadsheet_id')

# set up the credentials token if it doesnt exist, read it if it does
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('gapps-auth.json', api_scope)
    creds = tools.run_flow(flow, store)

# build the sheets API service object
service = build('sheets', 'v4', http=creds.authorize(Http()))


# TODO: implement reading, example below
# request = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME)
# response = request.execute()
# return response


def update_row(tab_name, spreadsheet_range, update_rows):
    """
    Appends spreadsheet rows to a spreadsheet tab
    :param tab_name:
    :param spreadsheet_range:
    :param update_rows:
    :return:
    """
    target_body = {
        'majorDimension': 'ROWS',
        'values': update_rows
    }
    range_string = f"{tab_name}!{spreadsheet_range}"

    try:
        request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_string,
                                                         valueInputOption='RAW', body=target_body)
        response = request.execute()
        return response

    except:
        print(traceback.format_exc())
