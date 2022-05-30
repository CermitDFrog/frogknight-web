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

function renderDicePool(parent = "dice-roller-header", clicky = "add", dice = dicebag) {
  var parent = document.getElementById(parent);
  while (parent.firstChild) { parent.removeChild(parent.firstChild);}
  for (var i = 0; i < dice.length; i++) {
    var diespan = document.createElement("span");
    var dieimg = document.createElement('img');
    var tagprefix = ''
    if (clicky === 'add') 
    {  dieimg.setAttribute('onClick', 'addToPool('+i+')' ) ; } 
    else 
    {  dieimg.setAttribute('onClick', 'removeFromPool('+i+')' ); tagprefix='small-' }
    dieimg.src = dice[i]; dieimg.className = tagprefix+'dice';    
    diespan.className = tagprefix+'dice-span';
    diespan.appendChild(dieimg);
    parent.appendChild(diespan);
  }
};
// removeButton.setAttribute('onClick','removeName('+i+')');
function addToPool(die) {
  dicepool.push(dicebag[die]);
  renderDicePool('dice-roller-business-pool','remove',dicepool)
};

function removeFromPool(die) {
  dicepool.splice(die,1);
  renderDicePool('dice-roller-business-pool','remove',dicepool)
};

function rollPool() {
  var rollstring = '';
  for (var i = 0; i<dicepool.length; i++) {
    rollstring = rollstring.concat(dicemap[dicepool[i]]);
  }
  var results = httpGet('http://127.0.0.1:8000/swcs/rest/roll?dicepool=' + rollstring);
  var restext = ''
  for (let key in results) {
    if (key ==='face'){continue;}
    let value = results[key];
    console.log(key, value);
    restext = restext + key + ': ' + value + ' ';
  }
  // for (let [key, value] of Object.entries(result)) {
  // }
  var parent = document.getElementById("dice-roller-results");
  while (parent.firstChild) { parent.removeChild(parent.firstChild);}
  var resultselement = document.createTextNode(restext)
  parent.appendChild(resultselement)
};

function httpGet(theUrl)
{
   var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );

    return JSON.parse(xmlHttp.responseText);
};

function clearDicePool() {
  dicepool = [];
  renderDicePool('dice-roller-business-pool','remove',dicepool);
  var parent = document.getElementById("dice-roller-results");
  while (parent.firstChild) { parent.removeChild(parent.firstChild);}
};