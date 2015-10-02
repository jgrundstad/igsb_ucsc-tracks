from flask import Flask, request, render_template, jsonify
import os
import parse_trackDB
__author__ = 'jgrundst'
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'templates')
app = Flask(__name__, template_folder=template_dir)

dm_filter_options = ['W3l', 'Embryo', 'WPP', 'Adult m/f', 'Adult f', 'Adult m']
ws_filter_options = []

@app.route("/")
def main_page():
    genomes = config['genomes']
    return render_template('select.html', genomes=genomes)

@app.route("/show_available_tracks", methods=['POST'])
def show_available():
    print "called select_available_tracks"
    selected_genome = request.form['genome_select']
    # print "selected: " + selected_genome
    if selected_genome == '-- select genome --':
        global config
        return render_template('select.html', genomes=config['genomes'])
    else:
        genome_path = get_bw_files(genome=request.form['genome_select'])
        tracks = parse_trackDB.parse_master(genome_path)
        return render_template('select.html', genomes=config['genomes'],
                               genome_path=genome_path, genome=selected_genome,
                               tracks=tracks,)

@app.route("/update_trackDB", methods=['POST', 'GET'])
def update_tracks():
    print "Called update_tracks"
    selected_genome = request.form['selected_genome']
    selected_tracks = request.form['tracks']
    print "selected_genome is: {}".format(selected_genome)
    print "selected_tracks: {}".format(selected_tracks)

    return render_template('select.html', genomes=config['genomes'])

@app.route("/get_filter_options", methods=['GET'])
def get_filter_options():
    genome = request.args.get('genome')
    if 'dm' in genome:
        print "yes, dm is in genome"
        return jsonify(filters=dm_filter_options)
    elif 'WS' in genome:
        return jsonify(filters=ws_filter_options)
    else:
        return None

def get_bw_files(genome=None):
    global config
    genome_path = os.path.join(config['base_dir'], genome, 'trackDbs')
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