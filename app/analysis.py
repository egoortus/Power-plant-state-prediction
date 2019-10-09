import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table as dt


ui_messages = html.Div(
    id='ui-messages',
    children=[
        dt.DataTable(id='ui-messages-table'),
        html.Div(
            id='ui-messages-container',
            className='force-overflow',
            style={
                'position': 'fixed',
                'maxWidth': '320px',
                'top': '10px',
                'left': 'calc(50% - 160px)',
                'maxHeight': 'calc(100vh - 10px)',
                'overflow': 'auto',
                'z-index': '999'
            },
            children=[]
        ),
    ]
)

files_upload = dcc.Upload(
    id='files-upload',
    multiple=True,
    disable_click=True,
    children=[
        dcc.Upload(
            id='files-upload-btn',
            multiple=True,
            children=html.Button(
                children='Select Files',
                style={'width': '100%'}
            ),
            style={'padding': '10px'},
            style_active=None,
            style_reject=None,
        ),
        dt.DataTable(
            id='content-table',
            column_selectable='multi',
            selected_columns=[],
            fixed_rows={ 'headers': True},
            virtualization=True,
            page_action='native',
            style_table={'padding': '10px'},
        ),
    ],
    style={
        'padding': '2%',
        'height': '90vh'
    },
)


body = html.Div(
    children=[
        ui_messages,
        dbc.Row(
            children=[
                dbc.Col(files_upload, width=12, lg=5, xl=4),
                dbc.Col(html.Div(), width=12, lg=7, xl=8)
            ],
        )
    ],
    style={'padding': '0 15px 0 15px'}
)