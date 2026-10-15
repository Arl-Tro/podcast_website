"use strict";

const scrollTarget = document.querySelector("#scroll");
const rightButton = document.querySelector("#rightButton");
const leftButton = document.querySelector("#leftButton");

const scrollAmount = 100;

rightButton.addEventListener("click", (e) => {
    scrollTarget.scrollLeft += scrollAmount;
});

leftButton.addEventListener("click", (e) => {
    scrollTarget.scrollLeft -= scrollAmount;
});