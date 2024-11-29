package hooks

import (
	"github.com/gofiber/fiber/v2"
	"user-manager/controllers"
)

func (e ExampleAppHooks) InstallInternalRouter(router fiber.Router) {
	groupController := controllers.GroupController{}
	router.Get("/group/list", groupController.List)
	router.Get("/group/:userId/list", groupController.ListByUserId)
	router.Post("/group", groupController.Create)
	router.Post("/group/:groupId/child", groupController.CreateChildGroup)
	router.Put("/group/:groupId", groupController.Update)
	router.Delete("/group/:groupId", groupController.Delete)

	userController := controllers.UserController{}
	router.Post("/user", userController.Create)
	router.Put("/user/:userId/password", userController.SetPassword)
	router.Put("/user/:userId", userController.Update)
	router.Delete("/user/:userId", userController.Delete)
	router.Get("/user/list", userController.List)
	router.Get("/user/:userId/group/:groupId", userController.AddUserToGroup)
	router.Delete("/user/:userId/group/:groupId", userController.DeleteUserFromGroup)
	router.Post("/user/:userId/add_roles", userController.AddRoleToUser)
	router.Post("/user/:userId/remove_roles", userController.RemoveRoleFromUser)

	roleController := controllers.RoleController{}
	router.Get("/role/list", roleController.List)
	router.Post("/role", roleController.Create)
	router.Delete("/role/:roleId", roleController.Delete)
	router.Put("/role/:roleId", roleController.Update)
	router.Get("/role/:userId/list", roleController.ListByUserId)
}

func (e ExampleAppHooks) InstallPublicRouter(router fiber.Router) {
}
