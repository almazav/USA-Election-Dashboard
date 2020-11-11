import dash 
import dash_core_components as dcc
import dash_html_components as html 
import pandas as pd 
import dash_bootstrap_components as dbc
import plotly.express as px 

df = pd.read_csv("https://usa-election-bucket.s3.amazonaws.com/politics1.csv")
# print(df.head())
app = dash.Dash(__name__)
server = app.server


fig_map = px.choropleth(
                          df, locations="state", hover_name='electoral votes',
                          locationmode="USA-states", color="party",
                          scope="usa", color_discrete_map ={'democrat': 'blue',
                                                          'republican': 'red',
                                                          'unsure': 'grey'})

fig_bar = px.histogram(df, x='party', y='electoral votes', histfunc='sum',color='party',
                           range_y=[0,350], color_discrete_map={'democrat': 'blue',
                                                                'republican': 'red'})
fig_bar.update_layout(showlegend=False, shapes=[
        dict(type='line', yref='paper',y0=0.77,y1=0.77, xref='x',x0=-0.5,x1=1.5)
    ])
    # add annotation text above line
fig_bar.add_annotation(x=0.5, y=280, showarrow=False, text="270 votes to win")






app.layout = html.Div([
    dbc.Row([html.H1("USA Elections 2020", style ={'textAlign': 'center'})]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure =fig_map), xs = 12, sm = 12, md = 12, lg = 12 , xl = 12),
        dbc.Col(dcc.Graph(figure =fig_bar), xs = 12, sm = 12, md = 12, lg = 12 , xl = 12)])
    
])
if __name__ == '__main__':
        app.run_server(debug=False) 