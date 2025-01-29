package main

import (
	"crypto/tls"
	"fmt"
	"io"
	"net"
	"net/http"
	"time"
)

const (
	BaseUrl = "http://0.0.0.0:8080"
)

func main() {
	var (
		conn *tls.Conn
		err  error
	)
	url := createUrl("product/items/1")
	fmt.Println("script started,", url)
	tlsConfig := http.DefaultTransport.(*http.Transport).TLSClientConfig

	c := &http.Client{
		Timeout: 10 * time.Second,
		Transport: &http.Transport{
			DialTLS: func(network, addr string) (net.Conn, error) {
				conn, err = tls.Dial(network, addr, tlsConfig)
				return conn, err
			},
		},
	}

	get, err := c.Get(url)
	if err != nil {
		panic(fmt.Errorf("DoClient failed: %v", err))
	}

	all, err := io.ReadAll(get.Body)
	if err != nil {
		panic(fmt.Errorf("ReadAll all failed: %v", err))
	}
	fmt.Printf("status code was [%v]\n", get.StatusCode)
	fmt.Printf("response is [%v]\n", string(all))
}

func createUrl(route string) string {
	return fmt.Sprintf("%s/%s", BaseUrl, route)
}
