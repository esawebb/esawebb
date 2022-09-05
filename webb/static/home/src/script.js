import './bootstrap/css/style.css'
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import model from './scene.gltf'



// Scene
const scene = new THREE.Scene()

// Sizes
const sizes = {
    width: window.innerWidth,
    height: window.innerHeight /2
}

// Camera
const camera = new THREE.PerspectiveCamera(75, sizes.width / sizes.height)
camera.position.z = 4
scene.add(camera)

// Canvas
const canvas = document.querySelector('canvas.webgl')

//

// Renderer
const renderer = new THREE.WebGLRenderer({
    antialias: true,
    canvas: document.getElementById('webgl'),
    alpha: true
})
renderer.setClearColor(0x000000, 0);
renderer.physicallyCorrectLights = true
renderer.outputEncoding = THREE.sRGBEncoding
renderer.toneMapping = THREE.ReinhardToneMapping
renderer.toneMappingExposure = 3
renderer.shadowMap.enabled = true
renderer.shadowMap.type = THREE.PCFSoftShadowMap
renderer.setSize(sizes.width, sizes.height)
renderer.setPixelRatio(window.devicePixelRatio)

var loader = new GLTFLoader();
var obj;
loader.load(model, function (gltf) {
    obj = gltf.scene
    obj.scale.set(0.30, 0.30, 0.30)
    obj.position.set(0, -1, 0);
    obj.rotation.y = 4.0;
    scene.add(obj);
});
const ambientLight = new THREE.AmbientLight(0xffffff, 1)
scene.add(ambientLight)

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5)
directionalLight.castShadow = true
directionalLight.shadow.mapSize.set(1024, 1024)
directionalLight.shadow.camera.far = 15
directionalLight.shadow.camera.left = - 7
directionalLight.shadow.camera.top = 7
directionalLight.shadow.camera.right = 7
directionalLight.shadow.camera.bottom = - 7
directionalLight.position.set(- 2, 2, 0)
scene.add(directionalLight)

const directionalLight2 = new THREE.DirectionalLight(0xffffff, 0.5)
directionalLight2.castShadow = true
directionalLight2.shadow.mapSize.set(1024, 1024)
directionalLight2.shadow.camera.far = 15
directionalLight2.shadow.camera.left = - 7
directionalLight2.shadow.camera.top = 7
directionalLight2.shadow.camera.right = 7
directionalLight2.shadow.camera.bottom = - 7
directionalLight2.position.set(2, 2, 0)
scene.add(directionalLight2)

const directionalLight3 = new THREE.DirectionalLight(0xffffff, 0.5)
directionalLight3.castShadow = true
directionalLight3.shadow.mapSize.set(1024, 1024)
directionalLight3.shadow.camera.far = 15
directionalLight3.shadow.camera.left = - 7
directionalLight3.shadow.camera.top = 7
directionalLight3.shadow.camera.right = 7
directionalLight3.shadow.camera.bottom = - 7
directionalLight3.position.set(0, -1, 0)
scene.add(directionalLight3)

const directionalLight4 = new THREE.DirectionalLight(0xffffff, 0.5)
directionalLight4.castShadow = true
directionalLight4.shadow.mapSize.set(1024, 1024)
directionalLight4.shadow.camera.far = 15
directionalLight4.shadow.camera.left = - 7
directionalLight4.shadow.camera.top = 7
directionalLight4.shadow.camera.right = 7
directionalLight4.shadow.camera.bottom = - 7
directionalLight4.position.set(- 2, 2, -2)
scene.add(directionalLight4)

const directionalLight5 = new THREE.DirectionalLight(0xffffff, 0.5)
directionalLight5.castShadow = true
directionalLight5.shadow.mapSize.set(1024, 1024)
directionalLight5.shadow.camera.far = 15
directionalLight5.shadow.camera.left = - 7
directionalLight5.shadow.camera.top = 7
directionalLight5.shadow.camera.right = 7
directionalLight5.shadow.camera.bottom = - 7
directionalLight5.position.set(2, 2, 2)
scene.add(directionalLight5)

const controls = new OrbitControls(camera, renderer.domElement);
var statezoom = "f";
controls.enableZoom = false;
controls.update();

document.getElementById("webgl").addEventListener( 'click', (event) => {
    
    if(statezoom == "v"){
        statezoom = "f";
        controls.enableZoom = false;
        controls.update();
    }
    else{
        statezoom = "v"
        controls.enableZoom = true;
        controls.update();
    }  
});

// Object
const geometry = new THREE.BoxGeometry(0.001, 0.001, 0.001)
const material = new THREE.MeshBasicMaterial({ color: 0xffffff })
const mesh = new THREE.Mesh(geometry, material)

scene.add(mesh)

window.addEventListener('resize', () =>
{
       // Update sizes
       sizes.width = window.innerWidth
       sizes.height = window.innerHeight/2
   
       // Update camera
       camera.aspect = sizes.width / sizes.height
       camera.updateProjectionMatrix()
   
       // Update renderer
       renderer.setSize(sizes.width, sizes.height)
})



const animate = () =>
{   
    requestAnimationFrame(animate)
    controls.update();
    // Render
    renderer.setSize(sizes.width, sizes.height)
    renderer.render(scene, camera)

    if (obj){
        obj.rotation.y += 0.0005;
    }

}

animate()