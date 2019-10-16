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

import features


@app.callback(
    [
        Output('upload-table', 'data'),
        Output('messages-table', 'data'),
    ],
    [
        Input('files-upload', 'filename'),
        Input('files-upload-btn', 'filename'),
    ],
    [
        State('files-upload', 'contents'),
        State('files-upload-btn', 'contents'),
    ]
)
def upload_files(names1, names2, contents1, contents2):
    names, contents = names1 or names2, contents1 or contents2
    
    data, error_files = [], []
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
        
        if inv_fmt_files or inv_type_files:
            for name in inv_type_files:
                msg = f'Invalid type of ', html.B(name), '! Only CSV format!'
                error_files.append({'text': msg, 'type': 'danger'})
            
            for name in inv_fmt_files:
                msg = f'Invalid format of ', html.B(name), '! Only CSV format!'
                error_files.append({'text': msg, 'type': 'danger'})

    return data, error_files


@app.callback(
    [
        Output('files-table', 'data'),
        Output('files-table', 'selected_rows'),
        Output('table-controls-store', 'data'),
    ],
    [   
        Input('upload-table', 'data'),
        Input('select-files-btn', 'n_clicks'),
        Input('delete-files-btn', 'n_clicks'),
    ],
    [
        State('files-table', 'data'),
        State('files-table', 'selected_rows'),
        State('table-controls-store', 'data'),
    ],
)
def update_files(
    data,
    select_clicks,
    delete_clicks,
    files,
    selected_rows,
    controls_store
):
    if controls_store.get('select-files-btn-clicks', 0) != select_clicks:
        controls_store['select-files-btn-clicks'] = select_clicks
        if selected_rows:
            selected_rows = []
        else:
            selected_rows = list(range(len(files)))
    elif controls_store.get('delete-files-btn-clicks', 0) != delete_clicks:
        controls_store['delete-files-btn-clicks'] = delete_clicks
        files, selected_rows = [], []
    else:
        df = pd.DataFrame(data)

        files_df = pd.DataFrame(files)
        new_files_df = pd.DataFrame()

        for col in df.columns:
            new_files_df = new_files_df.append({
                'id': col,
                'filename': col, 
                'length': len(df[col])
            }, ignore_index=True)
        
        files_df = files_df \
            .append(new_files_df) \
            .drop_duplicates() \
            .reset_index(drop=True)

        files = files_df.to_dict('records')

        if data:
            selected_rows.extend(files_df[ \
                    files_df['filename'].isin(new_files_df['filename']) \
                ] \
                .index
            )
            selected_rows = list(set(selected_rows))

    return files, selected_rows, controls_store


@app.callback(
    Output('content-table', 'data'),
    [
        Input('upload-table', 'data'),
        Input('files-table', 'data')
    ],
    [State('content-table', 'data')]
)
def update_content(uploads, files, content):
    data = []
    columns = [file['filename'] for file in files]

    uploads_df = pd.DataFrame(uploads)
    content_df =  pd.DataFrame(content)
    duplicates = set(uploads_df.columns).intersection(set(content_df.columns))
    content_df = content_df.drop(columns=duplicates)

    df = pd.concat([uploads_df, content_df], axis=1)[columns]

    return df.to_dict('records')


@app.callback(
    Output('dummy', 'children'),
    [Input('delete-files-btn', 'n_clicks')],
    [State('delete-files-btn', 'n_clicks')],
)
def delete_all_files(n, m):
    return f'{n} {m}'


@app.callback(
    Output('counter-badge', 'children'),
    [Input('files-table', 'data')]
)
def update_counter_badge(data):
    return len(data)


@app.callback(
    Output('select-files-btn', 'disabled'),
    [Input('files-table', 'data')]
)
def toggle_select_files_btn(data):
    return False if data else True


@app.callback(
    Output('delete-files-btn', 'disabled'),
    [Input('files-table', 'data')]
)
def toggle_delete_files_btn(data):
    return False if data else True


@app.callback(
    Output('files-table-back', 'hidden'),
    [Input('files-table', 'data')]
)
def toggle_files_table_back(data):
    return True if data else False


@app.callback(
    Output('messages-container', 'children'),
    [Input('messages-table', 'data')],
    [State('messages-container', 'children')]
)
def show_errors(messages, old_messages):
    if not messages:
        return old_messages

    return old_messages + [dbc.Alert(
            children=message['text'],
            color=message['type'],
            dismissable=True,
            duration=5_000,
        )  for message in messages]


@app.callback(
    Output('graph-raw-signal', 'figure'),
    [
        Input('content-table', 'data'),
        Input('files-table', 'selected_rows'),
    ],
    [State('graph-raw-signal', 'figure')]
)
def update_graph_raw_signal(data, selected_rows, figure):
    figure['data'] = []
    df = pd.DataFrame(data).iloc[:, selected_rows]

    for col in df.columns:
        figure['data'].append({
            'name': col,
            'type': 'scatter',
            'mode': 'line',
            'x': df.index,
            'y': df[col],
        })

    return figure


@app.callback(
    Output('graph-delta-signal', 'figure'),
    [
        Input('content-table', 'data'),
        Input('files-table', 'selected_rows'),
    ],
    [State('graph-delta-signal', 'figure')]
)
def update_graph_delta_signal(data, selected_rows, figure):
    figure['data'] = []
    df = pd.DataFrame(data).iloc[:, selected_rows]
    df = features.get_delta(df)

    for col in df.columns:
        figure['data'].append({
            'name': col,
            'type': 'scatter',
            'mode': 'line',
            'x': df.index,
            'y': df[col],
        })

    return figure
