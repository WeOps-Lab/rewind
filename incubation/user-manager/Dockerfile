FROM golang:1.23.0 AS builder
WORKDIR /app/rewind
RUN apt-get update && \
    apt-get install -y curl pkg-config libssl-dev ca-certificates  &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
ADD . .

RUN go install github.com/swaggo/swag/cmd/swag@latest
RUN cd incubation/user-manager && \
    swag init --parseDependency
RUN cd incubation/user-manager && \
    go mod tidy && go mod vendor && go build -o /app/user-manager

FROM ubuntu
WORKDIR /app
COPY --from=builder /app/user-manager .

ADD ./incubation/user-manager/entrypoint.sh /entrypoint.sh
ADD ./incubation/user-manager/localize localize

RUN chmod 777 /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]



