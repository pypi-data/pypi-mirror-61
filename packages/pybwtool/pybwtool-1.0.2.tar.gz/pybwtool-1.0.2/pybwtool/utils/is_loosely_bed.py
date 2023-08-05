import pandas as pd

def is_loosely_bed(path:str)->bool:
    """Return if file at given path is not a bed at all.
    
    Parameters
    ---------------------
    path: str,
        the candidate bed to validate.

    Returns
    ---------------------
    Return boolean representing if given candidate bed
    is actually a bed file following loosely definition.
    """
    # The file path does not end with bed
    # Compressed files, such as .bed.gz 
    # are not supported by bwtools.
    if not path.endswith(".bed"):
        return False
    # Checking the first row of bed file
    header = pd.read_csv(path, sep="\t", nrows=1)
    # File to be a valid bed must contain at least
    # 3 columns: chrom, chromStart and chromEnd
    if len(header.columns) < 3:
        return False
    return True