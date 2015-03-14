Automated operational platform
====

##环境需求：
 * python >=2.5
 * mysql >5.1
 * nginx >1.2

##python模块：
 * django >=1.4.5
 * flup
 * paramiko
 * django-excel-response
 * MySQL-python

##主要功能
 * 服务器的资源统计
 * svn的在线发布
 * 脚本的批量执行

##安装部署
* 修改aopproject/settings.py 设置数据库类型，账号密码
* 运行python manage.py syncdb    进行创建数据库表结构  期间添加管理员账号
* 开启服务器:python manage.py runfcgi method=prefork host=127.0.0.1 port=9001
* 配置nginx转发到127.0.0.1:90001端口
* nginx配置文件参考：

<pre><code>
server {
        listen       80;
        server_name  www.linuxyan.com;
        root /var/www/html;

        access_log  /tmp/python.access.log;
        error_log   /tmp/python.error.log;

        location /static/ {
                root /var/www/html;
        }

        location / {
                fastcgi_pass 127.0.0.1:9001;
                fastcgi_pass_header Authorization;
                fastcgi_intercept_errors off;
                fastcgi_param PATH_INFO         $fastcgi_script_name;
                fastcgi_param REQUEST_METHOD    $request_method;
                fastcgi_param QUERY_STRING      $query_string;
                fastcgi_param CONTENT_TYPE      $content_type;
                fastcgi_param CONTENT_LENGTH    $content_length;
                fastcgi_param SERVER_PORT       $server_port;
                fastcgi_param SERVER_PROTOCOL   $server_protocol;
                fastcgi_param SERVER_NAME       $server_name;
                fastcgi_param REQUEST_URI       $request_uri;
                fastcgi_param DOCUMENT_URI      $document_uri;
                fastcgi_param DOCUMENT_ROOT     $document_root;
                fastcgi_param SERVER_ADDR       $server_addr;
                fastcgi_param REMOTE_USER       $remote_user;
                fastcgi_param REMOTE_ADDR       $remote_addr;
                fastcgi_param REMOTE_PORT       $remote_port;
                fastcgi_param SERVER_SOFTWARE   "nginx";
                fastcgi_param GATEWAY_INTERFACE "CGI/1.1";
        }
}
</code></pre>
