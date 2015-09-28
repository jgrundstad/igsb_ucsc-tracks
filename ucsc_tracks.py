from flask import Flask, request, render_template
import os
import parse_trackDB
__author__ = 'jgrundst'
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route("/")
def hello():
    genomes = config['genomes']
    return render_template('select.html', genomes=genomes)

@app.route("/show_available_tracks", methods=['POST'])
def echo():
    print "called select_available_tracks"
    selected_genome = request.form['genome_select']
    print "selected: " + selected_genome
    if selected_genome == '-- select genome --':
        global config
        return render_template('select.html', genomes=config['genomes'])
    else:
        genome_path = get_bw_files(genome=request.form['genome_select'])
        tracks = parse_trackDB.parse_master(genome_path)
        return render_template('select.html', genomes=config['genomes'],
                               genome_path=genome_path, tracks=tracks,)

def get_bw_files(genome=None):
    global config
    genome_path = os.path.join(config['base_dir'], genome)
    print genome_path
    return genome_path

def parse_config(filename=None):
    d = {'genomes': ['dm3', 'dm6', 'WS220', 'WS235', 'histone'],
         'base_dir': 'modERN_TrackHub'}
    return d


if __name__ == "__main__":
    global config
    config = parse_config(filename='config.json')
    app.run(debug=True)