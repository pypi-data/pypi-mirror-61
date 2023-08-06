from nada_dataprofilering.vizualisation.table_data import *
from nada_dataprofilering.vizualisation.bins import Interval
import plotly.graph_objects as go


def var2_hist(resp, threshold=10):
    data = make_table_data(resp, threshold)
    values = [row[0] for row in data]
    counts = [row[1] for row in data]

    fig = go.Figure(go.Bar(x=values, y=counts), layout=go.Layout(yaxis_title='Antall', xaxis={'type': 'category'}))

    return fig.to_json()


def date_hist(resp, nbins=10):
    try:
        values = resp['VERDI']
        counts = resp['ANTALL']
    except KeyError:
        raise VizualKeysNotFound(f"Expected ['VERDI', 'ANTALL'] as keys but got {list(resp.keys())}")

    if len(values) < 6:
        fig = go.Figure(go.Bar(x=values, y=counts),
                        layout=go.Layout(yaxis_title='Antall', xaxis=dict(tickmode='array', tickvals=values)))
        return fig.to_json()

    else:
        bound = make_boundaries(values, nbins)
        bins = make_bins(bound)

        fill_bins(bins, values, counts)

        mid_plot, count_plot, width_plot = bins_to_plot(bins)

        fig = go.Figure(go.Bar(x=mid_plot, y=count_plot), go.Layout(yaxis_title='Antall'))

        return fig.to_json()


def num_hist(resp, nbins=10):
    try:
        values = resp['VERDI']
        counts = resp['ANTALL']
    except KeyError:
        raise VizualKeysNotFound(f"Expected ['VERDI', 'ANTALL'] as keys but got {list(resp.keys())}")

    if len(values) < 6:
        fig = go.Figure(go.Bar(x=values, y=counts),
                        layout=go.Layout(yaxis_title='Antall', xaxis=dict(tickmode='array', tickvals=values)))
        return fig.to_json()

    else:

        bound = make_boundaries(values, nbins)
        bins = make_bins(bound)

        fill_bins(bins, values, counts)

        mid_plot, count_plot, width_plot = bins_to_plot(bins)

        fig = go.Figure(go.Bar(x=mid_plot, y=count_plot, width=width_plot), go.Layout(yaxis_title='Antall'))

        return fig.to_json()


def fill_bins(bins, values, counts):
    for i in range(len(bins)):
        for v in range(len(values)):
            if bins[i].is_in(values[v]):
                bins[i].add_count(counts[v])


def make_bins(bound):
    bins = []
    for i in range(len(bound) - 1):
        if i + 1 == len(bound) - 1:
            bins.append(Interval(bound[i], bound[i + 1], closed='both'))
        else:
            bins.append(Interval(bound[i], bound[i + 1]))

    return bins


def make_boundaries(values, nbins=10):
    min_value = min(values)
    max_value = max(values)
    range_value = max_value - min_value

    width = range_value / nbins

    return [min_value + i * width for i in range(nbins + 1)]


def bins_to_plot(bins):
    mid_plot = []
    counts_plot = []
    width_plot = []
    for i in bins:
        mid, width, count = i.plot_info()
        mid_plot.append(mid)
        counts_plot.append(count)
        width_plot.append(width)

    return mid_plot, counts_plot, width_plot
