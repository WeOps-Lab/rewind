package keycloak

import (
	"context"

	"github.com/Nerzal/gocloak/v13"
)

type KeycloakAdminClient struct {
	token  *gocloak.JWT
	client *gocloak.GoCloak
	realm  string
	ctx    context.Context
}

func NewKeyCloakAdminClient(endpoint string, realm string, username string, password string) *KeycloakAdminClient {
	client := gocloak.NewClient(endpoint)
	ctx := context.Background()
	token, err := client.LoginAdmin(ctx, username, password, "master")
	if err != nil {
		panic(err)
	}
	return &KeycloakAdminClient{
		token:  token,
		client: client,
		realm:  realm,
		ctx:    ctx,
	}
}

// User functions
func (c *KeycloakAdminClient) CreateUser(user gocloak.User) error {
	_, err := c.client.CreateUser(c.ctx, c.token.AccessToken, c.realm, user)
	return err
}

func (c *KeycloakAdminClient) DeleteUser(userID string) error {
	return c.client.DeleteUser(c.ctx, c.token.AccessToken, c.realm, userID)
}

func (c *KeycloakAdminClient) UpdateUser(user gocloak.User) error {
	return c.client.UpdateUser(c.ctx, c.token.AccessToken, c.realm, user)
}

func (c *KeycloakAdminClient) GetUserList(page int, size int) ([]*gocloak.User, error) {
	first := size * page
	maxSize := first + size
	users, err := c.client.GetUsers(c.ctx, c.token.AccessToken, c.realm, gocloak.GetUsersParams{
		First: &first,
		Max:   &maxSize,
	})
	return users, err
}

func (c *KeycloakAdminClient) GetUserByUserName(userName string) (*gocloak.User, error) {
	users, err := c.client.GetUsers(c.ctx, c.token.AccessToken, c.realm, gocloak.GetUsersParams{
		Username: &userName,
	})
	if err != nil {
		return nil, err
	}
	return users[0], nil
}

// Role functions
func (c *KeycloakAdminClient) CreateRole(role gocloak.Role) error {
	_, err := c.client.CreateRealmRole(c.ctx, c.token.AccessToken, c.realm, role)
	return err
}

func (c *KeycloakAdminClient) DeleteRole(roleName string) error {
	return c.client.DeleteRealmRole(c.ctx, c.token.AccessToken, c.realm, roleName)
}

func (c *KeycloakAdminClient) UpdateRole(roleName string, updatedRole gocloak.Role) error {
	role, err := c.client.GetRealmRole(c.ctx, c.token.AccessToken, c.realm, roleName)
	if err != nil {
		return err
	}
	role.Name = updatedRole.Name
	role.Description = updatedRole.Description
	return c.client.UpdateRealmRole(c.ctx, c.token.AccessToken, c.realm, *role.Name, *role)
}

func (c *KeycloakAdminClient) GetRole(roleName string) (*gocloak.Role, error) {
	return c.client.GetRealmRole(c.ctx, c.token.AccessToken, c.realm, roleName)
}

func (c *KeycloakAdminClient) GetRoleList(page int, size int) ([]*gocloak.Role, error) {
	first := size * page
	maxSize := first + size
	roles, err := c.client.GetRealmRoles(c.ctx, c.token.AccessToken, c.realm, gocloak.GetRoleParams{
		First: &first,
		Max:   &maxSize,
	})
	return roles, err
}

// User-Role assignment functions
func (c *KeycloakAdminClient) AssignRoleToUser(userID string, roleName string) error {
	role, err := c.client.GetRealmRole(c.ctx, c.token.AccessToken, c.realm, roleName)
	if err != nil {
		return err
	}
	return c.client.AddRealmRoleToUser(c.ctx, c.token.AccessToken, c.realm, userID, []gocloak.Role{*role})
}

func (c *KeycloakAdminClient) RemoveRoleFromUser(userID string, roleName string) error {
	role, err := c.client.GetRealmRole(c.ctx, c.token.AccessToken, c.realm, roleName)
	if err != nil {
		return err
	}
	return c.client.DeleteRealmRoleFromUser(c.ctx, c.token.AccessToken, c.realm, userID, []gocloak.Role{*role})
}
