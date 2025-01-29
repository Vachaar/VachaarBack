package main

import (
	"bytes"
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	_ "github.com/lib/pq"
	"io"
	"net/http"
	"time"
)

const (
	BaseUrl          = "http://0.0.0.0:8080"
	testUserPassword = "password"
	testUserEmail    = "mohamadkhalafi.82@gmail.com"
)

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
		panic(err)
	}
	fmt.Println("user token is:", login)

	item, err := client.getProductItem(1)
	if err != nil {
		panic(err)
	}
	fmt.Println(item)

}

func AddTwoUsersToDatabaseForTest() {
	open, err := sql.Open("postgres", "postgres://postgres:postgres@0.0.0.0:5432/test_db?sslmode=disable")
	if err != nil {
		panic(err)
	}
	defer open.Close()
	_, err = open.Exec("INSERT INTO public.user_user(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, national_id, phone, address, is_email_verified, verification_code, verification_code_expires_at, sso_user_id, is_banned)\n  VALUES ($1, null, false, $2, '','', $2, false, true, NOW() , null, '09373668000', null, true, null, null, 1, false)", testUserPassword, testUserEmail)
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
		return nil, fmt.Errorf("status code was [%v]", get.StatusCode)
	}
	var result GetAllItemsResponse
	err = json.Unmarshal(all, &result)
	if err != nil {
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
	get, err := s.c.Do(newRequest)
	if err != nil {
		return "", err
	}
	all, err := json.Marshal(get.Cookies())
	if err != nil {
		return "", err
	}
	fmt.Println("cookies response is ", string(all))

	if get.StatusCode != http.StatusOK {
		fmt.Printf("status code was [%v]\n", get.StatusCode)
		return "", fmt.Errorf("status code was [%v]", get.StatusCode)
	}
	if len(get.Cookies()) == 0 {
		return "", errors.New("no cookies found")
	}

	return get.Cookies()[0].Value, nil
}
