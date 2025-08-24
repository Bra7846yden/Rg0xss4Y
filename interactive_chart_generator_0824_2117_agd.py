# 代码生成时间: 2025-08-24 21:17:22
# interactive_chart_generator.py
# This program serves as an interactive chart generator using Python and Starlette framework.

import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category10

# Define the schema for the data
class ChartData:
    def __init__(self, categories, values):
        self.categories = categories
        self.values = values

# Define the Bokeh chart
def create_chart(data):
    # Create a ColumnDataSource from the provided data
    source = ColumnDataSource(data=dict(categories=data.categories, values=data.values))
    # Create a new plot with a title and axis labels
    p = figure(title="Interactive Chart", x_axis_label='Category', y_axis_label='Value',
                tools="pan,wheel_zoom,box_zoom,reset,save")
    # Add a line to the plot
    p.line(x='categories', y='values', source=source)
    # Add a legend
    p.legend.label Stand_alone = ['values']
    # Return the components needed for embedding
    return components(p)

# Define the Starlette routes
routes = [
    Route("/chart", endpoint=lambda request: HTMLResponse(
        content="""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Interactive Chart Generator</title>
            <script src="https://cdn.bokeh.org/bokeh/release/bokeh-2.4.2.min.js"></script>
            <script src="https://cdn.bokeh.org/bokeh/release/bokeh-widgets-2.4.2.min.js"></script>
            <script src="https://cdn.bokeh.org/bokeh/release/bokeh-tables-2.4.2.min.js"></script>
        </head>
        <body>
            <div id="123"></div>
            <script>
                Bokeh.safely(function() {
                    var div = document.getElementById("123");
                    // Fetch chart data from the server
                    fetch("/chart/data").then(function(response) {
                        return response.json();
                    }).then(function(data) {
                        // Embed the chart
                        Bokeh.embed.embed_item(data);
                    }).catch(function(error) {
                        console.error("Error embedding chart: " + error.message);
                    });
                });
            </script>
        </body>
        </html>
        """),
        media_type="text/html")),
    Route("/chart/data", endpoint=lambda request: JSONResponse(create_chart(ChartData(["A", "B", "C"], [10, 20, 15])))),
]

# Define the application
app = Starlette(debug=True, routes=routes)

# Run the application
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
