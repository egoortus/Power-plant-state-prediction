import base64
import datetime
import io
import re

import pandas as pd

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table as dt

from dash.dependencies import Input, Output, State

from app import app


@app.callback(
    [
        Output('content-table', 'data'),
        Output('content-table', 'columns'),
        Output('content-table', 'selected_columns'),
        Output('ui-messages-table', 'data')
    ],
    [
        Input('files-upload', 'filename'),
        Input('files-upload-btn', 'filename')
    ],
    [
        State('files-upload', 'contents'),
        State('files-upload-btn', 'contents')
    ]
)
def update_filelist(names1, names2, contents1, contents2):
    names = names1 or names2
    contents = contents1 or contents2

    data, columns, selected_columns, error_files = [], [], [], []
    inv_type_files, inv_fmt_files = [], []

    if names and contents:
        file = dict(zip(names, contents))
        series = []

        for name, content in file.items():
            if not re.match(r'.+\.csv$', name):
                inv_type_files.append(name)
            else:
                content_type, content = content.split(',')
                content = base64.b64decode(content)
                content = io.StringIO(content.decode('utf-8'))

                try:
                    s = pd.read_csv(
                        content,
                        header=None,
                        sep=';',
                        usecols=[0],
                        squeeze=True
                    )
                    s.name = name
                    series.append(s)
                except Exception as e:
                    inv_fmt_files.append(name)

        if series:
            df = pd.DataFrame(series).T

            data = df.to_dict('records')
            columns = [
                {
                    'id': name,
                    'name': name,
                    'selectable': True,
                    'deletable': True
                } for name in df.columns
            ]
            selected_columns = df.columns
        
        if inv_fmt_files or inv_type_files:
            for name in inv_type_files:
                msg = f'Invalid type of ', html.B(name), '! Only CSV format!'
                error_files.append({'text': msg, 'type': 'danger'})
            
            for name in inv_fmt_files:
                msg = f'Invalid format of ', html.B(name), '! Only CSV format!'
                error_files.append({'text': msg, 'type': 'danger'})

    return data, columns, selected_columns, error_files


@app.callback(
    [Output('ui-messages-container', 'children')],
    [Input('ui-messages-table', 'data')],
    [State('ui-messages-container', 'children')]
)
def show_errors(messages, old_messages):
    if not messages:
        return [old_messages]

    return [old_messages + 
        [dbc.Alert(
            children=message['text'],
            color=message['type'],
            dismissable=True,
            duration=5_000,
        )  for message in messages]
    ]
