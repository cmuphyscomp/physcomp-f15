#!/usr/bin/env python

import re
import os
import argparse

header = """<!doctype html>
<html lang="en-US">
  <head>
    <meta charset="utf-8" />
    <title>Physical Computing Exercises</title>
    <link rel="stylesheet" type="text/css" href="../support/css/physcomp.css" />
  </head>
  <body>
    <h2>Physical Computing Exercises</h2>
    <ul>
"""

footer = """    </ul>
  </body>
</html>
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description = """Rebuild the index page for the exercises folder.""")
    parser.add_argument( '-v', '--verbose', action='store_true', help='Enable more detailed output.' )
    args = parser.parse_args()

    if os.path.basename(os.getcwd()) != 'css':
        print "Error: this script must be run from within the css folder, it uses relative paths."
        exit(1)

    # relative path to the root of the repository
    root_path = '../..'
    exercises_path = os.path.join(root_path, 'exercises')
    exercises_index = os.path.join(exercises_path, 'index.html')

    # list of folders found for the index
    folders = list()
    
    for root, dirs, files in os.walk(exercises_path):
        if 'index.html' in files:

            # find the folder path within the repository naming scheme
            relpath = os.path.relpath(root, exercises_path)

            # find the depth and name elements
            path_parts = relpath.split('/' )
            if len(path_parts) == 2:
                folders.append( (relpath, path_parts[0], path_parts[1] ))

    # generate a single index file
    with open(exercises_index, 'w') as output:
        output.write(header)
        for f in folders:
            output.write( """      <li><a href="%s/index.html">%s : %s</a></li>\n""" % f)
        output.write(footer)
