import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Infografía Ética de Datos Agrícolas",
    layout="wide"
)

html_code = """
<!DOCTYPE html>
<html lang="es">

<head>
<meta charset="UTF-8">

<style>

body{
font-family: Arial;
background: linear-gradient(120deg,#e8f5e9,#f1f8e9);
text-align:center;
margin:0;
}

h1{
margin-top:40px;
color:#1b5e20;
font-size:40px;
}

.container{
position:relative;
width:800px;
height:800px;
margin:auto;
margin-top:40px;
}

.center{

position:absolute;
top:50%;
left:50%;
transform:translate(-50%,-50%);
width:220px;
height:220px;

background:#2e7d32;
color:white;

border-radius:50%;

display:flex;
align-items:center;
justify-content:center;

font-size:22px;
font-weight:bold;

box-shadow:0 0 30px rgba(0,0,0,0.3);

}

.node{

position:absolute;

width:180px;
height:180px;

background:white;
border-radius:50%;

box-shadow:0 8px 20px rgba(0,0,0,0.2);

padding:10px;

transition:0.4s;

cursor:pointer;

}

.node:hover{

transform:scale(1.15) rotate(3deg);

box-shadow:0 12px 30px rgba(0,0,0,0.4);

}

.node img{

width:70px;
height:70px;

border-radius:50%;
margin-top:5px;

}

.node p{

font-size:14px;
padding:5px;

}

/* posiciones circulares */

.n1{ top:0; left:310px; }

.n2{ top:120px; right:0; }

.n3{ top:310px; right:0; }

.n4{ bottom:120px; right:0; }

.n5{ bottom:0; left:310px; }

.n6{ bottom:120px; left:0; }

.n7{ top:310px; left:0; }

.n8{ top:120px; left:0; }

</style>

</head>

<body>

<h1>Ética del Análisis de Datos Agrícolas</h1>

<div class="container">

<div class="center">
Agricultura<br>Digital<br>y Ética
</div>

<div class="node n1">

<img src="https://cdn-icons-png.flaticon.com/512/2909/2909767.png">

<p><b>Agricultura digital</b><br>
Uso de sensores, drones y análisis de datos para mejorar la producción.</p>

</div>


<div class="node n2">

<img src="https://cdn-icons-png.flaticon.com/512/3062/3062634.png">

<p><b>Privacidad</b><br>
Protección de la información personal y productiva de los agricultores.</p>

</div>


<div class="node n3">

<img src="https://cdn-icons-png.flaticon.com/512/2721/2721297.png">

<p><b>Empresas tecnológicas</b><br>
Plataformas digitales que recopilan y analizan grandes volúmenes de datos.</p>

</div>


<div class="node n4">

<img src="https://cdn-icons-png.flaticon.com/512/1828/1828919.png">

<p><b>Transparencia</b><br>
Los agricultores deben conocer cómo se utilizan sus datos.</p>

</div>


<div class="node n5">

<img src="https://cdn-icons-png.flaticon.com/512/3176/3176364.png">

<p><b>Consentimiento</b><br>
Autorización clara para el uso y procesamiento de datos.</p>

</div>


<div class="node n6">

<img src="https://cdn-icons-png.flaticon.com/512/1041/1041916.png">

<p><b>Impacto social</b><br>
La tecnología puede generar beneficios pero también desigualdades.</p>

</div>


<div class="node n7">

<img src="https://cdn-icons-png.flaticon.com/512/4359/4359963.png">

<p><b>Inclusión</b><br>
Participación de mujeres, jóvenes y comunidades rurales.</p>

</div>


<div class="node n8">

<img src="https://cdn-icons-png.flaticon.com/512/3064/3064197.png">

<p><b>Seguridad</b><br>
Uso de encriptación y sistemas de protección de datos.</p>

</div>

</div>

</body>

</html>
"""

components.html(html_code, height=900)
