import * as THREE from './vendor/three/three.module.min.js';
import {OrbitControls} from './vendor/three/OrbitControls.js';
// Geometry, lighting, selection and thermal palette adapted from Digital-Twin 1b999d1.
export function createTwinViewer(host,onSelect){
 const scene=new THREE.Scene();scene.background=new THREE.Color('#0c1623');
 const camera=new THREE.PerspectiveCamera(40,1,.1,100);camera.position.set(8,6,12);
 const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));host.replaceChildren(renderer.domElement);
 const controls=new OrbitControls(camera,renderer.domElement);controls.target.set(0,2.5,0);controls.enableDamping=true;controls.minDistance=3;controls.maxDistance=35;
 scene.add(new THREE.HemisphereLight(0xe1f4ff,0x24384c,2.4));const light=new THREE.DirectionalLight(0xffffff,3);light.position.set(5,8,6);scene.add(light);
 const group=new THREE.Group();scene.add(group);let key='',meshes=[],outlines=[],cells=[];
 const palette=['#2563eb','#06b6d4','#22c55e','#facc15','#ef4444'].map(c=>new THREE.Color(c));
 function thermal(t){if(t==null)return new THREE.Color('#526b80');const x=Math.max(0,Math.min(1,(t-20)/25))*4,i=Math.min(3,Math.floor(x));return palette[i].clone().lerp(palette[i+1],x-i)}
 function box(w,h,d,x,y,z,color){const mesh=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),new THREE.MeshStandardMaterial({color,roughness:.55,metalness:.4}));mesh.position.set(x,y,z);group.add(mesh);return mesh}
 function clear(){for(const child of [...group.children]){group.remove(child);child.geometry?.dispose();const materials=Array.isArray(child.material)?child.material:[child.material];for(const m of materials){m?.map?.dispose();m?.dispose()}}meshes=[];outlines=[]}
 function update(next,selected,mode='rack'){
  cells=next;const signature=mode+JSON.stringify(next.map(c=>[c.id,c.form_factor,c.width_mm,c.height_mm,c.thickness_mm,c.diameter_mm]));
  if(signature!==key){key=signature;clear();
   if(mode==='rack'){
    for(const x of [-3.25,3.25])for(const z of [-1.1,1.1])box(.15,5.9,.15,x,2.9,z,'#61788f');
    for(const y of [0,1.85,3.7,5.6])box(6.7,.13,2.5,0,y,0,'#334b61');box(6.6,5.6,.12,0,2.8,-1.15,'#1a2b3d');
   }
   const heights=next.map(c=>c.height_mm||135),scale=1.3/Math.max(...heights,1);
   next.forEach((c,index)=>{const prism=String(c.form_factor).toLowerCase()==='prismatic',rawIndex=c.rack_index??index;
    let x,y,width,height,depth;
    if(mode==='rack'){const col=(prism?0:2)+rawIndex%2,row=Math.floor((rawIndex%6)/2);x=(col-1.5)*1.55;y=4.55-row*1.85;width=prism?.95:.84;height=1.3;depth=prism?.55:.84}
    else{x=(index%3-1)*2.2;y=.8+Math.floor(index/3)*2;height=c.height_mm*scale;width=(prism?c.width_mm:c.diameter_mm)*scale;depth=(prism?c.thickness_mm:c.diameter_mm)*scale;}
    const body=new THREE.Mesh(prism?new THREE.BoxGeometry(width,height,depth):new THREE.CylinderGeometry(width/2,width/2,height,40),new THREE.MeshStandardMaterial({color:thermal(c.temperature_c),roughness:.4,metalness:.22}));body.position.set(x,y,.1);body.userData.id=String(c.id);group.add(body);meshes.push(body);
    if(prism){box(width*.18,.12,depth*.4,x-width*.28,y+height/2+.06,.1,'#ed786a');box(width*.18,.12,depth*.4,x+width*.28,y+height/2+.06,.1,'#b5c5d3')}else box(width*.38,.1,width*.38,x,y+height/2+.05,.1,'#b5c5d3');
    const edge=new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(width+.15,height+.25,depth+.15)),new THREE.LineBasicMaterial({color:'#e7fffa'}));edge.position.copy(body.position);group.add(edge);outlines.push(edge);
    const canvas=document.createElement('canvas');canvas.width=512;canvas.height=64;const context=canvas.getContext('2d');context.fillStyle='#c4dae9';context.font='bold 22px sans-serif';context.textAlign='center';context.fillText(c.name||String(c.id),256,42);const label=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(canvas)}));label.position.set(x,y-height/2-.22,Math.max(depth,.6));label.scale.set(2,.25,1);group.add(label);
   });
   if(mode==='rack'){const prism=next.every(c=>String(c.form_factor).toLowerCase()==='prismatic');controls.target.set(prism?-1.55:0,2.5,0);camera.position.set(prism?-3:8,6,12)}else{controls.target.set(0,1.5,0);camera.position.set(7,6,11)}
  }
  next.forEach((c,i)=>{meshes[i].material.color.copy(thermal(c.temperature_c));outlines[i].visible=String(c.id)===String(selected)});
 }
 const observer=new ResizeObserver(()=>{const w=host.clientWidth,h=host.clientHeight;if(w&&h){renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix()}});observer.observe(host);
 const ray=new THREE.Raycaster(),pointer=new THREE.Vector2();let down;
 renderer.domElement.addEventListener('pointerdown',e=>down=[e.clientX,e.clientY]);renderer.domElement.addEventListener('pointerup',e=>{if(!down||Math.hypot(e.clientX-down[0],e.clientY-down[1])>6)return;const r=renderer.domElement.getBoundingClientRect();pointer.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1);ray.setFromCamera(pointer,camera);const hit=ray.intersectObjects(meshes)[0];if(hit)onSelect(hit.object.userData.id)});
 renderer.setAnimationLoop(()=>{controls.update();renderer.render(scene,camera)});
 return {update,dispose(){observer.disconnect();renderer.setAnimationLoop(null);controls.dispose();clear();renderer.dispose();host.replaceChildren()}};
}
