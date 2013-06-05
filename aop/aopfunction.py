# -*- coding: UTF-8 -*- 
import paramiko,os,time
import threading
from aopproject import settings
import random
import base64

def ordinary_ssh(host,username,password,port,cmd):
    password = de_str(settings.SECRET_KEY,str(password))
    s=paramiko.SSHClient()  
    s.load_system_host_keys()  
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname = host,port=int(port),username=username, password=password)
    stdin, stdout, stderr = s.exec_command(cmd)
    result = stdout.read()
    result = str(result)
    s.close()
    return result



#验证服务器信息
def verification_ssh(host,username,password,port,root_pwd,cmd):
    root_pwd = de_str(str(settings.SECRET_KEY),str(root_pwd))
    password = de_str(str(settings.SECRET_KEY),str(password))
    
    s=paramiko.SSHClient()  
    s.load_system_host_keys()  
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname = host,port=int(port),username=username, password=password)
    if username != 'root':
        ssh = s.invoke_shell()
        time.sleep(0.1)
        ssh.send('su - root\n')
        buff = ''
        while not buff.endswith(': ') or buff.endswith('： '):
            resp = ssh.recv(9999)
            buff +=resp
        ssh.send(root_pwd)
        ssh.send('\n')
        buff = ''
        while not buff.endswith('# '):
            resp = ssh.recv(9999)
            buff +=resp
        ssh.send(cmd)
        ssh.send('\n')
        buff = ''
        while not buff.endswith('# '):
            resp = ssh.recv(9999)
            buff +=resp
        s.close()
        #result = buff.replace('\n','<br>')
        result = buff
    else:
        stdin, stdout, stderr = s.exec_command(cmd)
        result = stdout.read()
        result = str(result)
        #result = str(result).replace('\n','<br>')
        s.close()
    return result


def upload_run_script(tasklogpath,host,script_list):
    try:
        out = open(tasklogpath,'a')
        script_dir = str(host.script_dir)
        cmd = r"mkdir %s;chmod 777 %s" %(script_dir,script_dir)
        verification_ssh(host.host_w_ip,host.host_user,host.host_pass,host.host_w_port,host.host_root_pwd,cmd)
        print "Start upload script"
        t = paramiko.Transport((host.host_w_ip,host.host_w_port))
        t.connect(username=host.host_user,password=de_str(settings.SECRET_KEY,str(host.host_pass)))
        sftp=paramiko.SFTPClient.from_transport(t)
        for script in script_list:
            local_file_path = os.path.join(settings.WEB_ROOT,'..\\').replace('\\','/')+str(script.script_file)
            server_file_path = os.path.join(str(host.script_dir),os.path.basename(str(script.script_file)))
            sftp.put(local_file_path,server_file_path)
            result = "\nScript %s upload to %s Success!\n" %(os.path.basename(str(script.script_file)),host.host_w_ip)
            out.write(result)
            file_path = script_dir+'/'+os.path.basename(str(script.script_file))
            cmd = r"chmod 777 %s ; %s" %(file_path,file_path)
            print cmd
            out.write("\n%s run %s result:\n\n" %(host.host_w_ip,os.path.basename(str(script.script_file))))
            result = verification_ssh(host.host_w_ip,host.host_user,host.host_pass,host.host_w_port,host.host_root_pwd,cmd)
            out.write(result+'\n-------------------------------------------------\n')
    except Exception as e:
        result = "\nScript upload to %s Faild!\n" %host.host_w_ip
        out.write(result)
        out.write(str(e))
        print e
    t.close()
    out.close()
    

class task_thread(threading.Thread):
    def __init__(self,tasklogpath,host,script_list):
        threading.Thread.__init__(self)
        self.tasklogpath = tasklogpath
        self.host = host
        self.script_list = script_list
    def run(self):
        print "Start upload"
        upload_run_script(self.tasklogpath,self.host,self.script_list) 

def start_task_thread(tasklogpath,host_list,script_list):
    try:
        for host in host_list:
            thread = task_thread(tasklogpath,host,script_list)
            thread.setDaemon(True)
            thread.start()
    except Exception as e:
        print e
        


def en_str(key,s):
    kar=bytearray(key)
    klen=len(kar)
    bar=bytearray(s)
    offset=random.randint(0,0xff)
    rs=bytearray()
    rs.append(offset)
    for idx,sc in enumerate(bar):
        k=idx % klen
        rs.append(((sc+offset) % 0xff) ^ (kar[k] & kar[-(k+1)]))
    return base64.urlsafe_b64encode(str(rs))

def de_str(key,s):
    kar=bytearray(key)
    klen=len(kar)
    bar=bytearray(base64.urlsafe_b64decode(s))
    offset=bar[0]
    rs=bytearray()
    for idx,sc in enumerate(bar[1:]):
        k=idx % klen
        t=(sc ^ (kar[k] & kar[-(k+1)]))
        if t<=offset:
            t+=0xff - offset
        else:
            t-=offset
        rs.append(t)
    return str(rs)
    
if __name__ == "__main__":
    pass