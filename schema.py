import parse

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
    def __init__(self, node, **kwargs):
        if len(node.tokens) > 1:            
            self.name = node.tokens[1]
            if 'title' not in kwargs:
                self.title = self.name
        self.node = node
        self.__dict__.update(kwargs)
        self.text = ''.join(getattr(node, 'text', ())) # convert list to string



def init_graph(forest):
    d = parse.index_rust(forest)
    positions = {}
    moves = []
    for tree in forest:
        for node in tree.walk():
            token = node.tokens[0][1:-1]
            if token == 'position': # create A and D roles for this position
                metadata = node.metadata_dict()
                name = node.tokens[1]
                pos = MoveBase(node, role='A', **metadata)
                pos.id = name + ':A'
                positions[pos.id] = pos
                pos = MoveBase(node, role='D', **metadata)
                pos.id = name + ':D'
                positions[pos.id] = pos
                
            elif token == 'transition' or token == 'submission':
                metadata = node.metadata_dict()
                node.child_dict(metadata)
                move = MoveBase(node, **metadata)
                fromPos = get_singleton_attr(move, 'from')
                fromPos = positions[fromPos]
                move.fromPos = fromPos
                try:
                    getattr(fromPos, token).append(move)
                except AttributeError:
                    setattr(fromPos, token, [move])
                if token == 'transition':
                    toPos = get_singleton_attr(move, 'to')
                    toPos = positions[toPos]
                    move.toPos = toPos
                    if not hasattr(move, 'title'):
                        move.title = 'Transition to %s' % toPos.id
                else:
                    if not hasattr(move, 'title'):
                        move.title = '%s submission' % move.type[0]
                move.id = len(moves)
                moves.append(move)

    return positions, moves


