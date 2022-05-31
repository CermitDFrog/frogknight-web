var dicepool = []
var dicebag = [boost, ability, proficiency, setback, difficulty, challenge, force];
var dicemap = {
  [boost]: "b",
  [ability]: "a",
  [proficiency]: "p",
  [setback]: "s",
  [difficulty]: "d",
  [challenge]: "c",
  [force]: "f"
}

function renderDicePool(parent = "dice-roller-header") {
  // Clear current pool
  var parent = document.getElementById(parent);
  while (parent.firstChild) { parent.removeChild(parent.firstChild); }

  for (var i = 0; i < dicepool.length; i++) {
    // Create span for containing die element.
    var diespan = document.createElement("span");
    parent.appendChild(diespan);
    diespan.className = 'roller-span';
    var dieimg = document.createElement('img');
    diespan.appendChild(dieimg);
    dieimg.src = dicepool[i];
    dieimg.setAttribute('onClick', 'removeFromPool(' + i + ')');
    dieimg.className = 'small-dice';
  }
};

function addToPool(die) {
  dicepool.push(dicebag[die]);
  renderDicePool('dice-pool', 'remove', dicepool)
};

function removeFromPool(die) {
  dicepool.splice(die, 1);
  renderDicePool('dice-pool', 'remove', dicepool)
};

function rollPool() {
  renderDicePool('dice-pool', 'remove', dicepool);
  var rollstring = '';
  for (var i = 0; i < dicepool.length; i++) {
    rollstring = rollstring.concat(dicemap[dicepool[i]]);
  }
  var results = httpGet('/swcs/rest/roll?dicepool=' + rollstring);
  var restext = ''
  var pool = document.getElementById("dice-pool");
  for (let key in results) {
    if (key === 'face') {
      var children = pool.children;
      for (var i = 0; i < children.length; i++) {
        var dicetext = document.createElement('p');
        dicetext.className = 'response-text';
        var dicetextval = document.createTextNode(results[key][i])
        dicetext.appendChild(dicetextval);
        children[i].appendChild(dicetext);
      }
      continue;
    }
    let value = results[key];
    restext = restext + key + ': ' + value + ' ';
  }
  var parent = document.getElementById("dice-roller-results");
  while (parent.firstChild) { parent.removeChild(parent.firstChild); }
  var resultselement = document.createTextNode(restext)
  // resultselement.className = 'respons-text';
  parent.appendChild(resultselement)
};

function httpGet(theUrl) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("GET", theUrl, false); // false for synchronous request
  xmlHttp.send(null);

  return JSON.parse(xmlHttp.responseText);
};

function clearDicePool() {
  dicepool = [];
  var parent = document.getElementById('dice-pool');
  while (parent.firstChild) { parent.removeChild(parent.firstChild); }
  var parent = document.getElementById("dice-roller-results");
  while (parent.firstChild) { parent.removeChild(parent.firstChild); }
};