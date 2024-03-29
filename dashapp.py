import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.io as pio
from nba_api.stats.static import players
from nba_api.stats.endpoints.shotchartdetail import ShotChartDetail
import datetime

pio.templates.default= "none"

court_shapes = []
 
outer_lines_shape = dict(
    type='rect',
    xref='x',
    yref='y',
    x0='-250',
    y0='-47.5',
    x1='250',
    y1='422.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)
 
court_shapes.append(outer_lines_shape)

hoop_shape = dict(
    type='circle',
    xref='x',
    yref='y',
    x0='7.5',
    y0='7.5',
    x1='-7.5',
    y1='-7.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)
 
court_shapes.append(hoop_shape)

backboard_shape = dict(
    type='rect',
    xref='x',
    yref='y',
    x0='-30',
    y0='-7.5',
    x1='30',
    y1='-6.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    ),
    fillcolor='rgba(10, 10, 10, 1)'
)
 
court_shapes.append(backboard_shape)

outer_three_sec_shape = dict(
    type='rect',
    xref='x',
    yref='y',
    x0='-80',
    y0='-47.5',
    x1='80',
    y1='143.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)
 
court_shapes.append(outer_three_sec_shape)

inner_three_sec_shape = dict(
    type='rect',
    xref='x',
    yref='y',
    x0='-60',
    y0='-47.5',
    x1='60',
    y1='143.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)
 
court_shapes.append(inner_three_sec_shape)

left_line_shape = dict(
    type='line',
    xref='x',
    yref='y',
    x0='-220',
    y0='-47.5',
    x1='-220',
    y1='92.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)
 
court_shapes.append(left_line_shape)

right_line_shape = dict(
    type='line',
    xref='x',
    yref='y',
    x0='220',
    y0='-47.5',
    x1='220',
    y1='92.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)   
 
court_shapes.append(right_line_shape)

three_point_arc_shape = dict(
    type='path',
    xref='x',
    yref='y',
    path='M -220 92.5 C -70 300, 70 300, 220 92.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)
 
court_shapes.append(three_point_arc_shape)

center_circle_shape = dict(
    type='circle',
    xref='x',
    yref='y',
    x0='60',
    y0='482.5',
    x1='-60',
    y1='362.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)
 
court_shapes.append(center_circle_shape)

res_circle_shape = dict(
    type='circle',
    xref='x',
    yref='y',
    x0='20',
    y0='442.5',
    x1='-20',
    y1='402.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)
 
court_shapes.append(res_circle_shape)

free_throw_circle_shape = dict(
    type='circle',
    xref='x',
    yref='y',
    x0='60',
    y0='200',
    x1='-60',
    y1='80',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)
 
court_shapes.append(free_throw_circle_shape)

res_area_shape = dict(
    type='circle',
    xref='x',
    yref='y',
    x0='40',
    y0='40',
    x1='-40',
    y1='-40',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1,
        dash='dot'
    )
)
 
court_shapes.append(res_area_shape)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='shot-graph',
            figure={
                'layout': go.Layout( 
                    title="test",
                    shapes= court_shapes,
                    height=800,
                    xaxis= dict(
                        showgrid=False,
                        range=[-300, 300],
                        showticklabels=False,
                        zeroline=False
                    ),
                    yaxis= dict(
                        showgrid=False,
                        range=[-100, 500],
                        showticklabels=False,
                        zeroline=False
                    )
                )
            },
            config={
                'displayModeBar': False,
                'staticPlot': True
            }
        ),
    ]),#,style = {'margin': 'auto', 'width': '50%'}), #need 'width': '50%' for some reason. Could use margin-left to "center" this too
    html.Div([
            dcc.Input(id='playerName-state', type='text', value='Brook Lopez'),
            dcc.Input(id='season-state', type='text', value='2018-19'),
            html.Button('Submit', id='button')
    ],style = {"width": "100%", "display": "flex", "align-items": "center", "justify-content": "center"})
])

@app.callback(
    Output('shot-graph', 'figure'),
    [Input('button', 'n_clicks')],
    state=[
        State(component_id='playerName-state', component_property='value'),
        State(component_id='season-state', component_property='value')]
)
def update_figure(n_clicks, playerName, season):
    try:
        playerID = players.find_players_by_full_name(str(playerName))[0]['id']
        shotchart_detail = ShotChartDetail(team_id = 0, player_id = playerID, season_nullable= str(season), context_measure_simple= "FGA")
        shotData = shotchart_detail.get_data_frames()[0]

        seasonFirst = season[2:4]
        if(int(seasonFirst) < 0 or int(seasonFirst) < 13 or int(seasonFirst) > (datetime.datetime.now().year % 100) or len(shotData) == 0): #check to see if a bad season has been entered even if formatting is fine
                raise ValueError

        shotData["LOC_X"] *= -1
        made_shots = shotData.loc[shotData.SHOT_MADE_FLAG == 1]
        missed_shots = shotData.loc[shotData.SHOT_MADE_FLAG == 0]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=made_shots["LOC_X"], y=made_shots["LOC_Y"], mode='markers', marker_color="BLUE", name="Made Shot"))
        fig.add_trace(go.Scatter(x=missed_shots["LOC_X"], y=missed_shots["LOC_Y"], mode='markers', marker_color="RED", name="Missed Shot"))
        
        layout = go.Layout(
            title='Shots by %s in the %s NBA season' % (playerName, season), 
            showlegend=False,
            xaxis=dict(
                showgrid=False,
                range=[-300, 300],
                showticklabels=False,
                zeroline=False
            ),
            yaxis=dict(
                showgrid=False,
                range=[-100, 500],
                showticklabels=False,
                zeroline=False
            ),
            height=800,
            shapes=court_shapes,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode=False
        )
        fig.update(layout=layout)

        return fig
    except(IndexError): #goes here if playerID fails
        fig = go.Figure()

        try: #goes here if season formatting is fine
            playerID = players.find_players_by_full_name(str("Lebron James"))[0]['id']
            shotchart_detail = ShotChartDetail(team_id = 0, player_id = playerID, season_nullable= str(season), context_measure_simple= "FGA")
            shotData = shotchart_detail.get_data_frames()[0]
            
            seasonFirst = season[2:4]
            if(int(seasonFirst) < 0 or int(seasonFirst) < 13 or int(seasonFirst) > (datetime.datetime.now().year % 100) or len(shotData) == 0): #check to see if a bad season has been entered even if formatting is fine
                raise ValueError
            
            layout = go.Layout(
                title='Error: Invalid input for player name', 
                showlegend=False,
                xaxis=dict(
                    showgrid=False,
                    range=[-300, 300],
                    showticklabels=False,
                    zeroline=False
                ),
                yaxis=dict(
                    showgrid=False,
                    range=[-100, 500],
                    showticklabels=False,
                    zeroline=False
                ),
                height=800,
                shapes=court_shapes,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                hovermode=False
            )
            fig.update(layout=layout)

            return fig
        except(ValueError):#goes here is season formatting is incorrect also
            layout = go.Layout(
                title='Error: Invalid input for both player name and season year', 
                showlegend=False,
                xaxis=dict(
                    showgrid=False,
                    range=[-300, 300],
                    showticklabels=False,
                    zeroline=False
                ),
                yaxis=dict(
                    showgrid=False,
                    range=[-100, 500],
                    showticklabels=False,
                    zeroline=False
                ),
                height=800,
                shapes=court_shapes,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                hovermode=False
            )
            fig.update(layout=layout)

            return fig

    except(ValueError): #goes here is player formatting is fine but season formatting is wrong
        fig = go.Figure()
        layout = go.Layout(
            title='Error: Invalid input for season year', 
            showlegend=False,
            xaxis=dict(
                showgrid=False,
                range=[-300, 300],
                showticklabels=False,
                zeroline=False
            ),
            yaxis=dict(
                showgrid=False,
                range=[-100, 500],
                showticklabels=False,
                zeroline=False
            ),
            height=800,
            shapes=court_shapes,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode=False
        )
        fig.update(layout=layout)

        return fig

if __name__ == '__main__':
    app.run_server(debug=True)