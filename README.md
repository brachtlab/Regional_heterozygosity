# Regional_heterozygosity
Repository of custom python scripts used in "Regional sequence expansion or collapse in heterozygous genome assemblies", Asalone et al. 2020.

blast_analysis.py can create a file with a new percent identity cut off from a previous BLAST output. Can also be used to determine the percent missing from query fasta based on matches:
./blast_analysis.py <query fasta> <blast_to_reference_outfmt6.txt> <percent identity to consider, as integer (like '98' for 98 %)>


extract_regions.py extracts defined regions (regions_to_extract_file.txt) from assembly of interest:
./extract_regions.py <genome.fasta> <regions_to_extract_file.txt>


get_protein_stats.py calculates the standard deviation, mean, and median protein lengths for proteins with and without evidence. Will also perform a t-test to obtain the t-statistic and p-value comparing the protein lengths of evidence vs no-evidence proteins:
./get_protein_stats.py <*.all.maker.proteins.fasta> <output file prefix>


get_regional_depth2.py extracts regional depth and records length covered from Alternate assembly:
./get_regional_depth2.py <genome_gene_coordinates_file> <depthfile.txt>
#note, depthfile is output by Samtools Depth command#


get_regional_heterozygosity.py analyzes the output of parse_genes2.py:
./get_regional_heterozygosity.py <output_from_parse_genes2.py> <vcf_file>


get_total_reference_depth2.py outputs the total depth for the reference assembly:
./get_total_reference_depth2.py <genome_coordinates_file> <depthfile.txt>
#note, depthfile is output by Samtools Depth command#


getN50.py is used to obtain the N50 of an assembly along with the length of the shortest contig, longest contig, total genome, and number of contigs in the assembly:
./getN50.py <genome.fasta>


getRef.py creates a file with BLAST output outformat 6 lines where the reference is the query: 
getRef.py <outfmt 6> 


parse_genes2.py produces the genomic locations from the assembly:
./parse_genes2.py <PANTHER_enrichment_file_for_GO_category> <PantherScore_generic_mapping_file> <genome_gene_coordinates_file>


parseOrthoMCL.py extracts position of matches to the reference proteins from the all-vs-all BLAST for OrthoMCL:
./parseOrthoMCL.py <output from getRef.py>


ref_len_covered_fixed.py extracts the length covered from the Reference assembly: 
./ref_len_covered_fixed.py <query.fasta> <blast-to-reference-outfmt6.txt> 
 #NOTE query.fasta comes from extract_regions.py in heterozygosity pipeline#


reference_get_regional_depth2.py extracts regional depth for the Reference assembly:
./reference_get_regional_depth2.py <blast-to-reference-outfmt6.txt> <reference_depthfile.txt>
#note, depthfile is output by Samtools Depth command#


reference_get_regional_heterozygosity.py calculates the regional heterozygosity of the reference assembly for region defined from the Alternative assembly:
./reference_get_regional_heterozygosity.py <outfmt6 from blast of subject assembly to omega> <vcf>


rm_blast_redundancy.py removes duplicate hits from BLAST outformat 6 output:
./rm_blast_redundancy.py <output from blast in outfmt 6>



****for heterozygosity****

Heterozygosity analysis for Reference assembly:

parse_genes2.py —> extract_regions.py —> blastn against reference assembly, 98% identity as pid cutoff, outfmt 6 —> reference_get_regional_heterozygosity.py


Heterozygosity analysis for Alternate genome assembly:

parse_genes2.py -> get_regional_heterozygosity.py



****for depth of coverage****

for Alternate assembly depth: use get_regional_depth2.py 

for Reference assembly depth: use reference_get_regional_depth2.py 



****for length of coverage****

For Alternate assemblies, get_regional_depth2.py records lengths covered

For Reference lengths, run ref_len_covered_fixed.py 

****for OrthoMCL analysis of fragmentation vs duplication****

Start with OrthoMCL's all-vs-all non-redundant tabular blast output. getRef.py is used to extract only the lines whose query starts with 'ref' for reference. This creates a new blast output file which is used for the next step.

The analysis of the reference-query-only OrthoMCL tabular blast output is conducted with parseOrthoMCL.py <reference-only-blast-output> and generates a text file listing the relative contribution of duplications, fragmentations and correct matches from each assembly relative to reference proteins. It automatically discounts paralogy by looking for non-self reference matches.




