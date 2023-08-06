#!/usr/bin/python
import sys

import click

import matplotlib
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

import numpy as np
matplotlib.use('Agg')


def plotFourColor(plotData, hasN, height, width, dpi, outputName, xLabel, plotTitle, sites):
    """
    function to create the four color plot image and save it as png.
    """
    # setting the last tick on x-axis to be the #columns in the data.
    lastTick = plotData.shape[1]

    # RGB equivalents for below colors
    # ['254,25,24','50,204,60','252,252,80','43,49,246','128,128,128']

    # A,T,G,C colors (matplotlib takes hexcodes)
    colors = ['#fe1918', '#32cc3c', '#fcfc50', '#2b31f6']

    # A,T,G,C,N colors (matplotlib takes hexcodes)
    ncolors = ['#fe1918', '#32cc3c', '#fcfc50', '#2b31f6', '#808080']

    if hasN is True:
        colorMap = mcolors.LinearSegmentedColormap.from_list(
            name='NColors', colors=ncolors, N=5)
    else:
        colorMap = mcolors.LinearSegmentedColormap.from_list(
            name='Colors', colors=colors, N=4)

    # figsize sets the figure dimensions as we need it
    plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)
    ax = plt.axes([0, 0, 1, 1])  # remove margins
    plt.imshow(plotData, cmap=colorMap, interpolation='nearest',
               aspect='auto')  # plot heatmap

    # retrieve current ticks for x-axis
    ax.xaxis.set_major_locator(MultipleLocator(15))
    mid = int(int(lastTick) // 2)  # calculate the midpoint

    # setting new ticks and labels

    # get the initial ticks
    locs, labels = plt.xticks()

    # remove the first location to get proper heatmap tick position.
    locs = np.delete(locs, 0)
    labels.pop()

    # find the mid value and set it to zero, since ax is helping to make sure there are odd number of ticks.
    mid = int(len(labels) // 2)
    labels[0] = "-" + "30"
    labels[mid] = "0"
    labels[len(labels) - 1] = "30"

    # display the new ticks
    plt.xticks(locs, labels, fontsize=14)

    ax.tick_params(which='major', length=10, width=2, color='black')
    ax.tick_params(which='minor', length=6, width=2, color='black')

    # refernce for ticks dimensions
    # https://matplotlib.org/2.1.1/api/_as_gen/matplotlib.pyplot.tick_params.html
    # plt.tick_params(length=8, width=2, labelright=True)

    plt.yticks([])
    plt.xlabel(xLabel, fontsize=14)
    ylabel = "{:,}".format(sites) + " sites"
    plt.ylabel(ylabel, fontsize=14)
    plt.title(plotTitle, fontsize=18)

    # to increase the width of the plot borders
    plt.setp(ax.spines.values(), linewidth=2)

    plt.savefig(outputName, bbox_inches='tight',
                pad_inches=0, dpi=dpi, facecolor=None)
    return 0


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(options_metavar='<options>', context_settings=CONTEXT_SETTINGS)
@click.argument('fasta', type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=False,))
@click.option('-pt', '--title', metavar="<string>", default=' ', prompt=True, show_default=' ', help='Plot title')
@click.option('-xl', '--xlabel', metavar="<string>", default=' ', prompt=True, show_default=' ', help='Label under X-axis')
@click.option('-ph', '--height', metavar="<int>", type=int, default=700, prompt=True, show_default='True', help='Plot Height')
@click.option('-pw', '--width', metavar="<int>", type=int, default=300, prompt=True, show_default='True', help='Plot Width')
@click.option('-hn', '--hasn', metavar="<string>", type=click.BOOL, default='False', prompt=True, show_default='False', help='Does fasta contain "N" ? ')
@click.option('-d', '--dpi', metavar="<int>", type=int, default=100, prompt=True, show_default='100', help='Plot pixel density')
@click.option('-o', '--out', metavar="<string>", default='fourcolor.png', prompt=True, show_default='fourcolor.png', help='output filename')
def cli(fasta, height, width, title, xlabel, hasn, dpi, out):
    """
    Creates a fourcolor plot from the input fasta sequences.

    \b
    The --hasn option is used to specify if you have an unknown base pair in the fasta sequence,
    usually represented as 'N' in the file.
    If set to True, it adjusts the color scheme to show 'N' in the plot.

    """
    click.echo('\n' + '.' * 50)

    # nucleotide to color mapper (doesnt include N or n , since other letters are converted mapped to 5 (grey color) by default)
    NCMapper = {
        'a': 1,
        'A': 1,
        't': 2,
        'T': 2,
        'g': 3,
        'G': 3,
        'c': 4,
        'C': 4,
    }

    hasN = hasn  # flag to switch the colormap to represent the five colors in the colorplot
    sequences = {}  # to store fasta sequences as (k,v)
    data = []  # To store the sequences
    key = "firstLine"  # temporary key to ignore if first line doesnt start with >chr
    openfile = open(fasta, 'r').readlines()

    # checking if the first line startswith '>chr'
    if openfile[0].startswith('>') is False:
        print("Invalid fasta file ! \nsequences header is missing .. need to start with '>chr'\nRequires standard fasta file")
        sys.exit()

    # reading each line
    for line in openfile:
        line = line.strip()
        if line.startswith('>') is False:
            # to store the sequences that are processed
            sequences[key].append(line)
        else:
            key = line
            sequences[key] = []

    for k, v in sequences.items():
        seq = ''.join(sequences[k])
        temp = []  # to store numeric equivalents for the sequences
        for nucleotide in list(seq):
            if nucleotide in NCMapper.keys():
                temp.append(NCMapper[nucleotide])
            else:
                # setting the color code for other alphabets
                temp.append(5)
                hasN = True
        data.append(temp)

    plotData = np.array(data, dtype=int)

    print("\nprocessed sequences: {}\n".format(sequences.keys()))
    print("plotData : \n{}".format(plotData))

    # creating the four Color with proper dimensions
    plotFourColor(plotData, hasN, height, width, dpi,
                  out, xlabel, title, len(sequences))
    click.echo('\n' + '.' * 50)
