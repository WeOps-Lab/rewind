FROM golang:1.23.0 AS builder
WORKDIR /app
ADD . .
RUN go install github.com/swaggo/swag/cmd/swag@latest
RUN cd incubation/user-manager && \
    swag init --parseDependency
RUN cd incubation/user-manager && \
    go mod tidy && go mod vendor && go build

FROM ubuntu
WORKDIR /app
COPY --from=builder /app/user-manager .

CMD ["./user-manager"]


