const d=document
const $form_caballero=d.querySelector("#form_caballero"),
      $text_caballero=$form_caballero.querySelector("#text_caballero"),
      $text_constelacion=$form_caballero.querySelector("#text_constelacion"),
      $text_dios=$form_caballero.querySelector("#text_dios");

const $submit_enviar=$form_caballero.querySelector("#submit_enviar");
const $submit_websocket=d.querySelector("#submit_websocket");
const $contenedor=d.querySelector("#contenedor");

const $form_token=d.querySelector("#form_token"),
      $text_password=$form_token.querySelector("#text_password"),
      $submit_token=$form_token.querySelector("#submit_token"),
      $contenedor_token=d.querySelector("#contenedor_token");
      

let url1="https://render-fbxh.onrender.com/enviar";
let url2="http://192.168.100.16:3000/enviar"
let url_ws="ws://192.168.100.16:3000/ws"
let url_login="http://192.168.100.16:3000/login"

const ws=new WebSocket(url_ws)
let form=new FormData()

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

const enviar_password=async (paquete)=>{
    let {url,data,method,mode,headers,msgError}=paquete;
    let res=await fetch(url,{
        body:data,
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
            url:url1,
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
    if(e.target===$submit_token){
        //let {url,data,method,mode,headers,msgError}=paquete;
        form.append("password",$text_password.value);
        form.append("username","jesus")
        let paquete={
            url:"http://192.168.100.16:3000/login",
            data:form,
            method:"POST",
            mode:"cors",
            headers:{},
            msgError:"error al mandar password"
        }

        enviar_password(paquete)
        .then(res=>{
            $contenedor_token.innerHTML=JSON.stringify(res)
        })
        .catch(err=>console.log(err))

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