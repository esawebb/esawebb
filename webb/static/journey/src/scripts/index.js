import "../styles/index.scss";
import "bootstrap/dist/js/bootstrap.bundle";

import * as THREE from "three";
//import { gsap } from 'gsap'
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

import vertexShader from '../shaders/vertex.glsl';
import fragmentShader from '../shaders/fragment.glsl';
import vertexShaderMoon from '../shaders/vertexMoon.glsl';
import fragmentShaderMoon from '../shaders/fragmentMoon.glsl';
import imageGlobe from '../globe.jpeg'
import imageSun from '../sun.jpeg'
import imageMoon from '../moon.jpeg'
//import imageJWST from '../jwst.png'
//import imageHubble from '../hubble.png'
import imageParticle from '../1.png'
//import imageOrbit from '../orbit.png'
//import modelbin from '../scene.bin'
import model from '../model/scene.gltf'


// create scene for model
const scene = new THREE.Scene()

// create scene for space
const scene2 = new THREE.Scene()

// Sizes
const sizes = {
    width: window.innerWidth,
    height: window.innerHeight
}

window.addEventListener('resize', () => {
    // Update sizes
    sizes.width = window.innerWidth,
        sizes.height = window.innerHeight,

        camera.aspect = sizes.width / sizes.height,
        camera1.aspect = sizes.width / sizes.height,
        camera2.aspect = sizes.width / sizes.height,

        camera.updateProjectionMatrix(),
        camera1.updateProjectionMatrix(),
        camera2.updateProjectionMatrix(),

        renderer.setSize(sizes.width, sizes.height),
        renderer2.setSize(sizes.width, sizes.height)
       
})

// // create camera
const camera = new THREE.PerspectiveCamera(75, sizes.width / sizes.height, 0.1, 4000)

// // create camera
const camera1 = new THREE.PerspectiveCamera(75, sizes.width / sizes.height, 0.1, 4000)
camera1.position.set(0, 0, 5)

// // create camera
const camera2 = new THREE.PerspectiveCamera(75, sizes.width / sizes.height, 0.1, 4000)
camera2.position.z = 15
camera2.position.y = 15
camera2.position.x = -5


// create render for model
const renderer = new THREE.WebGLRenderer({
    antialias: true,
    canvas: document.getElementById('scene'),
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

// create render por space
const renderer2 = new THREE.WebGLRenderer({
    antialias: true,
    canvas: document.getElementById('scene2'),
    alpha: true
})
renderer2.setClearColor(0x000000, 0);
renderer2.setSize(sizes.width, sizes.height)
renderer2.setPixelRatio(window.devicePixelRatio)


// //-------------------------------scene ---------------------------------------------------------

// function mdY() {
//     if (window.innerWidth < 768) {
//         return -2000;
//     } else {
//         if (window.innerWidth < 992) {
//             return -1700;
//         } else {
//             return -1550;
//         }
//     }
// }

const floor = new THREE.Mesh(
    new THREE.PlaneGeometry(0.01, 0.01),
    new THREE.MeshStandardMaterial({

        metalness: 0,
        roughness: 0.5
    })
)
floor.receiveShadow = true
floor.rotation.x = - Math.PI * 0.5
scene.add(floor)

/**
 * Loaders
 */

// const loadingManager = new THREE.LoadingManager(
//     // Loaded
//     () => {
//         // Animate overlay
//         gsap.to(overlayMaterial.uniforms.uAlpha, { duration: 3, value: 0})

//     },

//     // Progress
//     (itemUrl, itemsLoaded, itemsTotal) => {
//         // Calculate the progress and update the loadingBarElement
//         const progressRatio = itemsLoaded / itemsTotal

//     }
// )

// const cubeTextureLoader = new THREE.CubeTextureLoader(loadingManager)

// model

var loader = new GLTFLoader();
var obj;
loader.load(model, function (gltf) {
    obj = gltf.scene
    obj.scale.set(0.30, 0.30, 0.30)
    obj.position.set(0, -1, 0);
    obj.rotation.y = 3.0;
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

// const overlayGeometry = new THREE.PlaneGeometry(2, 2, 1, 1)
// const overlayMaterial = new THREE.ShaderMaterial({
//     // wireframe: true,
//     transparent: true,
//     uniforms:
//     {
//         uAlpha: { value: 1 }
//     },
//     vertexShader: `
//         void main()
//         {
//             gl_Position = vec4(position, 1.0);
//         }
//     `,
//     fragmentShader: `
//         uniform float uAlpha;

//         void main()
//         {
//             gl_FragColor = vec4(0.0, 0.0, 0.0, uAlpha);
//         }
//     `
// })
// const overlay = new THREE.Mesh(overlayGeometry, overlayMaterial)
// scene.add(overlay)

const pointsModel = [
    {
        //                            z   y  x
        position: new THREE.Vector3(-0.4, 1, 0.5),
        element: document.querySelector('.point-0')
    },
    // {
    //     position: new THREE.Vector3(-0.3, 1.6, - 0.6),
    //     element: document.querySelector('.point-1')
    // },
    {
        position: new THREE.Vector3(0.5, 1.2, - 0.4),
        element: document.querySelector('.point-2')
    },
    {
        position: new THREE.Vector3(-2.4, 0.9, -0.3),
        element: document.querySelector('.point-3')
    },
    {
        position: new THREE.Vector3(2, 0.4, -0.3),
        element: document.querySelector('.point-4')
    }
    // ,
    // {
    //     position: new THREE.Vector3(0.2, -0.9, -0.4),
    //     element: document.querySelector('.point-5')
    // },
    // {
    //     position: new THREE.Vector3(-0.4, -0.9, 0.3),
    //     element: document.querySelector('.point-6')
    // }

]

// Cursor
const cursor = {
    x: 0,
    y: 0
}

window.addEventListener('mousemove', (event) => {
    cursor.x = event.clientX / sizes.width - 0.5
    cursor.y = - (event.clientY / sizes.height - 0.5)
    //console.log(cursor.x, cursor.y)
})
const controls = new OrbitControls(camera1, renderer.domElement);
controls.enableZoom = false;
//controls.enabled = false;
//camera1.lookAt(gltf.asset)
controls.update();

// //////////////////// default box
// const geometryCube = new THREE.BoxGeometry( 0.1, 0.1, 0.1 );
// const materialCube = new THREE.MeshBasicMaterial( {color: 0x000000} );
// const cube = new THREE.Mesh( geometryCube, materialCube );
// scene.add( cube );
// //-------------------------------scene 2---------------------------------------------------------

//sphere Globe
const sphere = new THREE.Mesh(new THREE.SphereGeometry(1, 100, 100),
    new THREE.ShaderMaterial({
        vertexShader,
        fragmentShader,
        uniforms: {
            globeTexture: {
                value: new THREE.TextureLoader().load(imageGlobe)
            }
        }

    })
)
scene2.add(sphere)
sphere.position.x = 3

//sphere Moon
const sphereMoon = new THREE.Mesh(new THREE.SphereGeometry(0.2, 100, 100),
    new THREE.ShaderMaterial({
        vertexShader: vertexShaderMoon,
        fragmentShader: fragmentShaderMoon,
        uniforms: {
            globeTexture: {
                value: new THREE.TextureLoader().load(imageMoon)
            }
        }

    })
)
scene2.add(sphereMoon)
sphereMoon.position.x = 5

//sphere sun
const sphereSun = new THREE.Mesh(new THREE.SphereGeometry(4, 100, 100),
    new THREE.ShaderMaterial({
        vertexShader: vertexShaderMoon,
        fragmentShader: fragmentShaderMoon,
        uniforms: {
            globeTexture: {
                value: new THREE.TextureLoader().load(imageSun)
            }
        }

    })
)
scene2.add(sphereSun)
sphereSun.position.x = -10

////////////////////// circle
const curve = new THREE.EllipseCurve(
    0, 0,            // ax, aY
    2, 2,           // xRadius, yRadius
    0, 2 * Math.PI,  // aStartAngle, aEndAngle
    false,            // aClockwise
    0               // aRotation
);
const pointsCurve = curve.getPoints(50);
const geometryCurve = new THREE.BufferGeometry().setFromPoints(pointsCurve);
const materialCurve = new THREE.LineBasicMaterial({ color: 0xffffff });
// Create the final object to add to the scene
const ellipse = new THREE.Line(geometryCurve, materialCurve);
ellipse.position.x = 10;
ellipse.rotation.y = 1.5;
scene2.add(ellipse)

//////////////////// Position start
// const geometryJWST = new THREE.PlaneGeometry(0.5,0.5);
// const materialJWST = new THREE.MeshBasicMaterial( { color: 0xffffff,map: new THREE.TextureLoader().load(imageJWST ), } );
// const circleJWST = new THREE.Mesh( geometryJWST, materialJWST );
// circleJWST.position.x= 2
// circleJWST.position.y= 2
// scene2.add( circleJWST );

// model

//var loader2 = new GLTFLoader();
var obj2;
loader.load(model, function (gltf) {
    obj2 = gltf.scene;
    obj2.position.set(10, 0, 0);
    obj2.rotation.z = -1
    obj2.rotation.x = 1.8
    obj2.scale.set(0.05, 0.05, 0.05)
    scene2.add(obj2);
});
var light2 = new THREE.HemisphereLight(0xffffff, 0x000000, 2);
scene2.add(light2);

/**
 * Textures
 */
const textureLoader = new THREE.TextureLoader()
const particleTexture = textureLoader.load(imageParticle)

// Geometry
const particlesGeometry = new THREE.BufferGeometry()
const count = 1500

const positions = new Float32Array(count * 3);


for (let i = 0; i < count * 3; i++) {
    positions[i] = (Math.random() - 0.5) * 85

}

particlesGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 4))

// Material
const particlesMaterial = new THREE.PointsMaterial()

particlesMaterial.size = 0.05
//particlesMaterial.sizeAttenuation = true

//particlesMaterial.color = new THREE.Color('#000000')

particlesMaterial.transparent = true
particlesMaterial.alphaMap = particleTexture

//particlesMaterial.depthWrite = false
particlesMaterial.blending = THREE.AdditiveBlending

//particlesMaterial.vertexColors = true

// Points
const particles = new THREE.Points(particlesGeometry, particlesMaterial)
particles.position.set(-5, 0, 0)
scene2.add(particles)

const controls2 = new OrbitControls(camera2, renderer2.domElement);
controls2.enableZoom = false;
controls2.enableRotate = false;
controls2.update();

// //-------------------------------scene 3---------------------------------------------------------


const clock = new THREE.Clock()


var timeOut = false;

document.getElementById("timeOut").addEventListener("click", () => {


    var playTimeOut = document.getElementById('timeOut');

    if (timeOut == true) {
        timeOut = false;
        playTimeOut.innerHTML = `<ion-icon name="play" size="large"></ion-icon>`;


    } else {
        timeOut = true;
        playTimeOut.innerHTML = `<ion-icon name="undo" size="large"></ion-icon>`;

    }


})

var rotationModel = true;
for (const pointModel of pointsModel) {
    pointModel.element.classList.remove('visible')
}

document.getElementById("rotationModel").addEventListener("click", () => {

    var playRotationModel = document.getElementById('rotationModel');

    if (rotationModel == true) {
        rotationModel = false;
        playRotationModel.innerHTML = `<ion-icon name="play" size="large"></ion-icon>`;
        for (const pointModel of pointsModel) {
            pointModel.element.classList.add('visible')
        }
        obj.rotation.y = 3.0;

    } else {
        rotationModel = true;
        playRotationModel.innerHTML = `<ion-icon name="pause" size="large"></ion-icon>`;
        pointsModel.enabled = false;
        for (const pointModel of pointsModel) {
            pointModel.element.classList.remove('visible')
        }

    }


})

///////////////////////////////// CLOCK ///////////////////////////////

const getRemainingTime = deadline => {
    let now = new Date(),
        remainTime = (now - new Date(deadline) + 1000) / 1000,
        remainSeconds = ('0' + Math.floor(remainTime % 60)).slice(-2),
        remainMinutes = ('0' + Math.floor(remainTime / 60 % 60)).slice(-2),
        remainHours = ('0' + Math.floor(remainTime / 3600 % 24)).slice(-2),
        remainDays = Math.floor(remainTime / (3600 * 24));

    return {
        remainSeconds,
        remainMinutes,
        remainHours,
        remainDays,
        remainTime
    }
};

//const countdown = (deadline,elem,finalMessage, name) => {
const countdown = (deadline) => {
    //const el = document.getElementById(elem);
    const daysTraveled = document.getElementById('Days traveled');
    //const distanceTraveled = document.getElementById('Distance traveled');

    setInterval( () => {
      let t = getRemainingTime(deadline);

        if (t != null){
            daysTraveled.innerHTML = `${t.remainDays} days and ${t.remainHours} hours`
            //distanceTraveled.innerHTML = `1.5 million kilometres`
            
        }

    }, 1000)
 
  };


countdown('Dec 25 2021 07:20:00 GMT-0500', 'clock', '', 'Journey to L2:')

///////////////////////////////// END CLOCK ///////////////////////////////


function animate() {
    requestAnimationFrame(animate)
    const elapsedTime = clock.getElapsedTime()
    controls.update();
    controls2.update();
    

    renderer.setSize(sizes.width, sizes.height)
    renderer.render(scene, camera1)
    renderer2.setSize(sizes.width, sizes.height)
    renderer2.render(scene2, camera2)
 

    if (sphere) {
        sphere.rotation.y += 0.002;
        sphereMoon.rotation.y += 0.01;
        sphereSun.rotation.y += 0.001;
        particles.rotation.y += 0.0001;
    }

    if (obj2) {
        obj2.position.y = Math.cos(elapsedTime / 2) * 2;
        obj2.position.z = Math.sin(elapsedTime / 2) * 2;
    }

    if (rotationModel == true) {
        if (obj) {
            obj.rotation.y += 0.002;
        }
        //obj.position.z = Math.sin(elapsedTime/2) * 0.5;
    }

    if (camera2.position.x < 20 && timeOut == true) {
        camera2.position.x += 0.1;
        camera2.position.z -= 0.06;
        camera2.position.y = 0
    }

    if (camera2.position.x > 0 && timeOut == false) {
        camera2.position.x -= 0.1;
        camera2.position.z += 0.06;
        camera2.position.y = 12
    }

    controls.update()



    for (const pointModel of pointsModel) {
        const screenPosition = pointModel.position.clone()
        screenPosition.project(camera1)

        const translateX = screenPosition.x * sizes.width * 0.5
        const translateY = - screenPosition.y * sizes.height * 0.5
        pointModel.element.style.transform = `translateX(${translateX}px) translateY(${translateY}px)`

    }

}
animate()