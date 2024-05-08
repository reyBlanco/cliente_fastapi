const d=document
const $form_caballero=d.querySelector("#form_caballero"),
      $text_caballero=$form_caballero.querySelector("#text_caballero"),
      $text_constelacion=$form_caballero.querySelector("#text_constelacion"),
      $text_dios=$form_caballero.querySelector("#text_dios");

const $submit_enviar=$form_caballero.querySelector("#submit_enviar");
const $submit_websocket=d.querySelector("#submit_websocket");
const $contenedor=d.querySelector("#contenedor");

let url1="https://render-fbxh.onrender.com/enviar";
let url2="http://192.168.100.16:3000/enviar"

let url_ws1="wss://render-fbxh.onrender.com/ws"
let url_ws2="ws://192.168.100.16:3000/ws"

const ws=new WebSocket(url_ws1)

const enviar=async (paquete)=>{
    let {url,data,method,mode,headers,msgError}=paquete;
    let res=await fetch(url,{
        body:JSON.stringify(data),
        headers,
        method,
        mode
    });

    if(res.ok){
        return await res.json()
    }else{
        throw(msgError)
    }
}

d.addEventListener("click",(e)=>{
    e.preventDefault()
    if(e.target===$submit_enviar){
        let nombre=$text_caballero.value;
        let constelacion=$text_constelacion.value;
        let dios=$text_dios.value
        
        let caballero={
            nombre,
            constelacion,
            dios
        }

        //let {url,data,method,mode,headers,msgError}=paquete;
        let paquete={
            url:url2,
            method:"POST",
            mode:"cors",
            data:caballero,
            headers:{
                "content-type":"application/json"
            },
            msgError:"error al mandar los datos al servidor"
        }

        enviar(paquete)
        .then(res=>{
            $contenedor.innerHTML=JSON.stringify(res);
        })
        .catch(error=>{
            $contenedor.innerHTML=error
        })
        
    }
    if (e.target===$submit_websocket){
        let nombre=$text_caballero.value;
        let constelacion=$text_constelacion.value;
        let dios=$text_dios.value
        
        let caballero={
            nombre,
            constelacion,
            dios
        }

        ws.send(JSON.stringify(caballero))
    }
});

ws.addEventListener("open",(e)=>{
    $contenedor.innerHTML="conectado con el websocket";
    
});

ws.addEventListener("error",(e)=>{
    $contenedor.innerHTML="erro al conectar con el websocket";
});

ws.addEventListener("close",(e)=>{
    $contenedor.innerHTML="se cerro la conexion con el servidor";
});

ws.addEventListener("message",(msg)=>{
    mensaje=msg.data;
    $contenedor.innerHTML=mensaje;
});