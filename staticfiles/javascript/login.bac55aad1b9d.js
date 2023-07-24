const logo = document.querySelector(".logo-move");
const content = document.querySelector(".content-static");
const submit = document.querySelector("#submited");
const companyName = document.querySelector(".comp");
console.log(companyName);
const playAnimation = submit.addEventListener("click", function () {
  logo.classList.add("animation");
  content.classList.add("content");
  companyName.classList.add("animation");
});
