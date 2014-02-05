WebalizerStatsScripts
=====================

Old script to split apache log file in multiple file and run webalizer on a per vhost basis.


Usage
=====

You're supposed to have your website under the directory /home/www-something/* and webalizer installed.
You also have to add the vhost in the apache logfile by adding %V at the end (or customizing the regex used in splitlog.py). Eg :

        CustomLog /home/www-public/logs/access.log "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %V"


This script is composed of 4 files :

- run_analog : the final "entry point", used by logrotate. It'll split the log and run webalizer for each website found.
- apache2.logrotate : a example of an adapted logrotate configuration
- gendomainsplit : a python script which generate a config file for splitlog.py
- splitlog.py : a python script which split a access.log file in multiple file, per vhost.
