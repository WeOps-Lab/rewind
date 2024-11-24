package controllers

import (
	"github.com/WeOps-Lab/rewind/lib/web/response"
	"github.com/gofiber/fiber/v2"
)

type GroupController struct{}

// @Tags Group
// @Router /reqApi/internal/group/list [get]
// @Accept json
// @Produce json
// @Success 200 {object} entity.GroupListResponse
func (receiver GroupController) List(c *fiber.Ctx) error {
	current, size, urlValues := response.ExtractPageParam(c)
}
