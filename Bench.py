# anomaly_detection.py

from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import SQLContext
from DFBench import DFJoin,DFOrderBy,DFGroupBy
from RDDBench import RDDJoin,RDDSort, RDDReduceByKey
from HWBench import HWNetwork
from HWBench import HWDiskWrite
from HWBench import HWDiskRead
from HWBench import HWCPU
from TPCH2Data import TPCH2Data
import os

#TPCH_DATASET_PATH="Data/tpch-small"
#TPCH_DATASET_PATH="Data/tpch-5"
TPCH_DATASET_PATH="Data/a4-tpch-1"
NUMBER_OF_TRIES=6
SIZE_OF_CLUSTER=20

#1000001137
#1000004123
#1000004207
#1000004233
#1000004249
#10000001251
SIZE_OF_PRIME=1000001137




if __name__ == "__main__":
    conf = SparkConf().setAppName('Spark benchmark')
    sc = SparkContext(conf=conf)
    sqlCt = SQLContext(sc)
    log4j = sc._jvm.org.apache.log4j
    log = log4j.LogManager.getLogger(__name__)
    log4j.PropertyConfigurator.configure("log4j.properties")
    log4j.LogManager.getLogger(__name__).setLevel(log4j.Level.DEBUG)

    data = TPCH2Data(sc, TPCH_DATASET_PATH)
    benchs = []

#    benchs.append(DFJoin(sqlCt,NUMBER_OF_TRIES))
#    benchs.append(DFOrderBy(sqlCt,NUMBER_OF_TRIES))
#    benchs.append(DFGroupBy(sqlCt,NUMBER_OF_TRIES))
#    benchs.append(RDDJoin(data.RDDs, NUMBER_OF_TRIES))
#    benchs.append(RDDSort(data.RDDs, NUMBER_OF_TRIES))
#    benchs.append(RDDReduceByKey(data.RDDs, NUMBER_OF_TRIES))
    #benchs.append(HWNetwork(sqlCt, NUMBER_OF_TRIES))
    #benchs.append(HWDiskWrite(sqlCt, NUMBER_OF_TRIES))
    #benchs.append(HWDiskRead(sqlCt, NUMBER_OF_TRIES))
    benchs.append(HWCPU(SIZE_OF_PRIME, SIZE_OF_CLUSTER*2, sc, sqlCt, NUMBER_OF_TRIES))

    for b in benchs:
	print "Name of test:", b.Name
#        os.system("date")
        b.Measure()
#        print "Hostname:", b.Hostname
        print "Results:", b.GetResults(), " seconds"
#	os.system("date")


    log4j.LogManager.getLogger(__name__).setLevel(log4j.Level.INFO)



















