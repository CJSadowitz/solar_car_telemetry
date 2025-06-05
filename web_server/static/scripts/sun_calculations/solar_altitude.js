import { latitude, longitude } from "../../constants/location.js";

export function calculate_solar_angle(time=new Date()) {
    return SunCalc.getPosition(time, latitude, longitude).altitude;
}

// adapt to work for other days
export function integrate_solar_angle(start_time, end_time) {
    let sum = 0;
    let step_minutes = 1;

    let chunks = 0;
    for (let time = new Date(start_time); time <= end_time; time.setMinutes(time.getMinutes() + step_minutes)) {
        let slice = Math.abs(calculate_solar_angle(time) * step_minutes);
        sum += Math.cos(slice);
        chunks++;
    }

    return sum / 60;
}

export function calculate_high_noon_angle() {
    return 14;
}
