import os

from flask import Flask, request, render_template, jsonify
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import parse_trackDB

config = dict()

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
    if selected_genome == '-- select genome --':
        global config
        return render_template('select.html', genomes=config['genomes'])
    else:
        trackdb_master = get_track_master(genome=request.form['genome_select'])
        tracks = parse_trackDB.parse_master(trackdb_master)
        return render_template('select.html', genomes=config['genomes'],
                               genome_path=trackdb_master,
                               genome=selected_genome, tracks=tracks,)


@app.route("/update_trackDB", methods=['POST', 'GET'])
def update_tracks():
    global config
    print "Called update_tracks"
    selected_genome = request.args.get('selected_genome')
    selected_tracks = request.args.get('tracks')
    outfile_name = os.path.join(config['base_dir'], selected_genome,
                                'trackDbs', request.args.get('outfile'))
    print "selected_genome is: {}".format(selected_genome)
    print "selected_tracks: {}".format(selected_tracks)
    print "provided linkDb name: {}".format(outfile_name)

    master_file = os.path.join(config['base_dir'], selected_genome, 'trackDbs',
                               'trackDb.txt.master')
    print "base_dir in config: {}".format(config['base_dir'])
    master_tracks = parse_trackDB.parse_master(track_master=master_file)
    parse_trackDB.update_trackdbfiles(tracks=master_tracks,
                                      visible_list=selected_tracks,
                                      output=outfile_name,
                                      genome=selected_genome)

    # add_hub(url=config['hubUrl'], filename=outfile_name)

    return render_template('select.html', genomes=config['genomes'])


@app.route("/get_filter_options", methods=['GET'])
def get_filter_options():
    genome = request.args.get('genome')
    if 'dm' in genome:
        return jsonify(filters=dm_filter_options)
    elif 'WS' in genome:
        return jsonify(filters=ws_filter_options)
    else:
        return None


@app.route("/get_config", methods=['GET'])
def get_config():
    global config
    return jsonify(config=config)


def get_track_master(genome=None):
    global config
    trackdb_master = os.path.join(config['base_dir'], genome,
                                  'trackDbs', 'trackDb.txt.master')
    print trackdb_master
    return trackdb_master


def parse_config(filename=None):
    d = {'genomes': ['dm3', 'dm6', 'WS220', 'WS235', 'histone'],
         'base_dir': 'modERN_TrackHub',
         'hubUrl':
             'https://genome.ucsc.edu/cgi-bin/hgHubConnect?hgsid=443214985_l1fwTXq7lMR7Z7W9lliOUu1XHJ4c',
         'hubFileUrl': 'http://igsbmod.uchicago.edu/~avictorsen/modERN_TrackHub'}

    return d


def find_by_xpath(locator=None, driver=None):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, locator))
    )
    return element


def add_hub(url=None, filename=None):
    """

    :param url: location of "add a hub" page
    :param filename: relative location of new hub file
    :return:
    """
    global config
    d = Display(visible=0, size=(800, 600))
    d.start()
    driver = webdriver.Firefox()
    driver.get(url)
    find_by_xpath('//input[@name = "hubText"]').send_keys(
        os.path.join(config['hubFileUrl'], filename)
    )
    # find_by_xpath('//input[@name = "hubAddButton"]').click()
    # d.stop()


if __name__ == "__main__":
    # global config
    config = parse_config(filename='config.json')
    app.run(debug=True)