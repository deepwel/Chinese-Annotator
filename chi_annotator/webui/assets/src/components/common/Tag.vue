<template>
  <div
    id="tag"
    :class="{ 'machine-active': machineSelected, active: selected }"
    @click="selectTag"
  >
    <div class="tag-name">{{ name }}</div>
    <div class="shortcuts">（{{ shortcuts }}）</div>
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
      }
    },
    methods: {
      selectTag: function () {
        this.$emit('selectTag')
      }
    }
  }
</script>

<style>
  #tag {
    position: relative;
    width: 200px;
    height: 160px;
    display: inline-flex;
    align-items: center;
    -webkit-border-radius: 4px;
    -moz-border-radius: 4px;
    border-radius: 4px;
    border: 1px solid #dcdfe6;
    font-size: 25px;
    color: #606266;
    font-weight: 500;
  }

  #tag:hover {
    color: #409EFF;
    border: 1px solid #c6e2ff;
    background-color: #ecf5ff;
  }

  #tag.machine-active {
    border: 6px solid #2196f3;
  }

  #tag.active {
    color: white;
    background-color: #4caf50;
  }

  #tag .tag-name {
    flex: 1;
  }

  #tag .shortcuts {
    position: absolute;
    bottom: 10px;
    width: 100%;
    text-align: center;
    z-index: 0;
  }
</style>
