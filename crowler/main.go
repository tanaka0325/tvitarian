package main

import (
	"fmt"
)

type Program struct {
	Id   int
	name string
	url  string
}

func getProgramInfo() []Program {
	jounetsu := Program{Id: 1, name: "情熱大陸"}
	pro := Program{Id: 2, name: "プロフェッショナル仕事の流儀"}

	programList := []Program{jounetsu, pro}
	return programList
}

func main() {
	// programList
	programList := getProgramInfo()

	// episode
	for _, program := range programList {
		fmt.Println(program)
	}
}
