from urllib.request import urlretrieve
import gzip
import shutil
from math import floor

HG19_FASTA_URL = 'http://ftp.ensembl.org/pub/release-75/fasta/homo_sapiens/dna/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa.gz'
HG38_FASTA_URL = 'http://ftp.ensembl.org/pub/release-85/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz'

def print_download_progress(x, y, z):
    if floor(x*y*100/z) - floor((x-1)*y*100/z) >= 1:
        print("Download progress: {}%".format(floor(x*y*100/z)))

# Rules
rule genomes_human_all:
    input:
        config['output']['hg19'],
        config['output']['hg38']

rule genomes_human_hg19_extract:
    input:
        config['output']['hg19'] + '.gz'
    output:
        config['output']['hg19']
    run:
        with gzip.open(config['output']['hg19'] + '.gz', 'rb') as f_in:
            with open(config['output']['hg19'], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

rule genomes_human_hg38_extract:
    input:
        config['output']['hg38'] + '.gz'
    output:
        config['output']['hg38']
    run:
        with gzip.open(config['output']['hg38'] + '.gz', 'rb') as f_in:
            with open(config['output']['hg38'], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

rule genomes_human_hg19_download:
    output:
        config['output']['hg19'] + '.gz'
    run:
        urlretrieve(
            HG19_FASTA_URL, 
            config['output']['hg19'] + '.gz', 
            reporthook=print_download_progress
        )

rule genomes_human_hg38_download:
    output:
        config['output']['hg38'] + '.gz'
    run:
        urlretrieve(
            HG38_FASTA_URL, 
            config['output']['hg38'] + '.gz', 
            reporthook=print_download_progress
        )