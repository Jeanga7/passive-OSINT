GITHUB_TOKEN ?= $(shell prGITHUB_TOKENintenv )
MESSAGE ?= $(shell printenv MESSAGE)

config:
	cd .git && git remote add github https://$(GITHUB_TOKEN)@github.com/Jeanga7/passive-OSINT.git
push:
	git add .
	git commit -m "$(MESSAGE)"
	git push origin
	git push github



