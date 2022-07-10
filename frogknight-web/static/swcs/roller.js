async function httpGet(url) {
  let response = await fetch(url);
  let data = await response.json();
  return data;
}

let dicepool = []
const dicebag = [boost, ability, proficiency, setback, difficulty, challenge, force];
const dicemap = {
  [boost]: "b",
  [ability]: "a",
  [proficiency]: "p",
  [setback]: "s",
  [difficulty]: "d",
  [challenge]: "c",
  [force]: "f"
}
let character = 'unknown'

async function setCharacter() {
  character = document.getElementById('character-dropdown').value;
}

async function renderDicePool(parent = "dice-roller-header") {
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
}

async function addToPool(die) {
  dicepool.push(dicebag[die]);
  await renderDicePool('dice-pool', 'remove', dicepool)
}

async function removeFromPool(die) {
  dicepool.splice(die, 1);
  await renderDicePool('dice-pool', 'remove', dicepool)
}

async function rollPool() {
  await renderDicePool('dice-pool', 'remove', dicepool);
  var rollstring = '';
  for (var i = 0; i < dicepool.length; i++) {
    rollstring = rollstring.concat(dicemap[dicepool[i]]);
  }
  var results = await httpGet('/swcs/rest/roll?dicepool=' + rollstring +'&character='+character);
  var restext = ''
  var pool = document.getElementById("dice-pool");
  for (let key in results) {
    if (key === 'face') {
      var children = pool.children;
      for (var i = 0; i < children.length; i++) {
        var dicetext = document.createElement('p');
        dicetext.classList.add('response-text');
        if (['s', 'd'].indexOf(dicemap[dicepool[i]]) + 1) { dicetext.classList.add('setback-die'); }
        if (results[key][i].length === 1) { dicetext.classList.add('single-die'); }
        var dicetextval = document.createTextNode(results[key][i]);
        dicetext.appendChild(dicetextval);
        children[i].appendChild(dicetext);
      }
    }
    let value = results[key];
    restext = restext + results[key] + ' ' + key + '    ';
  }
  var parent = document.getElementById("dice-roller-results");
  while (parent.firstChild) { parent.removeChild(parent.firstChild); }
  var resultselement = document.createTextNode(restext);
  parent.appendChild(resultselement);
}

async function clearDicePool() {
  dicepool = [];
  var parent = document.getElementById('dice-pool');
  while (parent.firstChild) { parent.removeChild(parent.firstChild); }
  var parent = document.getElementById("dice-roller-results");
  while (parent.firstChild) { parent.removeChild(parent.firstChild); }
}
