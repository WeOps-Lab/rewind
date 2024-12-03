package entity

type GroupReq struct {
	Name string `json:"name"`
}

type GroupIdRes struct {
	Id string `json:"id"`
}

type GroupActionRes struct {
	Mes string `json:"message"`
}

type GroupRes struct {
	Id        string     `json:"id"`
	Name      string     `json:"name"`
	Path      string     `json:"path"`
	SubGroups []GroupRes `json:"subGroups"`
}
