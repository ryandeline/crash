import tempfile
import os
import pandas as pd

def _getLineNumber():
    cf = currentframe()
    return cf.f_back.f_lineno

def sshQuery(queryStr):
    fd, path = tempfile.mkstemp()
    argsDict = {'HIVE_USER':os.environ['HIVE_USER'],
                'HIVE_MACHINE':os.environ['HIVE_MACHINE'],
                'QUERY':queryStr, 'PATH':path, 'HIVE_DATABASE':os.environ['HIVE_DATABASE']}

    cmd = ("ssh %(HIVE_USER)s@%(HIVE_MACHINE)s \"hive --database %(HIVE_DATABASE)s -e "
          "\\\"set hive.cli.print.header=true; %(QUERY)s\\\"\" > %(PATH)s 2> /dev/null")%argsDict
    os.system(cmd)
    lines = [x.strip() for x in open(path, 'r').readlines()]
    os.remove(path)
    return lines

def sshQuery_json_header(queryStr):
    lines = sshQuery(queryStr)
    #print len(lines)
    #print lines[0:5]
    return lines[0], lines[1:]


def sshQuery_dataframe(queryStr, dtypeDict=None):
    fd, path = tempfile.mkstemp()
    argsDict = {'HIVE_USER':os.environ['HIVE_USER'],
                'HIVE_MACHINE':os.environ['HIVE_MACHINE'],
                'QUERY':queryStr, 'PATH':path, 'HIVE_DATABASE':os.environ['HIVE_DATABASE']}

    cmd = ("ssh %(HIVE_USER)s@%(HIVE_MACHINE)s \"hive --database %(HIVE_DATABASE)s -e "
          "\\\"set hive.cli.print.header=true; %(QUERY)s\\\"\" > %(PATH)s 2> /dev/null")%argsDict
    os.system(cmd)
    df = pd.io.parsers.read_csv(path, '\t', dtype=dtypeDict)
    os.remove(path)
    return df

def getHiveConn():
    E = lambda x: os.environ[x]
    return pyhs2.connect(host=os.environ['HIVE_MACHINE'],
                   user=os.environ['HIVE_USER'],
                   password=os.environ['HIVE_PASSWORD'],
                   database=os.environ['HIVE_DATABASE'],
                   authMechanism='PLAIN')

def getHiveCursor(conn=None):
    if conn is None:
        conn = getHiveConn()
    return conn.cursor(), conn