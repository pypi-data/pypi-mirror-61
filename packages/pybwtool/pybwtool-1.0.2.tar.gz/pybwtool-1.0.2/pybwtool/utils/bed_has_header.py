import pandas as pd

def bed_has_header(path:str)->bool:
    """Return if bed file at given path has header.
    
    Parameters
    ---------------------
    path: str,
        the candidate bed to validate.

    Returns
    ---------------------
    Return boolean representing if given candidate bed
    has a header.
    """
    # Checking the first row of bed file
    header = pd.read_csv(path, sep="\t", nrows=1)
    return any(
        column in header.columns
        for column in ("chrom", "chromStart", "chromEnd")
    )