import argparse
import numpy

class DemoCmdl(object):
    """Manage demo of of showin command line parsing"""
    def __init__(self):
        self.parser = self.SetupCmdlineParser()
        self.args = self.parser.parse_args()

    def SetupCmdlineParser(self):
        """Create parser for command line arguments"""
        parser = argparse.ArgumentParser(description=
           'Demonstrate building and saving mesh for rectangle')
        parser.add_argument('--nodes',
                        dest='nodes_count',
                        default=5,
                        type=int,
                        help='Number of nodes'
                       )
        return parser

    def Run(self):
        """Run demonstration of generaging simple mesh model"""
        nodes = numpy.array(range(self.args.nodes_count))
        print('Nodes: ', nodes)

if __name__ == '__main__':
    demo = DemoCmdl()
    demo.Run()
