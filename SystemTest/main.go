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
	fmt.Println("script started")
	request, err := http.NewRequest("GET", createUrl("product/items/1"), nil)
	if err != nil {
		panic(fmt.Errorf("NewRequest failed: %v", err))
	}
	do, err := http.DefaultClient.Do(request)
	if err != nil {
		panic(fmt.Errorf("DoClient failed: %v", err))
	}

	all, err := io.ReadAll(do.Body)
	if err != nil {
		panic(fmt.Errorf("ReadAll all failed: %v", err))
	}
	fmt.Printf("status code was [%v]\n", do.StatusCode)
	fmt.Printf("response is [%v]\n", string(all))
}

func createUrl(route string) string {
	return fmt.Sprintf("%s/%s", BaseUrl, route)
}
