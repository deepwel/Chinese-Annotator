<template>
  <div id="loading-page" class="page">
    <menu-bar></menu-bar>
    <div class="loading-btn btn">加载数据</div>
  </div>
</template>

<script>
  import axios from 'axios'
  import MenuBar from '../common/MenuBar'
  export default {
    name: 'Loading',
    components: {
      'menu-bar': MenuBar
    },
    created: function () {
      axios.get('/static/project_config.json').then((res) => {
        const _this = this
        const url = res.data.interfaceUrl

        if (url) {
          this.$store.commit('updateInterFaceUrl', url)

          setTimeout(function () {
            _this.$router.replace('index')
          }, 2000)
        }
      })
    }
  }
</script>

<style>
  .page{
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

  .loading-btn{
    position: absolute;
    left: 50%;
    margin-left: -120px;
    top: 50%;
    margin-top: -50px;
  }
</style>
