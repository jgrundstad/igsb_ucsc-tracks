import argparse
import collections
import os
import sys

__author__ = 'A. Jason Grundstad'


def parse_master(track_master=None):
    template_file = open(track_master, 'r')
    d = collections.OrderedDict()
    sub_d = collections.OrderedDict()
    current_track = ''
    for line in template_file:
        line = line.rstrip()
        if line is not '':
            toks = line.split(' ')
            if toks[0] == 'track':
                current_track = toks[1]
            sub_d[toks[0]] = toks[1]
        else:
            if current_track:
                d[current_track] = sub_d
            current_track = ''
            sub_d = collections.OrderedDict()
    template_file.close()
    return d


def update_trackdbfiles(tracks=None, visible_list=None,
                       output=None, genome=None):
    """
    Take in dict of orderedDicts, print to provided output [stdout]
    Must also update:
        config['base_dir']/hub.txt
        config['base_dir']/genome.txt
    :param tracks: orderedDict of orderedDicts
    :param visible_list: track names to be set to 'dense'
    :param output: mode of output, file or stdout (default)
    :return: None
    """

    outfile = open(output, 'w')
    outfile_base = output.split(os.path.sep)[-1]
    outfile_dir = os.path.sep.join(output.split(os.path.sep)[0:-1])
    print "outfile base: {}".format(outfile_base)
    print "outfile dir: {}".format(outfile_dir)
    visible_list += ',flyTrack1'
    visible_set = set(visible_list.split(','))
    print "writing list: {}\n to outfile {}".format(visible_set, output)
    for track_name in tracks:
        tracks[track_name]['visibility'] = 'hide'
        if track_name in visible_set:
            tracks[track_name]['visibility'] = 'dense'
        for key in tracks[track_name]:
            print >>outfile, "{} {}".format(key, tracks[track_name][key])
        print >>outfile, ''
    outfile.close()

    hubfile_name = outfile_base + '.hub.txt'
    genomefile_name = outfile_base + '.genome.txt'
    print "hubfile_name: {}".format(hubfile_name)
    print "genomefile_name: {}".format(genomefile_name)
    print "dir: {}".format(outfile_dir)
    create_hub_file(dir=outfile_dir, hubfile_name=hubfile_name,
                    hub_name=outfile_base, genomefile_name=genomefile_name)
    create_genome_file(dir=outfile_dir, genomefile_name=genomefile_name,
                       genome=genome, outfile_base=outfile_base)


def create_genome_file(dir=None, genomefile_name=None, genome=None,
                       outfile_base=None):
    genome_file = open(os.path.join(dir, genomefile_name), 'w')
    content = '''genome {}
trackDb {}
'''
    print >>genome_file, content.format(genome, outfile_base)
    genome_file.close()


def create_hub_file(dir=None, hubfile_name=None, hub_name=None,
                    genomefile_name=None):
    hubfile = open(os.path.join(dir, hubfile_name), 'w')
    content = '''hub {}
shortLabel {}
longLabel Fly-Worm Project signal tracks ({})
genomesFile {}
email avictorsen@uchicago.edu
'''
    print >>hubfile, content.format(hub_name, hub_name, hub_name,
                                    genomefile_name)


def main():
    parser = argparse.ArgumentParser("Update visibility of tracks in " +
                                     "the given trackDB file")
    parser.add_argument('-g', dest='genome_dir', required=True,
                        help="modERN_TrackHub/(?)")
    parser.add_argument('-l', dest='visible_list',
                        help="list of track names to be set to 'dense'.  " +
                        "Comma delimited")
    parser.add_argument('-o', dest='output_filename', required=True,
                        help="name of outfile containing track collection.")
    args = parser.parse_args()

    tracks = parse_master(args.genome_dir)
    outfile = os.path.join(args.genome_dir, args.output_filename)
    update_trackdbfiles(tracks=tracks, visible_list=args.visible_list.split(','),
                       output=outfile)


if __name__ == '__main__':
    main()
