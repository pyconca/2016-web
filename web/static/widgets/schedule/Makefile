css:
	node_modules/node-sass/bin/node-sass \
		$(CSS_OPT) \
		--recursive \
		--source-map true \
		--output compiled \
		scss

js: md-2-json
	node_modules/webpack/bin/webpack.js \
		$(JS_OPT) \
		--progress

md-2-json:
	python bin/md2session.py ../../../markdown/talks/

run:
	python3 -m http.server 8000
