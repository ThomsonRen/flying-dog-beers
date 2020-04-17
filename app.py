import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

px.set_mapbox_access_token('pk.eyJ1IjoidG9uZ3hpbnJlbiIsImEiOiJjazZnM2phcXEwdTJ5M2pxcHQ3MDRteHNlIn0.ci2XKyZQRC_tAEcvxVIeAQ')

## loading data


#data = pd.read_csv("https://raw.githubusercontent.com/ThomsonRen/flying-dog-beers/master/data/MCM-Data-2020-03-19.csv")
#loc = pd.read_csv('https://raw.githubusercontent.com/ThomsonRen/flying-dog-beers/master/data/Loc.csv')



data = pd.read_csv("data/MCM-Data-2020-03-19.csv")
loc = pd.read_csv('data/Loc.csv')


Geo_Dict = {loc['Institution'][i]:(loc['lat'][i],loc['lng'][i]) for i in range(len(loc)) }
data2 = data.groupby('Institution').count().reset_index()
lat = []
lng = []
for i in range(len(data2)):
    lat.append(Geo_Dict[data2['Institution'][i]][0])
    lng.append(Geo_Dict[data2['Institution'][i]][1])
data2['lat'] = lat
data2['lng'] = lng



## 项目介绍

introtext = '''
美国大学生数学建模竞赛（MCM/ICM）是唯一的国际性数学建模竞赛，
也是世界范围内最具影响力的数学建模竞赛，
主办方是COMAP（the Consortium for Mathematics and Its Application，
美国数学及其应用联合会）。
赛题内容涉及经济、管理、环境、资源、生态、医学、安全、等众多领域。
竞赛要求三人（本科生）为一组，
在四天时间内，就指定的问题完成从建立模型、求解、验证到论文撰写的全部工作，
体现了参赛选手研究问题、解决方案的能力及团队合作精神，
为现今各类[数学建模竞赛](https://baike.baidu.com/item/数学建模竞赛)之鼻祖。

'''








# 获奖总人数
HistoryParticipate = data.groupby("Year").count()
HistoryParticipate = HistoryParticipate.reset_index()
fig_total_number = px.bar(HistoryParticipate, x='Year', y='Problem',labels={'Problem':'Number of Teams'},color='Problem')


# 选题人数和获奖人数

## 每一年的总人数，选题，奖项
Problem_Time_History =pd.crosstab(data.Year,data.Problem)
Problem_Time_History = Problem_Time_History.reset_index(drop = False)
## 每一年的总人数，选题，奖项
Designation_Time_History = pd.crosstab(data.Year,data.Designation1)
Designation_Time_History = Designation_Time_History.reset_index(drop = False)


ProblemList  = ['A','B','C','D','E','F']
LabelList = ['A(continuous)','B(discrete)','C(data insights)',
             'D(operations/network science)','E(environmental science)','F(policy)']
PrizeList = ['Disqualified','Unsuccessful', 'Successful Participant',
             'Honorable Mention','Meritorious Winner','Finalist',  'Outstanding Winner']

x = Problem_Time_History.Year
fig_problem_desi = go.Figure()

for problem,label in zip(ProblemList,LabelList):
    fig_problem_desi.add_trace(go.Bar(x=x, y=Problem_Time_History[problem], name=label,visible=False))

for prize in PrizeList:
    fig_problem_desi.add_trace(go.Bar(x=x, y=Designation_Time_History[prize],name=prize))
    
    
    
#     if problem == 'A':
#         fig = go.Figure(go.Bar(x=x, y=Problem_Time_History[problem], name=label))
#     else:
#         fig.add_trace(go.Bar(x=x, y=Problem_Time_History[problem], name=label))

fig_problem_desi.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'},legend_orientation="h")

fig_problem_desi.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            active=0,
            x=0.57,
            y=1.2,
            buttons=list([
                dict(label="选题",
                     method="update",
                     args=[{"visible": [True]*6+[False]*7},
                           {"title": "",
                            "annotations": []}]),
                dict(label="获奖数",
                     method="update",
                     args=[{"visible": [False]*6+[True]*7},
                           {"title": "",
                            }]),
            ]),
        )
    ])

## 国家分布
YearCountry = pd.crosstab(data.Year,data.Country)
YearCountry = YearCountry.reset_index(drop = False)
CountryList = data.Country.unique()
x = YearCountry.Year

fig_country = make_subplots(rows=1, cols=2, column_widths=[0.4, 0.6],specs=[[{"type": "domain"}, {"type": "xy"}]])   
for country in CountryList:
    # Create traces
    fig_country.add_trace(go.Scatter(x=x, y=YearCountry[country],
                        mode='lines',
                        name=country),row = 1,col = 2)

 
    
    
    
YearCountry = pd.crosstab(data.Country,data.Year)
YearCountry = YearCountry.reset_index(drop = False)
YearCountry.loc[(YearCountry['Country'] != 'China')&(YearCountry['Country'] != 'USA'),'Country']= 'Other Countries'
fig_country.add_trace(go.Pie(labels=YearCountry['Country'],values=YearCountry[2019],textinfo='label+percent'),row  = 1,col = 1)



## 地理分布可视化

fig_geo = px.density_mapbox(data2, 
                        lat="lat", 
                        lon="lng",
                        #size = 'ID',
                        #color = 'ID',
                        height = 600,
#                        width = 1000,
                        radius=7,
                        hover_data=['Institution','ID'],
                        labels={'ID':'数量'},
                        color_continuous_scale = 'Oranges',
                        center = go.layout.mapbox.Center(lat=33.5,lon=175),
                        zoom = 1,
                        hover_name = 'Institution',
                        #size_max  =20
                       )

fig_geo2 = px.scatter_mapbox(data2, lat="lat", 
                        lon="lng",
                        size = 'ID',color = 'ID',
#                        height = 600,
#                        width = 1000,
                        #color_continuous_scale = 'Oranges',
                        center = go.layout.mapbox.Center(lat=33.5,lon=175),
                        zoom = 0,
                        hover_name = 'Institution',size_max  =20)




########### Define your variables
beers=['Chesapeake Stout', 'Snake Dog IPA', 'Imperial Porter', 'Double Dog IPA']
ibu_values=[35, 60, 85, 75]
abv_values=[5.4, 7.1, 9.2, 14.3]
color1='lightblue'
color2='darkgreen'
mytitle='Beer Comparison'
tabtitle='beer!'
myheading='Flying Dog Beers'
label1='IBU'
label2='ABV'
# githublink='https://github.com/austinlasseter/flying-dog-beers'
# sourceurl='https://www.flyingdog.com/beers/'


introduction = '''
这是我们为了展示MCM/ICM比赛结果而建立的网站，希望能够帮助到大家。
'''





########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div(children=[
    #html.H1(myheading,style={"margin-left": "300px","margin-top": "50px"}),
    html.Div(
    [
     html.Div(
                [
                    html.Div(
                        [
                            html.H3(
                                "美国大学生数学建模竞赛（MCM/ICM）获奖数据可视化",
                            ),
                        ]
                    )
                ],
           
            id="title",
            className="nine columns named-card",
            ),
                        
                        
        
        html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash-logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="three columns named-card",
        
                ),                    
                        
                        
    ],
    id="header",
    className="twelve columns",
    style={"margin-top": "20px","margin-left": "50px","margin-bottom": "0px",},
    ),

    html.Div(
     html.P(
        introtext,
      style={"margin-top": "20px","margin-left": "50px","margin-bottom": "0px",},  
        ),
     className="twelve columns",
     
     ),
    
    
    
    html.Div(
    [      
    html.Div(       
    dcc.Graph(id = 'fig_geo4',figure = fig_geo2,),
    className="one-half column",
    ),
    
          
            
    html.Div(       
    [dcc.Graph(id='fig_problem_desi',
        figure=fig_problem_desi),
    dcc.Graph(id='fig_country',
        figure=fig_country),   
        ],
    className="one-half column",
    ), 
                        
                        
               
                        
    ]  ,   
     id="header2",
     className="row flex-display",           
     ),
               
        
               
#    dcc.Graph(id='fig_problem_desi',
#        figure=fig_problem_desi), 
#    dcc.Graph(id='fig_country',
#        figure=fig_country),          
#                
    # html.A('Code on Github', href=githublink),
    # html.A('Data Source', href=sourceurl),
    ],style={"margin-top": "0px","margin-left": "0px"},

)

if __name__ == '__main__':
    app.run_server(debug=True)
