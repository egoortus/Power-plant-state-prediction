import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table as dt


ui_messages = html.Div(
    id='messages',
    children=[
        dt.DataTable(id='messages-table'),
        html.Div(
            id='messages-container',
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


header = dbc.Row([
    dbc.Col(
        width=12,
        lg=3,
        xl=3,
        children=html.Img(src='/assets/logo.png', style={'width': '100px'}),
        style={'textAlign': 'center'}
    ),
    dbc.Col(
        width=12,
        lg=6,
        xl=6,
        children=[
            html.H1(
                children='Power Plant State Prediction',
                style={'color': '#323232'}
            ),
            html.H3(
                children='Expert System',
                style={'color': '#505050'}
            ),
        ],
        style={'textAlign': 'center'}
    )
])


files_upload = dbc.Card(dbc.CardBody([
    dcc.Upload(
        id='files-upload',
        multiple=True,
        disable_click=True,
        style={
            'position': 'relative',
            'marginBottom': '1.25rem'
        },
        style_active={'background': '#94c8ff52'},
        children=[
            html.Div(id='files-table-back'),
            dt.DataTable(
                id='files-table',
                columns=[
                    {'id': 'filename', 'name': 'File'},
                    {'id': 'length', 'name': 'Ticks'},
                ],
                data=[],
                fixed_rows={'headers': True},
                page_action='none',
                row_selectable="multi",
                row_deletable=True,
                selected_rows=[],
                selected_row_ids=[],
                style_header={'display': 'none'},
                style_table={
                    'height': '300px',
                    'overflowY': 'auto'
                }
            )
        ]
    ),
    dbc.Row([
        dbc.Col(
            width=6,
            children=dcc.Upload(
                id='files-upload-btn',
                multiple=True,
                style_active=None,
                style_reject=None,
                children=[
                    dbc.Button(
                        children=[
                            "Upload Files ",
                            dbc.Badge(
                                id='counter-badge',
                                color="light",
                                className="ml-1",
                                children=0,
                            )
                        ],
                        color='primary',
                        style={'width': '100%'}
                    )
                ]
            )
        ),
        dbc.Col(
            width={'size': 4, 'offset': 2},
            style={'textAlign': 'right'},
            children=[
                dcc.Store(id='table-controls-store', data={}),
                dbc.Button(
                    id='select-files-btn',
                    className='unselected',
                    color="primary",
                    disabled=True,
                    style={'height': '38px', 'width': '38px'}
                ),
                dbc.Button(
                    id='delete-files-btn',
                    className="ml-1",
                    color="primary",
                    disabled=True,
                    style={'height': '38px', 'width': '38px'}
                ),
            ]
        ),
    ],
    justify="between"
    )
]))

visualizations = [
    dcc.Graph(
        id='graph-raw-signal',
        config={
            'responsive': True,
            'displayModeBar': False,
        },
        style={
            'width': '100%',
            'height': '200px',
        },
        figure={
            'layout': {
                'title': 'Original Time Signal',
                'margin': {'t': 40, 'l': 40, 'b': 30, 'r': 20},
                'showlegend': False
            }
        }
    ),
    dcc.Graph(
        id='graph-delta-signal',
        config={
            'responsive': True,
            'displayModeBar': False,
        },
        style={
            'width': '100%',
            'height': '200px',
        },
        figure={
            'layout': {
                'title': 'Original Delta Time Signal',
                'margin': {'t': 40, 'l': 40, 'b': 30, 'r': 20},
                'showlegend': False
            }
        }
    ),
    dcc.Graph(
        id='graph-fft-signal',
        config={
            'responsive': True,
            'displayModeBar': False,
        },
        style={
            'width': '100%',
            'height': '200px',
        },
        figure={
            'layout': {
                'title': 'Original Time Signal Fast Fourier Transform',
                'margin': {'t': 40, 'l': 40, 'b': 30, 'r': 20},
                'showlegend': False
            }
        }
    ),
    dcc.Graph(
        id='graph-radar-chart',
        config={
            'responsive': True,
            'displayModeBar': False,
        },
        style={
            'width': '100%',
            'height': '300px',
        },
        figure={'layout': {'polar': True}}
        )
]


body = html.Div(
    children=[
        dt.DataTable(id='content-table', page_action='none', data=[]),
        dt.DataTable(id='upload-table', page_action='none', data=[]),
        ui_messages,
        header,
        dbc.Row([
            dbc.Col(files_upload, width=12, lg=5, xl=4),
            dbc.Col(visualizations, width=12, lg=7, xl=8)
        ]),
        html.Div(id='dummy')
    ],
    style={
        'padding': '0 15px 0 15px',
        'backgroundColor': '#f2f2f2',
        'minHeight': '100vh',
    }
)