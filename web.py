try:
    import cherrypy
except ImportError: # not needed unless we really want to run webserver
    pass
import thread
from jinja2 import Environment, FileSystemLoader
import os
import glob
import sys
import random
import schema

def redirect(path='/', body=None, delay=0):
    'redirect browser, if desired after showing a message'
    s = '<HTML><HEAD>\n'
    s += '<meta http-equiv="Refresh" content="%d; url=%s">\n' % (delay, path)
    s += '</HEAD>\n'
    if body:
        s += '<BODY>%s</BODY>\n' % body
    s += '</HTML>\n'
    return s

def load_templates(path='_templates/*.html'):
    'return dictionary of Jinja2 templates from specified path/*.html'
    d = {}
    loader = FileSystemLoader(os.path.dirname(path))
    env = Environment(loader=loader)
    for fname in glob.glob(path):
        basename = os.path.basename(fname)
        name = basename.split('.')[0]
        d[name] = env.get_template(basename)
    return d, env

def load_template_vars(path='_templates'):
    sys.path.append(path)
    spnet_base = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(spnet_base)
    try:
        import template_vars
        return template_vars.templates, template_vars.views
    except ImportError:
        print 'Warning: no %s/template_vars.py?' % path
    except AttributeError:
        raise ImportError('template_vars.py must define templates, views')


def render_jinja(template, **kwargs):
    'apply the template to kwargs'
    return template.render(**kwargs)

def init_template_views(templateDict, templateVars={}, templateViews={}):
    'set up views for jinja templates'
    d = {}
    for k,viewFunc in templateViews.items(): # add view functions
        funcArgs = {}
        try:
            funcArgs['template'] = templateDict[k]
        except KeyError:
            pass
        funcArgs.update(templateVars.get(k, {}))
        d[k] = (viewFunc, funcArgs)
    for k,v in templateDict.items():
        if k not in d: # use render_jinja trivial view function
            funcArgs = dict(template=v)
            funcArgs.update(templateVars.get(k, {}))
            d[k] = (render_jinja, funcArgs)
    return d

def fetch_data(d, positions, moves):
    'just a dumb prototype for general-purpose obj retrieval'
    try: # get requested position
        position = d['position']
    except KeyError:
        pass
    else:
        d['position'] = positions[position]
    try: # get requested submission
        subID = d['submission']
    except KeyError:
        pass
    else:
        d['submission'] = moves[int(subID)]
    try: # get requested submission
        trID = d['transition']
    except KeyError:
        pass
    else:
        d['transition'] = moves[int(trID)]

def make_url(view, **kwargs):
    'return URL format for this server'
    if view.startswith('/') or view.startswith('http://'): # treat as root path
        path = view
        opts = []
    else: # treat as standard view
        path = '/view'
        opts = ['view=' + view]
    opts += ['%s=%s' % (k,str(v)) for k,v in kwargs.items()]
    if opts:
        return path + '?' + '&'.join(opts)
    else:
        return path

class Server(object):
    def __init__(self, positions, moves, views):
        self.positions = positions
        self.moves = moves
        self.views = views

    def start(self):
        'start cherrypy server as background thread, retaining control of main thread'
        self.threadID = thread.start_new_thread(self.serve_forever, ())

    def serve_forever(self):
        cherrypy.quickstart(self, '/', 'cp.conf')

    def index(self):
        'just reroute to our standard index view'
        return self.view('index')
    index.exposed = True
        
    def view(self, view, **kwargs):
        'generic view method, primarily for HTML pages'
        try:
            v = self.views[view]
        except KeyError:
            cherrypy.response.status = 404
            return 'invalid request'
        l = [0, {}, {}]
        l[0:len(v)] = v
        func, funcargs, intargs = l
        # use intargs to check things like privileges before calling func
        d = funcargs.copy()
        d.update(kwargs)
        try:
            fetch_data(d, self.positions, self.moves) # retrieve objects
            s = func(make_url=make_url, hasattr=hasattr, getattr=getattr,
                     positions=self.positions, **d) # run the requested view function
        except Exception, e:
            cherrypy.log.error('view function error', traceback=True)
            cherrypy.response.status = 500
            return 'server error'
        return s
    view.exposed = True

    def random(self):
        n = 0
        while n == 0:
            pos = random.choice(self.positions.keys())
            n = len(self.positions[pos].submission) \
                + len(self.positions[pos].transition)
        return self.view('position', position=pos)
    random.exposed = True

def init_data(filename):
    from reusabletext import parse
    print 'loading templates...'
    templateDict, env = load_templates()
    #templateVars, templateViews = load_template_vars()
    #views = init_template_views(templateDict, templateVars, templateViews)
    views = init_template_views(templateDict)
    rust = parse.parse_file(filename, blockTokens=schema.defaultBlocks)
    positions, moves = schema.init_graph(rust)
    return positions, moves, views

def get_server(filename):
    positions, moves, views = init_data(filename)
    return Server(positions, moves, views), positions, moves

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('usage: %s RUSTFILE' % sys.argv[0])
    s, positions, moves = get_server(sys.argv[1])
    print 'starting server...'
    s.serve_forever()
