async function get_recent() {
	let response = await fetch("https://server.deoliveira.tech/get_recent");
	let data = await response.json();
	return data;
}

async function get_dash() {
	let response = await fetch("https://server.deoliveira.tech/get_dash_data");
	let data = await response.json();
	return data;
}

async function get_all_gps() {
	let response = await fetch("https://server.deoliveira.tech/get_all_gps");
	let data = await response.json();
	return data;
}

async function get_recent_gps() {
	let response = await fetch("https://server.deoliveira.tech/get_recent_gps");
	let data = await response.json();
	return data;
}

async function get_power_map() {
	var message = await get_all_gps();
	var lists = message["message"]["gps"];
	var positions = [];
	for (list in lists) {
		positions.push(lists[list][1]);
		positions.push(lists[list][2]);
		// calculate associated color
		// temp
		positions.push(1);
		positions.push(1);
		positions.push(1);
	}
	console.log(positions);
	return positions;
}

async function update_power_map_loop(positions) {
	var message = await get_recent_gps();
	var lists = message["message"]["gps_recent"];
	for (list in lists) {
		positions.push(list[1]);
		positions.push(list[2]);
	}
	return positions;
}



async function update_tables() {
	let data = await get_recent();
	let object = data["message"];

	for (const key in object) {
		var element = document.getElementById(key);
		element.replaceChildren();
		for (const subkey in object[key]) {
			const heading = document.createElement("h3");
			heading.textContent = subkey;
			const paragraph = document.createElement("p");
			paragraph.textContent = object[key][subkey];
			element.appendChild(heading);
			element.appendChild(paragraph);
		}
	}
}
