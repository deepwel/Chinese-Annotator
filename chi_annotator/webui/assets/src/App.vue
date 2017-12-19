<!-- It is the main layout as the Starter Page -->

<template>
  <div id="app">
    <div class="content-view">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'app'
  }
</script>

<style>
  #app {
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
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
  #app > .content-view {
      background: #f6f6f6;
      color: var(--color-text);
      display: -webkit-box;
      display: flex;
      -webkit-box-flex: 1;
      flex: 1;
      -webkit-box-orient: vertical;
      -webkit-box-direction: normal;
      flex-flow: column nowrap;
      font-family: var(--font-primary);
      line-height: 1.5;
      max-height: 100vh;
      max-width: 100%;
      position: relative;
  }
</style>
