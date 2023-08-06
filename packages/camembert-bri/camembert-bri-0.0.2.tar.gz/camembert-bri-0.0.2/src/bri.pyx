#cython: language_level=3

import os

from pysam import AlignmentFile

__all__ = ['Bri', 'bench']

"""
    Expose bare minimum from jts/bri headers
"""
cdef extern from "bri_index.h":
    struct bam_read_idx_record:
        size_t file_offset

    struct bam_read_idx:
        bam_read_idx_record* records

    bam_read_idx*bam_read_idx_load(const char* input_bam)
    void bam_read_idx_build(const char* input_bam)
    void bam_read_idx_destroy(bam_read_idx* bri)

cdef extern from "bri_get.h":
    void bam_read_idx_get_range(const bam_read_idx* bri,
                                const char* readname,
                                bam_read_idx_record** start,
                                bam_read_idx_record** end)

cdef extern from "bri_benchmark.h":
    int bam_read_idx_benchmark_main(int argc, char** argv)

def bench(input_bam):
    bam_read_idx_benchmark_main(2, ['benchmark', input_bam.encode('utf-8')])

cdef class Bri:
    """ Wrapper class for Jared's bri, supports creating and reading .bri index and extracting reads using pysam

    Attributes:
        index (bam_read_idx*): Bri index instance
        input_bam_path (bytes): Path to bam file
        input_bri_path (bytes): Path to bri file
        hts (pysam.AlignmentFile): Bam file instance
    """
    cdef:
        bam_read_idx*index
        object hts
        bytes input_bam_path
        bytes input_bri_path

    def __init__(self, input_bam):
        """
        Args:
            input_bam (str): Path to .bam file
        """
        self.input_bam_path = input_bam.encode('utf-8')
        self.input_bri_path = (input_bam + '.bri').encode('utf-8')

        if not os.path.exists(self.input_bam_path):
            raise IOError("Bam file does not exist")

    def create(self):
        """ Create bri index for bam file by calling bam_read_idx_build and bam_read_idx_save. Index is immediately
        destroyed, call load() after this to recycle this object.
        """
        bam_read_idx_build(self.input_bam_path)

    # noinspection PyAttributeOutsideInit
    def load(self):
        """ Load the index from .bri file """
        if not os.path.exists(self.input_bri_path):
            # Avoid exit() calls in bri_index.c
            raise IOError("Bri file does not exist")

        self.index = bam_read_idx_load(self.input_bam_path)  # load .bri index
        self.hts = AlignmentFile(self.input_bam_path, 'rb')  # load .bam file

    def get(self, read_name):
        """ Get reads for read_name from the bam file using .bri index
        Args:
            read_name (str): Reads to search for
        Yields:
            pysam.AlignedSegment: found reads
        """
        if not self.index:
            raise ValueError('Bri index is not loaded, call load() function first')

        cdef:
            bam_read_idx_record*start
            bam_read_idx_record*end

        bam_read_idx_get_range(self.index, read_name.encode('utf-8'), &start, &end)

        hts_iter = iter(self.hts)

        while start != end:
            self.hts.seek(start.file_offset)
            read = next(hts_iter)
            yield read
            start += 1

    def __dealloc__(self):
        """ Proper cleanup """
        if self.index:
            bam_read_idx_destroy(self.index)
        if self.hts:
            self.hts.close()
