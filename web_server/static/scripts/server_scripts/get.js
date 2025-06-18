export async function get_recent() {
	let response = await fetch("https://server.deoliveira.tech/get_recent");
	let data = await response.json();
	return data;
}

export async function get_dash() {
	let response = await fetch("https://server.deoliveira.tech/get_dash_data");
	let data = await response.json();
	return data;
}

export async function get_all_gps() {
	let response = await fetch("https://server.deoliveira.tech/get_all_gps");
	let data = await response.json();
	return data;
}

export async function get_recent_gps() {
	let response = await fetch("https://server.deoliveira.tech/get_recent_gps");
	let data = await response.json();
	return data;
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

window.update_tables = update_tables;
