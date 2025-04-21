let constrain = 2000;
let mouseOverContainer = document.getElementById("ex1");
let ex1Layer = document.getElementById("ex1-layer");

//website UI graphics
function transforms(x, y, el) {
  let box = el.getBoundingClientRect();
  let calcX = -(y - box.y - (box.height / 2)) / constrain;
  let calcY = (x - box.x - (box.width / 2)) / constrain;
  
  return "perspective(100px) "
    + "   rotateX("+ calcX +"deg) "
    + "   rotateY("+ calcY +"deg) ";
};

 function transformElement(el, xyEl) {
  el.style.transform  = transforms.apply(null, xyEl);
}

mouseOverContainer.onmousemove = function(e) {
  let xy = [e.clientX, e.clientY];
  let position = xy.concat([ex1Layer]);

  window.requestAnimationFrame(function(){
    transformElement(ex1Layer, position);
  });
};

// When the user clicks the convert button, start loader
var loader = document.getElementById("loader");

function startLoader() {
  loader.style.display = "block";
}

//CHICKEN LOADER
/*Minecraft Chicken in TREEJS */
var scene, camera, controls, fieldOfView, aspectRatio, nearPlane, farPlane, shadowLight, backLight, light, renderer, container;
var floor, chicken, isBlowing = false;
var HEIGHT, WIDTH, windowHalfX, windowHalfY, mousePos = {x: 0, y: 0};
dist = 0;

function init() {
    scene = new THREE.Scene();
    HEIGHT = window.innerHeight;
    WIDTH = window.innerWidth;
    aspectRatio = WIDTH / HEIGHT;
    fieldOfView = 60;
    nearPlane = 1;
    farPlane = 2000;
    camera = new THREE.PerspectiveCamera(
            fieldOfView,
            aspectRatio,
            nearPlane,
            farPlane);
    camera.position.z = 1500;
    camera.position.y = 0;
    camera.lookAt(new THREE.Vector3(0, 0, 0));
    renderer = new THREE.WebGLRenderer({alpha: true, antialias: true});
    renderer.setSize(WIDTH, HEIGHT);
    renderer.shadowMapEnabled = true;
    container = document.getElementById('minecraft');
    container.appendChild(renderer.domElement);
    windowHalfX = WIDTH / 2;
    windowHalfY = HEIGHT / 2;
    window.addEventListener('resize', onWindowResize, false);
    document.addEventListener('mousemove', handleMouseMove, false);
    document.addEventListener('mousedown', handleMouseDown, false);
    document.addEventListener('mouseup', handleMouseUp, false);
    document.addEventListener('touchstart', handleTouchStart, false);
    document.addEventListener('touchend', handleTouchEnd, false);
    document.addEventListener('touchmove', handleTouchMove, false);
}

function onWindowResize() {
    HEIGHT = window.innerHeight;
    WIDTH = window.innerWidth;
    windowHalfX = WIDTH / 2;
    windowHalfY = HEIGHT / 2;
    renderer.setSize(WIDTH, HEIGHT);
    camera.aspect = WIDTH / HEIGHT;
    camera.updateProjectionMatrix();
}

function handleMouseMove(event) {
    mousePos = {x: event.clientX, y: event.clientY};
}

function handleMouseDown(event) {
    isBlowing = true;
}
function handleMouseUp(event) {
    isBlowing = false;
}

function handleTouchStart(event) {
    if (event.touches.length > 1) {
        event.preventDefault();
        mousePos = {x: event.touches[0].pageX, y: event.touches[0].pageY};
        isBlowing = true;
    }
}

function handleTouchEnd(event) {
    mousePos = {x: windowHalfX, y: windowHalfY};
    isBlowing = false;
}

function handleTouchMove(event) {
    if (event.touches.length === 1) {
        event.preventDefault();
        mousePos = {x: event.touches[0].pageX, y: event.touches[0].pageY};
    }
}

function createLights() {

    light = new THREE.HemisphereLight(0xffffff, 0xffffff, .5);

    shadowLight = new THREE.DirectionalLight(0xffffff, .8);
    shadowLight.position.set(200, 200, 200);
    shadowLight.castShadow = true;
    shadowLight.shadowDarkness = .2;

    backLight = new THREE.DirectionalLight(0xffffff, .4);
    backLight.position.set(-100, 200, 50);
    backLight.shadowDarkness = .1;
    backLight.castShadow = true;

    scene.add(backLight);
    scene.add(light);
    scene.add(shadowLight);
}

function createChicken() {
    chicken = new Chicken();
    scene.add(chicken.threegroup);
}
//Model Chicken
Chicken = function () {

    this.windTime = 0;
    this.threegroup = new THREE.Group();

    this.yellowMat = new THREE.MeshLambertMaterial({
        color: "rgb(255,224,65)",
        shading: THREE.FlatShading
    });
    this.whiteMat = new THREE.MeshLambertMaterial({
        color: "rgb(240,240,240)",
        shading: THREE.FlatShading
    });
    this.blackMat = new THREE.MeshLambertMaterial({
        color: "rgb(0,0,0)",
        shading: THREE.FlatShading
    });
    this.redMat = new THREE.MeshLambertMaterial({
        color: "rgb(226, 123, 131)",
        shading: THREE.FlatShading
    });

    //body
    var body = new THREE.BoxGeometry(150, 150, 180);
    this.body = new THREE.Mesh(body, this.whiteMat);
    this.body.position.z = -120;
    this.body.position.y = -40;
    //wings
    var wings = new THREE.BoxGeometry(35, 120, 120);
    // wing left
    this.wingLeft = new THREE.Mesh(wings, this.whiteMat);
    this.wingLeft.position.z = -50;
    this.wingLeft.position.y = 0;
    this.wingLeft.position.x = -90;
    // wing right
    this.wingRight = new THREE.Mesh(wings, this.whiteMat);
    this.wingRight.position.z = -50;
    this.wingRight.position.y = 0;
    this.wingRight.position.x = 90;
    //legs
    var legs = new THREE.BoxGeometry(30, 100, 30);
    // leg left
    this.legLeft = new THREE.Mesh(legs, this.yellowMat);
    this.legLeft.position.z = -50;
    this.legLeft.position.y = -130;
    this.legLeft.position.x = -50;
    // leg right
    this.legRight = new THREE.Mesh(legs, this.yellowMat);
    this.legRight.position.z = -50;
    this.legRight.position.y = -130;
    this.legRight.position.x = 50;
    //finger
    var fingers = new THREE.BoxGeometry(70, 10, 30);
    // finger left
    this.fingerLeft = new THREE.Mesh(fingers, this.yellowMat);
    this.fingerLeft.position.z = -20;
    this.fingerLeft.position.y = -180;
    this.fingerLeft.position.x = -50;
    // finger right
    this.fingerRight = new THREE.Mesh(fingers, this.yellowMat);
    this.fingerRight.position.z = -20;
    this.fingerRight.position.y = -180;
    this.fingerRight.position.x = 50;
    //head
    var head = new THREE.BoxGeometry(100, 140, 50);
    this.head = new THREE.Mesh(head, this.whiteMat);
    this.head.position.z = 20;
    this.head.position.y = 60;
    //eyes
    //eye left
    var eyes = new THREE.BoxGeometry(25, 25, 10);
    this.eyeLeft = new THREE.Mesh(eyes, this.blackMat);
    this.eyeLeft.position.x = -35;
    this.eyeLeft.position.z = 25;
    this.eyeLeft.position.y = 30;
    //eye right
    this.eyeRight = new THREE.Mesh(eyes, this.blackMat);
    this.eyeRight.position.x = 35;
    this.eyeRight.position.z = 25;
    this.eyeRight.position.y = 30;
    //peak
    var Peak = new THREE.BoxGeometry(100, 45, 50);
    this.peak = new THREE.Mesh(Peak, this.yellowMat);
    this.peak.position.x = 0;
    this.peak.position.z = 50;
    this.peak.position.y = -7;
    //beard
    var beard = new THREE.BoxGeometry(40, 40, 25);
    this.beard = new THREE.Mesh(beard, this.redMat);
    this.beard.position.x = 0;
    this.beard.position.z = 40;
    this.beard.position.y = -50;
    // Add Elements to head
    this.head.add(this.eyeLeft);
    this.head.add(this.eyeRight);
    this.head.add(this.peak);
    this.head.add(this.beard);
    // Add Elements to body
    this.body.add(this.wingRight);
    this.body.add(this.wingLeft);
    this.body.add(this.legLeft);
    this.body.add(this.legRight);
    this.body.add(this.fingerRight);
    this.body.add(this.fingerLeft);

    this.threegroup.add(this.head);
    this.threegroup.add(this.body);

    this.threegroup.traverse(function (object) {
        if (object instanceof THREE.Mesh) {
            object.castShadow = true;
            object.receiveShadow = true;
        }
    });
};

Chicken.prototype.updateBody = function (speed) {
    this.head.rotation.y += (this.tHeagRotY - this.head.rotation.y) / speed;
    this.head.rotation.x += (this.tHeadRotX - this.head.rotation.x) / speed;
    this.head.position.x += (this.tHeadPosX - this.head.position.x) / speed;
    this.head.position.y += (this.tHeadPosY - this.head.position.y) / speed;
    this.head.position.z += (this.tHeadPosZ - this.head.position.z) / speed;
    this.body.rotation.y = ((this.tHeagRotY - this.head.rotation.y) + 0.5) / speed;
    this.body.rotation.x = ((this.tHeadRotX - this.head.rotation.x) + 0.5) / speed;
    this.body.position.x += (this.tHeadPosX - this.head.position.x) / speed;
    this.body.position.y += (this.tHeadPosY - this.head.position.y) / speed;
    this.body.position.z += (this.tHeadPosZ - this.head.position.z) / speed;
};

Chicken.prototype.look = function (xTarget, yTarget) {
    this.tHeagRotY = rule3(xTarget, -200, 200, -Math.PI / 4, Math.PI / 4);
    this.tHeadRotX = rule3(yTarget, -200, 200, -Math.PI / 4, Math.PI / 4);
    this.tHeadPosX = rule3(xTarget, -200, 200, 70, -70);
    this.tHeadPosY = rule3(yTarget, -140, 260, 20, 100);
    this.tHeadPosZ = 0;
    this.updateBody(10);
};

Chicken.prototype.cool = function (xTarget, yTarget) {
    var dt = 20000 / (xTarget * xTarget + yTarget * yTarget);
    dt = Math.max(Math.min(dt, 1), .5);
    this.windTime += dt;
    this.tHeagRotY = rule3(xTarget, -200, 200, -Math.PI / 4, Math.PI / 4);
    this.tHeadRotX = rule3(yTarget, -200, 200, -Math.PI / 4, Math.PI / 4);
    this.tHeadPosX = rule3(xTarget, -200, 200, 70, -70);
    this.tHeadPosY = rule3(yTarget, -140, 260, 20, 100);
    this.tHeadPosZ = 0;
    this.updateBody(10);
    this.body.rotation.x = -Math.cos(this.windTime) * Math.PI / 8 * dt;
    this.wingRight.rotation.x = -Math.cos(this.windTime) * Math.PI / 8 * dt;
    this.wingLeft.rotation.x = -Math.cos(this.windTime) * Math.PI / 8 * dt;
};


function createSeed() {
    seed = new Seed();
    seed.threegroup.position.z = 350;
    scene.add(seed.threegroup);
}

//Model Seed
Seed = function () {
    this.greenMat = new THREE.MeshLambertMaterial({
        color: "rgb(122, 199, 113)",
        shading: THREE.FlatShading
    });
    this.greenOMat = new THREE.MeshLambertMaterial({
        color: "rgb(31, 155, 17)",
        shading: THREE.FlatShading
    });
    this.coffeMat = new THREE.MeshLambertMaterial({
        color: "rgb(134, 98, 76)",
        shading: THREE.FlatShading
    });
    var Seed = new THREE.BoxGeometry(10, 10, 10);

    this.seedOne = new THREE.Mesh(Seed, this.greenMat);
    this.seedOne.position.x = -25;
    this.seedOne.position.y = 25;

    this.seedTwo = new THREE.Mesh(Seed, this.greenOMat);
    this.seedTwo.position.x = -25;
    this.seedTwo.position.y = -25;

    this.seedThree = new THREE.Mesh(Seed, this.coffeMat);
    this.seedThree.position.x = -35;
    this.seedThree.position.y = 5;

    this.seedFour = new THREE.Mesh(Seed, this.coffeMat);
    this.seedFour.position.x = -10;
    this.seedFour.position.y = -5;

    this.seedFive = new THREE.Mesh(Seed, this.greenOMat);
    this.seedFive.position.x = -5;
    this.seedFive.position.y = 5;

    this.seedSix = new THREE.Mesh(Seed, this.greenOMat);
    this.seedSix.position.x = -35;
    this.seedSix.position.y = 17;

    this.threegroup = new THREE.Group();
    this.threegroup.add(this.seedOne);
    this.threegroup.add(this.seedTwo);
    this.threegroup.add(this.seedThree);
    this.threegroup.add(this.seedFour);
    this.threegroup.add(this.seedFive);
    this.threegroup.add(this.seedSix);


};

Seed.prototype.update = function (xTarget, yTarget) {
    this.threegroup.lookAt(new THREE.Vector3(0, 80, 60));
    this.tPosX = rule3(xTarget, -200, 200, -250, 250);
    this.tPosY = rule3(yTarget, -200, 200, 250, -250);
    this.threegroup.position.x += (this.tPosX - this.threegroup.position.x) / 10;
    this.threegroup.position.y += (this.tPosY - this.threegroup.position.y) / 10;
};

//loop
function loop() {
    render();

    var xTarget = (mousePos.x - windowHalfX);
    var yTarget = (mousePos.y - windowHalfY);

    seed.isBlowing = isBlowing;
    seed.update(xTarget, yTarget);

    if (isBlowing) {
        chicken.cool(xTarget, yTarget);
    } else {
        chicken.look(xTarget, yTarget);
    }
    requestAnimationFrame(loop);

}

function render() {
    renderer.render(scene, camera);
}
init();
createLights();
createSeed();
createChicken();
loop();
function rule3(v, vmin, vmax, tmin, tmax) {
    var nv = Math.max(Math.min(v, vmax), vmin);
    var dv = vmax - vmin;
    var pc = (nv - vmin) / dv;
    var dt = tmax - tmin;
    var tv = tmin + (pc * dt);
    return tv;
}
/*library https://threejs.org/*/
/*based on the lion of @Yakudoo*/