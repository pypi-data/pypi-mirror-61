# py4javaerror happen when the path of the file is not correct
# !pip install pyspark[sql]
from __future__ import print_function
from functools import wraps
import pyspark as spark
from pyspark import SparkConf
import time
from operator import add
import os
from subprocess import STDOUT, check_call, check_output



class Fastq:
    def __init__(self, path:str) -> str:
        self.path = path
        self.install_java_scala()
        self.stop_context()
        self.sc = spark.SparkContext.getOrCreate(conf=self.set_conf())
        self.data = self.sc.textFile(self.path)

    def stop_context(self):
        try:
          self.sc.stop()
        except:
          pass

    def set_conf(self):
        conf = SparkConf().setAppName("App")
        conf = (conf.setMaster('local[*]')
          .set('spark.executor.memory', '4G')
          .set('spark.driver.memory', '16G')
          .set('spark.driver.maxResultSize', '8G'))
        return conf

    def install_java_scala(self):
        try:
          java_ver = check_output(['java', '-version'], stderr=STDOUT)
        except:
          java_ver = b''
        try:
          scala_ver = check_output(['scala', '-version'], stderr=STDOUT)
        except:
          scala_ver = b''
        if b'1.8.0_232' not in java_ver:
          java_8_install = ['apt-get', '--quiet', 'install',
                            '-y', 'openjdk-8-jdk']
          java_set_alt = ['update-alternatives', '--set', 'java',
                          '/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java' ]
          check_call(java_8_install, stdout=open(os.devnull, 'wb'),
                     stderr=STDOUT)
          os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
          check_call(java_set_alt)
        if b'2.11.12' not in scala_ver:
          scala_install = ['apt-get', '--quiet', 'install', 'scala']
          check_call(scala_install)


    def _logging(func):
        @wraps(func)
        def log_print(instance, *args, **kwargs):
          start = time.time()
          res = func(instance, *args, **kwargs)
          print("Finished Executing {}  in {}s!".format(func.__name__, time.time() - start))
          return res
        return log_print

    @_logging
    def get_data(self):
        return self.data


    @_logging
    def count_bases(self):
      seqs = self.extract_seq()
      seqs = seqs.flatMap(lambda line: list(line))
      seqs = seqs.map(lambda c: (c, 1))
      return seqs.reduceByKey(lambda a, b: a+b)#\
            #  .map(lambda c: (c, 1)) \
            #  .reduceByKey(lambda k1, k2: k1 + k2)
      # counts.saveAsTextFile('outputs')
      # print("saved output")

    @_logging
    def extract_seq(self):
        return self.data.filter(lambda x: x.isalpha())

    @_logging
    def get_lengths(self):
        seqs = self.extract_seq()
        return seqs.map(lambda x: len(x))

    def extract_qual(self):
        pass

    def extract_meta(self):
        pass


if __name__ == "__main__":
    fasta = Fastq('/home/aneesh/pyscr/pyscr/test/test.fastq')
