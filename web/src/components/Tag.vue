<template>
  <div :class="['tag', classObject, size]" @click="selectTag">
    <div class="tag-name">{{ name }}</div>
    <div class="shortcuts" v-if="shortcuts">（{{ shortcuts }}）</div>
  </div>
</template>

<script>
export default {
  name: 'tag',
  props: {
    name: {
      type: String,
      required: true
    },
    shortcuts: {
      type: String,
      default: ''
    },
    selected: {
      type: Boolean,
      default: false
    },
    machineSelected: {
      type: Boolean,
      default: false
    },
    // small or large
    size: {
      type: String,
      default: 'large'
    }
  },
  computed: {
    classObject() {
      return {
        'machine-active': this.machineSelected,
        active: this.selected
      }
    }
  },
  methods: {
    selectTag() {
      this.$emit('selectTag')
    }
  }
}
</script>

<style lang="scss" scoped>
.tag {
  position: relative;
  display: inline-flex;
  align-items: center;
  -webkit-border-radius: 4px;
  -moz-border-radius: 4px;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  color: #606266;

  .tag-name {
    flex: 1;
  }

  .shortcuts {
    position: absolute;
    width: 100%;
    text-align: center;
    z-index: 0;
  }

  &:hover {
    color: #409eff;
    border: 1px solid #c6e2ff;
    background-color: #ecf5ff;
  }

  &.machine-active {
    border: 6px solid #2196f3;
  }

  &.active {
    color: white;
    background-color: #4caf50;
  }

  &.large {
    width: 180px;
    height: 140px;
    font-size: 25px;
    font-weight: 500;

    .shortcuts {
      margin-top: 40px;
    }
  }

  &.small {
    width: 90px;
    height: 80px;
    font-size: 18px;
    font-weight: 400;

    .shortcuts {
      margin-top: 22px;
    }
  }
}
</style>
