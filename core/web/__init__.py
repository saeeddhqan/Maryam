from flask import Flask, cli, render_template
from flasgger import Swagger
from core import initial
from core import core
from redis import Redis
import rq
import os
import requests
import json
import numpy as np 
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid, Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource

cli.show_server_banner = lambda *x: None

core_obj = core.core()
base_obj = initial.initialize(core_obj)

REDIS_URL = os.environ.get('REDIS_URL','redis://')
SWAGGER = {
	'title': 'Swagger',
	'info': {
		'title': 'Maryam-Api',
		'description': 'A RESTful API for Maryam'
	},
	'specs_route': '/api/'
}

WORKSPACE = base_obj.workspace.split('/')[-1]
print((f" * Workspace initialized: {WORKSPACE}"))


def create_hover_tool():
    """Generates the HTML for the Bokeh's hover data tool on our graph."""
    hover_html = """
      <div>
        <span class="hover-tooltip">@modules</span>
      </div>
      <div>
        <span class="hover-tooltip">@targets targets</span>
      </div>
      <div>
        <span class="hover-tooltip">@name</span>
      </div>
    """
    return HoverTool(tooltips=hover_html)


def create_bar_chart(data, title, x_name, y_name, hover_tool=None,
                     width=1200, height=300):
    """Creates a bar chart plot with the exact styling for the centcom
       dashboard. Pass in data as a dictionary, desired plot title,
       name of x axis, y axis and the hover tool HTML.
    """
    source = ColumnDataSource(data)
    xdr = FactorRange(factors=data[x_name])
    ydr = Range1d(start=0,end=max(data[y_name])*1.5)

    tools = []
    if hover_tool:
        tools = [hover_tool,]

    plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=width,
                  plot_height=height,
                  min_border=0, toolbar_location="above", tools=tools,
                 outline_line_color="#666666")

    glyph = VBar(x=x_name, top=y_name, bottom=0, width=.8,
                 fill_color="#e12127")
    plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.toolbar.logo = None
    plot.min_border_top = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "#999999"
    plot.yaxis.axis_label = "Targets Found"
    plot.ygrid.grid_line_alpha = 0.1
    plot.xaxis.axis_label = "All Modules"
    plot.xaxis.major_label_orientation = 1
    return plot

headings = ('Type', 'Modules', 'Targets', 'Results')
def create_app():

    # setting the static_url_path to blank serves static files from the web root
    app = Flask(__name__, static_url_path='')
    app.config.from_object(__name__)

    Swagger(app)

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('recon-tasks', connection=app.redis)

    @app.route('/')
    def index():
        r = requests.get('http://localhost:5000/api/graph/')
        dataPoints = json.loads(r.text)

        hover = create_hover_tool()
        plot = create_bar_chart(dataPoints, "targets found per module", "modules", "targets", hover)

        script, div = components(plot)

        return render_template('index.html', workspaces=base_obj._get_workspaces(), headings=headings, div = div, script=script)

    @app.route('/run')
    def run():
        return render_template('run.html', workspaces=base_obj._get_workspaces(), headings=headings)

    from core.web.api import resources
    app.register_blueprint(resources)

    return app
