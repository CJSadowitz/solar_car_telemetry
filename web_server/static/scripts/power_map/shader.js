export async function get_shader_program() {
    var vertex_source = await fetch("/static/scripts/power_map/vertex.glsl");
    var fragment_source = await fetch("/static/scripts/power_map/fragment.glsl");
    var vertex_shader = create_shader(gl.VERTEX_SHADER, await vertex_source.text());
    var fragment_shader = create_shader(gl.FRAGMENT_SHADER, await fragment_source.text());
    var program = create_program(vertex_shader, fragment_shader);
    gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);
    gl.clearColor(0, 0, 0, 1);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.enable(gl.DEPTH_TEST);
    gl.useProgram(program);
    return program
}

function create_shader(type, source) {
    var shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    var success = gl.getShaderParameter(shader, gl.COMPILE_STATUS);
    if(success) {
        return shader;
    }
    console.error(gl.getShaderInfoLog(shader));
    gl.deleteShader(shader);
}

function create_program(vs, fs) {
    var program = gl.createProgram();
    gl.attachShader(program, vs);
    gl.attachShader(program, fs);
    gl.linkProgram(program);
    var success = gl.getProgramParameter(program, gl.LINK_STATUS);
    if(success) {
        return program;
    }
    console.error(gl.getProgramInfoLog(program));
    gl.deleteProgram(program);	
}
