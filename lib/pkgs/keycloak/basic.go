package keycloak

import (
	"context"
	"github.com/Nerzal/gocloak/v13"
)

type KeycloakBasicClient struct {
	token        *gocloak.JWT
	client       *gocloak.GoCloak
	realm        string
	clientID     string
	clientSecret string
}

func NewKeyCloakBasicClient(endpoint string, realm string, clientID string, clientSecret string) *KeycloakBasicClient {
	client := gocloak.NewClient(endpoint)
	token, err := client.LoginClient(context.Background(), clientID, clientSecret, realm)
	if err != nil {
		panic(err)
	}
	return &KeycloakBasicClient{
		token:        token,
		client:       client,
		realm:        realm,
		clientID:     clientID,
		clientSecret: clientSecret,
	}
}

func (receiver KeycloakBasicClient) IntrospectToken(token string) (*gocloak.IntroSpectTokenResult, error) {
	result, err := receiver.client.RetrospectToken(context.Background(), token, receiver.clientID, receiver.clientSecret, receiver.realm)
	return result, err
}

type KeyCloakUserInfo struct {
	Locale      string
	Account     string
	DisplayName string
}

func (receiver KeycloakBasicClient) DecodeToken(token string) KeyCloakUserInfo {
	_, rs, _ := receiver.client.DecodeAccessToken(context.Background(), token, receiver.realm)
	claimMaps := *rs

	userLocale := "zh"
	if claimMaps["Locale"] != nil {
		userLocale = claimMaps["Locale"].(string)
	}
	userInfo := KeyCloakUserInfo{
		Locale:      userLocale,
		DisplayName: claimMaps["name"].(string),
		Account:     claimMaps["preferred_username"].(string),
	}
	return userInfo
}

func (receiver KeycloakBasicClient) GetToken(username string, password string) (*gocloak.JWT, error) {
	return receiver.client.GetToken(context.Background(), receiver.realm, gocloak.TokenOptions{
		ClientID:     &receiver.clientID,
		ClientSecret: &receiver.clientSecret,
		GrantType:    gocloak.StringP("password"),
		Username:     gocloak.StringP(username),
		Password:     gocloak.StringP(password),
	})
}
