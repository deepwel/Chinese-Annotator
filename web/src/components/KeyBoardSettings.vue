<template>
  <el-card id="key-board-settings">
    <div class="setting-header">
      <span>快捷键设置</span>
    </div>
    <div v-for="(annotation, index) in annotations" :key="annotation.id">
      <el-row>
        <el-col :span="16">
          <span>{{ annotation.name }}：</span>
        </el-col>
        <el-col :span="8">
          <input
            type="text"
            ondragenter="return false"
            oncontextmenu="return false;"
            :value="annotation.key"
            @focus="inFocus(annotation, index)"
            @blur="onBlur"
          />
        </el-col>
      </el-row>
    </div>
  </el-card>
</template>

<script>
export default {
  name: 'tag',
  props: {
    annotations: {
      type: Array,
      required: true
    }
  },
  methods: {
    inFocus(annotation, index) {
      const _this = this

      document.onkeydown = function(e) {
        e.preventDefault()

        if (
          window.event.keyCode === 32 ||
          (window.event.keyCode >= 37 && window.event.keyCode <= 40)
        ) {
          return false
        }

        annotation.key =
          window.event.keyCode === 8
            ? 'Back'
            : window.event.keyCode === 20
            ? 'Lock'
            : window.event.key
        annotation.keyCode = window.event.keyCode

        _this.$emit('update', index, annotation)
      }
    },
    onBlur() {
      this.$emit('onBlur')
    }
  }
}
</script>

<style>
#key-board-settings {
  position: relative;
  width: 180px;
  height: 100%;
  padding: 20px 0;
  -webkit-border-radius: 4px;
  -moz-border-radius: 4px;
  border-radius: 4px;
  text-align: left;
}

#key-board-settings .setting-header {
  font-size: 20px;
  text-align: center;
}

#key-board-settings .el-card__body {
  height: 100%;
  padding: 0 20px;
  overflow-y: auto;
}

#key-board-settings .el-card__body > div:not(:last-child) {
  margin-bottom: 20px;
}

#key-board-settings .el-row {
  height: 22px;
  font-size: 16px;
}

#key-board-settings .el-row > div:first-child {
  height: 100%;
  text-align: right;
}

#key-board-settings .el-row > div:last-child {
  height: 100%;
  text-align: left;
}

#key-board-settings .el-row input {
  height: 100%;
  width: 100%;
  border: 1px solid #dcdfe6;
  float: left;
  -webkit-border-radius: 4px;
  -moz-border-radius: 4px;
  border-radius: 4px;
  text-align: center;
  ime-mode: disabled;
}
</style>
