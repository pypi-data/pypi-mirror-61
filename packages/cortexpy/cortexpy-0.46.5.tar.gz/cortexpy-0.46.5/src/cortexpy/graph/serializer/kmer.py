import struct

import attr

from cortexpy.graph.parser.header import Header
from cortexpy.graph.parser.kmer import calc_kmer_container_size


@attr.s(slots=True)
class ColorInformationBlock(object):
    is_clipped = attr.ib(False)
    are_low_cov_unitigs_removed = attr.ib(False)
    are_low_cov_kmers_removed = attr.ib(False)
    is_cleaned_against_another_graph = attr.ib(False)
    cov_threshold_on_unitigs = attr.ib(0)
    cov_threshold_on_kmers = attr.ib(0)
    name_of_graph_cleaned_against = attr.ib(b'')

    def dump(self, buffer):
        assert isinstance(self.name_of_graph_cleaned_against, bytes)
        string_length = len(self.name_of_graph_cleaned_against)
        binary = struct.pack('4?3I',
                             self.is_clipped,
                             self.are_low_cov_unitigs_removed,
                             self.are_low_cov_kmers_removed,
                             self.is_cleaned_against_another_graph,
                             self.cov_threshold_on_unitigs,
                             self.cov_threshold_on_kmers,
                             string_length)
        buffer.write(binary)
        buffer.write(self.name_of_graph_cleaned_against)


def dump_colored_de_bruijn_graph_to_cortex(graph, output_fh):
    Kmers(keys=list(graph.nodes()),
          val_callable=lambda k: graph.node[k],
          sample_names=graph.graph['sample_names'],
          kmer_size=graph.graph['kmer_size'],
          num_colors=graph.graph['num_colors']) \
        .dump(output_fh)


@attr.s(slots=True)
class Kmers(object):
    """Serializes kmers to cortex binary format"""
    keys = attr.ib()
    val_callable = attr.ib()
    sample_names = attr.ib()
    kmer_size = attr.ib()
    num_colors = attr.ib()
    kmer_container_size = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.kmer_container_size = calc_kmer_container_size(self.kmer_size)
        self.keys = sorted(self.keys)

    @property
    def n_kmers(self):
        return len(self.keys)

    @property
    def header(self):
        color_info_blocks = [ColorInformationBlock() for _ in range(self.num_colors)]
        return Header(kmer_size=self.kmer_size,
                      kmer_container_size=self.kmer_container_size,
                      num_colors=self.num_colors,
                      sample_names=self.sample_names,
                      color_info_blocks=color_info_blocks)

    def dump(self, buffer):
        """to a filehandle"""
        self.header.dump(buffer)
        for kmer_string in self.keys:
            self.val_callable(kmer_string).dump(buffer)
