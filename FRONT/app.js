const API = "https://dhollandia-consignas.onrender.com"

async function cargar(){

    let r = await fetch(API + "/stock")

    let data = await r.json()

    let html = `
    <table>

    <tr>
        <th>Ciudad</th>
        <th>Codigo</th>
        <th>Descripcion</th>
        <th>Stock</th>
        <th>Minimo</th>
        <th>Estado</th>
        <th>Salida</th>
        <th>Entrada</th>
    </tr>
    `

    data.forEach(x=>{

        let clase = ""

        if(x.estado == "ALERTA"){
            clase = "alerta"
        }

        html += `
        <tr class="${clase}">

            <td>${x.ciudad}</td>

            <td>${x.codigo}</td>

            <td>${x.descripcion}</td>

            <td>${x.stock}</td>

            <td>${x.minimo}</td>

            <td>${x.estado}</td>

            <td>
                <button onclick="movimiento(${x.id}, 'SALIDA')">
                -
                </button>
            </td>

            <td>
                <button onclick="movimiento(${x.id}, 'ENTRADA')">
                +
                </button>
            </td>

        </tr>
        `
    })

    html += "</table>"

    document.getElementById("tabla").innerHTML = html

    cargarHistorial()
}

async function movimiento(id, tipo){

    let cantidad = prompt("Cantidad")

    let observaciones = prompt("Observaciones")

    await fetch(API + "/movimiento",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            id:id,

            tipo:tipo,

            cantidad:cantidad,

            observaciones:observaciones

        })

    })

    cargar()
}

async function agregar(){

    let ciudad = document.getElementById("ciudad").value
    let codigo = document.getElementById("codigo").value
    let descripcion = document.getElementById("descripcion").value
    let stock = document.getElementById("stock").value
    let minimo = document.getElementById("minimo").value

    await fetch(API + "/agregar",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            ciudad,
            codigo,
            descripcion,
            stock,
            minimo

        })

    })

    cargar()
}

async function cargarHistorial(){

    let r = await fetch(API + "/historial")

    let data = await r.json()

    let html = `
    <table>

    <tr>
        <th>Fecha</th>
        <th>Ciudad</th>
        <th>Codigo</th>
        <th>Descripcion</th>
        <th>Tipo</th>
        <th>Cantidad</th>
        <th>Observaciones</th>
    </tr>
    `

    data.forEach(x=>{

        html += `
        <tr>

            <td>${x.fecha}</td>

            <td>${x.ciudad}</td>

            <td>${x.codigo}</td>

            <td>${x.descripcion}</td>

            <td>${x.tipo}</td>

            <td>${x.cantidad}</td>

            <td>${x.observaciones}</td>

        </tr>
        `
    })

    html += "</table>"

    document.getElementById("historial").innerHTML = html
}

cargar()