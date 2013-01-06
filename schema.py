from reusabletext import graphviz

defaultBlocks = (':position:', ':transition:', ':submission:',
                 ':opportunity:', ':brief:',
                 ':warning:', ':comment:', ':key:', ':counter:',
                 )

def get_singleton_attr(obj, attr):
    l = getattr(obj, attr)
    if len(l) > 1:
        raise ValueError('attribute %s cannot have multiple values' % attr)
    return l[0]


class MoveBase(object):
    def __init__(self, node, image=(), video=(), **kwargs):
        if len(node.tokens) > 1:            
            self.name = node.tokens[1]
            if 'title' not in kwargs:
                self.title = self.name
        self.node = node
        self.__dict__.update(kwargs)
        s = '\n'.join(getattr(node, 'text', ())) # convert list to string
        self.text = graphviz.trivial_html(s)
        images = []
        for line in image:
            images.append(Image(line))
        if images:
            self.image = images
        videos = []
        for line in video:
            videos.append(Video(line))
        if videos:
            self.video = videos

class Position(MoveBase):
    def __init__(self, *args, **kwargs):
        MoveBase.__init__(self, *args, **kwargs)
        self.id = '%s:%s' % (self.name, self.role)
        self.title = self.id
        self.submission = []
        self.transition = []

class Image(object):
    def __init__(self, path):
        if path.startswith('http://'):
            self.url = path
        else:
            self.url = '/images/' + path

class Video(object):
    def __init__(self, path):
        if path.startswith('youtube:'):
            self.__class__ = YouTubeVideo
            self.id = path[8:]

class YouTubeVideo(Video):
    def get_html(self):
        return '''<iframe width="560" height="315"
        src="http://www.youtube.com/embed/%s?rel=0"
        frameborder="0" allowfullscreen></iframe>\n''' % self.id
        

def switch_role(positionID):
    'swap D and A roles'
    d = dict(A='D', D='A')
    l = positionID.split(':')
    return  l[0] + ':' + d[l[1]]

def init_graph(tree):
    positions = {}
    moves = []
    for node in tree.walk():
        token = getattr(node, 'tokens', ('skip',))[0][1:-1]
        if token == 'position': # create A and D roles for this position
            metadata = node.metadata_dict()
            name = node.tokens[1]
            pos = Position(node, role='A', **metadata)
            positions[pos.id] = pos
            pos = Position(node, role='D', **metadata)
            positions[pos.id] = pos

        elif token == 'transition' or token == 'submission':
            metadata = node.metadata_dict()
            node.child_dict(metadata)
            move = MoveBase(node, **metadata)
            fromPos = get_singleton_attr(move, 'from')
            fromPos = positions[fromPos]
            move.fromPos = fromPos
            getattr(fromPos, token).append(move)
            if token == 'transition':
                toPos = get_singleton_attr(move, 'to')
                toPos = positions[toPos]
                move.toPos = toPos
                if not hasattr(move, 'title'):
                    move.title = 'Transition to %s' % toPos.id
                else:
                    move.title = move.title[0]
            else:
                if not hasattr(move, 'title'):
                    move.title = '%s submission' % move.type[0]
                else:
                    move.title = move.title[0]
            move.id = len(moves)
            moves.append(move)

    for k,v in positions.items(): # link each position to its opponent position
        opponent = switch_role(k)
        try:
            v.opponent = positions[opponent]
        except KeyError:
            pass

    return positions, moves


