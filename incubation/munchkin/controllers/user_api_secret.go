package controllers

import (
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"github.com/WeOps-Lab/rewind/lib/web/server"
	"github.com/gofiber/fiber/v2"
	"munchkin/entity"
	"munchkin/models"
)

type UserApiSecretController struct{}

// List @Tags user_api_secret
// @Router /reqApi/internal/user_api_secret/ [get]
// @Accept json
// @Produce json
// @Success 200 {object} entity.UserApiSecretItemResponse
func (receiver UserApiSecretController) List(c *fiber.Ctx) error {
	// 获取当前访问接口的用户信息
	username := c.Locals("account").(string)
	// 如果有 username 参数，则添加模糊搜索
	c.Request().URI().QueryArgs().Add("username", username)

	return server.ListEntities[models.UserAPISecret, entity.UserApiSecretItemResponse](c)
}

// GenerateApiSecret @Tags user_api_secret
// @Router /reqApi/internal/user_api_secret/generate_api_secret/ [post]
// @Accept json
// @Produce json
// @Success 200 {object} interface{}
func (receiver UserApiSecretController) GenerateApiSecret(c *fiber.Ctx) error {
	data := map[string]string{}
	data["api_secret"], _ = GenerateAPISecret()
	return c.JSON(data)
}

func GenerateAPISecret() (string, error) {
	// Create a byte slice to hold the random bytes
	bytes := make([]byte, 32) // 32 bytes give 64 hex characters
	_, err := rand.Read(bytes)
	if err != nil {
		return "", err
	}

	// Encode the bytes as a hexadecimal string
	return hex.EncodeToString(bytes), nil
}

// CreateEntity @Tags user_api_secret
// @Router /reqApi/internal/user_api_secret/ [post]
// @Accept json
// @Produce json
// @Success 200 {object} interface{}
func (receiver UserApiSecretController) CreateEntity(c *fiber.Ctx) error {
	username := c.Locals("account").(string)
	apiSecret, _ := GenerateAPISecret()
	var body entity.CreateRequest
	if err := c.BodyParser(&body); err != nil {
		return err
	}
	// 修改请求体，添加新的字段
	body.ApiSecret = apiSecret
	body.Username = username
	modifiedBody, err := json.Marshal(body)
	if err != nil {
		return err
	}
	// 重置请求体
	c.Request().SetBody(modifiedBody)

	req, err := server.ParseAndValidateRequest[entity.CreateRequest](c)
	if err != nil {
		return err
	}

	var userApiSecret models.UserAPISecret
	if err := server.CopyRequestToModel(c, req, &userApiSecret); err != nil {
		return err
	}
	return server.InsertEntity[models.UserAPISecret](c, &userApiSecret)
}
