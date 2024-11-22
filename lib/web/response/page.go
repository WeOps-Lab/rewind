package response

import (
	"github.com/gofiber/fiber/v2"
	"github.com/gookit/goutil"
	"net/url"
)

type PageEntity struct {
	Current int   `json:"current"`
	Size    int   `json:"size"`
	Total   int64 `json:"total"`
}

func ExtractPageParam(c *fiber.Ctx) (int, int, url.Values) {
	current := c.Query("current", "0")
	size := c.Query("size", "10")

	queryParams := c.Queries()
	urlValues := make(url.Values)

	for key, value := range queryParams {
		urlValues.Add(key, value)
	}

	return goutil.Int(current), goutil.Int(size), urlValues
}
