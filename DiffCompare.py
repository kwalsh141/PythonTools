import os
import sys
import logging
import pandas as pd
from datetime import datetime

logger = logging.getLogger('debuglevel')
logger.setLevel('DEBUG')

filehandlerdbg = logging.FileHandler('logs\\{:%Y%m%d%H%M}_logs.log'.format(datetime.now()), mode='w')
filehandlerdbg.setLevel('DEBUG')
filehandlerstream = logging.StreamHandler(sys.stdout)
filehandlerstream.setLevel('WARNING')

logger.addHandler(filehandlerdbg)
logger.addHandler(filehandlerstream)

logger.debug('Log file for checking output of baseline and results files\n')

filterid = sys.argv
filterid.pop(0)

matchall = []
test = False

# get path to each file within baseline and results folders
filelistbaseline = [os.path.join(roots, filenames) for roots, dirs, files in os.walk('Outputs\\Baseline')
                    for filenames in files]
filelistresults = [os.path.join(roots, filenames) for roots, dirs, files in os.walk('Outputs\\Results')
                    for filenames in files]

logger.debug("Baseline: {}, Results: {}\n".format(len(filelistbaseline), len(filelistresults)))

if test:
    filelistbaseline = filelistbaseline[0:5]
    filelistresults = filelistresults[0:5]

for fn in filelistbaseline:

    baseline = pd.read_csv(fn)
    baselinefilter = baseline[~baseline.operatorid.isin(filterid)]

    # check to see if result file exists
    fnresult = fn.replace("Baseline", "Results")

    try:
        if fnresult not in filelistresults:
            raise ValueError(fnresult)
        else:
            result = pd.read_csv(fnresult)
            resultfilter = result.loc[~result.operatorid.isin(filterid)]
            resultfilter = resultfilter.reset_index(drop=True)
            logger.debug("{}, Shape Baseline: {}, Shape BaselineFilter: {}".
                          format(fn, baseline.shape, baselinefilter.shape))
            logger.debug("{}, Shape Result: {}, Shape ResultFilter: {}".
                          format(fnresult, result.shape, resultfilter.shape))

            match = resultfilter.equals(baselinefilter)
            logger.debug("Match above?: {}\n".format(match))
            matchall.append(match)

    except ValueError as e:
        logger.warning("Results file {} missing\n".format(e))

if all(matchall):
    logger.debug("All files match. Woop woop.")
else:
    mismatch = [filelistbaseline[i] for i, m in enumerate(matchall) if not m]
    logger.warning("File mismatch at {}".format(mismatch))










