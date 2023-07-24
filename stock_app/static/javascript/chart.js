function solve() {
  let x = document.getElementById("number_1").value;
  let y = document.getElementById("number_2").value;
  let result = y - x;
  let percentage = (result / x) * 100;
  document.getElementById("result").value = "= " + result + "$";
  document.getElementById("percentage").value = percentage + "%";
}
