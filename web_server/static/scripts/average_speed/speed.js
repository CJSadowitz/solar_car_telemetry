import { max_capacity } from "../../constants/battery";
import { array_power_t_to_t } from "./array_prediction";

function speed(start_percent, end_percent, start_time, end_time) {
	var initial_pack_charge = start_percent * max_capacity;
	var final_pack_charge = end_percent * max_capacity;
	var power_in = array_power_t_to_t(start_time, end_time);

}
