# create as many databases as you want
CREATE DATABASE IF NOT EXISTS db2
CREATE DATABASE IF NOT EXISTS db3;

# grant rights to user `user`
GRANT ALL ON *.* TO 'user'@'%';