<template>
  <div id="action-button">
    <el-button class="action-button" v-on:click="onClick">
      <i class="shortcuts-icon" :class="icon"></i>
      {{ name }}
    </el-button>
  </div>
</template>

<script>
  export default {
    name: 'action-button',
    props: {
      name: {
        type: String,
        required: true
      },
      icon: {
        type: String,
        default: ''
      }
    },
    methods: {
      onClick: function () {
        this.$emit('onClick')
      }
    }
  }
</script>

<style>
  #action-button {
    position: relative;
    width: 180px;
    height: 140px;
    display: inline-block;
  }

  #action-button .action-button {
    width: 100%;
    height: 100%;
    padding-top: 100px;
    font-size: 25px;
  }

  #action-button .action-button .shortcuts-icon {
    position: absolute;
    top: 0;
    left: 40px;
    font-size: 100px;
    z-index: 0;
  }
</style>
