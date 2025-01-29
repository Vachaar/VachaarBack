package main

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
