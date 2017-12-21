<template>
  <div id="menu-bar">
    <div class="container">
      <h1>CN-Annotator</h1>
      <div class="basic" v-if="basic">
        <div>
          <span>类型</span>
          <span>{{ basic.type }}</span>
        </div>
        <div>
          <span>数据集</span>
          <span>{{ basic.dataSet }}</span>
        </div>
      </div>
      <div class="progress" v-if="progress">
        <div class="progress-text">已标注 {{ progress.done }}/{{ progress.count }}</div>
        <el-progress :text-inside="true" :stroke-width="18" :percentage="percentage"></el-progress>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'menu-bar',
    props: {
      info: {
        type: Object
      }
    },
    computed: {
      basic: function () {
        return this.info ? this.info.basic : null
      },
      progress: function () {
        return this.info ? this.info.progress : null
      },
      percentage: function () {
        const progress = this.progress
        return Math.floor(progress.done / progress.count * 100)
      }
    }
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
    height: 100vh;
    overflow-y: auto;
    transition: transform .2s ease,-webkit-transform .2s ease;
    width: 260px;
    z-index: 10;
    font-size: 18px;
  }

  #menu-bar .container h1{
    margin-bottom: 20px;
    padding:10px 0;
    background:#384451;
  }

  #menu-bar .container .basic > div {
    display: flex;
    padding: 5px 10px;
    text-align: left;
  }

  #menu-bar .container .basic span:first-child {
    width: 80px;
  }

  #menu-bar .container .basic span:last-child {
    flex: 1;
  }

  #menu-bar .container .progress {
    margin-top: 40px;
    padding: 10px
  }

  #menu-bar .container .progress-text {
    text-align: left;
    margin-bottom: 10px;
  }
</style>
