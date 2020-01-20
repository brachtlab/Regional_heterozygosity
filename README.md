# Regional_heterozygosity
Repository of custom python scripts used in "Regional sequence expansion or collapse in heterozygous genome assemblies", Asalone et al. 2020.

****for heterozygosity****

For Alternate genome assembly:

./parse_genes2.py <PANTHER_enrichment_file_for_GO_category> <PantherScore_generic_mapping_file> <genome_gene_coordinates_file>

parse_genes2.py produces the genomic locations from the assembly for analysis with:

./get_regional_heterozygosity.py <output_from_parse_genes2.py> <vcf_file>

 
for Reference assembly:

parse_genes2.py —>extract_regions.py—>blastn against reference assembly, 98% identity as pid cutoff, outfmt 6—>
—>reference_get_regional_heterozygosity.py <outfmt 6> <creference.vcf>


****for depth of coverage****

for Alternate assembly depth: use ./get_regional_depth2.py <genome_gene_coordinates_file> <depthfile.txt>
#note, depthfile is output by Samtools Depth command#

for Reference assembly depth: ./reference_get_regional_depth2.py <blast-to-reference-outfmt6.txt> <reference_depthfile.txt>
#note, depthfile is output by Samtools Depth command#

****for length of coverage****

For Alternate assemblies, get_regional_depth2.py records lengths covered

for Reference lengths:

run ./ref_len_covered_fixed.py <query.fasta> <blast-to-reference-outfmt6.txt> 
 #NOTE query.fasta comes from extract_regions.py in heterozygosity pipeline#

