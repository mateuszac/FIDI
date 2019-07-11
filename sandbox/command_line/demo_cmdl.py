import argparse
import numpy


class DemoCmdl(object):
    """Manage demo of showing command line parsing"""
    def __init__(self):
        self.parser = self.setup_cmdline_parser()
        self.args = self.parser.parse_args()

    def setup_cmdline_parser(self):
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

    def run(self):
        """Run demonstration of generating simple mesh model"""
        nodes = numpy.array(range(self.args.nodes_count))
        print('Nodes: ', nodes)


if __name__ == '__main__':
    demo = DemoCmdl()
    demo.run()
