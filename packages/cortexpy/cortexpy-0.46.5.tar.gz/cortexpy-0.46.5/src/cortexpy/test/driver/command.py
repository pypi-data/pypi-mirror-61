import json
import os
import sys
from pathlib import Path

import Bio
import attr
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from cortexpy.graph.cortex import CortexDiGraph
from cortexpy.graph.parser.random_access import RandomAccess
from cortexpy.test import builder, expectation
from cortexpy.test import runner
from cortexpy.test.builder.mccortex import MccortexLinks

if os.environ.get('CI'):
    SPAWN_PROCESS = True
else:
    SPAWN_PROCESS = False


@attr.s(slots=True)
class Assemble(object):
    tmpdir = attr.ib()
    initial_seqs = attr.ib(attr.Factory(list))
    mccortex_builder = attr.ib(attr.Factory(builder.Mccortex))

    def with_records(self, *records):
        for rec in records:
            self.mccortex_builder.with_dna_sequence(rec)
        return self

    def with_dna_sequence(self, sequence, **kwargs):
        self.mccortex_builder.with_dna_sequence(sequence, **kwargs)
        return self

    def with_initial_sequences(self, *seqs):
        self.initial_seqs = seqs
        return self

    def with_kmer_size(self, size):
        self.mccortex_builder.with_kmer_size(size)
        return self

    def run(self):
        inital_seq_fasta = self.tmpdir / 'initial_seqs.fasta'
        initial_seqs = [SeqRecord(Seq(rec), id=str(idx)) for idx, rec in
                        enumerate(self.initial_seqs)]
        SeqIO.write(initial_seqs, str(inital_seq_fasta), "fasta")
        output_graph = self.mccortex_builder.build(self.tmpdir)
        output = self.tmpdir / 'output.fa'

        completed_process = runner.Cortexpy(SPAWN_PROCESS).assemble(graph=output_graph,
                                                                    initial_seqs=inital_seq_fasta,
                                                                    out=output)

        assert completed_process.returncode == 0, completed_process
        return expectation.Fasta(open(output, 'r').read())


@attr.s(slots=True)
class Prune(object):
    tmpdir = attr.ib()
    mccortex_builder = attr.ib(attr.Factory(builder.Mccortex))
    min_tip_length = attr.ib(None)
    records = attr.ib(attr.Factory(list))
    kmer_size = attr.ib(None)

    def with_records(self, *records):
        for rec in records:
            self.mccortex_builder.with_dna_sequence(rec)
            self.records.append(SeqRecord(Seq(rec)))
        return self

    def prune_tips_less_than(self, n):
        self.min_tip_length = n
        return self

    def with_kmer_size(self, size):
        self.mccortex_builder.with_kmer_size(size)
        self.kmer_size = size
        return self

    def run(self):
        mccortex_graph = self.mccortex_builder.build(self.tmpdir)

        contig_fasta = self.tmpdir / 'initial_contigs.fa'
        with open(str(contig_fasta), 'w') as fh:
            SeqIO.write(self.records, fh, 'fasta')
        ctp_runner = runner.Cortexpy(SPAWN_PROCESS)
        pruned_graph = Path(str(mccortex_graph)).with_suffix('.pruned.ctx')
        completed_process = ctp_runner.prune(graph=mccortex_graph, out=pruned_graph,
                                             remove_tips=self.min_tip_length, verbose=True)

        assert completed_process.returncode == 0, completed_process
        print(completed_process.stdout)
        print(completed_process.stderr, file=sys.stderr)

        return expectation.graph.KmerGraphExpectation(load_cortex_graph(pruned_graph))


@attr.s(slots=True)
class Subgraph(object):
    """Driver for subgraph acceptance tests"""
    tmpdir = attr.ib()
    mccortex_builder_factory = builder.mccortex.MccortexGraphLinks
    mccortex_builder = attr.ib(None)
    mccortex_builders = attr.ib(attr.Factory(list))
    traversal_contigs = attr.ib(None)
    added_records = attr.ib(attr.Factory(list))
    output_subgraphs = attr.ib(False)
    traversal = attr.ib(init=False)
    colors = attr.ib(None)
    spawn_process = attr.ib(None)
    verbose = attr.ib(False)
    silent = attr.ib(False)
    logging_interval_seconds = attr.ib(0)
    kmer_size = attr.ib(None)

    def __attrs_post_init__(self):
        if self.mccortex_builder is None:
            self.mccortex_builder = self.mccortex_builder_factory()

    def with_record(self, record, name=None):
        if name:
            self.mccortex_builder.with_dna_sequence(record, name=name)
        else:
            self.mccortex_builder.with_dna_sequence(record)
        self.added_records.append(record)

    def with_records(self, *records, names=None):
        if names:
            assert len(records) == len(names)
        else:
            names = ['sample_0' for _ in records]
        for rec, name in zip(records, names):
            self.mccortex_builder.with_dna_sequence(rec, name=name)
            self.added_records.append(rec)
        return self

    def with_initial_contigs(self, *contigs):
        self.traversal_contigs = contigs

    def with_subgraph_output(self):
        assert False
        self.output_subgraphs = True
        return self

    def with_kmer_size(self, size):
        self.kmer_size = size
        return self

    def with_verbose_arg(self):
        self.verbose = True
        return self

    def with_logging_interval(self, seconds):
        self.logging_interval_seconds = seconds
        return self

    def with_silent_arg(self):
        self.silent = True
        return self

    def without_traversal_colors(self):
        self.colors = None

    def with_traversal_colors(self, *colors):
        self.colors = colors
        return self

    def with_extra_graph(self):
        self.mccortex_builders.append(self.mccortex_builder)
        self.mccortex_builder = self.mccortex_builder_factory()
        return self

    def _write_contig_fasta(self):
        contig_fasta = self.tmpdir / 'cortexpy_initial_contigs.fa'
        if self.traversal_contigs:
            initial_contigs = self.traversal_contigs
        else:
            initial_contigs = self.added_records
        Bio.SeqIO.write(
            [SeqRecord(Seq(s), id=f'{i}', description='') for i, s in enumerate(initial_contigs)],
            str(contig_fasta), 'fasta'
        )
        return contig_fasta

    def _run(self):
        mccortex_graphs = []
        self.mccortex_builders.append(self.mccortex_builder)
        for idx, mc_builder in enumerate(self.mccortex_builders):
            mc_builder.with_kmer_size(self.kmer_size)
            builder_dir = self.tmpdir / 'mc_graph_{}'.format(idx)
            builder_dir.mkdir()
            mc_graph, _ = mc_builder.build(builder_dir)
            mccortex_graphs.append(mc_graph)

        contig_fasta = self._write_contig_fasta()

        self.traversal = self.tmpdir / 'traversal.ctx'
        if self.spawn_process is None:
            ctp_runner = runner.Cortexpy(SPAWN_PROCESS)
        else:
            ctp_runner = runner.Cortexpy(self.spawn_process)
        return ctp_runner.subgraph(graphs=mccortex_graphs,
                                   out=self.traversal,
                                   contig=contig_fasta,
                                   contig_fasta=True,
                                   verbose=self.verbose,
                                   silent=self.silent,
                                   colors=self.colors,
                                   logging_interval=self.logging_interval_seconds)

    def run_for_stderr(self):
        self.spawn_process = True
        completed_process = self._run()
        print(completed_process.stdout)
        return completed_process.stderr

    def run(self):
        completed_process = self._run()

        assert completed_process.returncode == 0, completed_process

        return expectation.graph.KmerGraphExpectation(load_cortex_graph(self.traversal))


@attr.s(slots=True)
class TraverseDriver(object):
    """Driver for traversal acceptance tests"""
    tmpdir = attr.ib()
    to_json = attr.ib(False)
    subgraphs = attr.ib(False)
    seed_strings = attr.ib(None)
    graph_index = attr.ib(None)
    extra_start_kmer = attr.ib(None)
    traverse_driver = attr.ib(init=False)
    link_builder = attr.ib(attr.Factory(MccortexLinks))

    def __attrs_post_init__(self):
        self.traverse_driver = Subgraph(self.tmpdir)

    def __getattr__(self, name):
        """Let's delegate most of our responsibilities to the driver"""
        delegate = [s.strip() for s in """with_record
        with_records
        with_kmer_size
        with_initial_contigs
        with_traversal_colors""".split('\n')]
        if name in delegate:
            return getattr(self.traverse_driver, name)
        raise NotImplementedError(f'Could not find attribute {name}')

    def with_sample_records(self, *records):
        self.with_records(*records, names=['sample_{}'.format(i) for i in range(3)])
        return self

    def with_subgraph_traversal(self):
        self.traverse_driver.with_subgraph_output()
        return self

    def with_json_output(self):
        self.to_json = True
        return self

    def with_seed_strings(self, *strings):
        self.seed_strings = strings
        return self

    def with_subgraph_view(self):
        self.subgraphs = True
        self.with_subgraph_traversal()
        return self

    def with_graph_index(self, idx):
        self.graph_index = idx
        return self

    def with_extra_start_kmer(self, kmer):
        self.extra_start_kmer = kmer
        return self

    def with_link_records(self, *records):
        self.link_builder.with_link_dna_sequences(*records)
        return self

    def run(self):
        self.traverse_driver.run()
        if self.subgraphs:
            assert self.to_json
            out_prefix = Path(str(self.tmpdir)) / 'subgraphs'
        else:
            out_prefix = None

        links = self.link_builder.build(self.tmpdir, self.traverse_driver.traversal)

        ret = runner.Cortexpy(SPAWN_PROCESS).traverse(
            self.traverse_driver.traversal,
            to_json=self.to_json,
            contig=self.seed_strings,
            graph_index=self.graph_index,
            extra_start_kmer=self.extra_start_kmer,
            links_file=links
        )
        print(ret.stdout)
        print(ret.stderr, file=sys.stderr)
        assert ret.returncode == 0, ret
        if self.to_json:
            if self.subgraphs:
                return expectation.JsonGraphs(
                    list(out_prefix.parent.glob(out_prefix.name + '*')))
            else:
                return expectation.JsonGraph(json.loads(ret.stdout))
        return expectation.Fasta(ret.stdout)


def load_cortex_graph(path):
    return CortexDiGraph(RandomAccess(open(str(path), 'rb')))
