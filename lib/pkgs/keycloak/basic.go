package keycloak

import (
	"context"
	"github.com/Nerzal/gocloak/v13"
)

type KeycloakBasicClient struct {
	Token        *gocloak.JWT
	Client       *gocloak.GoCloak
	Realm        string
	ClientID     string
	ClientSecret string
}

func NewKeyCloakBasicClient(endpoint string, realm string, clientID string, clientSecret string) *KeycloakBasicClient {
	client := gocloak.NewClient(endpoint)
	token, err := client.LoginClient(context.Background(), clientID, clientSecret, realm)
	if err != nil {
		panic(err)
	}
	return &KeycloakBasicClient{
		Token:        token,
		Client:       client,
		Realm:        realm,
		ClientID:     clientID,
		ClientSecret: clientSecret,
	}
}

func (receiver KeycloakBasicClient) IntrospectToken(token string) (*gocloak.IntroSpectTokenResult, error) {
	result, err := receiver.Client.RetrospectToken(context.Background(), token, receiver.ClientID, receiver.ClientSecret, receiver.Realm)
	return result, err
}

type KeyCloakUserInfo struct {
	Locale      string
	Account     string
	DisplayName string
}

func (receiver KeycloakBasicClient) DecodeToken(token string) KeyCloakUserInfo {
	_, rs, _ := receiver.Client.DecodeAccessToken(context.Background(), token, receiver.Realm)
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
	return receiver.Client.GetToken(context.Background(), receiver.Realm, gocloak.TokenOptions{
		ClientID:     &receiver.ClientID,
		ClientSecret: &receiver.ClientSecret,
		GrantType:    gocloak.StringP("password"),
		Username:     gocloak.StringP(username),
		Password:     gocloak.StringP(password),
	})
}
