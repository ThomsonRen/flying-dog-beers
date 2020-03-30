# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
# df = px.data.gapminder()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']






# df = df[df['continent'] == 'Asia']  # 提取亚洲数据
# fig = px.line(df,   # 指定数据的名字
#              x='year',  # 年份为横坐标
#              y='lifeExp',  # 预期寿命为纵坐标 
#              color='country') # 以国家进行染色




app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div'),
    dcc.Graph(id='graph-with-slider'),
    # dcc.Graph(figure=fig),
    
    dcc.Slider(
        id='year-slider',  # 指定变量的名字
        min=df['year'].min(), # 最小值
        max=df['year'].max(),  # 最大值
        value=df['year'].min(), # 初始值
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    ),
])






@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])

# 函数的输入值为slider的一个属性，函数的输出值为一张图片（的字典）
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(dict(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'type': 'log', 'title': 'GDP Per Capita',
                   'range':[2.3, 4.8]},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition = {'duration': 1500},
        )
    }




if __name__ == '__main__':
    app.run_server()