import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


team_stats = pd.read_csv('teamwise_home_and_away.csv')
player_data = pd.read_csv('player_data_final.csv')
team_data = pd.read_csv('teams.csv')
matches = pd.read_csv('matches_final.csv')
deliveries = pd.read_csv('deliveries_final.csv')
wickets = deliveries[deliveries['dismissal_kind'].notnull()][['season', 'over', 'ball','batsman', 'bowler', 'player_dismissed', 'dismissal_kind', 'fielder' ]]
player_tuple = tuple(player_data['player'].unique())
season_tuple = tuple(np.insert(deliveries['season'].unique(),0, 'All'))
team_tuple = tuple(matches['team_1'].unique())
st.title('IPL in Numbers')

def head_to_head(team_1, team_2):
    st.write(matches[((matches['team_1'] == team_1) & (matches['team_2'] == team_2)) | ((matches['team_2'] == team_1) & (matches['team_1'] == team_2))]['winner'].value_counts())
    
page = st.sidebar.radio('Navigation', ['Home', 'Player Dashboard'])

if page == 'Home':

    fig = go.Figure(data=[go.Bar(
        name = 'Home win %',
        x = team_stats['team'],
        y = team_stats['home_win_percentage']
    ),
                        go.Bar(
        name = 'Away win %',
        x = team_stats['team'],
        y = team_stats['away_win_percentage'],
        marker_color = 'rgb(128, 0, 128)'
    )
    ])
    fig.update_xaxes(tickangle=300)
    fig.update_layout({
    'title_text': "Home win % and away win %",
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig)


    fig = px.bar(x=player_data['player'][:15], y=player_data['total_runs'][:15], title='Top run scorers', labels={'x': '', 'y':'Runs scored'})
    fig.update_xaxes(tickangle=300)
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig)


    fig = px.bar(x=player_data['player'][:15], y=player_data['average'][:15], title='Averages of top run scorers', labels={'x': '', 'y':'Average'})
    fig.update_xaxes(tickangle=300)
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig)


    fig = px.bar(x=player_data['player'][:15], y=player_data['strikerate'][:15], title='Strike rates of top run scorers', labels={'x': '', 'y':'Strike rate'})
    fig.update_xaxes(tickangle=300)
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig)


    inn_1_score_venue = []
    inn_2_score_venue = []
    for venue in matches['venue'].unique():
        inn_1_score_venue.append(round(matches[matches['venue'] == venue]['inning_1_score'].mean()))
        inn_2_score_venue.append(round(matches[matches['venue'] == venue]['inning_2_score'].mean()))

    fig = go.Figure(data=[go.Bar(
        name = 'Avg. 1st inning score',
        x = inn_1_score_venue,
        y = list(matches['venue'].unique()),
        orientation='h' 
    ),
                        go.Bar(
        name = 'Avg. 2nd inning score',
        x = inn_2_score_venue,
        y = list(matches['venue'].unique()),
        marker_color = 'rgb(128, 0, 128)', 
        orientation='h'
    )
    ])
    fig.update_layout({
        'title_text': "Avg. first and second inning scores (view fullscreen)",
        'height': 1000,
        'width': 900,
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig, use_container_width=False)


    subfig = make_subplots(rows=1, cols=2, subplot_titles=("Most matches won batting first", "Most matches won chasing"))
    subfig.add_bar(row=1, col=1, y=list(dict(matches[matches['win_by_runs'] > 0]['venue'].value_counts()[:5]).values()), x=list(dict(matches[matches['win_by_runs'] > 0]['venue'].value_counts()[:5]).keys()))
    subfig.add_bar(marker_color='rgb(128,0,128)',row=1, col=2, x=list(dict(matches[matches['win_by_wickets'] > 0]['venue'].value_counts()[:5]).keys()), y=list(dict(matches[matches['win_by_wickets'] > 0]['venue'].value_counts()[:5]).values()))
    subfig.update_xaxes(tickangle=320)
    subfig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)'} ,showlegend=False)
    st.plotly_chart(subfig)


    fig = px.bar( x=wickets[wickets['dismissal_kind'] != 'run out']['bowler'].value_counts()[:10][::-1], y=wickets[wickets['dismissal_kind'] != 'run out']['bowler'].value_counts().index[:10][::-1], orientation='h', title='Leading wicket takers', labels={'x':'Wickets', 'y':''})
    fig.update_layout({
        'height': 600,
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)'
    })
    st.plotly_chart(fig)


    st.text('Most successful pacers: SL Malinga, DJ Bravo')
    st.text('Most successful spinners: P Chawla, S Narine')

    fig = px.bar(data_frame=pd.DataFrame(matches['player_of_match'].value_counts()[:10]), title='Most no. of MOTM awards won', labels={'index': '', 'value':'No. of awards'})
    fig.update_xaxes(tickangle=330)
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)'}, showlegend=False)  
    st.plotly_chart(fig)

    st.subheader('Head to Head')
    team_1 = st.selectbox('Choose first team', team_tuple)
    team_2 = st.selectbox('Choose second team', team_tuple)
    if st.button('Go'):
        head_to_head(team_1, team_2)
    

elif page == 'Player Dashboard':
    st.header('Player Dashboard')
    player  = st.selectbox('Select a player', player_tuple)
    season = st.selectbox('Select season', season_tuple)
    season_avg = deliveries[(deliveries['batsman'] == player) & (deliveries['season'] == season)]['batsman_runs'].sum()
    record = player_data[player_data['player'] == player]
    catch_record = wickets[(wickets['dismissal_kind'] == 'caught') & (wickets['fielder'] == player)]
    run_out_record = wickets[(wickets['dismissal_kind'] == 'run out') & (wickets['fielder'] == player)]
    season_wicket_record = wickets[(wickets['bowler'] == player) & (wickets['season'] == season) & (wickets['dismissal_kind'] != 'run out')]
    season_run_out_record = wickets[(wickets['dismissal_kind'] == 'run out') & (wickets['fielder'] == player) & (wickets['season'] == season)]
    season_catch_record = wickets[(wickets['dismissal_kind'] == 'caught') & (wickets['fielder'] == player) & (wickets['season'] == season)]
    col1, col2 = st.beta_columns(2)
    with col1:
        if season == 'All':
            st.write('Total runs: ', record['total_runs'].values[0])
        else:
            st.write('Total runs: ', deliveries[(deliveries['season'] == season) & (deliveries['batsman'] == player)]['batsman_runs'].sum())
    with col2:
        if season == 'All':
            st.write('Average: ', round(record['average'].values[0]))
        else:
            st.write('Average: ', season_avg)

    with col1:
        st.write('Strike rate: ', round(record['strikerate'].values[0]))

    with col2:
        if season == 'All':
            st.write('Wickets taken: ', record['wickets'].values[0])
        else:
            st.write('Wickets taken: ', len(season_wicket_record))
    with col1:
        if season == 'All':
            st.write('Catches taken: ', len(catch_record))
        else:
            st.write('Catches taken: ', len(season_catch_record))
    with col2:
        if season == 'All':
            st.write('Run outs: ', len(run_out_record))
        else:
            st.write('Run outs: ', len(season_run_out_record))
