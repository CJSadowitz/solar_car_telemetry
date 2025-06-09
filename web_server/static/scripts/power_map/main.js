import { get_shader_program } from "./shader.js";
import { get_recent_power } from "./get_power_data.js";


async function main(points) {
    var shader_program = await get_shader_program();
    var buffer = create_buffer(shader_program);
    console.log("Entered main");
    requestAnimationFrame(() => main_loop(buffer, points));
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

    let transformed_points = transform_points(points);
    console.log(transformed_points);
    update_buf(buffer, transformed_points);
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

function transform_points(points) {
    var largest_lat = 0;
    var largest_lon = 0;
    for (let i = 0; i < points.length; i+=5) {
        largest_lat = Math.max(largest_lat, Math.abs(points[i + 0]));
        largest_lon = Math.max(largest_lon, Math.abs(points[i + 1]));
    }

    for (let i = 0; i < points.length; i+=5) {
        let first = points[i + 0] / largest_lat;
        if (first < 0) { points[i + 0] = 2 * first + 1; }
        else { points[i + 0] = 2 * first - 1; }

        let second = points[i + 1] / largest_lon;
        if (second < 0) { points[i + 1] = 2 * second + 1; }
        else { points[i + 1] = 2 * second - 1; }
    }

    return points;
}

window.main = main;
