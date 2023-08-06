#!python
"""
CCMetagen main script

@ V.R.Marcelino
Created on Wed Jul 25 17:13:10 2018

"""


import sys
import subprocess
import re
import argparse


import pandas as pd
from ete3 import NCBITaxa


from ccmetagen import fParseKMA
from ccmetagen import version

class TaxThresholdsSettings:
    """Struct like approach to keep threshold settings sane. The tx prefix
       is required since attributes may clash with Python keywords."""
    def __init__(self, args):
      self.txspecies = 0.0 if args.turn_off_sim_thresholdsoff else args.species_threshold
      self.txgenus = 0.0 if args.turn_off_sim_thresholdsoff else args.genus_threshold
      self.txfamily = 0.0 if args.turn_off_sim_thresholdsoff else args.family_threshold
      self.txorder = 0.0 if args.turn_off_sim_thresholdsoff else args.order_threshold
      self.txclass = 0.0 if args.turn_off_sim_thresholdsoff else args.class_threshold
      self.txphylum = 0.0 if args.turn_off_sim_thresholdsoff else args.phylum_threshold

if len(sys.argv) == 1:
    sys.exit("CCMetagen - Identify species in metagenome datasets \nv{0}\n \
             \rTo be used with KMA\n\nUsage: CCMetagen.py <options>\n\n\
             Ex: CCMetagen.py -i KMA_out/2_mtg.res -o 2_mtg_result \n\n\
            For more help and options type: CCMetagen.py -h \n\
            When running CCMetagen on multiple files in a folder:\n\n\
             input_dir=KMA_out \n\
             output_dir=CCMetagen_results\n\
             mkdir $output_dir \n\
             for f in $input_dir/\*.res; do \n\
               out={1}\n\
               CCMetagen.py -i $f -o $out\n\
             done\n".format(version.get_version(), "$output_dir/${f/$input_dir/}"))

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode',
                    default='both',
                    required=False,
                    help="""what do you want CCMetagen to do?
                    Valid options are 'visual', 'text' or 'both':
                        text: parses kma, filters based on quality and output a text file with taxonomic information and detailed mapping information
                        visual: parses kma, filters based on quality and output a simplified text file and a krona html file for visualization
                        both: outputs both text and visual file formats. Default = both""")
parser.add_argument('-i', '--res_fp',
                    help='Path to the KMA result (.res file)',
                    required=True)
parser.add_argument('-o', '--output_fp',
                    default='CCMetagen_out',
                    required=False,
                    help='Path to the output file. Default = CCMetagen_out')
parser.add_argument('-r', '--reference_database',
                    default='nt',
                    required=False,
                    help='Which reference database was used. Options: UNITE, RefSeq or nt. Default = nt')
parser.add_argument('-du', '--depth_unit',
                    default='kma',
                    required=False,
                    help="""Desired unit for Depth(abundance) measurements.
                    Default = kma (KMA default depth, which is the number of nucleotides overlapping each template,
                    divided by the lengh of the template).
                    Alternatively, you can have abundance calculated in Reads Per Million (RPM, option 'rpm'), or
                    simply count the number of nucleotides overlaping the template (option 'nc').
                    If you use the 'nc' or 'rpm' options, remember to change the default --depth parameter accordingly.
                    Valid options are nc, rpm and kma""")
parser.add_argument('-map', '--mapstat',
                    required=False,
                    help="""Path to the mapstat file produced with KMA when using the -ef flag (.mapstat).
                            Required when calculating abundances in RPM.""")
parser.add_argument('-d', '--depth',
                    type=float,
                    default=0.2,
                    required=False,
                    help="""minimum sequencing depth. Default = 0.2.
                    If you use --depth_unit nc, change this accordingly. For example, -d 200 (200 nucleotides)
                    is similar to -d 0.2 when using the default '--depth_unit kma' option.""")
parser.add_argument('-c', '--coverage',
                    type=float,
                    default=20,
                    required=False,
                    help='Minimum coverage. Default = 20')
parser.add_argument('-q', '--query_identity',
                    type=float,
                    default=50,
                    required=False,
                    help='Minimum query identity (Phylum level). Default = 50')
parser.add_argument('-p', '--pvalue',
                    type=float,
                    default=0.05,
                    required=False,
                    help='Minimum p-value. Default = 0.05.')

# similarity thresholds:
parser.add_argument('-st', '--species_threshold',
                    type=float,
                    default=98.41,
                    required=False,
                    help='Species-level similarity threshold. Default = 98.41')
parser.add_argument('-gt', '--genus_threshold',
                    type=float,
                    default=96.31,
                    required=False,
                    help='Genus-level similarity threshold. Default = 96.31')
parser.add_argument('-ft', '--family_threshold',
                    type=float,
                    default=88.51,
                    required=False,
                    help='Family-level similarity threshold. Default = 88.51')
parser.add_argument('-ot', '--order_threshold',
                    type=float,
                    default=81.21,
                    required=False,
                    help='Order-level similarity threshold. Default = 81.21')
parser.add_argument('-ct', '--class_threshold',
                    type=float,
                    default=80.91,
                    required=False,
                    help='Class-level similarity threshold. Default = 80.91')
parser.add_argument('-pt', '--phylum_threshold',
                    type=float,
                    default=0.0,
                    required=False,
                    help='Phylum-level similarity threshold. Default = 0 - not applied')
parser.add_argument('-off', '--turn_off_sim_thresholds',
                    action='store_true',
                    default=False,
                    required=False,
                    help='Turns simularity-based filtering off. Options = y or n. Default = n')
parser.add_argument('--dev',
                    action='store_true',
                    default=False,
                    required=False,
                    help='Set parameters for development and debugging. Do not use for analysis')

parser.add_argument('--version', action='version', version=version.get_version())
args = parser.parse_args()

# taxononomic thresholds:
tts = TaxThresholdsSettings(args)

# developing and debugging:
if args.dev:
  print("Warning: using debugging options!")
  args.output_fp = "CCMetagen_nt_results"
  args.res_fp = "KMA_res/1_mtt_nt.res"
  args.mapstat = "KMA_res/1_mtt_nt.mapstat" # make a way of finding this automatically?? Flag -mapstat?
  args.reference_database = "nt"
  args.mode = 'both'
  args.coverage = 20
  args.query_identity = 50
  args.depth = 0.2
  args.pvalue = 0.05
  args.depth_unit = 'kma'
  tts.txspecies = 99
  tts.txgenus = 98
  tts.txfamily = 95
  tts.txorder = 80
  tts.txclass = 0
  tts.txphylum = 0


##### Checks:
# Run implicitly ete3.NCBITaxa.__init__() to check for valid taxonomy database
NCBITaxa()

# Warning if RefDatabase is unknown
if args.reference_database not in ("UNITE", "RefSeq", "nt"):
    sys.exit("""Reference database (-r) must be either UNITE, RefSeq or nt.
                the input is case sensitive and the default is nt. Try again.""")

##### Read input files and output a pandas dataframe
print("\"\nReading file {} \n\"".format(args.res_fp))
df = pd.read_csv(args.res_fp, sep='\t', index_col=0, encoding='latin1')

# Rename headers:
df.index.name = "Closest_match"

##### Adjust depth to reflect number of bases or RPM if needed:
# number of nucleotides:

#if du == 'nc':
if args.depth_unit == 'nc':
    print("Calculating depth as number of nucleotides, ignoring template length.")
    print("""Remember to adjust minimum depth value (ex: -d 200) to filter low abundance hits.""")
    df['Depth'] = df.Depth * df.Template_length
elif args.depth_unit == 'rpm':
    print("""
           Calculating RPM...
           Note 1: to calculate RPM, you need to generate the mapstat file when
           running KMA (flag -ef), and use it as input in CCMetagen (flag --mapstat).

           Note 2: you might want to adjust the minimum depth (-d) value accordingly.
           The default minimum depth is 0.2.
           """)
    with open(args.mapstat) as mapfile:
        fragments_line = mapfile.readlines()[3]
    total_frags = re.split(r'(\t|\n)',fragments_line)[2]
    df_stats = pd.read_csv(args.mapstat, sep='\t', index_col=0, header=6, encoding='latin1')
    df['Depth'] = 1000000 * df_stats['fragmentCount'] / int(total_frags)
else:
  if args.depth_unit != 'kma':
    print("""Warning: the depth unit you specified makes no sense.
           --depth_unit option must be nc, rpm, or kma. Using 'kma'.""")

##### Quality control + taxonomic assignments

# quality filter (coverage, query identity, Depth and p-value)
df = fParseKMA.res_filter(df, args.reference_database, args.coverage,
                              args.query_identity, args.depth, args.pvalue)

# add tax info
df = fParseKMA.populate_w_tax(df, args.reference_database, tts)

##### Output a file with tax info
if args.mode in ('text', 'both'):
    # save to file
    out = args.output_fp + ".csv"
    pd.DataFrame.to_csv(df, out)
    print("csv file saved as {}".format(out))

##### Output a Krona file
if args.mode in ('visual', 'both'):
    krona_info = df[['Depth', 'Superkingdom', 'Kingdom', 'Phylum', 'Class',
                     'Order', 'Family', 'Genus', 'Species']]

    # remove the unk_xx for better krona representation
    krona_info = krona_info.replace('unk_.*$', value='',regex=True)

    # save dataframe to file
    out1 = args.output_fp + ".tsv"
    pd.DataFrame.to_csv(krona_info, out1, sep='\t', index=False, header=False)

    # save krona file
    out2 = args.output_fp + ".html"
    subprocess.run(["ktImportText", out1, "-o ", out2], shell=True)
    print("krona file saved as {}".format(out2))
