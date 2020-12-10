from flask import Flask, render_template
import pandas as pd
from flask import request
import sys
import bokeh.io
from bokeh.io import output_file, show, output_notebook
from bokeh.models import *
from bokeh.io import output_file, show
from bokeh.embed import components, file_html

app = Flask(__name__)
@app.route('/')
def user_input_form():

    return render_template("main1.html")

@app.route('/map', methods = ['POST', 'GET'])
def map_immigration():
    #user input to make the user df and then manipulate that df to create longitude and latitude lists for bokeh map display
    userinput = request.form.get('userinput')
    #limit used to truncate the df so that only top recommendations are showed
    limit = int(request.form.get('limit'))

    # Applying what we did in ipynb for data cleaning 
    working_df = pd.read_csv("./dataset/working_finale.csv",low_memory=False)
    user_df = working_df[working_df['Country of Birth']==userinput]
    user_df = user_df.sort_values(by="Total Admissions", ascending=False)
    user_df= user_df.sort_values(by="Total Admissions", ascending=False)[:limit]

    #making the list out of our user df for bokeh
    lat_list = list(user_df['latitude'])
    lon_list = list(user_df['longitude'])
    add_list = list(user_df['Total Admissions'])
    cob_list= list(user_df['Country of Birth'])
    state_list = list(user_df['State of Residence'])
    county_list = list(user_df['County of Residence'])
    rating_list = list(user_df['hate_crime_rating'])
    hate_list = list(user_df['hate_crimes(2019-2007)'])
    total_adm_list = list(user_df['Total Admissions (2007-2019)'])

    # implementing bokeh

    map_options = GMapOptions(lat=37.0902, lng=-95.7129, map_type="roadmap", zoom=3)

    plot = GMapPlot(x_range=Range1d(), y_range=Range1d(), map_options=map_options,api_key = "AIzaSyCkotDdb8K46AEHxQ_0G4zOzYbLvqXtYCA")

    source = ColumnDataSource(
        data = dict(
            lat=lat_list,
            lon=lon_list,
            Admissions = add_list,
            cob = cob_list,
            State= state_list,
            County = county_list,
            Rating = rating_list,
            Hatecrime = hate_list,
            totaladm = total_adm_list
        ))

    circle = Circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, line_color=None)
    plot.add_glyph(source, circle)

    plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool(), BoxZoomTool())

    plot.title.text="IMMIGRATION RECOMMENDATION SYSTEM"

    plot.add_tools(HoverTool(
        tooltips=[
        
            
            ('State', '@State'),
            ('County', '@County'),
            ( 'Country of Birth',  '@cob' ),
            ('Total Admission in the State:', '@totaladm'),
            ( 'Nationality Admissions',   '@Admissions' ),
            ('Total Hate Crimes (All Nationalities)', '@Hatecrime'),
            ('Hate Crime Rating', '@Rating')
        ],

        formatters={
            'Admissions' : 'numeral', 
            'Country of Birth' : 'printf',
            'State' : 'printf',
            'County' : 'printf',
            'Hate Crime Rating': 'printf',
            'Total Hate Crime' : 'printf',
            'Total Admission in the State' : 'numeral'
        },

        mode='vline'
    ))

    output_file("gmap_plot.html")
    show(plot)
    script, div = components(plot)
    return render_template('map.html', script = script, div = div)
#linking about us page
@app.route('/aboutus')
def aboutus():

    return render_template("aboutus.html")

#for the purposes of returning to home from about us or about the tool pages
@app.route('/home')
def home():

    return render_template("main1.html")


app.run(host='0.0.0.0', port=5000, debug=True) # anyone can connect, and we're running on port 5000