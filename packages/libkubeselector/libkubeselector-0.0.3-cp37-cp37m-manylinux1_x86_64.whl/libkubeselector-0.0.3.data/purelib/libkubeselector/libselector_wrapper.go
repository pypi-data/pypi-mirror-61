//libselector_wrapper.go
package main

import "C"

import (
	"encoding/json"
	"k8s.io/apimachinery/pkg/labels"
	 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"fmt"
)

//export match_label
func match_label(Cselector *C.char, Cls *C.char) int {
	selector := C.GoString(Cselector)
	ls := C.GoString(Cls)
	sel, err := labels.Parse(selector)
	if err != nil {
		fmt.Println(selector, " error ", err)
		return -1
	}
	l := make(map[string]string)
    if err := json.Unmarshal([]byte(ls), &l); err != nil {
		fmt.Println(err)
        return -2
	}
	 if sel.Matches(labels.Set(l)) {
	 	return 0
	 }
	return 1
}

//export match_label_selector
func match_label_selector(ClabelsSelectorString *C.char, Cls *C.char) int {
	labelsSelectorString := C.GoString(ClabelsSelectorString)
	ls := C.GoString(Cls)
	var labelsSelector struct {
		LabelSelector v1.LabelSelector `json:"labelSelector"`
	}
	if err := json.Unmarshal([]byte(labelsSelectorString), &labelsSelector); err != nil {
		fmt.Println(err)
        return -2
	}

	sel, err := v1.LabelSelectorAsSelector(&labelsSelector.LabelSelector)
	if err != nil {
		return -4
	}

	l := make(map[string]string)

    if err := json.Unmarshal([]byte(ls), &l); err != nil {
        return -3
	}
	if sel.Matches(labels.Set(l)) {
		return 0
	}
   return 1

}


func main(){
	fmt.Println("Test match_label")
	test1 := [][]string{[]string{"app in (nginx)","{\"app\": \"nginx\", \"project\": \"nibiru\"}", "true"},
		[]string{"app=nginx","{\"app\": \"nginx\", \"project\": \"nibiru\"}", "true"},
		[]string{"app in (nginx)","{\"app1\": \"nginx\", \"project\": \"nibiru\"}", "false"},
	}
	for _, val := range test1 {
		fmt.Println("test ", val, match_label(C.CString(val[0]),C.CString(val[1])) == 0 , "==", val[2])

	}
	fmt.Println("Test match_label_selector")

	
	test2 := "{\"labelSelector\":{\"matchExpressions\":[{\"key\":\"app\",\"operator\": \"In\",\"values\": [\"nginx\"]}]}}"
	
	for _, val := range test1 {
		fmt.Println("test ", test2, " ", val[1], match_label_selector(C.CString(test2), C.CString(val[1])) == 0 , "==", val[2])

	}

}
