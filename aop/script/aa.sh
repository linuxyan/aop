#!/usr/bin/bash
sed -i 's/variables_order = "GPCS"/variables_order = "EGPCS"/g' /usr/local/php/etc/php.ini
status=`grep -q "DUANKOU_ENV" /usr/local/php/etc/php-fpm.conf && echo "0" || echo "1"` 
if [ $status == 1 ];then
	echo "env[DUANKOU_ENV] = localhost" >> /usr/local/php/etc/php-fpm.conf
fi
status=`grep -q "DUANKOU_ENV" /etc/profile && echo "0" || echo "1"`
if [ $status == 1  ];then
	echo "export DUANKOU_ENV = localhost" >> /etc/profile
fi
/etc/init.d/php-fpm restart
