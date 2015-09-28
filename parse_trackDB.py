import argparse
import collections
import os
import sys

__author__ = 'A. Jason Grundstad'


def parse_master(genome_dir=None):
    template_file = open(os.path.join(genome_dir, 'trackDb.txt.master'), 'r')
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
    return d


def update_trackdbfile(tracks=None, visible_list=None,
                       output=None):
    """
    Take in dict of orderedDicts, print to provided output [stdout]
    :param tracks: orderedDict of orderedDicts
    :param visible_list: track names to be set to 'dense'
    :param output: mode of output, file or stdout (default)
    :return: None
    """
    outfile = open(output, 'w')
    visible_list.append('flyTrack1')  # always make flyTrack1 visible
    visible_list = set(visible_list)  # no redundancy

    for track_name in tracks:
        tracks[track_name]['visibility'] = 'hide'
        if track_name in visible_list:
            tracks[track_name]['visibility'] = 'dense'
        for key in tracks[track_name]:
            print >>outfile, "{} {}".format(key, tracks[track_name][key])
        print >>outfile, ''


def main():
    parser = argparse.ArgumentParser("Update visibility of tracks in " +
                                     "the given trackDB file")
    parser.add_argument('-g', dest='genome_dir', required=True,
                        help="modERN_TrackHub/(?)")
    parser.add_argument('-v', dest='visible_list',
                        help="list of track names to be set to 'dense'.  " +
                        "Comma delimited")
    args = parser.parse_args()

    tracks = parse_master(args.genome_dir)
    outfile = os.path.join(args.genome_dir, 'trackDb.txt')
    update_trackdbfile(tracks=tracks, visible_list=args.visible_list.split(','),
                       output=outfile)


if __name__ == '__main__':
    main()
