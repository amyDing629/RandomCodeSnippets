// Author: Harsh Nayyar
// Copyright 2017 - PocketHealth

package main

import(
	"net/http"
	"html/template"
)

var LISTENING_PORT = "80"

type RegisterConfirmPage struct {
	Name string 
	Email string 
	Tel string 
        Col string 
}

func handleRegisterConfirm(w http.ResponseWriter, r *http.Request) {
	if (r.Method == "POST") {
		registerConfirmPage := RegisterConfirmPage{
			Name: r.FormValue("name"),
			Email: r.FormValue("email"),
			Tel: r.FormValue("tel"),
                        Col: r.FormValue("col"),
		}
                t, _ := template.ParseFiles("tmpl/registerconfirm.html")
        	t.Execute(w, registerConfirmPage)
	} else {
		w.Header().Set("Allow", "POST")
                w.WriteHeader(http.StatusMethodNotAllowed)
                return
	}
}

func handleDefault(w http.ResponseWriter, r *http.Request) {
	t, _ := template.ParseFiles("tmpl/default.html")
	t.Execute(w, "")
}

func handleRegister(w http.ResponseWriter, r *http.Request) {
        if (r.Method == "GET") {
	   http.ServeFile(w, r, "tmpl/form.html")
	}
}

func main() {
        mux := http.NewServeMux()
        mux.HandleFunc("/", handleDefault)
        mux.HandleFunc("/register", handleRegister)
        mux.HandleFunc("/registerconfirm", handleRegisterConfirm)
        mux.Handle("/assets/", http.StripPrefix("/assets/", http.FileServer(http.Dir("assets"))))
        
	// specify listening port
	server := &http.Server{Addr: ":" + LISTENING_PORT, Handler: mux}
	// start the server, listening to LISTENING_PORT
        server.ListenAndServe()
}


