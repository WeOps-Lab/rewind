package controllers

import (
	"github.com/WeOps-Lab/rewind/lib/web/response"
	"github.com/WeOps-Lab/rewind/lib/web/server"
	"github.com/acmestack/gorm-plus/gplus"
	"github.com/gofiber/contrib/fiberi18n/v2"
	"github.com/gofiber/fiber/v2"
	"github.com/jinzhu/copier"
	"net/http"
	"rewind_example/entity"
	"rewind_example/models"
)

// @Tags Example
// @Accept json
// @Produce json
// @Success 200 {object} interface{}
// @Router /api/public/example/hello [get]
func HelloWorld(c *fiber.Ctx) error {
	helloMsg, _ := fiberi18n.Localize(c, "hello")

	m := map[string]interface{}{}
	m["hello"] = helloMsg
	return c.JSON(m)
}

// @Tags Example
// @Router /api/internal/example/list [get]
// @Accept json
// @Produce json
// @Success 200 {object} entity.ExampleListResponse
func List(c *fiber.Ctx) error {
	current, size, urlValues := response.ExtractPageParam(c)

	pagerList, _ := gplus.SelectPage(
		gplus.NewPage[models.Example](current, size),
		gplus.BuildQuery[models.Example](urlValues))

	items := make([]entity.ExampleItemResponse, len(pagerList.Records))
	copier.Copy(&items, &pagerList.Records)

	responseData := entity.ExampleListResponse{
		PageEntity: response.PageEntity{
			Current: pagerList.Current,
			Size:    pagerList.Size,
			Total:   pagerList.Total,
		},
		Items: items,
	}

	return c.Status(fiber.StatusOK).JSON(responseData)
}

// @Tags Example
// @Param id path string true "id"
// @Router /api/internal/example/{id} [get]
// @Accept json
// @Produce json
// @Success 200 {object} entity.ExampleItemResponse
func GetEntity(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return c.SendStatus(fiber.StatusBadRequest)
	}

	m, t := gplus.SelectById[models.Example](id)
	if t.Error != nil {
		return c.Status(fiber.StatusNotFound).SendString(t.Error.Error())
	}

	var target entity.ExampleItemResponse
	if err := copier.Copy(&target, m); err != nil {
		return c.Status(fiber.StatusInternalServerError).SendString(err.Error())
	}

	return c.Status(fiber.StatusOK).JSON(target)
}

// @Tags Example
// @Param id path string true "id"
// @Router /api/internal/example/{id} [delete]
// @Accept json
// @Produce json
// @Success 200 {object} interface{}
func DeleteEntity(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return c.SendStatus(fiber.StatusBadRequest)
	}

	err := gplus.DeleteById[models.Example](id).Error
	if err != nil {
		return c.SendStatus(fiber.StatusInternalServerError)
	}

	return c.SendStatus(fiber.StatusOK)
}

// @Tags Example
// @Param req body entity.ExampleCreateRequest true "entity"
// @Router /api/internal/example [post]
// @Accept json
// @Produce json
// @Success 200 {object} interface{}
func CreateEntity(c *fiber.Ctx) error {
	m := entity.ExampleCreateRequest{}
	if err := c.BodyParser(&m); err != nil {
		return c.SendStatus(http.StatusBadRequest)
	}

	validate, msg := server.ValidateRequest(m)
	if !validate {
		return c.Status(fiber.StatusBadRequest).SendString(msg)
	}

	var example models.Example
	if err := copier.Copy(&example, &m); err != nil {
		return c.SendStatus(http.StatusInternalServerError)
	}

	err := gplus.Insert[models.Example](&example).Error
	if err != nil {
		return c.SendStatus(fiber.StatusBadRequest)
	}

	return c.SendStatus(fiber.StatusOK)
}

// @Tags Example
// @Produce json
// @Param req body entity.ExampleUpdateRequest true "entity"
// @Router /api/internal/example [put]
// @Accept json
// @Produce json
// @Success 200 {object} interface{}
func UpdateEntity(c *fiber.Ctx) error {
	req := entity.ExampleUpdateRequest{}
	if err := c.BodyParser(&req); err != nil {
		return c.SendStatus(fiber.StatusBadRequest)
	}

	validate, msg := server.ValidateRequest(req)
	if !validate {
		return c.Status(fiber.StatusBadRequest).SendString(msg)
	}

	m, t := gplus.SelectById[models.Example](req.ID)
	if t.Error != nil {
		return c.Status(fiber.StatusNotFound).SendString(t.Error.Error())
	}

	if err := copier.Copy(m, &req); err != nil {
		return c.Status(fiber.StatusInternalServerError).SendString(err.Error())
	}

	err := gplus.UpdateById[models.Example](m).Error
	if err != nil {
		return c.SendStatus(fiber.StatusInternalServerError)
	}

	return c.SendStatus(fiber.StatusOK)
}
