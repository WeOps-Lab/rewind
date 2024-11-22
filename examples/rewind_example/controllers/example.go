package controllers

import (
	"github.com/WeOps-Lab/rewind/lib/web/response"
	"github.com/acmestack/gorm-plus/gplus"
	"github.com/gofiber/contrib/fiberi18n/v2"
	"github.com/gofiber/fiber/v2"
	"net/http"
	"rewind_example/entity"
	"rewind_example/models"
)

// @Tags Example
// @Accept json
// @Produce json
// @Success 200 {object} interface{}
// @Router /api/v1/example/hello [get]
func HelloWorld(c *fiber.Ctx) error {
	helloMsg, _ := fiberi18n.Localize(c, "hello")

	m := map[string]interface{}{}
	m["hello"] = helloMsg
	m["account"] = c.Locals("account")
	m["displayName"] = c.Locals("displayName")
	return c.JSON(m)
}

// @Tags Example
// @Router /api/v1/example/list [get]
// @Accept json
// @Produce json
// @Success 200 {object} entity.ExampleListEntity
func List(c *fiber.Ctx) error {
	current, size, urlValues := response.ExtractPageParam(c)

	pagerList, _ := gplus.SelectPage(
		gplus.NewPage[models.Example](current, size),
		gplus.BuildQuery[models.Example](urlValues))

	responseData := entity.ExampleListEntity{
		PageEntity: response.PageEntity{
			Current: pagerList.Current,
			Size:    pagerList.Size,
			Total:   pagerList.Total,
		},
		Items: []entity.ExampleWrapperEntity{},
	}

	for _, target := range pagerList.Records {
		responseData.Items = append(responseData.Items, entity.ExampleWrapperEntity{
			ID: target.ID,
			ExampleEntity: entity.ExampleEntity{
				Name: target.Name,
			},
		})
	}

	return c.JSON(responseData)
}

// @Tags Example
// @Param id path string true "id"
// @Router /api/v1/example/{id} [get]
// @Accept json
// @Produce json
// @Success 200 {object} entity.ExampleWrapperEntity
func GetEntity(c *fiber.Ctx) error {
	id := c.Params("id")

	m, _ := gplus.SelectById[models.Example](id)
	target := entity.ExampleWrapperEntity{
		ID: m.ID,
		ExampleEntity: entity.ExampleEntity{
			Name: m.Name,
		},
	}

	return c.JSON(target)
}

// @Tags Example
// @Param id path string true "id"
// @Router /api/v1/example/{id} [delete]
// @Accept json
// @Produce json
// @Success 200 {object} interface{}
func DeleteEntity(c *fiber.Ctx) error {
	id := c.Params("id")

	err := gplus.DeleteById[models.Example](id).Error
	if err != nil {
		return c.SendStatus(http.StatusInternalServerError)
	}

	return c.SendStatus(http.StatusOK)
}

// @Tags Example
// @Param req body entity.ExampleEntity true "entity"
// @Router /api/v1/example [post]
// @Accept json
// @Produce json
// @Success 200 {object} interface{}
func CreateEntity(c *fiber.Ctx) error {
	m := entity.ExampleEntity{}
	if err := c.BodyParser(&m); err != nil {
		return c.SendStatus(http.StatusBadRequest)
	}

	err := gplus.Insert[models.Example](&models.Example{
		Name: m.Name,
	}).Error
	if err != nil {
		return c.SendStatus(http.StatusBadRequest)
	}

	return c.SendStatus(http.StatusOK)
}

// @Tags Example
// @Produce json
// @Param req body entity.ExampleWrapperEntity true "entity"
// @Router /api/v1/example [put]
// @Accept json
// @Produce json
// @Success 200 {object} interface{}
func UpdateEntity(c *fiber.Ctx) error {
	m := entity.ExampleWrapperEntity{}
	if err := c.BodyParser(&m); err != nil {
		return c.JSON(
			response.HTTPResponse(400, "", nil),
		)
	}

	obj := &models.Example{Name: m.Name}
	obj.ID = m.ID
	err := gplus.UpdateById[models.Example](obj).Error

	if err != nil {
		return c.SendStatus(http.StatusBadRequest)
	}

	return c.SendStatus(http.StatusOK)

}
