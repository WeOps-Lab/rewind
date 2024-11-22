package server

import (
	"github.com/WeOps-Lab/rewind/lib/web/response"
	"github.com/acmestack/gorm-plus/gplus"
	"github.com/gofiber/fiber/v2"
	"github.com/jinzhu/copier"
	"net/http"
	"net/url"
	"strconv"
	"strings"
)

func DeleteEntityById[T any](c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return c.SendStatus(fiber.StatusBadRequest)
	}

	decodeIds, _ := url.QueryUnescape(id)
	ids := strings.Split(decodeIds, ",")
	intIds := make([]int, len(ids))
	for i, id := range ids {
		intId, err := strconv.Atoi(id)
		if err != nil {
			return c.Status(fiber.StatusBadRequest).SendString("Invalid ID format")
		}
		intIds[i] = intId
	}
	err := gplus.DeleteByIds[T](intIds).Error
	if err != nil {
		return c.SendStatus(fiber.StatusInternalServerError)
	}

	return c.SendStatus(fiber.StatusOK)
}

func InsertEntity[T any](c *fiber.Ctx, entity *T) error {
	err := gplus.Insert[T](entity).Error
	if err != nil {
		return c.SendStatus(fiber.StatusBadRequest)
	}

	return c.SendStatus(fiber.StatusOK)
}

func ParseAndValidateRequest[T any](c *fiber.Ctx) (*T, error) {
	var req T
	if err := c.BodyParser(&req); err != nil {
		return nil, c.SendStatus(http.StatusBadRequest)
	}

	validate, msg := ValidateRequest(req)
	if !validate {
		return nil, c.Status(fiber.StatusBadRequest).SendString(msg)
	}

	return &req, nil
}

func CopyRequestToModel[T any, U any](c *fiber.Ctx, req *T, model *U) error {
	if err := copier.Copy(model, req); err != nil {
		return c.SendStatus(fiber.StatusInternalServerError)
	}
	return nil
}

func SelectAndCopyToModel[T any, U any](c *fiber.Ctx, id uint, req *U) (*T, error) {
	m, t := gplus.SelectById[T](id)
	if t.Error != nil {
		return nil, c.Status(fiber.StatusNotFound).SendString(t.Error.Error())
	}

	if err := copier.Copy(m, req); err != nil {
		return nil, c.Status(fiber.StatusInternalServerError).SendString(err.Error())
	}

	return m, nil
}

func UpdateEntityById[T any](c *fiber.Ctx, entity *T) error {
	err := gplus.UpdateById[T](entity).Error
	if err != nil {
		return c.SendStatus(fiber.StatusInternalServerError)
	}
	return c.SendStatus(fiber.StatusOK)
}

func GetEntityById[T any, U any](c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return c.SendStatus(fiber.StatusBadRequest)
	}

	m, t := gplus.SelectById[T](id)
	if t.Error != nil {
		return c.Status(fiber.StatusNotFound).SendString(t.Error.Error())
	}

	var target U
	if err := copier.Copy(&target, m); err != nil {
		return c.Status(fiber.StatusInternalServerError).SendString(err.Error())
	}

	return c.Status(fiber.StatusOK).JSON(target)
}

func ListEntities[T any, U any](c *fiber.Ctx) error {
	current, size, urlValues := response.ExtractPageParam(c)

	pagerList, _ := gplus.SelectPage(
		gplus.NewPage[T](current, size),
		gplus.BuildQuery[T](urlValues))

	items := make([]U, len(pagerList.Records))
	copier.Copy(&items, &pagerList.Records)

	responseData := struct {
		response.PageEntity
		Items []U `json:"items"`
	}{
		PageEntity: response.PageEntity{
			Current: pagerList.Current,
			Size:    pagerList.Size,
			Total:   pagerList.Total,
		},
		Items: items,
	}

	return c.Status(fiber.StatusOK).JSON(responseData)
}
