package main

import (
	"fmt"
	"io"
	"net/http"
)

const (
	BaseUrl = "http://localhost:8080"
)

func main() {
	url := createUrl("product/items/1")
	fmt.Println("script started,", url)
	get, err := http.Get(url)
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
