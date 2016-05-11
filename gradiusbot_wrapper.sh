bot_dir=

while true; do
	gradiusbot_count=`pgrep -f gradiusbot.conf -c`

	if [ $gradiusbot_count = 0 ]; then
		echo "Running gradiusbot"
		cd $bot_dir
		venv3/bin/python gradiusbot.py gradiusbot.conf
	fi
	echo "Gradiusbot Discord loop ended. Sleeping."
	sleep 60
done
