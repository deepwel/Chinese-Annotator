<template>
<div id="menu-bar">
  <div class="container">
	<h1>CN-Annotator</h1>
  </div>
</div>

</template>

<script>
export default {
  name: 'menu-bar'
}
</script>

<style>
#menu-bar .container{	
    background: #54606e;
    color: white;
    display: -webkit-box;
    display: flex;
    -webkit-box-flex: 0;
    flex: 0 0 260px;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    flex-flow: column nowrap;
    font-family: var(--font-primary);
    font-size: 1.4rem;
    height: 100vh;
    overflow-y: auto;
    transition: -webkit-transform .2s ease;
    transition: transform .2s ease;
    transition: transform .2s ease,-webkit-transform .2s ease;
    width: 260px;
    z-index: 10;
}
#menu-bar .container h1{
	padding:10px 0;
	background:#384451;
}

</style>
