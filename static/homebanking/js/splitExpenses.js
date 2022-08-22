/**
 * splitExpenses.js
 *
 * @file  Split Expenses Script for adding items to a list
 * @author Tomás Sánchez
 * @since  05.29.2022
 */

/**
 * @type {[{name: string, amount: string}]}
 */
var aData = [];

var counter = 0;

document
  .getElementById("splitExpensesForm")
  .addEventListener("submit", function (e) {
    // Prevent Form default submit event
    e.preventDefault();
    // Obtain form Data container
    const formData = new FormData(e.target);
    // Obtain real form data {}
    const data = Object.fromEntries(formData);

    addEntryToList(data);
    updateSplit();
    e.target.reset();
  });

/**
 * Updates the values of Total and each.
 */
function updateSplit() {
  let sum = aData
    .map((d) => d.amount)
    .reduce((a, b) => Number(a) + Number(b), 0);
  let each = sum > 0 ? sum / aData.length : 0;

  document.getElementById("totalSum").innerHTML = sum.toLocaleString();
  document.getElementById("each").innerHTML = each.toLocaleString();
  document.getElementById("noOfFriends").innerHTML = aData.length;

  if (aData.length == 0) {
    document.getElementById("no-data-text").classList.remove("d-none");
  } else {
    document.getElementById("no-data-text").classList.add("d-none");
  }

  updateDownloadData();
}

/**
 * Adds an entry to the list of contributors.
 *
 * @param {{name: string, amount: number}} data the form data
 */
function addEntryToList(data) {
  var oList = document.getElementById("friendsList");

  data.id = `friend-${counter++}`;
  aData.push(data);

  var oItem = createListItem(data);

  oList.appendChild(oItem);
}

/**
 * Creates a list item to be displayed
 * @param {{id: string, name: string, amount: number}} data the form data
 * @returns {HTMLLIElement} the list item
 */
function createListItem(data) {
  var oItem = document.createElement("li");
  oItem.id = data.id;

  var sClasses =
    "list-group-item d-flex justify-content-between align-items-start p-3";
  addClasses(oItem, sClasses);

  var oAvatar = createAvatar(data);
  oItem.appendChild(oAvatar);
  var oDelete = createDelete();
  oItem.appendChild(oDelete);

  return oItem;
}

/**
 * Adds all classes to an element.
 * @param {HTMLElement} oElement an HTML element
 * @param {string} sClasses classnames seprated by space
 */
function addClasses(oElement, sClasses) {
  var aClasses = sClasses.split(" ");
  aClasses.forEach((sClass) => oElement.classList.add(sClass));
}

/**
 * Creates an Avatar.
 *
 * @param {{name: string, amount: number}} data the form data with name and amount
 * @returns a div element
 */
function createAvatar(data) {
  var oDiv = document.createElement("div");

  addClasses(oDiv, "d-flex align-items-center");

  var oImage = createImage(data);

  oDiv.appendChild(oImage);
  var oName = createName(data);
  oDiv.appendChild(oName);

  return oDiv;
}

/**
 * Creates an Styled Img
 *
 * @returns an img element
 */
function createImage(data) {
  var oImage = document.createElement("div");

  var aBgClasses = [
    "bg-blue",
    "bg-green",
    "bg-primary",
    "bg-secondary",
    "bg-warning",
    "bg-dark",
    "bg-danger",
    "bg-info",
  ];

  addClasses(
    oImage,
    `rounded-circle ${
      aBgClasses[getRandomInt(0, aBgClasses.length - 1)]
    } text-white position-relative user-select-none overflow-hidden`
  );

  oImage.style = "width: 45px; height: 45px";

  var sInitials = data.name.match(/\b\w/g).join("").toUpperCase();

  if (sInitials.length > 1)
    sInitials = sInitials[0] + sInitials[sInitials.length - 1];

  oImage.innerHTML = `<h5 class="position-absolute top-50 start-50 translate-middle">${sInitials}</h5>`;
  return oImage;
}

/**
 * Generates a div with a name.
 *
 * @param {{name: string, amount: number}} data the form data with name and amount
 * @returns {HTMLDivElement} div element
 */
function createName(data) {
  var oDiv = document.createElement("div");
  addClasses(oDiv, "ms-3");
  var oP = document.createElement("p");
  addClasses(oP, "fw-bold mb-0");
  oP.innerHTML = `${data.name}`;
  oDiv.appendChild(oP);
  var oBadge = createBadge(data);
  oDiv.appendChild(oBadge);
  return oDiv;
}

/**
 * Generates a badge with money amount.
 *
 * @param {{name: string, amount: number}} data the form data with name and amount
 * @returns {HTMLSpanElement} span badge element
 */
function createBadge(data) {
  var oSpan = document.createElement("span");

  var aBadgesClasses = [
    "badge-info",
    "badge-warning",
    "badge-danger",
    "badge-success",
    "badge-primary",
    "badge-secondary",
  ];

  addClasses(
    oSpan,
    `badge rounded-pill ${
      aBadgesClasses[getRandomInt(0, aBadgesClasses.length - 1)] || "badge-info"
    }`
  );

  oSpan.innerHTML = `$${Number(data.amount).toLocaleString()}`;

  return oSpan;
}

/**
 * Creates a delete button.
 *
 * @returns {HTMLAElement} a link delete button
 */
function createDelete() {
  var oA = document.createElement("a");
  oA.role = "button";
  oA.href = "#!";
  oIcon = document.createElement("i");
  addClasses(oIcon, "btn btn-link btn-rounded btn-sm text-dark fa-solid fa-x");
  oIcon.onclick = onDelete;
  oA.appendChild(oIcon);
  return oA;
}

/**
 * Deletes a frind of the list.
 *
 * @param {*} e an event
 */
function onDelete(e) {
  oListItem = e.target.parentElement.parentElement;
  aData = aData.filter((d) => d.id != oListItem.id);
  oListItem.remove();
  updateSplit();
}

/**
 * Generates a random Intenger number
 *
 * @param {int} min minimal value
 * @param {int} max max value
 * @returns a Random integer between the specified parameters
 */
function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Updates the download button encoded data.
 */
function updateDownloadData() {
  var sData =
    "text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(aData));
  var oButton = document.getElementById("downloadButton");
  oButton.setAttribute("href", `data:${sData}`);
}

updateDownloadData();
