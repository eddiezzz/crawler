online:
	git commit -m "update"
	git push
	#rsync -vzrtopg --progress target/crawl-api.jar root@47.244.8.67:/tmp/crawl-api.jar
	ssh root@47.244.8.67 "cd /root/techwood/crawler/wechat/wechat_crawler && git pull"

local_reset:
	mysql --protocol=tcp -uroot -p < reset_db.sql

local_do:
	sh -x run.sh

online_do:
	ssh root@47.244.8.67 "cd /root/techwood/crawler/wechat/wechat_crawler && sh -x run.sh"

online_reset:
	ssh root@47.244.8.67 "cd /root/techwood/crawler/wechat/wechat_crawler && mysql --protocol=tcp -uroot -p < reset_db.sql"

