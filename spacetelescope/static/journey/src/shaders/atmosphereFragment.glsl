
varying vec3 vertexNormal;

void main(){
    float intensity = pow(0.57 - dot(
        vertexNormal, vec3(1.0, 1.0, 1.0)),0.0);
    gl_FragColor = vec4(1, 1, 1, 1.0) * intensity;
}