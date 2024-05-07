const d=document
const $form_caballero=d.querySelector("#form_caballero"),
      $text_caballero=$form_caballero.querySelector("#text_caballero"),
      $text_constelacion=$form_caballero.querySelector("#text_constelacion"),
      $text_dios=$form_caballero.querySelector("#text_dios");

const $submit_enviar=$form_caballero.querySelector("#submit_enviar")
const $contenedor=d.querySelector("#contenedor");

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
            url:"http://192.168.100.16:3000/enviar",
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
            $contenedor.innerHTML=res;
        })
        .catch(error=>{
            $contenedor.innerHTML=error
        })
        
    }
});
