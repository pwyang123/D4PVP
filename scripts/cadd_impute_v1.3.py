#!/usr/bin/env python
# -*- coding: ASCII -*-

import sys
import math
from optparse import OptionParser

#Cl Name Min Max 99% Factor 99%/Max    
#28	EncExp	0.41	235313	593.36	396.58
#29	EncH3K27Ac	0.04	223899	84.24	2657.87
#30	EncH3K4Me1	0.04	6856.88	40.4	169.72
#31	EncH3K4Me3	0.04	52815	72.88	724.68
#32	EncNucleo	0	19045	3.9	4883.33
#33	EncOCC	1	4	4	-
#34	EncOCCombPVal	0	16	16	-
#35	EncOCDNasePVal	0	16	16	-
#36	EncOCFairePVal	0	5.4	16	-
#37	EncOCpolIIPVal	0	16	15.1	-
#38	EncOCctcfPVal	0	16	16	-
#39	EncOCmycPVal	0	16	5.44	-
#40	EncOCDNaseSig	0	2.61	0.51	5.12
#41	EncOCFaireSig	0	0.64	0.04	16.00
#42	EncOCpolIISig	0	10.08	0.25	40.32
#43	EncOCctcfSig	0	14.96	3.09	4.84
#44	EncOCmycSig	0	1.76	0.17	10.35
#
#("GC","0.418482"),("CpG","0.0244861")
#("priPhCons","0.114644"),("mamPhCons","0.0794826"),("verPhCons","0.0939182")
#("priPhyloP","-0.0331088"),("mamPhyloP","-0.0383832"),("verPhyloP","0.0169746")
#("GerpN","1.90901"),("GerpS","-0.20019"),("GerpRS","0"),("GerpRSpval","1"),("bStatistic","800.261"),
#("PolyPhenCat","unknown"),("PolyPhenVal",0.404105),("SIFTcat","unknown"),("SIFTval",0.218367)]
#
#      TFBS           TFBSPeaks        TFBSPeaksMax     
# Min.   :  1.000   Min.   :  1.000   Min.   :   9.717  
# 1st Qu.:  1.000   1st Qu.:  1.000   1st Qu.:  36.957  
# Median :  2.000   Median :  2.000   Median :  55.573  
# Mean   :  5.008   Mean   :  6.906   Mean   :  97.565  
# 3rd Qu.:  4.000   3rd Qu.:  6.000   3rd Qu.: 102.889  
# Max.   :123.000   Max.   :275.000   Max.   :1458.610
#
# Capped at 99th percentile:
#
#> quantile(data$TFBS,0.99)
#48 
#> quantile(data$TFBSPeaks,0.99)
#81 
#> quantile(data$TFBSPeaksMax,0.99)
#542.0574

transform = [("Chrom", (None,None,None)),
            ("Pos", (None,None,None)),
            ("Ref", ("DROP",None,None)),
            ("Anc", ("REMOVE",None,None)),
            ("Alt", ("DROP",None,None)),
            ("Type", ("DROP",None,None)),
            ("Length", ("DROP",None,None)),
            ("isTv", ("TV",None,None)),
            ("isDerived", ("REMOVE",None,None)),
            ("AnnoType", ("REMOVE",None,None)),
            ("Consequence", ("SET",None,None)),
            ("ConsScore", ("REMOVE",None,None)),
            ("ConsDetail", ("REMOVE",None,None)),
            ("GC", (None,"0.42",None)),
            ("CpG", (None,"0.02",None)),
            ("mapAbility20bp", (None,"0",None)),
            ("mapAbility35bp", (None,"0",None)),
            ("scoreSegDup", ("SPECIAL",None,None)),
            ("priPhCons", (None,"0.115",None)),
            ("mamPhCons", (None,"0.079",None)),
            ("verPhCons", (None,"0.094",None)),
            ("priPhyloP", (None,"-0.033",None)),
            ("mamPhyloP", (None,"-0.038",None)),
            ("verPhyloP", (None,"0.017",None)),
            ("GerpN", (None,"1.91",None)),
            ("GerpS", (None,"-0.200",None)),
            ("GerpRS", (None,"0",None)),
            ("GerpRSpval", (None,"1",None)),
            ("bStatistic", (None,"800",None)),
            ("mutIndex", ("REMOVE",None,None)),
            ("dnaHelt", ("REMOVE",None,None)),
            ("dnaMGW", ("REMOVE",None,None)),
            ("dnaProt", ("REMOVE",None,None)),
            ("dnaRoll", ("REMOVE",None,None)),
            ("mirSVR-Score", ("REMOVE",None,None)),
            ("mirSVR-E", ("REMOVE",None,None)),
            ("mirSVR-Aln", ("REMOVE",None,None)),
            ("targetScan", ("REMOVE",None,None)),
            ("fitCons", ("REMOVE",None,None)),
            ("cHmmTssA", ("REMOVE",None,None)),
            ("cHmmTssAFlnk", ("REMOVE",None,None)),
            ("cHmmTxFlnk", ("REMOVE",None,None)),
            ("cHmmTx", ("REMOVE",None,None)),
            ("cHmmTxWk", ("REMOVE",None,None)),
            ("cHmmEnhG", ("REMOVE",None,None)),
            ("cHmmEnh", ("REMOVE",None,None)),
            ("cHmmZnfRpts", ("REMOVE",None,None)),
            ("cHmmHet", ("REMOVE",None,None)),
            ("cHmmTssBiv", ("REMOVE",None,None)),
            ("cHmmBivFlnk", ("REMOVE",None,None)),
            ("cHmmEnhBiv", ("REMOVE",None,None)),
            ("cHmmReprPC", ("REMOVE",None,None)),
            ("cHmmReprPCWk", ("REMOVE",None,None)),
            ("cHmmQuies", ("REMOVE",None,None)),
            ("EncExp", ("0",593.36,"593.36")),
            ("EncH3K27Ac", ("0",84.24,"84.24")),
            ("EncH3K4Me1", ("0",40.4,"40.4")),
            ("EncH3K4Me3", ("0",72.88,"72.88")),
            ("EncNucleo", ("0",3.9,"3.9")),
            ("EncOCC", (None,"5",None)),
            ("EncOCCombPVal", (None,"0",None)),
            ("EncOCDNasePVal", (None,"0",None)),
            ("EncOCFairePVal", (None,"0",None)),
            ("EncOCpolIIPVal", (None,"0",None)),
            ("EncOCctcfPVal", (None,"0",None)),
            ("EncOCmycPVal", (None,"0",None)),
            ("EncOCDNaseSig", ("0",0.51,"0.51")),
            ("EncOCFaireSig", ("0",0.04,"0.04")),
            ("EncOCpolIISig", ("0",0.25,"0.25")),
            ("EncOCctcfSig", ("0",3.09,"3.09")),
            ("EncOCmycSig", ("0",0.17,"0.17")),
            ("Segway", (None, "UD", None)),
            ("tOverlapMotifs", (None, "0", None)),
            ("motifDist", (None, "0", None)),
            ("motifECount", (None, "0", None)),
            ("motifEName", ("REMOVE", None, None)),
            ("motifEHIPos", (None, "0", None)),
            ("motifEScoreChng", (None, "0", None)),
            ("TFBS", ("0", 48, "48")),
            ("TFBSPeaks", ("0", 81, "81")),
            ("TFBSPeaksMax", ("0", 542.0574, "542.0574")),
            ("isKnownVariant", ("REMOVE", "0", None)),
            ("ESP_AF", ("REMOVE", "0", None)),
            ("ESP_AFR", ("REMOVE", "0", None)),
            ("ESP_EUR", ("REMOVE", "0", None)),
            ("TG_AF", ("DAF", "0", None)),
            ("TG_ASN", ("REMOVE", "0", None)),
            ("TG_AMR", ("REMOVE", "0", None)),
            ("TG_AFR", ("REMOVE", "0", None)),
            ("TG_EUR", ("REMOVE", "0", None)),
            ("minDistTSS", ("LOG", "10000000", None)),
            ("minDistTSE", ("LOG", "10000000", None)),
            ("GeneID", ("REMOVE", None, None)),
            ("FeatureID", ("REMOVE", None, None)),
            ("CCDS", ("REMOVE", None, None)),
            ("GeneName", ("REMOVE", None, None)),
            ("cDNApos", (None, "0", "IND")),
            ("relcDNApos", (None, "0", "IND")),
            ("CDSpos", (None, "0", "IND")),
            ("relCDSpos", (None, "0", "IND")),
            ("protpos", (None, "0", "IND")),
            ("relProtpos", (None, "0", "IND")),
            ("Domain", (None, "UD", None)),
            ("Dst2Splice", (None, "0", "IND")),
            ("Dst2SplType", (None, "UD", None)),
            ("Exon", ("REMOVE", None, None)),
            ("Intron", ("REMOVE", None, None)),
            ("oAA", (None, "UD", None)),
            ("nAA", (None, "UD", None)),
            ("Grantham", (None, "0", "IND")),
            ("PolyPhenCat", ("NS", "unknown", None)),
            ("PolyPhenVal", ("NS", "0.404", "IND")),
            ("SIFTcat", ("NS", "unknown", None)),
            ("SIFTval", ("NS", "0.22", "IND"))]

consequence_set = { "3PRIME_UTR":"U3", "5PRIME_UTR":"U5", "DOWNSTREAM":"DN",
                    "INTERGENIC":"IG", "INTRONIC":"I", "NONCODING_CHANGE":"NC",
                    "NON_SYNONYMOUS":"NS", "REGULATORY":"R", "SPLICE_SITE":"S", "CANONICAL_SPLICE":"CS",
                    "STOP_GAINED":"SG", "STOP_LOST":"SL", "SYNONYMOUS":"SN", 
                    "UPSTREAM":"UP", "INFRAME":"IF", "FRAME_SHIFT":"FS" }

# domain_set = { "ncoils":"NC", "tmhmm":"TM", "sigp":"SP", "ndomain":"ND", "lcompl":"LC"}

transitions = set([('C','T'),('T','C'),('G','A'),('A','G')])
transversions = set([('A','C'),('C','A'),('T','A'),('A','T'),('C','G'),('G','C'),('G','T'),('T','G')])

parser = OptionParser("%prog [options]")
parser.add_option("-y","--state",dest="state", help="Associated y-Value (def 1)",default="1")
parser.add_option("--hcdiff",dest="hcdiff", help="Reverse time orientation of data in conversion (default Off)",default=False,action="store_true")
parser.add_option("--nofixTv",dest="nofixTv", help="Drop missing isTv lines instead of inferring isTV (default Off)",default=False,action="store_true")
parser.add_option("--nofixSplice",dest="fixSplice", help="Fix splice site definition to two categoricals (CANONICAL_SPLICE and SPLICE_SITE) (default Off)",default=False,action="store_true")
parser.add_option("--noGC",dest="noGC", help="Remove GC/CpG values from output lines (default Off)",default=False,action="store_true")
parser.add_option("--noSegDup",dest="noSegDup", help="Remove SegDup values from output lines (default On)",default=True,action="store_false")
parser.add_option("--noMap",dest="noMap", help="Remove mapabillity values from output lines (default On)",default=True,action="store_false")
parser.add_option("--noheader", dest="noheader", help="Do not print header line (default Off)",default=False,action="store_true")
(options, args) = parser.parse_args()

if options.noGC:
  for ind,(name,value) in enumerate(transform):
    if name == "GC" or name == "CpG":
      transform[ind] = (name,("REMOVE",value[1],value[2]))
  sys.stderr.write('Removing GC/CpG...\n')

if options.noSegDup:
  for ind,(name,value) in enumerate(transform):
    if name == "scoreSegDup":
      transform[ind] = (name,("REMOVE",value[1],value[2]))
else:
  sys.stderr.write('Keeping SegDup...\n')

if options.noMap:
  for ind,(name,value) in enumerate(transform):
    if (name == "mapAbility20bp") or (name == "mapAbility35bp"):
      transform[ind] = (name,("REMOVE",value[1],value[2]))
else:
  sys.stderr.write('Keeping mapability...\n')

if options.nofixTv:
  for ind,(name,value) in enumerate(transform):
    if name == "isTv":
      transform[ind]=(name,("DROP",None,None))
      sys.stderr.write('Droppping lines with missing isTV...\n')
      break

if options.hcdiff:
  sys.stderr.write('Changing time orientation of events...\n')

indices = {'chrom': None,
           'ref': None,
           'alt': None,
           'ctype': None,
           'is_derived': None,
           'consequence': None,
           'cons_score': None,
           'cons_detail': None,
           'oaa': None,
           'naa': None,
           'domain': None
          }

for ind,(name,(operation,value,capped)) in enumerate(transform):
  if name == "Chrom": indices['chrom'] = ind
  elif name == "Ref": indices['ref'] = ind
  elif name == "Alt": indices['alt'] = ind
  elif name == "Type": indices['ctype'] = ind
  elif name == "isDerived": indices['is_derived'] = ind
  elif name == "Consequence": indices['consequence'] = ind
  elif name == "Domain": indices['domain'] = ind
  elif name == "ConsScore": indices['cons_score'] = ind
  elif name == "ConsDetail": indices['cons_detail'] = ind
  elif name == "oAA": indices['oaa'] = ind
  elif name == "nAA": indices['naa'] = ind


def process_header(options, line, dataStore):
    '''
    '''
    header = line.lstrip('#').rstrip().split('\t')[:len(dataStore['transform'])]
    if len(header) != len(dataStore['transform']):
        sys.stderr.write('Unexpected number of fields\n')
        sys.exit()

    dataStore['new_header'] = ["y"]
    dataStore['add_header'] = []
    for ind,(name,(operation, value, capped)) in enumerate(dataStore['transform']):
        #if name == "Dst2Splice":
            #new_header.append("Dst2SplI")
            #new_header.append("Dst2SplE")
            #add_header.append("Dst2SplI.na")
            #add_header.append("Dst2SplE.na")
        #el  
        if operation != "REMOVE": 
            if operation == "DAF":
                dataStore['new_header'].append(operation)
            else:
                dataStore['new_header'].append(header[ind])
            if capped == "IND":
                dataStore['add_header'].append(header[ind] + ".na")
    if not options.noheader:
        sys.stdout.write("\t".join(dataStore['new_header'] + dataStore['add_header']) + "\n")


def process_line(options, line, dataStore):
    '''
    '''

    indices = dataStore['indices']
    fields = line.rstrip().split('\t')[:len(dataStore['transform'])]
    if len(fields) != len(dataStore['transform']):
        sys.stderr.write('Unexpected number of fields\n')
        sys.exit()

    if options.fixSplice:
        if fields[indices['consequence']] == "SPLICE_SITE":
            if ("splice_acceptor" in fields[indices['cons_detail']]) or ("splice_donor" in fields[indices['cons_detail']]):
                fields[indices['consequence']] = "CANONICAL_SPLICE"
                fields[indices['cons_score']] = "6"
            else:
                fields[indices['cons_score']] = "5"

    new_fields=[options.state]
    add_fields=[]
    Ref = None
    Alt = None
    if options.hcdiff:
        Ref = fields[indices['ref']]
        Alt = fields[indices['alt']]
        fields[indices['ref']] = Alt
        fields[indices['alt']] = Ref
        oAA = fields[indices['oaa']]
        nAA = fields[indices['naa']]
        fields[indices['oaa']] = nAA
        fields[indices['naa']] = oAA
        if "STOP_GAINED" == fields[indices['consequence']]:
            fields[indices['consequence']] = "STOP_LOST"
        elif "STOP_LOST" == fields[indices['consequence']]:
            fields[indices['consequence']] = "STOP_GAINED"
        if "INS" == fields[indices['ctype']]:
            fields[indices['ctype']] = "DEL"
        elif "DEL" == fields[indices['ctype']]:
            fields[indices['ctype']] = "INS"
    if len(fields[indices['ref']]) > 1 and fields[indices['ctype']] == "SNV":
        fields[indices['ctype']] = "DEL"
    if len(fields[indices['alt']]) > 1 and fields[indices['ctype']] == "SNV":
        fields[indices['ctype']] = "INS"
    vtype = fields[indices['ctype']]
    skip = False

    for ind,(name,(operation, value, capped)) in enumerate(transform):
        # print ind, name, operation, value, capped, fields[ind]
        if fields[ind] != "NA":
            if name == "Ref": 
                Ref = fields[ind]
<<<<<<< HEAD
                if (Ref == "-") or (vtype != "SNV") or (len(Ref) > 1): 
=======
                if (Ref == "-") or (vtype != "SNV"): 
>>>>>>> e8409ce35aa1724118aa834f2bb9bfc8c232fb68
                    Ref = "N"
                    fields[ind] = Ref
            elif name == "Alt": 
                Alt = fields[ind]
<<<<<<< HEAD
                if (Alt == "-") or (vtype != "SNV") or (len(Alt) > 1): 
                    Alt = "N"
                    fields[ind] = Alt
            elif (name == "oAA") and (vtype != "SNV") or (len(fields[indices['ref']]) > 1) or (len(fields[indices['alt']]) > 1): 
                fields[ind] = "UD"
            elif (name == "nAA") and (vtype != "SNV") or (len(fields[indices['ref']]) > 1) or (len(fields[indices['alt']]) > 1): 
=======
                if (Alt == "-") or (vtype != "SNV"): 
                    Alt = "N"
                    fields[ind] = Alt
            elif (name == "oAA") and (vtype != "SNV"): 
                fields[ind] = "UD"
            elif (name == "nAA") and (vtype != "SNV"): 
>>>>>>> e8409ce35aa1724118aa834f2bb9bfc8c232fb68
                fields[ind] = "UD"
            elif name == "Length":
                if int(fields[ind]) >= 50: 
                    fields[ind]="49"
        if capped == "IND" and operation != "NS":
            if fields[ind] == "NA":
                add_fields.append('1')
            else:
                add_fields.append('0')
        if operation == "REMOVE":
            continue
        elif operation == "TV":
            if fields[ind] == "NA":
                if (Ref,Alt) in transitions: 
                    cval = "0"
                elif (Ref,Alt) in transversions:
                    cval = "1"
                else: 
                    cval = "0.5"
            else:
                if fields[ind] == "TRUE":
                    cval = "1"
                else:
                    cval = "0"
            new_fields.append(cval)
        elif operation == "SET":
            if name == "Consequence": 
                new_fields.append(consequence_set.get(fields[ind], "O"))
        elif operation == "DROP":
            if fields[ind] == "NA": 
                skip = True
                break
            elif fields[ind] == "TRUE":
                new_fields.append("1")
            elif fields[ind] == "FALSE":
                new_fields.append("0")
            else: 
                new_fields.append(fields[ind])
        elif operation == None:
          #if name == "Dst2Splice":
            #if fields[ind] == "NA" and value != None: cval = value
            #else: cval = fields[ind]
            #if cval != "0":
              #ival = int(cval)
              #if ival > 0: 
                #new_fields.append("0")
                #new_fields.append(cval)
                #add_fields.append("1")
                #add_fields.append("0")
              #else:
                #new_fields.append(cval)
                #new_fields.append("0")
                #add_fields.append("0")
                #add_fields.append("1")
            #else:
              #new_fields.append("0")
              #new_fields.append("0")
              #add_fields.append("1")
              #add_fields.append("1")
          #else:
            if fields[ind] == "TRUE":
                new_fields.append("1")
            elif fields[ind] == "FALSE":
                new_fields.append("0")
            elif fields[ind] == "NA" and value != None:
                new_fields.append(value)
            else:
                new_fields.append(fields[ind])
        elif operation == "0":
            if fields[ind] == "NA":
                new_fields.append("0")
            elif float(fields[ind]) > value:
                new_fields.append(capped)
            else:
                new_fields.append(fields[ind])
        elif operation == "NS":
            if vtype == "SNV" and fields[indices['consequence']] == "NON_SYNONYMOUS" and fields[ind] == "NA": # NEW
                new_fields.append(value)
                if capped == "IND":
                    add_fields.append("0")
            else:
                if fields[ind] == "NA": 
                    if capped == "IND":
                        new_fields.append("0")
                        add_fields.append("1")
                    else:
                        new_fields.append("UD")
                else: 
                    new_fields.append(fields[ind])
                    if capped == "IND": add_fields.append("0")
        elif operation == "SPECIAL":
            if fields[ind] == "NA":
                new_fields.append("0")
            else:
                new_fields.append("1")
        elif operation == "DAF":
            if fields[ind] == "NA":
                fields[ind] = value 
            if fields[indices['is_derived']] != "FALSE":
                new_fields.append(fields[ind])
            else:
                new_fields.append("%.4f"%(1.0-float(fields[ind])))
        elif operation == "LOG":
            if fields[ind] == "NA" and value != None:
                cval = value
            else:
                cval = fields[ind]
            if cval != "0":
                cval = "%.4f"%(math.log(int(cval)))
            new_fields.append(cval)
        else:
            sys.stderr.write('Should not happen: %s %s %s %s!\n' % (name, operation, str(value), capped))
            sys.exit()

    if not skip: 
        sys.stdout.write("\t".join(new_fields + add_fields)+"\n")

dataStore = {'new_header': None, 'header': None, 'transform': transform, 'indices': indices}
header = None
new_header = None

# flines = open("test.0", 'r').readlines()
for line in sys.stdin:
  if line.startswith('##'): 
    continue
  if line.startswith('#'):
    process_header(options, line, dataStore)
  else:
    process_line(options, line, dataStore)