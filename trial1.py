from flask import Flask, render_template
import pandas as pd
from flask import request
import sys
import bokeh.io
from bokeh.io import output_file, show, output_notebook
from bokeh.models import *
# from web_app import app
from bokeh.io import output_file, show
from bokeh.embed import components, file_html
app = Flask(__name__)
@app.route('/')
def map_immigration():
    # if flask.request.method == 'POST':
    # lol = request.data
    # userinput = request.form.get('userinput')
    # limit = request.form.get('limit')
    userinput= "Pakistan"
    limit = 5
    # Applying what we did in ipynb for data cleaning 
    working_df = pd.read_csv("./dataset/cleaned_data.csv",low_memory=False)
    user_df = working_df[working_df['Country of Birth']==userinput]
    user_df= user_df.sort_values(by="Admissions", ascending=False)
    user_df= user_df.sort_values(by="Admissions", ascending=False)[:limit]

    # implementing bookeh
    lat_list = list(user_df['latitude'])
    lon_list = list(user_df['longitude'])
    add_list = list(user_df['Admissions'])
    cob_list= list(user_df['Country of Birth'])
    state_list = list(user_df['State of Residence'])
    county_list = list(user_df['County of Residence'])


    

    bokeh.io.output_notebook()


    map_options = GMapOptions(lat=37.0902, lng=-95.7129, map_type="roadmap", zoom=3)

    plot = GMapPlot(x_range=Range1d(), y_range=Range1d(), map_options=map_options,api_key = "AIzaSyDmyE8tAty-Lhd-rJQvIsGk8ocOIdHwYSE")

    source = ColumnDataSource(
        data = dict(
            lat=lat_list,
            lon=lon_list,
            Admissions = add_list,
            cob = cob_list,
            State= state_list,
            County = county_list


        ))

    circle = Circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, line_color=None)
    plot.add_glyph(source, circle)

    plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool(), BoxZoomTool())

    plot.title.text="IMMIGRATION RECOMMENDATION SYSTEM"

    plot.add_tools(HoverTool(
        tooltips=[
            ( 'Admissions',   '@Admissions' ),
            ( 'Country of Birth',  '@cob' ),
            ('State', '@State'),
            ('County', '@County')
        ],

        formatters={
            'Admissions' : 'numeral', # use 'datetime' formatter for 'date' field
            'Country of Birth' : 'printf',
            'State' : 'printf',
            'County' : 'printf'
        },

        mode='vline'
    ))

    output_file("gmap_plot.html")
    # trial 
    show(plot)
    script, div = components(plot)
    return render_template('map.html', script = script, div = div)

    #bokeh.io.show(plot)

    #return render_template("map.html", userinput=userinput, limit=limit)
 
app.run(host='0.0.0.0', port=5000, debug=True) # anyone can connect, and we're running on port 5000