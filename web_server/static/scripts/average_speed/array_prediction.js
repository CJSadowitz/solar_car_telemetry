import {calculate_solar_angle, integrate_solar_angle} from "../sun_calculations/solar_altitude.js";
import {array_power_coefficient, array_max_power} from "../../constants/array.js"

function array_power(time) {
    return array_power_coefficient * Math.cos(calculate_solar_angle(time));
}

export function array_power_t_to_t(start, end) {
    if (start instanceof Date && !isNaN(start) && end instanceof Date && !isNaN(end)) {
        return array_max_power * integrate_solar_angle(start, end);
    }
    console.error("ARRAY_PREDICTION::ARRAY_POWER_T_TO_T::invalid date", start, end);
    return -1;
}

window.array_power_t_to_t = array_power_t_to_t;
window.array_power = array_power;
