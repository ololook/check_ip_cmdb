#!/usr/bin/env python
# -*- coding:utf-8 -*-  
import MySQLdb
import string
import sys
import os
import time
from xlsxwriter.workbook import Workbook 
reload(sys)
from prettytable import PrettyTable 
sys.setdefaultencoding('utf8')
import sys
dt=time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))

def get_client():
    try:
      conn = MySQLdb.connect(host="ip",
                             port=port,
                             user='username',
                             passwd='passwd', 
                             charset='utf8' )
    except  MySQLdb.Error,e:
      print "Error %d:%s"%(e.args[0],e.args[1])
      exit(1)
    return conn

def main(v_ip) :
    cursor=get_client().cursor()
    ip=v_ip
    try :
        cursor.execute(exe_sql() %(v_ip,v_ip))
    except KeyboardInterrupt :
          print "exit .."
          sys.exit()
    return cursor 

def output_window():
    table = PrettyTable()
    if not os.path.exists("/home/mysql/ip.txt") :
             print
             print "\033[31m/home/mysql/ip.txt 文件不存在,请把ip以列方式保存在/home/mysql/目录下，并文件命名ip.txt\033[0m"
             print
             sys.exit(1)
    with open("/home/mysql/ip.txt", "r") as ins:
          for line in ins:
              line = line.strip('\n')
              line = line.strip('\'')
              line = line.strip(' ')
              cursor=main(line)
              table.field_names=[col[0] for col in cursor.description]
              for column in table.field_names:
                   table.align[column]='l'
              row = cursor.fetchone()
              if row == None:
                  print "%-16s %-32s" % (line,"NO_DATA_FOUND")
              else:
                  table.add_row(row)
          print table


def output_excel():
    workbook = Workbook('out_'+dt+'.xlsx')
    sheet = workbook.add_worksheet()
    r=0
    if not os.path.exists("/home/mysql/ip.txt") :
             print
             print "\033[31m/home/mysql/ip.txt 文件不存在,请把ip以列方式保存在/home/mysql/目录下，并文件命名ip.txt\033[0m"
             print
             sys.exit(1)
    with open("/home/mysql/ip.txt", "r") as ins:
          for line in ins:
              line = line.strip('\n')
              line = line.strip('\'')
              line = line.strip(' ')
              cursor=main(line)
              row=cursor.fetchone()
              if row == None:
                 print "%-16s %-32s" % (line,"NO_DATA_FOUND")
              else:
                 r=r+1
                 for c, col in enumerate(row):
                     sheet.write(r, c, col)

          field_names=[col[0] for col in cursor.description]
          for c,col in enumerate(field_names):
                 sheet.write(0,c, col)
def exe_sql(): 
    sql="""select
                  replace(t1.ip,'\t','') as ip,
                  replace(employee,'\t','') as employee,
                  replace(envname,'\t','') as env,
                  replace(t3.idcname,'\t','') as idc,
                  replace(t1.rackid,'\t','') as rack,
                  replace(t1.startrackid,'\t','') as srack,
                  replace(t1.endrackid,'\t','') as erack,
                  replace(t1.pn,'\t','') as pn,
                  replace(t4.project,'\t','') as project
             from cmdb.cmdb_server t1,cmdb.cmdb_env t2,cmdb.cmdb_idc t3 ,cmdb.cmdb_serverapp t4
                  where  t1.envid_id=t2.envid and t1.idcid_id=t3.idcid and t1.sn=t4.sn_id and ip like '%%%s%%'
             union all
               select
                  replace(t1.vip,'\t','') as ip,
                  replace(t1.employee,'\t','') as employee,
                  replace(envname,'\t','') as env,
                  replace(t4.idcname,'\t','') as idc,
                  replace(t3.rackid,'\t','') as rack,
                  replace(t3.startrackid,'\t','') as srackid,
                  replace(t3.endrackid,'\t','') as erackid,
                  'VM' ,
                  replace(t1.func,'\t','') as project
            from cmdb.cmdb_vserver t1,cmdb.cmdb_env t2,cmdb.cmdb_server t3,cmdb.cmdb_idc t4 #,cmdb.cmdb_serverapp t5
                  where t1.envid_id=t2.envid and t1.sn_id=t3.sn  and t3.idcid_id=t4.idcid and vip like '%%%s%%'"""    
    return sql       

if __name__ == '__main__':
    if len(sys.argv)>1:
        o=sys.argv[1]
        o.lower()=='y'
        output_excel()
    else:
        output_window()
