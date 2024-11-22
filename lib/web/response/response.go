package response

import "github.com/gofiber/fiber/v2"

var errorList []*Response

type Response struct {
	Code    int         `json:"code"`
	Message string      `json:"message"`
	Data    interface{} `json:"body"`
}

type ErrorBody struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
}

type FiberErrorResponse struct {
	Error []*ErrorBody `json:"errors"`
}

type ErrorResponse struct {
	Error []*Response `json:"errors"`
}

type PageResponse struct {
	Current int         `json:"current"`
	Size    int         `json:"size"`
	Total   int64       `json:"total"`
	Data    interface{} `json:"data"`
}

func HTTPResponse(httpCode int, message string, data interface{}) *Response {
	return &Response{
		Code:    httpCode,
		Message: message,
		Data:    data,
	}
}

func HTTPFiberErrorResponse(errorObj []*fiber.Error) *FiberErrorResponse {
	var errorSlice []*ErrorBody
	for i := 0; i < len(errorObj); i++ {
		errorSlice = append(errorSlice, mapToErrorOutput(errorObj[i]))
	}

	return &FiberErrorResponse{
		Error: errorSlice,
	}
}

func HTTPErrorResponse(errorObj []*Response) *ErrorResponse {
	var errorSlice []*Response
	for i := 0; i < len(errorObj); i++ {
		errorSlice = append(errorSlice, errorObj[i])
	}

	return &ErrorResponse{
		Error: errorSlice,
	}
}

func mapToErrorOutput(e *fiber.Error) *ErrorBody {
	return &ErrorBody{
		Code:    e.Code,
		Message: e.Message,
	}
}
