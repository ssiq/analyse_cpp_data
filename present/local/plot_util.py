def show_box(alldata, namelist, figsizex=8, figsizey=6, title='盒状图'):
    """
    create a box figure.
    :param alldata: data list which will be shown in plot. It is a list-list. Each list is data in ONE axis. Example: [[1,2,3], [4,5,6]]
    :param namelist: the name list of data axis. the number of namelist is same as the number of alldata
    :param figsizex: figure size of x, default is 8
    :param figsizey: figure size of y, default is 6
    :param title: the figure title
    """
    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(figsizex, figsizey))
    bplot = plt.boxplot(alldata,
                        notch=False,  # box instead of notch shape
                        sym='rs',  # red squares for outliers
                        vert=False)  # vertical box aligmnent
    plt.yticks([i for i in range(1, len(namelist)+1)], namelist)
    plt.ylabel('')

    for components in bplot.keys():
        for line in bplot[components]:
            line.set_color('black')  # black lines

    t = plt.title(title)

    plt.show()
