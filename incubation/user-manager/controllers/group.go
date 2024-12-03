package controllers

import (
	"context"
	"github.com/Nerzal/gocloak/v13"
	"github.com/WeOps-Lab/rewind/lib/pkgs/keycloak"
	"github.com/gofiber/fiber/v2"
)

type GroupController struct {
}

// @Tags GroupList
// @Router /user-manager/internal/group/list [get]
// @Accept json
// @Produce json
// @Success 200 {object} []entity.GroupRes
func (receiver GroupController) List(c *fiber.Ctx) error {
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	groups, err := adminClient.Client.GetGroups(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		gocloak.GetGroupsParams{},
	)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"message": err.Error(),
		})
	}
	return c.Status(fiber.StatusOK).JSON(groups)
}

// @Tags UserGroup
// @Router /user-manager/internal/group/{userId}/list [get]
// @Accept json
// @Produce json
// @Param userId path string true "User ID"
// @Success 200 {object} []entity.GroupRes
func (receiver GroupController) ListByUserId(c *fiber.Ctx) error {
	userId := c.Params("userId")
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	groups, err := adminClient.Client.GetUserGroups(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		userId,
		gocloak.GetGroupsParams{},
	)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"message": err.Error(),
		})
	}
	return c.Status(fiber.StatusOK).JSON(groups)
}

// @Tags GroupCreate
// @Router /user-manager/internal/group [post]
// @Accept json
// @Produce json
// @Param group body entity.GroupReq true "Group"
// @Success 200 {object} entity.GroupIdRes
func (receiver GroupController) Create(c *fiber.Ctx) error {
	var group gocloak.Group
	if err := c.BodyParser(&group); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"message": "Invalid request body",
		})
	}
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	groupId, err := adminClient.Client.CreateGroup(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		group,
	)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"message": err.Error(),
		})
	}
	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"Id": groupId,
	})
}

// @Tags CreateChildGroup
// @Router /user-manager/internal/group/{groupId}/child [post]
// @Accept json
// @Produce json
// @Param parentId path string true "Parent ID"
// @Param group body entity.GroupReq true "Group"
// @Success 200 {object} entity.GroupIdRes
func (receiver GroupController) CreateChildGroup(c *fiber.Ctx) error {
	parentId := c.Params("groupId")
	var group gocloak.Group
	if err := c.BodyParser(&group); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"message": "Invalid request body",
		})
	}
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	groupId, err := adminClient.Client.CreateChildGroup(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		parentId,
		group,
	)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"message": err.Error(),
		})
	}
	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"Id": groupId,
	})
}

// @Tags GroupUpdate
// @Router /user-manager/internal/group/{groupId} [put]
// @Accept json
// @Produce json
// @Param groupId path string true "Group ID"
// @Param group body entity.GroupReq true "Group"
// @Success 200 {object} entity.GroupActionRes
func (receiver GroupController) Update(c *fiber.Ctx) error {
	groupId := c.Params("groupId")
	var group gocloak.Group
	if err := c.BodyParser(&group); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"message": "Invalid request body",
		})
	}
	group.ID = &groupId
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	err := adminClient.Client.UpdateGroup(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		group,
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

// @Tags GroupDelete
// @Router /user-manager/internal/group/{groupId} [delete]
// @Accept json
// @Produce json
// @Param groupId path string true "Group ID"
// @Success 200 {object} entity.GroupActionRes
func (receiver GroupController) Delete(c *fiber.Ctx) error {
	groupId := c.Params("groupId")
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	err := adminClient.Client.DeleteGroup(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		groupId,
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
