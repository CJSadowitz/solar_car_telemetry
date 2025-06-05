attribute vec2 a_pos;
attribute vec3 a_col;

varying vec3 v_col;

void main() {
    v_col = a_col;
    gl_PointSize = 10.0;
    gl_Position = vec4(a_pos, 0.0, 1.0);
}