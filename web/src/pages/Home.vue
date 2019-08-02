<template>
  <ElContainer id="home-page">
    <ElAside>
      <MenuBar />
    </ElAside>
    <ElContainer>
      <ElMain>
        <div class="content-view">
          <router-view />
        </div>
      </ElMain>
    </ElContainer>
  </ElContainer>
</template>

<script>
import MenuBar from '@/components/MenuBar.vue'
import apis from '@/api'

export default {
  name: 'home-page',
  data() {
    return {
      loading: true
    }
  },
  components: {
    MenuBar
  },
  async mounted() {
    await apis.getProjectInfo()
    this.$router.push({ path: '/working_space' })
  }
}
</script>

<style lang="scss" scoped>
#home-page {
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

  .el-header,
  .el-main {
    padding: 0;
  }
}
</style>
