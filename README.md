Automated operational platform
====

###环境需求：

 * python >=2.5
 * django >=1.4.5
 * mysql >5.1
 * nginx >1.2
 * flup

#python model

 * paramiko
 * django-excel-response
 * MySQL-python

##主要功能
 * 服务器的资源统计
 * svn的在线发布
 * 脚本的批量执行

#2013.06.07
*添加了权限管理，各个帐号添加的资源只有该帐号和root超级管理员可以删除和编辑。

*每个帐号添加的任务，只有该帐号和root超级管理员可以执行以及删除。其他普通管理员只能查看执行状态。

*超级管理员root可以添加和删除用户，普通用户只能编辑自己该账户的资料。


