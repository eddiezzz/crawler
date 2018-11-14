db=techwood_new
fname=$db.$(date +"%F-%H").sql
cmd="mysqldump --protocol=tcp -uroot -p123456 $db > $fname"
echo $cmd
exit
eval($cmd)
