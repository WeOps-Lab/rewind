package controllers

import (
	"context"
	"github.com/Nerzal/gocloak/v13"
	"github.com/gofiber/fiber/v2"
	"user-manager/global"
)

type GroupController struct {
}

// @Tags Group
// @Router /reqApi/internal/group/list [get]
// @Accept json
// @Produce json
// @Success 200 {object} []gocloak.Group
func (receiver GroupController) List(c *fiber.Ctx) error {
	groups, err := global.KeycloakAdminClient.Client.GetGroups(context.Background(),
		global.KeycloakAdminClient.Token.AccessToken,
		global.KeycloakAdminClient.Realm, gocloak.GetGroupsParams{})
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"message": err.Error(),
		})
	}
	return c.Status(fiber.StatusOK).JSON(groups)
}
