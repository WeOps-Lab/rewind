package controllers

import (
	"github.com/WeOps-Lab/rewind/lib/web/server"
	"github.com/gofiber/contrib/fiberi18n/v2"
	"github.com/gofiber/fiber/v2"
	"rewind_example/entity"
	"rewind_example/models"
)

type ExampleController struct{}

// @Tags Example
// @Accept json
// @Produce json
// @Success 200 {object} interface{}
// @Router /api/public/example/hello [get]
func (receiver ExampleController) HelloWorld(c *fiber.Ctx) error {
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
func (receiver ExampleController) List(c *fiber.Ctx) error {
	return server.ListEntities[models.Example, entity.ExampleItemResponse](c)
}

// @Tags Example
// @Param id path string true "id"
// @Router /api/internal/example/{id} [get]
// @Accept json
// @Produce json
// @Success 200 {object} entity.ExampleItemResponse
func (receiver ExampleController) GetEntity(c *fiber.Ctx) error {
	return server.GetEntityById[models.Example, entity.ExampleItemResponse](c)
}

// @Tags Example
// @Param id path string true "id"
// @Router /api/internal/example/{id} [delete]
// @Accept json
// @Produce json
// @Success 200 {object} interface{}
func (receiver ExampleController) DeleteEntity(c *fiber.Ctx) error {
	return server.DeleteEntityById[models.Example](c)
}

// @Tags Example
// @Param req body entity.ExampleCreateRequest true "entity"
// @Router /api/internal/example [post]
// @Accept json
// @Produce json
// @Success 200 {object} interface{}
func (receiver ExampleController) CreateEntity(c *fiber.Ctx) error {
	req, err := server.ParseAndValidateRequest[entity.ExampleCreateRequest](c)
	if err != nil {
		return err
	}

	var example models.Example
	if err := server.CopyRequestToModel(c, req, &example); err != nil {
		return err
	}

	return server.InsertEntity[models.Example](c, &example)
}

// @Tags Example
// @Produce json
// @Param req body entity.ExampleUpdateRequest true "entity"
// @Router /api/internal/example [put]
// @Accept json
// @Produce json
// @Success 200 {object} interface{}
func (receiver ExampleController) UpdateEntity(c *fiber.Ctx) error {
	req, err := server.ParseAndValidateRequest[entity.ExampleUpdateRequest](c)
	if err != nil {
		return err
	}

	m, err := server.SelectAndCopyToModel[models.Example, entity.ExampleUpdateRequest](c, req.ID, req)
	if err != nil {
		return err
	}

	return server.UpdateEntityById[models.Example](c, m)
}
