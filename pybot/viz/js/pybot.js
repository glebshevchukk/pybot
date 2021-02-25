//adapted from https://github.com/stemkoski/stemkoski.github.com/tree/master/Three.js/js

var THREE = require('three')
const Redis = require("ioredis");
const redis = new Redis();

var OrbitControls = require('three-orbit-controls')(THREE)

var container, scene, camera, renderer, controls;

// custom global variables
var mesh;

init_3d();
animate();

// FUNCTIONS 		
function init_3d() 
{
	// SCENE
	scene = new THREE.Scene();
	// CAMERA
	var SCREEN_WIDTH = window.innerWidth, SCREEN_HEIGHT = window.innerHeight;
	var VIEW_ANGLE = 45, ASPECT = SCREEN_WIDTH / SCREEN_HEIGHT, NEAR = 0.1, FAR = 20000;
	camera = new THREE.PerspectiveCamera( VIEW_ANGLE, ASPECT, NEAR, FAR);
	scene.add(camera);
	camera.position.set(0,150,400);
	camera.lookAt(scene.position);	

    scene.background = new THREE.Color( 0xffffff );


	renderer = new THREE.WebGLRenderer( {antialias:true} );

	renderer.setSize(SCREEN_WIDTH, SCREEN_HEIGHT);
	document.body.appendChild( renderer.domElement );
	// CONTROLS
	controls = new OrbitControls( camera, renderer.domElement );

	// LIGHT
	var light = new THREE.PointLight(0xffffff);
	light.position.set(100,250,100);
	scene.add(light);
	
	

	var geometry = new THREE.SphereGeometry( 30, 32, 16 );
	var material = new THREE.MeshLambertMaterial( { color: 0x000088 } );
	mesh = new THREE.Mesh( geometry, material );
	mesh.position.set(40,40,40);
	scene.add(mesh);

	//THREE AXES
	// var axes = new THREE.AxisHelper(50);
	// axes.position = mesh.position;
	// scene.add(axes);
	
    //GRID
	var gridXY = new THREE.GridHelper(1000, 10,new THREE.Color(0x000066),new THREE.Color(0x000066));
	gridXY.position.set( 0,0,0 );
	scene.add(gridXY);

    //CAMERA VIZ
    const camera2 = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 10 );
    const helper = new THREE.CameraHelper( camera2 );
    scene.add(helper);


}

function animate() 
{
    requestAnimationFrame( animate );
	render();		
	update();
}

function update()
{
	controls.update();
}

function render() 
{
	renderer.render( scene, camera );
}
