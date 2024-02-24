const year_from = document.querySelector("#id_year_from");
const year_to = document.querySelector("#id_year_to");
const searchSubmitBtn = document.querySelector("#searchSubmit");

if (year_from && year_to && searchSubmitBtn) {
  const from = year_from.addEventListener("change", check);
  const to = year_to.addEventListener("change", check);

  function check() {
    const from = Number(year_from.value);
    const to = Number(year_to.value);
    if (to >= from) {
      searchSubmitBtn.removeAttribute("disabled");
    } else {
      searchSubmitBtn.setAttribute("disabled", true);
    }
  }
}
