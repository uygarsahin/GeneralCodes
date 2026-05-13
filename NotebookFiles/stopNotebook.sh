ps -ef | grep -v grep | grep upyter-notebook | awk {'print $2'} | xargs kill -9
