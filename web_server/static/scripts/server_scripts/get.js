async function get_recent() {
	let response = await fetch("https://server.deoliveira.tech/get_recent");
	let data = await response.json();
	console.log(data);
	return data;
}
