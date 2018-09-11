import numpy as np

from bokeh.layouts import row, widgetbox
from bokeh.models import CustomJS, Slider
from bokeh.plotting import figure, output_file, show, ColumnDataSource

A1 = -14.72757
A2 = 79.9554
x0 = 7.74771
dx = 0.41551

x = np.linspace(9.5, 6, 100)
y= A2+(A1-A2)/(1+np.exp((x-x0)/dx))
plot = figure(y_range=(-24, 90), plot_width=400, plot_height=400)

plot.line(x, y, line_width=3, line_alpha=0.6)

x = [9]
y = [A2+(A1-A2)/(1+np.exp((x[0]-x0)/dx))]
source = ColumnDataSource(data=dict(x=x, y=y, time_left=[f'{y[0]:.0f} hours'], text_color=['green']))
plot.circle('x', 'y', source=source, color='red', size=10)
plot.text(8.5, -7, text='time_left', text_color='text_color',
        alpha=0.6667, text_font_size='36pt', text_baseline='middle',
        text_align='center', source=source)

callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var U = volt.value
    var A1 = -14.72757
    var A2 = 79.9554
    var x0 = 7.74771
    var dx = 0.41551
    
    data['y'][0] = A2+(A1-A2)/(1+Math.exp((U-x0)/dx))
    data['x'][0] = U
    if (data['y'][0] < 12) {
        data['text_color'][0] = 'red'
    } else {
        data['text_color'][0] = 'green'
    }
    data['time_left'][0] = data['y'][0].toFixed(0).toString() + ' hours'
    
    source.change.emit();
""")

voltage_slider = Slider(start=6, end=9.5, value=9, step=.01,
                    title="Battery voltage", callback=callback)
callback.args["volt"] = voltage_slider




layout = row(
    plot,
    widgetbox(voltage_slider, width=400), sizing_mode="scale_height"
)

output_file("battery.html", title="9V battery consumption")
show(layout)