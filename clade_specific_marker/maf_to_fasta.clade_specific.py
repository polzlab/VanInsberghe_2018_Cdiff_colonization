#This script converts a .maf file to a fasta formatted alignment, INCLUDING
#all blocks not shared by all genomes in the alignment, but shared by two or
#more genomes
project_dir = "/nobackup1b/users/davevan/Cdiff_genomics/BA1801/ch_align/"
contig_dir = "/nobackup1b/users/davevan/Cdiff_genomics/reAMPHORA/genome/"
contig_extension = ".fa"
output_prefix = "ATCC"
strain_list_file = "strain_names.txt"

include_filename = "include.txt"
exclude_filename = "exclude.txt"

input_dir = project_dir+output_prefix+"_align/"
alignment_dir = input_dir+"alignment_blocks/"

ref_iso = 'random'
ref_contig = 'random'

len_block_threshold = 500
gap_prop_thresh = 0.5

slurm_prefix = "#!/bin/bash\n#SBATCH -N 1#SBATCH -n 1\n#SBATCH -p sched_mit_chisholm,sched_mit_hill,newnodes\n#SBATCH --mem=8000\n#SBATCH --time=48:00:00\ncd "+project_dir+"\n"
#############   FUNCTIONS   #############
def poly_count(msa_dict,loc):
	nt_dict = {'A':0,'C':0,'G':0,'T':0}
	for seq in msa_dict:
		nt = msa_dict[seq][loc]
		if nt != "N":
			nt_dict[nt] += 1
	poly = 0
	for nt in nt_dict:
		count = nt_dict[nt]
		if count > 1:
			poly += 1
	return poly

def remove_N_only_gaps(msa_dict):
	nt_dict = {}#{'N':0,'-':0}
	for strain in msa_dict:
		seq = msa_dict[strain]
		for i in range(0,len(seq)):

			try:
				nt_dict[i]
			except:
				nt_dict[i] = {'N':0,'-':0,'nt':0}
			nt = seq[i]
			if nt == '-':
				nt_dict[i]['-'] += 1
			elif nt == 'N':
				nt_dict[i]['N'] += 1
			else:
				nt_dict[i]['nt'] += 1
	seq_num = len(msa_dict)
	remove_sites = []
	for nt in nt_dict:
		count = nt_dict[nt]
		if nt_dict[i]['nt'] <= 1:
			remove_sites.append(nt)
	out_dict = {}
	for strain in msa_dict:
		seq = msa_dict[strain]
		out_dict[strain] = ''
		for i in range(0,len(seq)):
			if i not in remove_sites:
				out_dict[strain] += seq[i]

	return out_dict
#################   MAIN   #################
import os
import sys
if os.path.isdir(alignment_dir) == False:
	os.makedirs(alignment_dir)


#make list of strains
infile = open(project_dir+strain_list_file,"r")
isolist = []
for line in infile:
	line = line.strip()
	#line = line + contig_extension
	line = line.replace("-","_")
	isolist.append(line)
infile.close()
# print(isolist)
infile = open(project_dir+include_filename,"r")
include_list = []
for line in infile:
	line = line.strip()
	#line = line + contig_extension
	line = line.replace("-","_")
	include_list.append(line)
infile.close()
infile = open(project_dir+exclude_filename,"r")
exclude_list = []
for line in infile:
	line = line.strip()
	#line = line + contig_extension
	line = line.replace("-","_")
	exclude_list.append(line)
infile.close()



num = 0
iso = ""
seqdict = {}
for iso in include_list:
	seqdict[iso] = ""
temp_seqdict = {}
lenseq = 0

ref_order = []

infile = open(input_dir+output_prefix+".maf","r")
temp_seq_list = []
label = 0
mult = 0
wr = 0 #swtich for writing
for line in infile:
	if line == "\n":
		for iso in isolist:
			if iso not in temp_seq_list and iso not in exclude_list:
				wr = 0
				#print(iso)
				break
			elif iso in temp_seq_list and iso in exclude_list:
				wr = 0
				#print(iso)
				break
			elif iso in temp_seq_list and iso in include_list:
				wr = 1
		if wr == 1:
			#print(label)
			for iso in include_list:
				seq = temp_seqdict[iso]
				try:
					seqdict[label][iso] = seq
				except:
					seqdict[label] = {}
					seqdict[label][iso] = seq
		temp_seq_list = []
	elif line[0] == 'a':
		line = line.strip()
		mult = int(line.split("mult=")[1])
		try:
			label = int(line.split(" mult=")[0].split("label=")[1])
		except:
			label = line.split(" mult=")[0].split("label=")[1]
	elif line[0] == 's':
		line = line.strip()
		iso = line.split(".")[0].split(" ")[1]
		contig = line.split(".")[1].split("\t")[0]
		seq = line.split(" ")[5]
		
		temp_seq_list.append(iso)
		temp_seqdict[iso] = seq
		lenseq = len(seq)
		
		if contig == ref_contig:
			start = int(line.split("\t")[2].split(" ")[0])
			length = int(line.split("\t")[2].split(" ")[1])
			direc = line.split("\t")[2].split(" ")[3]
			if direc != "+":
				start = start+length
			tup = (start,label)
			ref_order.append(tup)
		elif ref_contig == "random" and mult >1:
			tup = (label,label)
			ref_order.append(tup)
# print(ref_order)
ref_order = list(set(ref_order))
ref_order.sort()
# print(seqdict)

#remove sites that contain either only Ns, or sequence from a single genome
for label in seqdict:
	seqdict[label] = remove_N_only_gaps(seqdict[label])

#filter the alignment blocks to remove short blocks and blocks with high number
#of gaps, then remove all gap containing columns from the sequence alignments

label_sizes = {}
use_labels = []

for label in ref_order:
	start = label[0]
	label = label[1]
	try:
		ref_seq = seqdict[label][include_list[0]]
		len_ref_seq = len(ref_seq)
		gapless_ref_seq = ref_seq.replace("-","")
		len_gapless_ref_seq = len(gapless_ref_seq)
		gap_prop = float(len_gapless_ref_seq)/float(len_ref_seq)
		
		if len_gapless_ref_seq >= len_block_threshold:
			if gap_prop >= gap_prop_thresh:
				use_labels.append(label)
				label_sizes[label] = {}
				label_sizes[label]["raw"] = len_ref_seq
				label_sizes[label]["degap"] = len_gapless_ref_seq
				label_sizes[label]["SNPcount"] = 0
	except:
		pass

#make the no-gap and SNP location lists
a = 0
writedict = {}
snplist = {}
snpcount = 0
nt = []
for label in use_labels:
	snpcount = 0
	nt = []
	ref_seq = seqdict[label][include_list[0]]
	len_ref_seq = len(ref_seq)
	for i in range(0,len_ref_seq):
		a = 0
		nt = []
		for iso in include_list:
			resi = seqdict[label][iso][i]
			if resi == "-":
				a = 1
			else:
				nt.append(resi)
		if a == 0:
			nt = list(set(nt))
			try:
				writedict[label][i] = ""
			except:
				writedict[label] = {}
				writedict[label][i] = ""
			if len(nt) > 1:
				snpcount += 1
	label_sizes[label]["SNPcount"] = snpcount
	#print(str(label)+"\t"+str(snpcount))


print("Done finding gap-columns and counting SNPs")

degap_seqdict = {}
for label in use_labels:
	for j in range(0,len(include_list)):
		iso = include_list[j]
		seq = seqdict[label][iso]
		ref_seq = seqdict[label][include_list[0]]
		len_ref_seq = len(ref_seq)
		try:
			degap_seqdict[iso][label] = ""
			for k in range(0,len_ref_seq):
				try:
					st = writedict[label][k]
					degap_seqdict[iso][label] += seq[k]
				except:
					pass
		except:
			degap_seqdict[iso] = {}
			degap_seqdict[iso][label] = ""
			for k in range(0,len_ref_seq):
				try:
					st = writedict[label][k]
					degap_seqdict[iso][label] += seq[k]
				except:
					pass
print("Done removing gap-columns")
#re-iterate over the use_labels list
temp_use_labels = []
for label in use_labels:
	len_gapless_ref_seq = len(degap_seqdict[include_list[0]][label])
	len_ref_seq = len(seqdict[label][include_list[0]])
	gap_prop = float(len_gapless_ref_seq)/float(len_ref_seq)
	if len_gapless_ref_seq >= len_block_threshold and gap_prop >= gap_prop_thresh:
		label_sizes[label]["raw"] = len_ref_seq
		label_sizes[label]["degap"] = len_gapless_ref_seq
		temp_use_labels.append(label)
use_labels = list(set(temp_use_labels))
del temp_use_labels

#make the full, degapped sequences and write the start:stop location of each block in the sequence
full_seqdict = {}
loc = 0
block_loc = open(input_dir+output_prefix+".block_location.txt","w")
block_loc.write("Label\tStart\tLocation_in_block_start\tLocation_in_block_stop\n")
for iso in degap_seqdict:
	for i in range(0,len(ref_order)):
		label = ref_order[i][1]
		start = ref_order[i][0]
		if label in use_labels:
			seq = degap_seqdict[iso][label]
			try:
				full_seqdict[iso] += seq
			except:
				full_seqdict[iso] = seq
			if iso == include_list[0]:
				block_loc.write(str(label) +"\t"+ str(start) +"\t"+ str(loc) +"\t"+ str(loc+len(seq)) +"\n")
				loc = loc+len(seq)
block_loc.close()

#write the full, degapped sequences
corefile = open(input_dir+output_prefix+".core.fasta","w")
for k in range(0,len(include_list)):
	iso = include_list[k]
	corefile.write(">"+iso +"\n"+ full_seqdict[iso] +"\n")
corefile.close()


#Write all of the blocks to separate files and write the block statistics
block_size = open(input_dir+output_prefix+".alignment_block_sizes.txt","w")
block_size.write("Label\tStart\tlen_ref_seq\tlen_gapless_ref_seq\tProp_gaps\tSNP_count\n")

for i in range(0,len(ref_order)):
	label = ref_order[i][1]
	if label in use_labels:
		start = ref_order[i][0]
		len_ref_seq = float(label_sizes[label]["raw"])
		len_gapless_ref_seq = float(label_sizes[label]["degap"])
		prop_gap = 1.0-round((len_gapless_ref_seq/len_ref_seq),4)
		SNPcount = label_sizes[label]["SNPcount"]
		block_size.write(str(label)+"\t"+str(start)+"\t"+str(len_ref_seq)+"\t"+str(len_gapless_ref_seq)+"\t"+str(prop_gap)+"\t"+str(SNPcount)+"\n")
		outfile = open(alignment_dir+output_prefix+"."+str(label)+"."+str(start)+".fasta","w")
		for iso in degap_seqdict:
			degapseq = degap_seqdict[iso][label]
			outfile.write(">"+iso+"\n"+degapseq+"\n")
block_size.close()
outfile.close()
print("Done. Finding SNP locations")

#store MSA in dictionary
msa_name = output_prefix+".core.fasta"
snp_loc_file = output_prefix+".core.SNPloc.txt"
msa = open(input_dir+msa_name,"r")
seq_dict = {}
head = ""
for line in msa:
	line = line.strip()
	if line[0] == ">":
		head = line[1:len(line)]
	else:
		line = line.replace('a','A')
		line = line.replace('c','C')
		line = line.replace('g','G')
		line = line.replace('t','T')
		line = line.replace('n','N')
		try:
			seq_dict[head] += line
		except:
			seq_dict[head] = line
msa.close()
msa_len = len(seq_dict[head])

#Find all SNP containing columns in the MSA
snp_loc_list = []
outfile = open(input_dir+snp_loc_file,"w")
snp_num = 0
for i in range(0,msa_len):
	poly = poly_count(seq_dict,i)
	if poly > 1:
		outfile.write(str(snp_num) +"\t"+ str(i) +"\t"+ str(poly) +"\n")
		snp_num += 1
outfile.close()
