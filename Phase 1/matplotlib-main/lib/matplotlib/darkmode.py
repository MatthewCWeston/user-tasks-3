import matplotlib

def invert_color(c):
    if (c == None):
        c = 'black'
    if (type(c) == str):
        c = matplotlib.colors.to_rgb(c)
    return (1.-c[0],1-c[1],1-c[2])

def invert_text_color(txt):
    txt._color = invert_color(txt._color)

def invert_tick_color(xs):
    tp = xs.get_tick_params()
    tc = tp['color'] if 'color' in tp else None
    xs.set_tick_params(colors=invert_color(tc))

def toggle_dark_mode_axis(ax):
    ax.set_facecolor(invert_color(ax.get_facecolor()))
    invert_text_color(ax.title)
    invert_text_color(ax.xaxis.label)
    invert_text_color(ax.yaxis.label)
    for t in ax.texts:
        invert_text_color(t)
    invert_tick_color(ax.yaxis)
    invert_tick_color(ax.xaxis)

def toggle_dark_mode(ax=None, fig=None):
    if (ax==None and fig==None):
        fig = plt.gcf()
    if (fig != None):
        fig.set_facecolor(invert_color(fig.get_facecolor()))
        ax_list = fig.axes
    else:
        ax_list = [ax]
    # Now, run on our axes
    for ax in ax_list:
        toggle_dark_mode_axis(ax)