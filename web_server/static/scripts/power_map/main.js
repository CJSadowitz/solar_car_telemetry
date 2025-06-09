import { get_shader_program } from "./shader.js";
import { get_recent_power } from "./get_power_data.js";


async function main(points) {
    var shader_program = await get_shader_program();
    var buffer = create_buffer(shader_program);
    
    let max = get_max(-1000, -1000, points);
    let min = get_min( 1000,  1000, points);
    // let transformed_points = transform_points(max, points);
    let transformed_points = min_max_rescale(min, max, points);
    for (let i = 0; i < transformed_points.length; i += 5) {
        console.log(transformed_points[i + 0]);
        console.log(transformed_points[i + 1]);
    }

    requestAnimationFrame(() => main_loop(buffer, transformed_points));
}

function main_loop(buffer, points) {
    update_buffer_data(buffer, points);
    render(buffer, points.length);
    
    requestAnimationFrame(() => main_loop(buffer, points));
}

function render(buffer, size) {
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.drawArrays(gl.POINTS, 0, size / 5)
}

function update_buffer_data(buffer, points) {
    // GET NEW DATA FROM SERVER HERE
    // Update new added points with the normalize function and append to data
    update_buf(buffer, points);
}

function update_buf(buffer, points) {
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(points), gl.STATIC_DRAW);
}

function create_buffer(program) {
    var buffer = gl.createBuffer();
    buffer = add_pos_to_buffer(buffer, program);
    buffer = add_col_to_buffer(buffer, program);

    return buffer;
}

function add_pos_to_buffer(buffer, program) {
    var position_attribute_location = gl.getAttribLocation(program, "a_pos");
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    var size = 2;
    var type = gl.FLOAT;
    var normalize = false;
    var stride = 5 * Float32Array.BYTES_PER_ELEMENT;
    var offset = 0;
    gl.vertexAttribPointer(position_attribute_location, size, type, normalize, stride, offset);
    gl.enableVertexAttribArray(position_attribute_location);
    return buffer;
}

function add_col_to_buffer(buffer, program) {
    var color_attribute_location = gl.getAttribLocation(program, "a_col");
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    var size = 3;
    var type = gl.FLOAT;
    var normalize = false;
    var stride = 5 * Float32Array.BYTES_PER_ELEMENT;
    var offset = 2 * Float32Array.BYTES_PER_ELEMENT;
    gl.vertexAttribPointer(color_attribute_location, size, type, normalize, stride, offset);
    gl.enableVertexAttribArray(color_attribute_location);
    return buffer;
}

function min_max_rescale(min, max, points) {
    let min_lat = min.lat, max_lat = max.lat;
    let min_lon = min.lon, max_lon = max.lon;

    for (let i = 0; i < points.length; i += 5) {
        min_lat = Math.min(min_lat, points[i + 0]);
        max_lat = Math.max(max_lat, points[i + 0]);

        min_lon = Math.min(min_lon, points[i + 1]);
        max_lon = Math.max(max_lon, points[i + 1]);
    }

    for (let i = 0; i < points.length; i += 5) {
        let norm_lat = (points[i + 0] - min_lat) / (max_lat - min_lat);
        let norm_lon = (points[i + 1] - min_lon) / (max_lat - min_lat);

        points[i + 0] = (Math.tanh(norm_lat * 3) * 0.8);
        points[i + 1] = (Math.tanh(norm_lon * 3) * 0.8);
    }

    return points;
}

function get_max(largest_lat, largest_lon, points) {
    for (let i = 0; i < points.length; i += 5) {
        largest_lat = Math.max(largest_lat, Math.abs(points[i + 0]));
        largest_lon = Math.max(largest_lon, Math.abs(points[i + 1]));
    }
    var max = {
        lat: largest_lat,
        lon: largest_lon
    };
    return max;
}

function get_min(smallest_lat, smallest_lon, points) {
    for (let i = 0; i < points.length; i += 5) {
        smallest_lat = Math.max(smallest_lat, Math.abs(points[i + 0]));
        smallest_lon = Math.max(smallest_lon, Math.abs(points[i + 1]));
    }
    var min = {
        lat: smallest_lat,
        lon: smallest_lon
    };
    return min;
}

window.main = main;
