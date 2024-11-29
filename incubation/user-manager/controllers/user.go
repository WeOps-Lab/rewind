package controllers

import (
	"context"
	"github.com/Nerzal/gocloak/v13"
	"github.com/WeOps-Lab/rewind/lib/pkgs/keycloak"
	"github.com/gofiber/fiber/v2"
)

type UserController struct {
}

// @Tags CreateUser
// @Router /internal/user [post]
// @Accept json
// @Produce json
// @Success 200 {object} string
// @Param username query string true "Username"
// @Param email query string true "Email"
// @Param firstName query string true "First Name"
// @Param lastName query string true "Last Name"
func (receiver UserController) Create(c *fiber.Ctx) error {
	username := c.Query("username")
	email := c.Query("email")
	firstName := c.Query("firstName")
	lastName := c.Query("lastName")
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	userId, err := adminClient.Client.CreateUser(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		gocloak.User{
			Username:  &username,
			Email:     &email,
			FirstName: &firstName,
			LastName:  &lastName,
		},
	)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"message": err.Error(),
		})
	}
	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"userId": userId,
	})
}

// @Tags SetPassword
// @Router /internal/user/{userId}/password [put]
// @Accept json
// @Produce json
// @Success 200 {object} string
// @Param userId path string true "User ID"
// @Param password query string true "Password"
func (receiver UserController) SetPassword(c *fiber.Ctx) error {
	userId := c.Params("userId")
	password := c.Query("password")
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	err := adminClient.Client.SetPassword(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		userId,
		password,
		false,
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

// @Tags UpdateUser
// @Router /internal/user/{userId} [put]
// @Accept json
// @Produce json
// @Success 200 {object} string
// @Param userId path string true "User ID"
// @Param username query string true "Username"
// @Param email query string true "Email"
// @Param firstName query string true "First Name"
// @Param lastName query string true "Last Name"
func (receiver UserController) Update(c *fiber.Ctx) error {
	userId := c.Params("userId")
	username := c.Query("username")
	email := c.Query("email")
	firstName := c.Query("firstName")
	lastName := c.Query("lastName")
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	err := adminClient.Client.UpdateUser(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		gocloak.User{
			ID:        &userId,
			Username:  &username,
			Email:     &email,
			FirstName: &firstName,
			LastName:  &lastName,
		},
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

// @Tags DeleteUser
// @Router /internal/user/{userId} [delete]
// @Accept json
// @Produce json
// @Success 200 {object} string
// @Param userId path string true "User ID"
func (receiver UserController) Delete(c *fiber.Ctx) error {
	userId := c.Params("userId")
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	err := adminClient.Client.DeleteUser(
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
	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"message": "success",
	})
}

// @Tags UserList
// @Router /internal/user/list [get]
// @Accept json
// @Produce json
// @Param search query string false "Search"
// @Param page query int false "Page"
// @Param page_size query int false "Page Size"
// @Success 200 {object} []gocloak.User
func (receiver UserController) List(c *fiber.Ctx) error {
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	search := c.Query("search")
	page := c.QueryInt("page", 1)
	pageSize := c.QueryInt("page_size", 10)
	_first := (page - 1) * pageSize
	_max := page * pageSize
	users, err := adminClient.Client.GetUsers(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		gocloak.GetUsersParams{
			Search: &search,
			First:  &_first,
			Max:    &_max,
		},
	)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"message": err.Error(),
		})
	}
	userCount, err := adminClient.Client.GetUserCount(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		gocloak.GetUsersParams{
			Search: &search,
		},
	)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"message": err.Error(),
		})
	}
	userMap := make(map[string]interface{})
	userMap["count"] = userCount
	userMap["users"] = users

	return c.Status(fiber.StatusOK).JSON(userMap)
}

// @Tags AddUserToGroup
// @Router /internal/user/{userId}/group/{groupId} [post]
// @Accept json
// @Produce json
// @Success 200 {object} string
// @Param userId path string true "User ID"
// @Param groupId path string true "Group ID"
func (receiver UserController) AddUserToGroup(c *fiber.Ctx) error {
	userId := c.Params("userId")
	groupId := c.Params("groupId")
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	err := adminClient.Client.AddUserToGroup(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		userId,
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

// @Tags DeleteUserFromGroup
// @Router /internal/user/{userId}/group/{groupId} [delete]
// @Accept json
// @Produce json
// @Success 200 {object} string
// @Param userId path string true "User ID"
// @Param groupId path string true "Group ID"
func (receiver UserController) DeleteUserFromGroup(c *fiber.Ctx) error {
	userId := c.Params("userId")
	groupId := c.Params("groupId")
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	err := adminClient.Client.DeleteUserFromGroup(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		userId,
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

// @Tags AddRealmRoleToUser
// @Router /internal/user/{userId}/add_roles [post]
// @Accept json
// @Produce json
// @Success 200 {object} string
// @Param userId path string true "User ID"
// @Param roles body []gocloak.Role true "Roles"
func (receiver UserController) AddRoleToUser(c *fiber.Ctx) error {
	userId := c.Params("userId")
	var roles []gocloak.Role
	if err := c.BodyParser(&roles); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"message": "Invalid request body",
		})
	}
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	err := adminClient.Client.AddRealmRoleToUser(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		userId,
		roles,
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

// @Tags RemoveRoleFromUser
// @Router /internal/user/{userId}/remove_roles [post]
// @Accept json
// @Produce json
// @Success 200 {object} string
// @Param userId path string true "User ID"
// @Param roles body []gocloak.Role true "Roles"
func (receiver UserController) RemoveRoleFromUser(c *fiber.Ctx) error {
	userId := c.Params("userId")
	var roles []gocloak.Role
	if err := c.BodyParser(&roles); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"message": "Invalid request body",
		})
	}
	adminClient := keycloak.NewKeyCloakAdminClientFromEnv()
	err := adminClient.Client.DeleteRealmRoleFromUser(
		context.Background(),
		adminClient.Token.AccessToken,
		adminClient.Realm,
		userId,
		roles,
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
