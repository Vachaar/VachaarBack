package main

import "fmt"

func createUrl(route string) string {
	return fmt.Sprintf("%s/%s", BaseUrl, route)
}
