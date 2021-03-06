//adapted from https://github.com/stemkoski/stemkoski.github.com/tree/master/Three.js/js

var THREE = require('three')
var STLLoader = require('three-stl-loader')(THREE)
var OrbitControls = require('three-orbit-controls')(THREE)

var container, scene, camera, robot, renderer, controls;

var robot_info = {};
var topics_visible = {};
var viz_objs = {}

const socket = new WebSocket('ws://localhost:8080/ws');
socket.addEventListener('message', function (event) {
    var msg = JSON.parse(event.data);
	for (const [key, value] of Object.entries(msg)){
		robot_info[key] = value;
	}
	fillActionMenu();
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
}

function animate() 
{
    requestAnimationFrame( animate );
	render();		
	update();
}

function update()
{
	for (const [key, value] of Object.entries(topics_visible)){
		if(value == true){
			let info = robot_info[key]
			let pos = info.pose.position
			let or = info.pose.orientation
			let quaternion = new THREE.Quaternion(or.x,or.y,or.z,or.w)
			
			let obj = viz_objs[key]
			
			obj.position.set(pos.x,pos.y,pos.z)
		
			if(key+"_helper" in viz_objs){
				let obj_helper = viz_objs[key+"_helper"]
				obj_helper.position.set(pos.x,pos.y,pos.z)
				obj_helper.update()
			}
			//obj.rotation.setEulerFromQuaternion(quaternion)
		}
	}
	controls.update();
}

function render() 
{
	renderer.render( scene, camera );
}

function fillActionMenu() {
	for (const [key, value] of Object.entries(robot_info)){
		if(!(key in topics_visible)){
			var ul = document.getElementById("topic-list");
			var li = document.createElement("li");
			var checkbox = document.createElement('input');
			checkbox.type = "checkbox";
			checkbox.name = key;
			checkbox.checked = true;
			checkbox.id = key;
			li.appendChild(document.createTextNode(key));
			li.appendChild(checkbox);
			ul.appendChild(li);
			topics_visible[key] = true;

			//finally add on click behavior
			var currbox=document.getElementById(key);
			currbox.addEventListener("click", function() { setVisibility(key); } );

			//also add the vizualization to the scene at the very end
			addViz(value.vizType,key)
		}
	}
  }

function setVisibility(key){
	topics_visible[key] = !topics_visible[key]

	if (!topics_visible[key]){
		scene.remove(topics_visible[key])
	} else{
		addViz(robot_info[key].vizType,key)
	}
}

function addViz(type,topic){
	if(type == "camera"){
		addCameraViz(topic)
	}
	else if(type == "tf"){
		addTFViz(topic)
	}
	else if(type == "robot"){
		addRobotViz(topic)
	}
	else{
		console.log("Viz type not supported yet.")
	}
}

function addCameraViz(topic){
	let info = robot_info[topic]
	var cam = new THREE.PerspectiveCamera(50, info.camera.width/info.camera.height, 0.1, 100 );
	scene.add(cam);
	cam.position.set(0,150,400)
	var helper = new THREE.CameraHelper(cam);
	scene.add(helper);
	viz_objs[topic]=cam;
	viz_objs[topic+"_helper"]=helper;
}

function addTFViz(topic){
	let info = robot_info[topic]
	var axesHelper = new THREE.AxesHelper( 5 );
	axesHelper.position= info.pose.position;
	axesHelper.orientation= info.pose.position;
	scene.add(axesHelper);
	viz_objs[topic]=axesHelper
}

function addRobotViz(topic){
	var loader = new STLLoader()
    loader.load( './src/stls/car.stl', function ( geometry ) {
	 var material = new THREE.MeshNormalMaterial()
	 var mesh = new THREE.Mesh( geometry,material )
	 robot = new THREE.Group();
	 robot.add(mesh);
	 scene.add(robot);
	 viz_objs[topic]=robot;
    });
}