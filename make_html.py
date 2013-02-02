import web
import os.path

def make_filename(view, objID):
    return '%s_%s.html' % (view, str(objID).replace(':', '_'))

def make_url(view, **kwargs):
    if view.startswith('http://'):
        return view
    elif view == '/':
        return 'index.html'
    elif view == '/random':
        return 'index.html'
    elif view.startswith('/'):
        return view[1:]
    return make_filename(view, kwargs.values()[0])
    

def render(outdir, template, filename, **kwargs):
    'render to static HTML file'
    path = os.path.join(outdir, filename)
    s = template.render(make_url=make_url, hasattr=hasattr, getattr=getattr,
                        **kwargs)
    with open(path, 'w') as ifile:
        ifile.write(s)
        
def generate_html(outdir, views, dataDict, varDict=dict(opponent='position'),
                  **kwargs):
    'generate static HTML pages for all templates vs. all data'
    for k,t in views.items():
        template = t[1]['template']
        varName = k
        if varName[-1].isupper(): # strip trailing capital letter
            varName = varName[:-1]
        varName = varDict.get(varName, varName) # remap if needed
        try:
            data = dataDict[varName]
        except KeyError: # generate single page
            render(outdir, template, k + '.html', **kwargs)
        else: # generate page for each obj in data
            for obj in data:
                d = {varName:obj}
                d.update(kwargs)
                render(outdir, template, make_filename(k, obj.id), **d)
            
def run_build(filename, outdir='htmlout'):
    'load data and generate HTML'
    positions, moves, views = web.init_data(filename)
    dataDict = dict(position=positions.values())
    dataDict['transition'] = [m for m in moves if hasattr(m, 'toPos')]
    dataDict['submission'] = [m for m in moves if not hasattr(m, 'toPos')]
    generate_html(outdir, views, dataDict, positions=positions)

def main():
    'script entry point for generating static HTML'
    import sys
    if len(sys.argv) < 1:
        raise ValueError('usage: %s RUSTFILE [OUTDIR]' % sys.argv[0])
    run_build(*sys.argv[1:])

if __name__ == '__main__':
    main()
