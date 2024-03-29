import plotly.graph_objs as go
from nba_api.stats.static import players
from nba_api.stats.endpoints.shotchartdetail import ShotChartDetail

def getShotData(name, year):

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

    string_season = f"{str(year)}-{str(year+1)[-2:]}"
    #playerID = players.find_players_by_full_name(name)[0]['id']
    try: 
        playerID = players.find_players_by_full_name(name)[0]['id']
        shotchart_detail = ShotChartDetail(team_id = 0, player_id = playerID, season_nullable= string_season, context_measure_simple= "FGA")
        shotData = shotchart_detail.get_data_frames()[0]
        shotData["LOC_X"] *= -1

        made_shots = shotData.loc[shotData.SHOT_MADE_FLAG == 1]
        missed_shots = shotData.loc[shotData.SHOT_MADE_FLAG == 0]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=made_shots["LOC_X"], y=made_shots["LOC_Y"], mode='markers', marker_color="BLUE", name="Made Shot"))
        fig.add_trace(go.Scatter(x=missed_shots["LOC_X"], y=missed_shots["LOC_Y"], mode='markers', marker_color="RED", name="Missed Shot"))

        layout = go.Layout(
            title='Shots by %s in the %s NBA season' % (str(name), str(string_season)), #change to be based on variable passed
            showlegend=True,
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
            height = 800,
            width = 1000,
            shapes=court_shapes,
            hovermode=False
        )

        fig.update(layout=layout)
        fig.show()
    except (IndexError, ValueError):
        fig=go.Figure()

        layout = go.Layout(
            title='Error: Invalid input for either player name, season or both', #change to be based on variable passed
            showlegend=True,
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
            height = 800,
            width = 1000,
            shapes=court_shapes,
            hovermode=False
        )
        fig.update(layout=layout)
        fig.show()
    

getShotData("Lebron James", 2018)