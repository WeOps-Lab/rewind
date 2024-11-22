package server

import (
	"fmt"
	"github.com/go-playground/validator/v10"
	_ "github.com/go-playground/validator/v10"
)

var requestValidator = validator.New()

func ValidateRequest(request interface{}) (bool, string) {
	errs := requestValidator.Struct(request)
	if errs != nil {
		var errMsg string
		for _, err := range errs.(validator.ValidationErrors) {
			errMsg += fmt.Sprintf("Field '%s' failed validation with tag '%s'. ", err.Field(), err.Tag())
		}
		return false, errMsg
	}
	return true, ""
}
