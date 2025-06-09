import { get_all_gps } from "../server_scripts/get.js";

export async function get_power_map() {
	var message = await get_all_gps();
	var lists = message["message"]["gps"];
	var positions = [];
	for (let list in lists) {
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

export async function get_recent_power(positions) {
	var message = await get_recent_gps();
	var lists = message["message"]["gps_recent"];
	for (let list in lists) {
		positions.push(list[1]);
		positions.push(list[2]);
	}
	return positions;
}


window.get_recent_power = get_recent_power;
window.get_power_map = get_power_map;
