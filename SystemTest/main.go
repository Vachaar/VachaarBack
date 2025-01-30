package main

import (
	"bytes"
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	_ "github.com/lib/pq"
	"io"
	"log"
	"net/http"
	"sync"
	"time"
)

const (
	BaseUrl          = "http://0.0.0.0:8080"
	databasePassword = "pbkdf2_sha256$870000$CkB2Fb1DEWX2DnlcziFS2U$RsOjB+9W7wNEwNqoMSgj/Tp1M5aeSwyZgvCWeUFe5OU="
	testUserPassword = "ALiAhmad100%"
	testUserEmail    = "mohamadkhalafi.82@gmail.com"
)

type Item struct {
	Id          int    `json:"id"`
	Title       string `json:"title"`
	CategoryId  int    `json:"category_id"`
	Price       string `json:"price"`
	Description string `json:"description"`
	ImageIds    []int  `json:"image_ids"`
}

type Banner struct {
	ImageId int `json:"image_id"`
	Order   int `json:"order"`
}

type CreateItemRequest struct {
	Title       string   `json:"title"`
	Category    int      `json:"category"`
	Price       int      `json:"price"`
	Description string   `json:"description"`
	Banners     []Banner `json:"banners"`
}

type GetAllItemsResponse struct {
	Count   int `json:"count"`
	Results struct {
		Items    []Item `json:"items"`
		MaxPrice int    `json:"max_price"`
	} `json:"results"`
}

type LoginRequest struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type ServiceClient struct {
	c *http.Client
}

func NewServiceClient() *ServiceClient {
	return &ServiceClient{
		c: &http.Client{
			Timeout: 10 * time.Second,
		},
	}
}

func main() {
	AddTwoUsersToDatabaseForTest()
	client := NewServiceClient()
	login, err := client.Login()
	if err != nil {
		log.Println("Login failed:", err)
	}
	log.Println("Token:", login)
	var wg sync.WaitGroup
	wg.Add(10)
	for i := 0; i < 10; i++ {
		go func() {
			var err error
			defer wg.Done()
			items, err := client.GetAllItems()
			if err != nil {
				log.Println("GetAllItems failed:", err)
				return
			}
			marshal, err := json.Marshal(items)
			if err != nil {
				log.Println("Marshal failed:", err)
				return
			}
			fmt.Println(string(marshal))
		}()
	}
	wg.Wait()

}

func AddTwoUsersToDatabaseForTest() {
	open, err := sql.Open("postgres", "postgres://postgres:postgres@0.0.0.0:5432/test_db?sslmode=disable")
	if err != nil {
		panic(err)
	}
	defer open.Close()
	_, err = open.Exec("INSERT INTO public.user_user(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, national_id, phone, address, is_email_verified, verification_code, verification_code_expires_at, sso_user_id, is_banned)\n  VALUES ($1, null, false, $2, '','', $2, false, true, NOW() , null, '09373668000', null, true, null, null, 1, false)", databasePassword, testUserEmail)
	if err != nil {
		panic(err)
	}
}

func (s *ServiceClient) getProductItem(itemId int) (*Item, error) {
	url := createUrl(fmt.Sprintf("product/items/%d", itemId))

	get, err := s.c.Get(url)
	if err != nil {
		return nil, err
	}

	all, err := io.ReadAll(get.Body)
	if err != nil {
		return nil, err
	}

	if get.StatusCode != http.StatusOK {
		fmt.Printf("status code was [%v]\n", get.StatusCode)
		return nil, fmt.Errorf("status code was [%v]", get.StatusCode)
	}
	var result Item
	err = json.Unmarshal(all, &result)
	if err != nil {
		return nil, err
	}
	fmt.Printf("response is [%v]\n", string(all))
	return &result, nil

}

func (s *ServiceClient) CreateNewItem(request CreateItemRequest) error {
	marshal, err := json.Marshal(request)
	if err != nil {
		return err
	}

	newRequest, err := http.NewRequest(http.MethodPost, createUrl("product/items/create"), bytes.NewBuffer(marshal))
	if err != nil {
		return err
	}
	do, err := s.c.Do(newRequest)
	if err != nil {
		return err
	}
	if do.StatusCode != http.StatusOK {
		return fmt.Errorf("status code was [%v]", do.StatusCode)
	}
	return nil
}

func (s *ServiceClient) GetAllItems() (*GetAllItemsResponse, error) {
	///product/items
	url := createUrl(fmt.Sprintf("product/items"))

	get, err := s.c.Get(url)
	if err != nil {
		return nil, err
	}

	all, err := io.ReadAll(get.Body)
	if err != nil {
		return nil, err
	}

	if get.StatusCode != http.StatusOK {
		fmt.Printf("status code was [%v]\n", get.StatusCode)
		log.Println("body was:", string(all))
		panic("djsclds")
		return nil, fmt.Errorf("status code was [%v]", get.StatusCode)
	}
	var result GetAllItemsResponse
	err = json.Unmarshal(all, &result)
	if err != nil {
		log.Println("Unmarshal failed:", err)
		log.Println("body was:", string(all))
		return nil, err
	}
	fmt.Printf("response is [%v]\n", string(all))
	return &result, nil
}

func (s *ServiceClient) Login() (string, error) {
	///product/items
	url := createUrl(fmt.Sprintf("usr/login"))

	request := LoginRequest{
		Email:    testUserEmail,
		Password: testUserPassword,
	}
	marshal, err := json.Marshal(request)
	if err != nil {
		return "", err
	}

	newRequest, err := http.NewRequest(http.MethodPost, url, bytes.NewBuffer(marshal))
	if err != nil {
		return "", err
	}
	newRequest.Header.Set("Content-Type", "application/json")
	newRequest.Header.Set("Host", "localhost")

	fmt.Println("inja1", newRequest.Header.Get("Host"))
	fmt.Println("inja2", newRequest.Header.Get("Content-Type"))

	get, err := s.c.Do(newRequest)
	if err != nil {
		return "", err
	}
	all, err := json.Marshal(get.Cookies())
	if err != nil {
		return "", err
	}
	fmt.Println("cookies response is ", string(all))

	defer get.Body.Close()
	readAll, err := io.ReadAll(get.Body)
	if err != nil {
		return "", err
	}

	if get.StatusCode != http.StatusOK {
		fmt.Printf("status code was [%v]\n", get.StatusCode)
		fmt.Println("body was:", string(readAll))
		return "", fmt.Errorf("status code was [%v]", get.StatusCode)
	}
	if len(get.Cookies()) == 0 {
		return "", errors.New("no cookies found")
	}

	return get.Cookies()[0].Value, nil
}

func createUrl(route string) string {
	return fmt.Sprintf("%s/%s", BaseUrl, route)
}
