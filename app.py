import bottle
import os
import sys
import json
import spell
from bottle import request, route, run, Response, template

@route("/")
@route("/home")
def home():
	return template('index.tpl', request=request)

@route("/check")
def check():
	word = request.params.get('word')
	result = autocorrect(word)
	return json.dumps({'result': result})

if '--debug' in sys.argv[1:] or 'SERVER_DEBUG' in os.environ:
    # Debug mode will enable more verbose output in the console window.
    # It must be set at the beginning of the script.
    bottle.debug(True)

def wsgi_app():
    """Returns the application to make available through wfastcgi. This is used
    when the site is published to Microsoft Azure."""
    return bottle.default_app()

if __name__ == '__main__':
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    @bottle.route('/static/<filepath:path>')
    def server_static(filepath):
        """Handler for static files, used with the development server.
        When running under a production server such as IIS or Apache,
        the server should be configured to serve the static files."""
        return bottle.static_file(filepath, root=STATIC_ROOT)

    # Starts a local test server.
    bottle.run(server='wsgiref', host=HOST, port=PORT)

global alphabets, badchars, corpus_list_raw, corpus_list
alphabets = string.ascii_lowercase
badchars = string.punctuation + string.digits
corpus_list_raw = []

with open("big.txt", "r") as txtfile:
	for corpus_line in txtfile:
		corpus_line = corpus_line.lower().strip()
		for char in corpus_line:
			if char in badchars:
				if (char == chr(39)) and (("n"+char+"t") or (char+"s") in corpus_line):
					continue
				else:
					corpus_line = corpus_line.replace(char," ")
		corpus_list_raw += corpus_line.split()

# Remove unwanted characters from corpus words that might still exist due to the addition of contraction words

corpus_list = [corpus_word.strip(badchars) for corpus_word in corpus_list_raw]