online:
	git commit -m "update"
	git push
	#rsync -vzrtopg --progress target/crawl-api.jar root@47.244.8.67:/tmp/crawl-api.jar
	ssh root@47.244.8.67 "cd /root/techwood/crawler/wechat/wechat_crawler && git pull"

onlinedo:
	ssh root@47.244.8.67 "cd /root/techwood/crawler/wechat/wechat_crawler && sh -x run.sh"
