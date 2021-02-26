//adapted from https://github.com/stemkoski/stemkoski.github.com/tree/master/Three.js/js

var THREE = require('three')
var STLLoader = require('three-stl-loader')(THREE)
var OrbitControls = require('three-orbit-controls')(THREE)

var container, scene, camera, robot, renderer, controls;

var robot_info = {};

const socket = new WebSocket('ws://localhost:8080/ws');
socket.addEventListener('message', function (event) {
    var msg = JSON.parse(event.data);
	for (const [key, value] of Object.entries(msg)){
		robot_info[key] = value;
	}
});

init_scene();
animate();

// FUNCTIONS 		
function init_scene() 
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
	
    //GRID
	var gridXY = new THREE.GridHelper(1000, 10,new THREE.Color(0x000066),new THREE.Color(0x000066));
	gridXY.position.set( 0,0,0 );
	scene.add(gridXY);

    //CAMERA VIZ
    //var lCam = new THREE.PerspectiveCamera( 75, 1920/1080, 0.1, 100 );
	//var lHelper = new THREE.CameraHelper(lCam);

	var loader = new STLLoader()
    loader.load( './src/stls/car.stl', function ( geometry ) {
	 var material = new THREE.MeshNormalMaterial()
	 var mesh = new THREE.Mesh( geometry,material )
	 robot = new THREE.Group();
	 robot.add(mesh);
	 scene.add( robot );
    });



}

function animate() 
{
    requestAnimationFrame( animate );
	render();		
	update();
}

function update()
{
	if(robot_info.base_transform){
		let pos = robot_info.base_transform.position
		let or = robot_info.base_transform.orientation
		let quaternion = new THREE.Quaternion(or.x,or.y,or.z,or.w)
		robot.position.set(pos.x,pos.y,pos.z)
		robot.rotation.setEulerFromQuaternion(quaternion)
	}
	controls.update();
}

function render() 
{
	renderer.render( scene, camera );
}
