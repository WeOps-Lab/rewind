.PHONY: setup docs vendor

setup:
	go install github.com/swaggo/swag/cmd/swag@latest

docs:
	cd examples/rewind_example && \
	swag init --parseDependency

vendor:
	go mod tidy && go mod vendor

push:
	git add . && codegpt commit . && git push
