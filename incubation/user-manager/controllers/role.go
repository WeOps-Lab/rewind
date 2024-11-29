package controllers

import (
	"context"
	"github.com/Nerzal/gocloak/v13"
	"github.com/WeOps-Lab/rewind/lib/pkgs/keycloak"
	"github.com/gofiber/fiber/v2"
)

type RoleController struct {
}

// @Tags RoleList
// @Router /internal/role/list [get]
// @Accept json
// @Produce json
// @Success 200 {object} []gocloak.Role
func (receiver RoleController) List(c *fiber.Ctx) error {
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	roles, err := adminClient.Client.GetRealmRoles(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		gocloak.GetRoleParams{},
	)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"message": err.Error(),
		})
	}
	return c.Status(fiber.StatusOK).JSON(roles)
}

// @Tags RoleCreate
// @Router /internal/role [post]
// @Accept json
// @Produce json
// @Success 200 {object} string
// @Param role body gocloak.Role true "Role"
func (receiver RoleController) Create(c *fiber.Ctx) error {
	var role gocloak.Role
	if err := c.BodyParser(&role); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"message": "Invalid request body",
		})
	}
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	roleId, err := adminClient.Client.CreateRealmRole(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		role,
	)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"message": err.Error(),
		})
	}
	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"roleId": roleId,
	})
}

// @Tags RoleDelete
// @Router /internal/role/{roleId} [delete]
// @Accept json
// @Produce json
// @Success 200 {object} string
// @Param roleId path string true "Role ID"
func (receiver RoleController) Delete(c *fiber.Ctx) error {
	roleId := c.Params("roleId")
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	err := adminClient.Client.DeleteRealmRole(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		roleId,
	)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"message": err.Error(),
		})
	}
	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"message": "success",
	})
}

// @Tags RoleUpdate
// @Router /internal/role/{roleId} [put]
// @Accept json
// @Produce json
// @Success 200 {object} string
// @Param roleId path string true "Role ID"
// @Param role body gocloak.Role true "Role"
func (receiver RoleController) Update(c *fiber.Ctx) error {
	roleId := c.Params("roleId")
	var role gocloak.Role
	if err := c.BodyParser(&role); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"message": "Invalid request body",
		})
	}
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	err := adminClient.Client.UpdateRealmRole(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		roleId,
		role,
	)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"message": err.Error(),
		})
	}
	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"message": "success",
	})
}

// @Tags GetRealmRolesByUserID
// @Router /internal/role/{userId}/list [get]
// @Accept json
// @Produce json
// @Success 200 {object} []gocloak.Role
// @Param userId path string true "User ID"
func (receiver RoleController) ListByUserId(c *fiber.Ctx) error {
	userId := c.Params("userId")
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	roles, err := adminClient.Client.GetRealmRolesByUserID(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		userId,
	)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"message": err.Error(),
		})
	}
	return c.Status(fiber.StatusOK).JSON(roles)
}
