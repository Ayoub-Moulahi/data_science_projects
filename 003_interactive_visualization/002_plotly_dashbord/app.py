import dash.dependencies
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Output, Input

app = Dash(__name__)

countries_by_continent = {
    'africa': ['Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cape Verde', 'Cameroon',
               'Central African Republic', 'Chad', 'Comoros', 'Ivory Coast', 'Djibouti',
               'Democratic Republic of the Congo', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia',
               'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Kenya', 'Lesotho', 'Liberia', 'Libya',
               'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger',
               'Nigeria', 'Republic of the Congo', 'Rwanda', 'Sao Tome & Principe', 'Senegal', 'Seychelles',
               'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Tanzania', 'Togo', 'Tunisia',
               'Uganda', 'Zambia', 'Zimbabwe'],
    'asia': ["Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China",
             "Cyprus", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan",
             "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar", "Nepal",
             "North Korea", "Oman", "Pakistan", "Palestine", "Philippines", "Qatar", "Saudi Arabia", "Singapore",
             "South Korea", "Sri Lanka", "Syria", "Taiwan", "Tajikistan", "Thailand", "Timor-Leste", "Turkey",
             "Turkmenistan", "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen"],
    'europe': ["Albania", "Andorra", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus",
               "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland",
               "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta", "Moldova",
               "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal", "Romania",
               "Russia", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine",
               "United Kingdom",
               "Vatican City"
               ],
    'south america': ["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Paraguay", "Peru", "Uruguay",
                      "Venezuela"],
    'north america': ["Antigua and Barbuda", 'Bermuda', 'Canada', 'Greenland', 'Saint Pierre and Miquelon',
                      'United States of America', "Dominican Republic", "Haiti", "Nicaragua", "Panama", "El Salvador",
                      "Grenada", "Guatemala", "Costa Rica", "Guyana", "Honduras", "Jamaica", "Mexico",
                      "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Suriname",
                      "Trinidad and Tobago", "The Bahamas", "Barbados", "Belize", "Cuba", "Dominica"],

    'oceania': [
        "Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia", "Nauru", "New Zealand", "Palau",
        "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu"
    ]
}
# load dataFrame
df = pd.read_csv("data.csv")
# load geojson file
import json
with open('world_countries.json') as f:
    geo_data = json.load(f)
# define Layout
app.layout = html.Div(className='container', children=[

    html.Div(className="aside",
             children=[html.Div(className='left', children=[dcc.Graph(id="left1", style={'width': '95%', 'height': '95%'})]),
                       html.Div(className='left', children=[dcc.Graph(id="left2", style={'width': '95%', 'height': '95%'})]),
                       html.Div(className='left', children=[dcc.Graph(id="left3", style={'width': '95%', 'height': '95%'})])]),
    html.Div(className="main", children=[html.Div(className='central', children=[
        html.H1('World Population Dashboard', style={'font-size': 30, 'textAlign': 'center', 'color': 'darkgoldenrod'}),
        'Select continent',
        (dcc.Dropdown(id="continent_dropdown",
                      options=[{'label': k, 'value': k} for k in countries_by_continent.keys()])),
        'Select Country',
        (dcc.Dropdown(
            id="countries_dropdown")),
        'Select year',
        dcc.Dropdown(id="year_dropdown",
                     options=list(
                         range(1950, 2023)),
                     value=1950)
    ]),
                                         html.Div(className='central', children=[dcc.Graph(id="center_down", style={'width': '95%', 'height': '95%'})])]),
    html.Div(className="aside", children=[html.Div(className='right', children=[dcc.Graph(id='right1', style={'width': '95%', 'height': '95%'})]),
                                          html.Div(className='right', children=[dcc.Graph(id='right2', style={'width': '95%', 'height': '95%'})]),
                                          html.Div(className='right', children=[dcc.Graph(id='right3', style={'width': '95%', 'height': '95%'})])]),

])


# set dependencies between the choice of continent and list of countries

@app.callback(dash.dependencies.Output('countries_dropdown', 'options'),
              [dash.dependencies.Input('continent_dropdown', 'value')])
def set_country_options(selected_continent):
    return [{'label': i, 'value': i} for i in countries_by_continent[selected_continent]]


@app.callback(
    dash.dependencies.Output('countries_dropdown', 'children'),
    [dash.dependencies.Input('countries_dropdown', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']


@app.callback([Output(component_id='left1', component_property='figure'),
               Output(component_id='left2', component_property='figure'),
                Output(component_id='left3', component_property='figure'),
               Output(component_id='center_down', component_property='figure'),
               Output(component_id='right1', component_property='figure'),
               Output(component_id='right2', component_property='figure'),
               Output(component_id='right3', component_property='figure')
               ],
              [Input(component_id='continent_dropdown', component_property='value'),
               Input(component_id='countries_dropdown', component_property='value'),
               Input(component_id='year_dropdown', component_property='value')])
def get_graph(continent, country, year):
    if continent is None:
        continent = 'WORLD'

    if country is None:
        country = 'Tunisia'


    left1 = px.line(data_frame=df[df['region'] == continent], x='year', y='total_sex', color='sex', title=f'{continent} population by year')
    left1.add_scatter(x=df[df['region'] == continent]['year'], y=df[df['region'] == continent]['total'], mode='lines',name='total')

    left2_data = df[(df['region'] == continent) & (df['year'] == int(year))]

    left3_data = pd.melt(left2_data, id_vars=['region', 'sex'],
                      value_vars=['early_child', 'middle_child', 'adolescent', 'young_adult', 'middle_adult',
                                  'late_adult'])

    left2 = px.pie(data_frame=left2_data, names="sex", values="total_sex", title=f'{continent} sex ratio in {year}')
    left3 = px.pie(data_frame=left3_data, names="variable", values='value', facet_col='sex', title=f'{continent} age structure in {year}')
    center_data = df[(df['type'] == 'Country/Area') & (df['year'] == int(year))].dropna()
    center_down = px.choropleth(data_frame=center_data, locations='region', geojson=geo_data, color='total', color_continuous_scale="Viridis", locationmode='country names', scope='world', title=f'World population map in {year}')


    right1 = px.line(data_frame=df[df['region'] == country], x='year', y='total_sex', color='sex', title=f'{country} population growth')
    right1.add_scatter(x=df[df['region'] == country]['year'], y=df[df['region'] == country]['total'], mode='lines',name='total')

    country_data = df[(df['region'] == country) & (df['year'] == int(year))]
    country_data = pd.melt(country_data, id_vars=['region', 'sex'],
                           value_vars=['early_child', 'middle_child', 'adolescent', 'young_adult', 'middle_adult',
                                       'late_adult'])

    right2 = px.pie(data_frame=country_data, names="variable", values='value', facet_col='sex', title=f'{country} age structure in {year}')


    right3 = px.choropleth(data_frame=center_data, locations='region', geojson=geo_data, color='total', color_continuous_scale="Viridis", locationmode='country names', scope=f'{continent}'.lower(), title=f'{continent} population map in {year}')


    return [left1, left2, left3, center_down, right1, right2, right3]
    

if __name__ == '__main__':
    app.run(debug=True, port=8052)
