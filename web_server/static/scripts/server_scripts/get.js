async function get_recent() {
	let response = await fetch("https://server.deoliveira.tech/get_recent");
	let data = await response.json();
	console.log(data);
	return data;
}

async function update_tables() {
	let data = await get_recent();
	let object = data["message"];
	for (const key in object) {
		console.log(key);
		console.log(object[key]);
	}
}
