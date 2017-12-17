<!-- It is the main layout as the Starter Page -->

<template>
<div id="loading-page">
  <menu-bar/>
  <div class="content-view">
	<div id="start-page" class="page">
	  <h2 style="margin-top:300px">加载项目数据...</h2>
	</div>
  </div>
  
</div>
</template>

<script>
import MenuBar from '@/components/MenuBar'
import axios from 'axios'

export default {
	name: 'loading-page',
	data: function() {
        return {
			loadedFile : '',	
		}
	},
	components: {
		'menu-bar': MenuBar
	},
	mounted: function () {
		axios({
			method: 'get',
			url: 'http://localhost:3000/project-info'			
		}).then(res=>{
			console.log(res);
			setTimeout(() => {
				this.$router.push({ path: '/working-space/text-classify' })
			},2000)
		})
		console.log('a is: ' + this.a)
	}
}
</script>

<style>

#loading-page {
	font-family: 'Avenir', Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	text-align: center;
	color: #2c3e50;
	display: -webkit-box;
	display: flex;
	-webkit-box-orient: horizontal;
	-webkit-box-direction: normal;
	flex-flow: row nowrap;
	height: 100%;
	max-width: 100%;
	min-height: 100vh;
	overflow-y: hidden;
	width: 100%;
}
html {
    font-size: 10px;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeSpeed;
    -ms-text-size-adjust: 100%;
    -webkit-text-size-adjust: 100%;
}
body {
    height: 100%;
    width: 100%;
}
* {
  border: 0;
  box-sizing: border-box;
  margin: 0;
  outline: 0;
  padding: 0; 
}
#loading-page > .content-view {
    background: #f6f6f6;
    color: var(--color-text);
    display: -webkit-box;
    display: flex;
    -webkit-box-flex: 100%;
    flex: 100%;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    flex-flow: column nowrap;
    font-family: var(--font-primary);
    line-height: 1.5;
    max-height: 100vh;
    max-width: 100%;
    position: relative;
}

.content-view .page{
	width:100%;
	height:100%;
}

.btn{
	width: 240px;
	height:80px;
	line-height:80px;
	display:block;
    font-size: 28px;
    border-radius: 5px;
    cursor: pointer;
    background: #b9b9b9;
    color: white;
}

.btn:hover{
	background: #999999;
}

</style>
