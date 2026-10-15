"use strict";

const barraRicerca = document.querySelector("#ricerca");
const elementiRicerca = document.querySelectorAll("[data-ricerca]");

barraRicerca.addEventListener("input", function () {
    for (let i = 0; i < elementiRicerca.length; i++) {
        let contenuto = elementiRicerca[i].dataset.ricerca;
        if (contenuto.indexOf(barraRicerca.value) < 0) {
            elementiRicerca[i].classList.add("d-none");
        } else {
            elementiRicerca[i].classList.remove("d-none");
        }
    }
});
