from openrec.tf1.legacy.modules import Module

class Extraction(Module):
    
    """
    A direct inheritance of the Module.
    """

    def __init__(self, train=True, l2_reg=None, scope=None, reuse=False):

        super(Extraction, self).__init__(train=train, l2_reg=l2_reg, scope=scope, reuse=reuse)