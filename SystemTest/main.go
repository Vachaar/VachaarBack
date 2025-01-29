package main

import (
	"fmt"
	"io"
	"net/http"
	"time"
)

const (
	BaseUrl = "http://localhost:8080"
)

func main() {
	url := createUrl("product/items/1")
	fmt.Println("script started,", url)
	c := http.Client{Timeout: 10 * time.Second}
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
