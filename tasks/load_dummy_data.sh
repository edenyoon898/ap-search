mysql -h ap-mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS ap"
mysql -h ap-mysql -u root -proot ap < ./tasks/data/category_insert_20200407.sql
mysql -h ap-mysql -u root -proot ap < ./tasks/data/product_insert_20200407.sql
