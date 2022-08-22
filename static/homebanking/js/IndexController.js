/**
 * IndexController.js
 *
 * @file  The Index Controller
 * @author Tomás Sánchez
 * @since  06.12.2022
 */

const API_URL = "https://www.dolarsi.com/api/api.php?type=valoresprincipales";

class Dollar {
  constructor(b = "--", s = "--") {
    this.buy = b;
    this.sell = s;
  }
}

(function IndexController() {
  getDollar();
})();

function getDollar() {
  fetch(API_URL)
    .then((data) =>
      data
        .json()
        .then((result) => {
          updateDollar(result.map((x) => x.casa));
        })
        .catch((e) => console.error(e))
    )
    .catch((e) => console.error(e));
}

/**
 * Updates Dollar Data.
 *
 * @param {{official: Dollar, mep: Dollar}} data the dollar data
 */
function updateDollar(data) {
  updateHeader(data);
  updateBody(data);
}
// FUNCTION APIS

//Function with Dolar Today
function dollarToday(dollar) {
  var buyTodayDollar = document.getElementById("dollar-today-buy-header");
  var sellTodayDollar = document.getElementById("dollar-today-sell-header");
  buyTodayDollar.innerHTML = `${dollar.compra}`;
  sellTodayDollar.innerHTML = `${dollar.venta}`;
}

function dollarMEP(dollar) {
  var buyTodayDollar = document.getElementById("dollar-mep-buy-header");
  var sellTodayDollar = document.getElementById("dollar-mep-sell-header");
  buyTodayDollar.innerHTML = `${dollar.compra}`;
  sellTodayDollar.innerHTML = `${dollar.venta}`;
}

function updateHeader(data) {
  dollarToday(data[0]);
  dollarMEP(data[1]);
}

// TODO:
function updateBody(data) {
  data.forEach((dollar) => updateHTMLBody(dollar));
}

function updateHTMLBody(dollar) {
  const hashDollar = {
    "Dolar Oficial": "dolar-oficial",
    "Dolar Blue": "dolar-blue",
    "Dolar Contado con Liqui": "dolar-ccl",
    "Dolar Bolsa": "dolar-bolsa",
    "Dolar Soja": "dolar-soja",
    "Dolar turista": "dolar-turista",
  };

  let hashValue = hashDollar[dollar.nombre];

  if (hashValue) {
    updateDollarToday(dollar, hashValue);
  }
}

function updateDollarToday(dollar, name) {
  var htmlSell = document.getElementById(`${name}-hoy-venta`);
  var htmlBuy = document.getElementById(`${name}-hoy-compra`);

  htmlSell.innerHTML = `${dollar.venta}`;
  htmlBuy.innerHTML = `${dollar.compra}`;
}
