async function updateSpecies() {
    var parent = document.getElementById('selection-details');
    while (parent.firstChild) { parent.removeChild(parent.firstChild); }
    species = document.getElementById('id_character_species').value;
    // if null or empty or error return
    if (species === null || species === '') { return; }

    var species = await httpGet('/swcs/rest/species/' + species);
    var name = document.createElement('h3');

    name.classList.add('selection-details-header');
    name.innerHTML = species.species_name;
    var description = document.createElement('div');
    description.classList.add('card');
    description.classList.add('selection-details-description');
    var descriptiontext = species.species_description;
    descriptiontext = descriptiontext.substring(descriptiontext.indexOf('\n') + 1);
    var descriptionp = document.createElement('p');
    descriptionp.innerHTML = descriptiontext;
    var grid = document.createElement('div');
    var brawn_card = await createAttributeCard('Brawn', species.species_brawn);
    var agility_card = await createAttributeCard('Agility', species.species_agility);
    var intellect_card = await createAttributeCard('Intellect', species.species_intellect);
    var cunning_card = await createAttributeCard('Cunning', species.species_cunning);
    var willpower_card = await createAttributeCard('Willpower', species.species_willpower);
    var presence_card = await createAttributeCard('Presence', species.species_presence);
    var wounds_card = await createAttributeCard('Wounds', species.species_wound);
    var strain_card = await createAttributeCard('Strain', species.species_strain);
    var startingxp_card = await createAttributeCard('Starting XP', species.species_starting_xp);

    grid.classList.add('species-attribute-grid');
    grid.appendChild(brawn_card);
    grid.appendChild(agility_card);
    grid.appendChild(intellect_card);
    grid.appendChild(cunning_card);
    grid.appendChild(willpower_card);
    grid.appendChild(presence_card);
    grid.appendChild(wounds_card);
    grid.appendChild(strain_card);
    grid.appendChild(startingxp_card);
    description.appendChild(name);
    description.appendChild(descriptionp);
    parent.appendChild(grid);
    parent.appendChild(description);
}

async function httpGet(url) {
    let response = await fetch(url);
    let data = await response.json();
    return data;
  }

async function createAttributeCard(label, value){
    var card = document.createElement('div');
    card.classList.add('species-attribute-card');
    card.classList.add('card');
    var label_p = document.createElement('p');
    label_p.innerHTML = label;
    var value_p = document.createElement('p');
    value_p.innerHTML = value;
    card.appendChild(label_p);
    card.appendChild(value_p);
    return card;
}