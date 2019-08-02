<template>
  <ElContainer id="menu-bar" class="container">
    <ElHeader>
      <h2>中文标注工具</h2>
    </ElHeader>
    <ElMain>
      <section>
        <h3 class="title">操作面板</h3>
        <div class="row">
          <ElButton type="info" size="mini" @click="handleExportDataSet">导出(annotation_data.json)</ElButton>
        </div>
        <div class="row">
          <ElButton type="info" size="mini" @click="handleLoadDataSet">导入(email_classify_chi_nolabel.txt)</ElButton>
        </div>
      </section>
      <section class="progress" v-if="progress">
        <h3 class="title">标注进度</h3>
        <div class="row">
          <span class="label">已标注</span>
          <span>{{ progress.done}}</span>
        </div>
        <div class="row">
          <span class="label">总计</span>
          <span>{{ dataSource.count }}</span>
        </div>
        <ElProgress :text-inside="false" :stroke-width="10" :percentage="percentage" show-text color="white"></ElProgress>
      </section>
      <section class="history">
        <h3 class="title">标注历史</h3>
        <div class="row" v-for="h in history" :key="h.dataset_uid">
          <span class="text">{{h.text}}</span>
          <div class="done">
            <i class="el-icon-check"></i>
          </div>
        </div>
      </section>
    </ElMain>
    <ElFooter height="40px">© {{ new Date().getFullYear()}} 中文标注</ElFooter>
  </ElContainer>
</template>

<script>
import { mapState } from 'vuex'
import apis from '@/api'

export default {
  name: 'menu-bar',
  data() {
    return {}
  },
  computed: {
    ...mapState({
      dataSource: state => state.dataSource,
      history: state => state.history,
      progress: state => state.progress
    }),
    percentage() {
      return this.progress ? +((this.progress.done / this.dataSource.count) * 100).toFixed(1) : 0
    }
  },
  methods: {
    handleOptionChange(value) {
      this.$store.commit('updateDataSourceType', value)
    },
    handleLoadDataSet() {
      apis
        .loadDataSet()
        .then(resp => {
          if (resp.data.code === 200) {
            this.$notify.success({
              title: '导入成功',
              showClose: false
            })
          } else {
            throw resp.data
          }
        })
        .catch(error => {
          this.$notify.error({
            title: '出错了',
            message: error.message || JSON.stringify(error),
            showClose: true
          })
        })
    },
    handleExportDataSet() {
      apis
        .exportDataSet()
        .then(resp => {
          if (resp.data.code === 200) {
            this.$notify.success({
              title: '导出成功',
              showClose: false
            })
          } else {
            throw resp.data
          }
        })
        .catch(error => {
          this.$notify.error({
            title: '出错了',
            message: error.message || JSON.stringify(error),
            showClose: true
          })
        })
    }
  }
}
</script>

<style lang="scss">
#menu-bar {
  background: #54606e;
  color: white;
  display: -webkit-box;
  display: flex;
  -webkit-box-flex: 0;
  flex: 0 0 1;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
  flex-flow: column nowrap;
  font-family: var(--font-primary);
  height: 100vh;
  overflow-y: auto;
  transition: transform 0.2s ease, -webkit-transform 0.2s ease;
  width: 100%;
  z-index: 10;
  font-size: 18px;

  h2 {
    padding: 10px 20px;
    background: #384451;
    font-size: 24px;
    text-align: start;
  }

  section {
    padding: 10px 20px;
    text-align: left;

    .title {
      font-size: 16px;
      margin: 0 0 10px 0;
    }

    .row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 10px;
      font-size: 14px;
      // line-height: 2;

      .label {
        color: #b9b9b9;
        font-weight: bold;
      }
    }

    &:not(:last-child) {
      border-bottom: 1px solid #384451;
    }
  }

  .history {
    .row {
      font-size: 12px;
      .text {
        max-width: 100%;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      &:first-of-type {
        font-size: 14px;
      }
    }
  }

  .el-header,
  .el-main {
    padding: 0;
  }

  .el-footer {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 12px;
    border-top: 1px solid #384451;
  }

  .el-progress {
    margin: 10px 0;
    white-space: nowrap;

    .el-progress__text {
      margin-left: 25px;
      text-align: end;
      font-size: 16px;
      font-weight: bold;
      color: white;
    }

    .el-progress-bar__outer {
      background-color: #384451;
    }
  }
}
</style>
