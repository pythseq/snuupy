import click


@click.group()
def main():
    pass


@main.command("parseIllumina")
@click.option("--bam", "secondBam", help="cellranger result")
@click.option(
    "--barcode",
    "secondIndex",
    help="the filtered barcode list which is output by cellranger; format tsv NOT gz!!!",
)
@click.option("--genome", "genomeIndex", help="the fai format file")
@click.option(
    "--genomeCounts",
    "useColumn",
    default=5,
    type=int,
    show_default=True,
    help="chromosome counts",
)
@click.option("--window", "windowSize", type=int, default=500, help="window size")
@click.option("--parsed", "parsedIndex", help="the parsedIndex; end with .index")
def _parseIllumina(
    secondBam, secondIndex, genomeIndex, windowSize, parsedIndex, useColumn
):
    """
    \b
    parse Illumina bam file and generate Illumina index
    """
    from scripts.parseIllumina import parseIllumina

    parseIllumina(
        secondBam, secondIndex, genomeIndex, windowSize, parsedIndex, useColumn
    )


@main.command("generateIlluminaWindow")
@click.option("-i", "ILLUMINA_INDEX", help="parseIllumina output index")
@click.option("-o", "OUT_DIR", help="illumina window dir; end with /")
def _generateIlluminaWindow(ILLUMINA_INDEX, OUT_DIR):
    """
    output illumina reads based on mapping info
    """
    from scripts.generateIlluminaWindow import generateIlluminaWindow

    generateIlluminaWindow(ILLUMINA_INDEX, OUT_DIR)


@main.command("generateH5adFromKb")
@click.option("--tg", "t2gPath")
@click.option("--ec", "ecPath")
@click.option("--splice-bus", "splicePath")
@click.option("--unsplice-bus", "unsplicePath")
@click.option("-o", "adataPath")
def _generateH5adFromKb(t2gPath, ecPath, splicePath, unsplicePath, adataPath):
    """
    get adata from kbpython result

    \b
    --tg:
        kbpython index t2g
    --ec:
        kbpython matrix ec
    --splice-bus:
        kbpython splice bus
    --unsplice-bus:
        kbpython unsplice bus
    -o:
        adata store path; must ends with h5ad!!!
    """
    from scripts.generateH5adFromKb import getAdataFromKbNucleiResult

    getAdataFromKbNucleiResult(t2gPath, ecPath, splicePath, unsplicePath, adataPath)


@main.command("generateIlluminaWindowFromKb")
@click.option("--tg", "t2gPath")
@click.option("--ec", "ecPath")
@click.option("--splice-bus", "splicePath")
@click.option("--unsplice-bus", "unsplicePath")
@click.option("--gtf", "gtfPath")
@click.option("-o", "illuminaWindowDir")
@click.option("--window", "windowSize", type=int, default=500)
def _generateIlluminaWindowFromKb(
    t2gPath, ecPath, splicePath, unsplicePath, gtfPath, illuminaWindowDir, windowSize
):
    """
    \b
    generate illumina windows from kb_python results(workflow: nuclei)
    --tg:
        index file
    --ec:
        matrix ec
    --splice-bus:
        filtered spliced bus
    --unsplice-bus:
        filtered spliced bus
    --gtf:
        gtf anno file, used to create kb ref
    -o:
        dir stored illumina reads, end with '/'
    windowSize:
        windowSize; default 500
    """
    from scripts.generateIlluminaWindowFromKb import generateIlluminaWindowFromKb

    generateIlluminaWindowFromKb(
        t2gPath,
        ecPath,
        splicePath,
        unsplicePath,
        gtfPath,
        illuminaWindowDir,
        windowSize,
    )


@main.command("addUnmappedBaseTag")
@click.option("-i", "BAM_PATH", help="minimap2 output; bam format")
@click.option("-f", "NANOPORE_FASTA", help="raw nanopore seq; fasta format")
@click.option("-o", "BAM_PATH_OUT", help="output bam")
def _addUnmappedBaseTag(BAM_PATH, NANOPORE_FASTA, BAM_PATH_OUT):
    """
    \b
    get unmapped base tag
    """
    from scripts.addUnmappedBaseTag import addUnmappedBaseTag

    addUnmappedBaseTag(BAM_PATH, NANOPORE_FASTA, BAM_PATH_OUT)


@main.command("generateNanoporeWindow")
@click.option("--genome", "GENOME_INDEX", help="the fai format file")
@click.option(
    "--genomeCounts",
    "useColumn",
    default=5,
    type=int,
    show_default=True,
    help="chromosome counts",
)
@click.option("-b", "BAM_PATH", help="bam added unmapped base tag ; format bam")
@click.option("-o", "OUT_PATH", help="output dir; end with / ")
@click.option("-w", "WINDOW", type=int, help="window size, same as Illumina")
def _generateNanoporeWindow(GENOME_INDEX, BAM_PATH, OUT_PATH, WINDOW, useColumn):
    """
    output nanopore reads based on mapping info
    """
    from scripts.generateNanoporeWindow import generateNanoporeWindow

    generateNanoporeWindow(GENOME_INDEX, BAM_PATH, OUT_PATH, WINDOW, useColumn)


@main.command("windowBlast")
@click.option("-i", "ILLUMINA_DIR", help='illumina dir; should end with "/"')
@click.option("-n", "NANOPORE_DIR", help='nanopore dir; should end with "/"')
@click.option("-o", "BLAST_DIR", help='result dir; should end with "/"')
@click.option("-t", "THREADS", type=int, help="threads")
@click.option("-b", "BLAST_PATH", help='blast path; should end with "/"')
def _windowBlast(ILLUMINA_DIR, NANOPORE_DIR, BLAST_DIR, THREADS, BLAST_PATH):
    """
    blast find potential UMI/Bc
    """
    from scripts.windowBlast import windowBlast

    windowBlast(ILLUMINA_DIR, NANOPORE_DIR, BLAST_DIR, THREADS, BLAST_PATH)


@main.command("getMismatch")
@click.option("-i", "MAPPING_RESULT", help="mergerd window blast results")
@click.option("-b", "ADD_SEQ_BAM", help="bam added unmapped seq tag")
@click.option("-o", "OUT_FEATHER", help="output feather format")
@click.option("-t", "THREADS", type=int, help="threads")
def _getMismatch(MAPPING_RESULT, ADD_SEQ_BAM, OUT_FEATHER, THREADS):
    """
    calculate mismatch based on blast results
    """
    from scripts.getMismatch import getMismatch

    getMismatch(MAPPING_RESULT, ADD_SEQ_BAM, OUT_FEATHER, THREADS)


@main.command("barcodeAssignment")
@click.option("-i", "MISMATCH_RESULT", help="getMismatch output")
@click.option(
    "-o", "OUTPUT_FEATHER", help="nanopore read id with barcode and umi; feather format"
)
@click.option("--ED-barcode", "MAX_BARCODE_ED", type=int)
@click.option("--ED-UMI", "MAX_UMI_ED", type=int)
def _barcodeAssignment(MISMATCH_RESULT, OUTPUT_FEATHER, MAX_BARCODE_ED, MAX_UMI_ED):
    """
    assign barcode for each Nanopore read; based on mismatch results
    """
    from scripts.barcodeAssignment import barcodeAssignment

    barcodeAssignment(MISMATCH_RESULT, OUTPUT_FEATHER, MAX_BARCODE_ED, MAX_UMI_ED)


@main.command("polishReads")
@click.option("-i", "MISMATCH_RESULT", help="step07 output")
@click.option("-f", "NANOPORE_READ", help="original nanopore read")
@click.option("-T", "TEMP_DIR", help="temp dir; end with /")
@click.option("-F", "FINAL_DIR", help="polished read stored dir; end with /")
@click.option("-o", "POLISHED_READ", help="polished read")
@click.option("-p", "PENALTY_PATH", help="penalty matrix used by poa")
@click.option("-t", "THREADS", type=int, help="threads")
@click.option("--minimap2", "minimapPath", show_default=True, default="minimap2")
@click.option("--poa", "poaPath", default="poa", show_default=True)
@click.option("--racon", "raconPath", default="racon", show_default=True)
@click.option("--seqkit", "seqkitPath", default="seqkit", show_default=True)
def _polishReads(
    MISMATCH_RESULT,
    NANOPORE_READ,
    TEMP_DIR,
    FINAL_DIR,
    POLISHED_READ,
    THREADS,
    PENALTY_PATH,
    minimapPath,
    poaPath,
    raconPath,
    seqkitPath,
):
    """
    polish barcode assigned Nanopore reads
    """
    from scripts.polishReads import polishReads

    polishReads(
        MISMATCH_RESULT,
        NANOPORE_READ,
        TEMP_DIR,
        FINAL_DIR,
        POLISHED_READ,
        THREADS,
        PENALTY_PATH,
        minimapPath,
        poaPath,
        raconPath,
        seqkitPath,
    )


@main.command("addGeneName")
@click.option("-i", "inBamPath", help="polished reads mapping bam")
@click.option("--bed", "bedAnno", help="genome annotation file; bed12 format")
@click.option(
    "--out-pickle", "outfile", help="out pickle; use for calculate splicing info"
)
@click.option("--out-bam", "outBamPath", help="bam with gene id tag")
@click.option(
    "--bedtools",
    "bedtoolsPath",
    default="bedtools",
    show_default=True,
    help="bedtools path",
)
@click.option(
    "--tag-gene", "geneIdTag", default="gi", show_default=True, help="gene tag name"
)
def _addGeneName(inBamPath, bedAnno, outfile, bedtoolsPath, outBamPath, geneIdTag):
    """
    parse polished reads mapping results and get gene name based on the overlap info with anno file.
    """
    from scripts.addGeneName import addGeneName

    addGeneName(inBamPath, bedAnno, outfile, bedtoolsPath, outBamPath, geneIdTag)


@main.command("getSpliceInfo")
@click.option("-i", "INBAM_PATH", help="polished reads mapping file; format bam")
@click.option(
    "-b",
    "BED_REPRE_ANNO",
    help="genome annotation file only including representative transcripts; bed12 format",
)
@click.option("-o", "OUT_PATH", help="output path; format tsv")
@click.option("-g", "GENE_NAME_INFO", help="addGeneName output; format pickle")
@click.option("--bedtools", "bedtoolsPath", default="bedtools", show_default=True)
@click.option(
    "--ratio",
    "NEED_RATIO",
    is_flag=True,
    help="need retention intron overlap ratio or not",
)
def _getSpliceInfo(
    INBAM_PATH, BED_REPRE_ANNO, GENE_NAME_INFO, OUT_PATH, NEED_RATIO, bedtoolsPath
):
    """
    get splice information which used for generate splicing matrix
    """
    from scripts.getSpliceInfo import getSpliceInfo

    getSpliceInfo(
        INBAM_PATH, BED_REPRE_ANNO, GENE_NAME_INFO, OUT_PATH, NEED_RATIO, bedtoolsPath
    )


@main.command("addPolyATag")
@click.option("--in-fasta", "infile", help="original fasta")
@click.option("--genome", "genome", help="genome file; format fasta")
@click.option("-t", "threads", type=int, help="threads")
@click.option("--in-f5-workspace", "f5dir", help="fast5 workspace; ends with /")
@click.option("--in-f5-summary", "f5summary", help="fast5 suquencing summary")
@click.option(
    "--bed", "bed", help="genome annotation file used for minimap2; bed12 format"
)
@click.option("--tempDir", "tempDir", help="Directory storing temp files; end with /")
@click.option(
    "--fp",
    "fp",
    default="CCCATGTACTCTGCGTTGATACCACTGCTT",
    show_default=True,
    help="fprimer seq",
)
@click.option(
    "--ep",
    "ep",
    default="CTACACGACGCTCTTCCGATCT",
    show_default=True,
    help="eprimer seq",
)
@click.option(
    "--feather", "featherPath", help="barcodeAssignment output; foramt feather"
)
@click.option("--in-bam", "bamFilePath", help="bam added gene name tag")
@click.option("--out-bam", "addPolyAFilePath", help="bam added polyA length tag")
@click.option("--tag-polyA", "polyATag", default="pa", help="polyA tag name")
@click.option(
    "--minimap",
    "minimapPath",
    default="minimap2",
    show_default=True,
    help="minimap2 path",
)
@click.option(
    "--samtools",
    "samtoolsPath",
    default="samtools",
    show_default=True,
    help="samtools path",
)
def _addPolyATag(
    infile,
    genome,
    threads,
    f5dir,
    f5summary,
    bed,
    tempDir,
    fp,
    ep,
    featherPath,
    bamFilePath,
    addPolyAFilePath,
    polyATag,
    minimapPath,
    samtoolsPath,
):
    """
    add polyA length tag for bam files
    """
    from scripts.addPolyATag import addPolyATag

    addPolyATag(
        infile,
        genome,
        threads,
        f5dir,
        f5summary,
        bed,
        tempDir,
        fp,
        ep,
        featherPath,
        bamFilePath,
        addPolyAFilePath,
        polyATag,
        minimapPath,
        samtoolsPath,
    )


@main.command("polyAClusterDetected")
@click.option("--infile", required=True, help="bam added gene tag and polyA tag")
@click.option("--gene-bed", required=True, help="GENE BED , NOT BED 12!")
@click.option("--out-dir", "out_suffix", required=True, help="out dir; ends with /")
@click.option("-t", "--threads", required=False, help="threads", default=10)
@click.option("--fasta", "fastaPath", help="genome fa")
def _polyAClusterDetected(fastaPath, infile, gene_bed, out_suffix, threads):
    """
    detect PolyA Cluster
    """
    from scripts.polyAClusterDetected import polyAClusterDetected

    polyAClusterDetected(fastaPath, infile, gene_bed, out_suffix, threads)


@main.command("generateMtx")
@click.option("-i", "inIrInfoPath", help="getSpliceInfo output")
@click.option(
    "--in-illumina",
    "illuminaEx",
    help="cell ranger count output <filtered_feature_bc_matrix.h5>; or h5ad",
)
@click.option(
    "--apa-pac",
    "apaClusterPath",
    default="False",
    help="polyAClusterDetected output; the filtered bed were recommended; if not provided the APA matrix will not be generated",
)
@click.option(
    "--apa-bam",
    "inBamPath",
    default="False",
    help="the nanopore bam added gene name tag; if not provided the APA matrix will not be generated",
)
@click.option("--tag", "geneTag", default="gi", help="gene name tag", show_default=True)
@click.option(
    "--ir/--no-ir", "irMode", default=True, help="generate splicing matrix or not"
)
@click.option(
    "--ir-list",
    "intronList",
    default=False,
    help="only use those intron to calculate splicing matrix; if not provided, all intron will be used",
)
@click.option(
    "--only-FullLength",
    "onlyFullLength",
    is_flag=True,
    help="only use full length generate splice matrix or not",
)
@click.option(
    "--out-nanopore",
    "outMtxDirPath",
    help="matrics including nanopore expression matrix; apa matrix; splicing mtx; end with /",
)
@click.option(
    "--out-illumina",
    "illuminaMtxDirPath",
    help="matrics including illumina expression matrix; apa matrix; splicing mtx; end with /",
)
def _generateMtx(
    apaClusterPath,
    inBamPath,
    geneTag,
    inIrInfoPath,
    outMtxDirPath,
    illuminaMtxDirPath,
    irMode,
    intronList,
    illuminaEx,
    onlyFullLength,
):
    """
    generate matrices
    """
    from scripts.generateMtx import generateMtx

    generateMtx(
        apaClusterPath,
        inBamPath,
        geneTag,
        inIrInfoPath,
        outMtxDirPath,
        illuminaMtxDirPath,
        irMode,
        intronList,
        illuminaEx,
        onlyFullLength,
    )


main()
